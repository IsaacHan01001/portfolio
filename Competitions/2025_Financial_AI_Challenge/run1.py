import ollama
import pandas as pd
import torch
import kss 
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_core.documents import Document
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from langchain_community.llms import Ollama
from typing import *
from collections import defaultdict
from datetime import datetime
import time

class Solution:
    def __init__(self, trainPath):
        # --- Load Data and Set Up RAG Chain ---
        self.input_file = pd.read_csv(trainPath)
        print("CSV data loaded successfully.")
        
        # --- RAG Setup (Moved from main to __init__) ---
        print("PDF 문서를 로딩합니다...")
        loader = PyPDFDirectoryLoader("./legal-gemma-rag/data/") # Adjusted path for common use case
        documents = loader.load()
        
        print("문서를 의미 있는 단위로 분할합니다...")
        
        # --- FINAL RECOMMENDED CODE with KSS ---
        print("KSS를 사용하여 문서를 문장 단위로 분할합니다...")
        processed_docs = []
        for doc in documents:
            # Split the document's content into sentences
            sentences = kss.split_sentences(doc.page_content)
            # Join the sentences back together with a clear separator
            cleaned_content = "\n\n".join(sentences)
            # Create a new document with the cleaned content, preserving metadata
            processed_docs.append(Document(page_content=cleaned_content, metadata=doc.metadata))

        print("의미 있는 단위로 문서를 분할합니다...")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=150)
        # Now, split the pre-processed documents. The splitter will respect the "\n\n" joins.
        docs = text_splitter.split_documents(processed_docs)

        print("텍스트 임베딩 및 벡터 스토어를 생성합니다...")
        self.emb_model_name = "BAAI/bge-m3"
        embeddings = HuggingFaceEmbeddings(
            model_name=self.emb_model_name,
            model_kwargs={'device': 'cuda' if torch.cuda.is_available() else 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
        vector_store = FAISS.from_documents(docs, embeddings)

        print("언어 모델과 프롬프트를 설정합니다...")
        self.llm_model_name = "gemma2:9b"
        llm = Ollama(model=self.llm_model_name) 


        template = f"""
        당신은 뛰어난 법률 및 기술 분야의 AI 어시스턴트입니다. 당신의 임무는 주어진 '컨텍스트' 정보만을 사용하여 질문에 대해 간결하고 정확한 한국어 문장으로 답변하는 것입니다.

        ### 지시사항 (Instructions)
        1.  **컨텍스트 기반 답변:** 답변은 반드시 주어진 '컨텍스트' 내용에만 100% 근거해야 합니다. 외부 지식을 사용하거나 추측해서는 안 됩니다.
        2.  **상세하고 완전한 문장:** 컨텍스트에 답변의 근거가 충분하다면, 핵심 정보를 최대한 많이 포함하여 1~3개의 완전한 문장으로 답변을 생성하세요.
        3.  **정보 부족 시 처리:** 만약 컨텍스트에 질문에 답변할 정보가 명확하게 없다면, **"컨텍스트의 정보가 부족하여 질문에 답변할 수 없습니다."** 라고만 답변해야 합니다. 다른 말을 추가하지 마세요.

        ### 예시 (EXAMPLE) - (실제 테스트 데이터와 관련 없는 일반적인 예시)
        컨텍스트: "클라우드 서비스 제공자는 '데이터 보호법' 제10조에 따라 사용자의 데이터를 전송 및 저장 시 강력한 암호화 기술을 적용해야 합니다. 특히, AES-256 암호화 알고리즘을 사용하여 데이터의 기밀성을 보장하는 것이 중요합니다."
        질문: "클라우드 데이터 보호를 위한 핵심 기술은 무엇인가요?"
        답변: "클라우드 서비스 제공자는 '데이터 보호법'에 따라 AES-256과 같은 강력한 암호화 기술을 적용하여 데이터 전송 및 저장 시 기밀성을 보장해야 합니다."

        ### 작업 (TASK)
        컨텍스트:
        {{context}}

        질문: {{input}}

        답변:
        """
        # =========================================================================
        # 프롬프트 템플릿 끝
        # =========================================================================

        # The rest of your code stays the same
        prompt = ChatPromptTemplate.from_template(template)


        print("RAG 체인을 생성합니다...")
        document_chain = create_stuff_documents_chain(llm, prompt)
        retriever = vector_store.as_retriever()
        # Storing the chain as an instance variable
        self.retrieval_chain = create_retrieval_chain(retriever, document_chain)
        print("\n--- RAG Chain is ready ---")

    def get_rag_response(self, question: str) -> tuple:
        # CORRECTED: Calling the instance variable self.retrieval_chain
        response = self.retrieval_chain.invoke({"input": question})
        
        sources = []
        for doc in response["context"]:
            source = doc.metadata.get("source", "unknown")
            page = doc.metadata.get("page", "N/A")
            # CORRECTED: Appending to 'sources' list, not 'source' string
            sources.append(f"source: {source}, page#: {page}")
        
        source_str = " | ".join(sources)
        
        # CORRECTED: Key is "answer" (lowercase)
        return response["answer"], source_str

    def run_inference_and_save(self):
        """
        Runs the RAG model on all questions in the input file and saves the result.
        """
        print(f"\nApplying RAG model to {len(self.input_file)} questions...")
        
        # This part remains the same and is correct
        self.input_file[["Answer", "Source_Documents"]] = self.input_file["Question"].apply(
            lambda q: pd.Series(self.get_rag_response(q))
        )
        
        # --- Save results to a new CSV file ---
        now = datetime.now()
        string_now = now.strftime("%Y-%m-%d_%H-%M")
        
        # CORRECTED: Sanitize model names for the filename
        safe_llm_name = self.llm_model_name.replace(":", "_")
        safe_emb_name = self.emb_model_name.split('/')[-1] # Get last part of model name
        
        output_filename = f"{string_now}_llm_{safe_llm_name}_emb_{safe_emb_name}.csv"
        
        self.input_file.to_csv(output_filename, index=False, encoding='utf-8-sig')
        
        print(f"\n--- Inference Complete ---")
        print("Displaying first 5 results:")
        print(self.input_file.head())
        print(f"\nAll results saved to: {output_filename}")
        
if __name__ == "__main__": 
    file_path = r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\LLM_Law\legal-gemma-rag\free_response.txt"
    App = Solution(file_path)
    t_start = time.time()
    App.run_inference_and_save()
    t_finish = time.time()
    print("elapsed time: ", t_finish - t_start)

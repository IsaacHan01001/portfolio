


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

        # CORRECTED PROMPT CREATION using an f-string
        # Use {{...}} to escape placeholders that LangChain needs to fill later.
        min_words = 10
        # A much more direct and example-driven prompt
        template = f"""
        당신은 주어진 컨텍스트와 질문에서 핵심 키워드를 추출하는 전문 시스템입니다.

        ### 지시사항 (INSTRUCTIONS)t
        1. 질문에 대한 답변이 되는 핵심 단어들을 컨텍스트에서 추출하세요.
        2. 추출한 단어들을 쉼표(,)로만 구분하여 한 줄로 나열하세요.
        3. **절대로 문장을 만들거나 설명을 추가하지 마세요.** 번호나 불릿 포인트도 사용하지 마세요.
        4. 최소 {min_words}개의 단어를 나열해야 합니다.
        5. 답변 형식은 반드시 '단어, 단어, 단어, ...' 형태여야 합니다.

        ### 예시 (EXAMPLE)
        컨텍스트: ...전자금융거래법 제2조는 '전자장치'를 전자적 방식으로 정보를 처리하는 장치로 정의한다...
        질문: 전자금융거래법상 '전자장치'의 정의는 무엇인가?
        답변: 전자금융거래법, 제2조, 전자장치, 전자적 방식, 정보 처리, 정의

        ### 작업 (TASK)
        컨텍스트:
        {{context}}

        질문: {{input}}

        답변:
        """

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

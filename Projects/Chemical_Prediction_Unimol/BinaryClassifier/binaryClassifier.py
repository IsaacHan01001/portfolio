import os
import pandas as pd
import numpy as np
import unimol_tools
from scipy.stats import pearsonr
from typing import *
from datetime import datetime
from sklearn.model_selection import KFold 
from sklearn.metrics import accuracy_score
from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold
from matplotlib import pyplot as plt
from sklearn.metrics import confusion_matrix, classification_report, matthews_corrcoef
import seaborn as sns
import matplotlib.pyplot as plt
import seaborn as sns
import torch
import joblib 

class Solution:
    def __init__(self, testPath, model_dir = None): #  trainPath, validPath, 
        self.dir = os.path.dirname(__file__)
        # self.train = pd.read_csv(trainPath)
        # self.val = pd.read_csv(validPath)
        self.test = pd.read_csv(testPath)
        if model_dir is None:
            self.model_dir = os.path.join(self.dir, "Model")
            os.makedirs(self.model_dir, exist_ok=True)
        else:
            self.model_dir = model_dir

    def canonical_smile(self, smi):
        try:
            return Chem.MolToSmiles(Chem.MolFromSmiles(smi), canonical=True)
        except:
            return smi
        
    def main(self):
        # self.run_fine_tuning()
        preds_raw = self.make_predictions()
        self.test["TDC_prob"] = preds_raw
        self.test.to_csv(r"exp2_TDC_prob.csv", index=False)

        # preds = (preds_raw > 0.5).astype(int)
        # cm = confusion_matrix(self.test["Y"], preds)
        # print("="*50)
        # print("Confusion Matrix:")
        # print(cm)
        # print("="*50)

        # print("\nClassification Report:")
        # print(classification_report(self.test["Y"], preds, target_names=['Non-Inhibitor (0)', 'Inhibitor (1)']))
        # print("="*50)

        # # 3. The MCC - The Best Single Score
        # mcc = matthews_corrcoef(self.test["Y"], preds)
        # print(f"\nMatthews Correlation Coefficient (MCC): {mcc:.4f}")
        # print("="*50)

        """
        TDC dataset results
        Confusion Matrix:
        [[1090  295]
        [ 186  896]]
        Classification Report:
        precision    recall  f1-score   support
        Non-Inhibitor (0)       0.85      0.79      0.82      1385
        Inhibitor (1)       0.75      0.83      0.79      1082
        Generated code
        accuracy                           0.81      2467
            macro avg       0.80      0.81      0.80      2467
        weighted avg       0.81      0.81      0.81      2467

        """

    def run_fine_tuning(self):
        trainer = unimol_tools.MolTrain(
            task='classification',
            data_type='molecule',
            epochs=20,
            learning_rate= 1e-4,
            batch_size=8,
            early_stopping=8,
            metrics='f1_score', 
            split= "random",
            kfold= 1, 
            save_path= self.model_dir,
            smiles_col='Canonical_Smiles',
            target_cols=['Y'], 
            use_cuda=True,
            use_amp=True,
            model_name='unimolv1'
        )
        
        trainer.fit(self.train, df_val=self.val)

    def make_predictions(self):
        self.test["Canonical_Smiles"] = self.test["canonical_smiles"].apply(self.canonical_smile)
        predictor = unimol_tools.predict.MolPredict(load_model = self.model_dir)
        test_predictions = predictor.predict(self.test)
        print(test_predictions)
        return test_predictions

if __name__ == "__main__":
    testPath = r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\BinaryClassifier\second_exp.csv"
    sol = Solution(testPath=testPath, model_dir=r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\BinaryClassifier\Model")
    sol.main()


# filtered data since TDC inhibitor classification contradicts our dataset##
############################################################################

def canonical_smile(smi):
    try:
        return Chem.MolToSmiles(Chem.MolFromSmiles(smi), canonical=True)
    except:
        return smi
    
# training = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\multiple_experts\train.csv")
# rdkit = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\multiple_experts\rdkit_probability1234.csv")
 
# training["Canonical_Smiles"] = training["Canonical_Smiles"].apply(canonical_smile)
# rdkit["Canonical_Smiles"] = rdkit["Canonical_Smiles"].apply(canonical_smile)

# conf_train = pd.merge(training, rdkit, on="Canonical_Smiles", how="left")
# cols = [col for col in conf_train.columns if col in ['ID', 'Canonical_Smiles', 'Inhibition','TDC_prob']]

# curr = os.path.dirname(__file__)
# temp1 = conf_train[cols]

# negative_expert = temp1["TDC_prob"] < 0.25
# positive_generalist = temp1["TDC_prob"] > 0.75
# middle = (temp1["TDC_prob"] >= 0.25) & (temp1["TDC_prob"] <=0.75)

# temp1.to_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\multiple_experts\conf_included_train.csv", index=False)

def canonical_smile(smi):
    try:
        return Chem.MolToSmiles(Chem.MolFromSmiles(smi), canonical=True)
    except:
        return smi
    
# temp1 = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\multiple_experts\conf_included_train.csv")
# curr = os.path.dirname(__file__)

# filter1 = (temp1["Inhibition"] > 15) & (temp1["TDC_prob"] < 0.1)
# filter2 = (temp1["Inhibition"] < 5) & (temp1["TDC_prob"] > 0.9)
# mask = (filter1 | filter2)

# temp2 = temp1[~mask]
# neutral_data = temp1[mask]

# t1 = 0.10
# t2 = 0.90
# negative_expert = temp2["TDC_prob"] < t1
# positive_expert = temp2["TDC_prob"] > t2
# neutral_generalist = ~(negative_expert | positive_expert)


# curr = os.path.dirname(__file__)

# negative = temp2[negative_expert].reset_index(drop=True)
# positive = temp2[positive_expert].reset_index(drop=True)
# neutral = pd.concat([neutral_data, temp2[neutral_generalist]]).reset_index(drop=True)

# negative.to_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\multiple_experts\df_negative.csv", index=False)
# positive.to_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\multiple_experts\df_positive.csv", index=False)
# neutral.to_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\multiple_experts\df_neutral.csv", index = False) 

r"""
PS C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat> & C:/Users/Isaac_Han/anaconda3/envs/uni_torch_env/python.exe c:/Users/Isaac_Han/Desktop/CS/IBM_RedHat/_data/dacon/BoostUpAI2025/BinaryClassifier/binaryClassifier.py
       Inhibition    TDC_prob
count  381.000000  381.000000
mean     5.264813    0.001187
std      5.102585    0.008539
min      0.000000    0.000007
25%      0.500000    0.000017
50%      4.000000    0.000031
75%      9.945625    0.000123
max     15.000000    0.098190
       Inhibition    TDC_prob
count  616.000000  616.000000
mean    48.160759    0.997146
std     25.423111    0.009572
min      5.242607    0.906875
25%     27.292735    0.998589
50%     46.360222    0.999498
75%     69.177684    0.999782
max     99.381547    0.999952
       Inhibition   TDC_prob
count   37.000000  37.000000
mean    37.180671   0.472143
std     26.388229   0.288792
min      0.000000   0.108855
25%     13.688069   0.193334
50%     40.052490   0.386506
75%     52.683481   0.780034
max     93.100000   0.894992
PS C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat> 
"""

# test = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\test.csv")
# rdkit = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\multiple_experts\rdkit_probability1234.csv")
# test["Canonical_Smiles"] = test["Canonical_Smiles"].apply(canonical_smile)
# rdkit["Canonical_Smiles"] = rdkit["Canonical_Smiles"].apply(canonical_smile)

# test_with_prob = pd.merge(test, rdkit, on="Canonical_Smiles", how ="left")
# test_with_prob.to_csv("test_with_rdkit_prob.csv", index = False)

# OOF = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\noisy_label_reduced\oof.csv")
# prob = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\noisy_label_reduced\conf_included_train.csv")

# OOF["Canonical_Smiles"] = OOF["Canonical_Smiles"].apply(canonical_smile)
# prob["Canonical_Smiles"] = prob["Canonical_Smiles"].apply(canonical_smile)
# temp = prob.rename(columns={"Inhibition": "Inhibition_true"})

# oof_with_tdc = pd.merge(OOF, temp[["Canonical_Smiles","Inhibition_true","TDC_prob"]], on="Canonical_Smiles", how="left")
# print(oof_with_tdc.head())
# print(oof_with_tdc.columns.to_list())
# final = oof_with_tdc[["ID", "Canonical_Smiles", "Inhibition", "Inhibition_true", "TDC_prob", "TDC_conf_true_inhibitor", "TDC_conf_non_inhibitor"]]
# final.to_csv("OOF_conf_included.csv", index=False)

############TEST PIPELINE############################
#####################################################

# test_prob = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\noisy_label_reduced\test_inhibit_prob_attached.csv")
# test_prob["Canonical_Smiles"] = test_prob["Canonical_Smiles"].apply(canonical_smile)
# test_prob["TDC_conf_true_inhibitor"] = test_prob["TDC_prob"] > 0.8
# test_prob["TDC_conf_non_inhibitor"] = test_prob["TDC_prob"] < 0.2

# result = test_prob[['ID', 'Canonical_Smiles', 'Inhibition', 'TDC_prob','TDC_conf_true_inhibitor', 'TDC_conf_non_inhibitor']]

# pd1 = result
# pd2 = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\noisy_label_reduced\rdkitcolumns.csv")
# pd1["Canonical_Smiles"] = pd1["Canonical_Smiles"].apply(canonical_smile)
# pd2["Canonical_Smiles"] = pd2["Canonical_Smiles"].apply(canonical_smile)

# result = pd.merge(pd1[['ID', 'Canonical_Smiles', 'Inhibition', 'TDC_prob', "TDC_conf_true_inhibitor", "TDC_conf_non_inhibitor"]], pd2, on = "Canonical_Smiles", how="left")
# print(result)
# result.to_csv("test_rdkit_features_attached.csv", index = False)
import os
import pandas as pd
import numpy as np
import unimol_tools
from scipy.stats import pearsonr
from typing import *
from datetime import datetime
from sklearn.model_selection import KFold
from rdkit import Chem
from rdkit.Chem.Scaffolds import MurckoScaffold
from matplotlib import pyplot as plt
import seaborn as sns
import torch
import joblib

class Solution:
    def __init__(self, train_path: str, test_path: str, save_dir: str, seed: int = 42):
        self.train_path = train_path
        self.test_path = test_path
        self.save_dir = save_dir
        self.seed = seed
        self.path_train = []
        self.path_val = []
        self.model_path = []
        self.lr = 5e-5
        self.bs = 16

        os.makedirs(self.save_dir, exist_ok=True)

    def main(self):
        # self.create_kfold_csv_splits()
        self.create_scaffold_kfold() 

        oof_fold_predictions = []
        for i, (path_train, path_val) in enumerate(zip(self.path_train, self.path_val)):
            model_path = os.path.join(self.save_dir, f"Model{i}")
            self.model_path.append(model_path)
            os.makedirs(model_path)
            
            df_train = pd.read_csv(path_train)
            df_val = pd.read_csv(path_val)

            self.run_fine_tuning(df_train, model_path, val_df = df_val)
            df_prediction = self.make_predictions(df_val, model_path)
            
            oof_fold_predictions.append(df_prediction)
        
        oof_df = pd.concat(oof_fold_predictions, axis = 0, ignore_index = True)
        sorted_oof_df = oof_df.sort_values(by = "ID", ascending = True)
        oof_path = os.path.join(self.save_dir, "oof.csv")
        sorted_oof_df.to_csv(oof_path, index = False)
        print(f"oof_df_saved to {self.save_dir}")

        df_oof = pd.read_csv(oof_path)
        df_train = pd.read_csv(self.train_path)
        
        competition_score_train = self.competitionscore(df_train["Inhibition"] , df_oof["Inhibition"])
        print("Score for training", competition_score_train)
        
        # preds = []

        # df_test = pd.read_csv(self.test_path)
        # for model_path in self.model_path:
        #     prediction = self.make_predictions(df_test, model_path)["Inhibition"]
        #     preds.append(prediction)
        
        # prediction = pd.concat(preds, axis = 1).mean(axis=1)
        # df_test["Inhibition"] = prediction
        # now = datetime.now()
        # string = now.strftime("%d%m%Y_%H%M")
        # df_test.to_csv(os.path.join(self.save_dir, f"Score_{competition_score_train}_time_{string}_Submission.csv"), index=False)

    def competitionscore(self, y_true, y_pred):
        y_true, y_pred = np.array(y_true), np.array(y_pred)
        if y_true.max() == y_true.min(): return 0.0
        rmse = np.sqrt(np.mean((y_true - y_pred) ** 2))
        nrmse = rmse / (y_true.max() - y_true.min())
        if np.isnan(nrmse): return 0.0
        pearson, _ = pearsonr(y_true, y_pred)
        if np.isnan(pearson): pearson = 0
        return 0.5 * (1 - min(1, nrmse)) + 0.5 * pearson

    def generate_scaffold_groups(self, df, smiles_col='Canonical_Smiles'):
        scaffolds = {}
        for idx, smiles in enumerate(df[smiles_col]):
            mol = Chem.MolFromSmiles(smiles)
            if mol is None:
                scaffold = f'unparsable_{idx}'
            else:
                scaffold = Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(mol))
            scaffolds.setdefault(scaffold, []).append(idx)
        return list(scaffolds.values())

    def scaffold_k_fold_split(self, df, n_splits=5, smiles_col='Canonical_Smiles', seed=42):
        # Group samples by scaffold
        scaffold_groups = self.generate_scaffold_groups(df, smiles_col)
        
        kf = KFold(n_splits=n_splits, shuffle=True)
        folds = []
        scaffold_groups = np.array(scaffold_groups, dtype=object)

        for train_group_idx, val_group_idx in kf.split(scaffold_groups):
            train_idx = [i for group in scaffold_groups[train_group_idx] for i in group]
            val_idx   = [i for group in scaffold_groups[val_group_idx] for i in group]
            folds.append((train_idx, val_idx))

        return folds

    def create_scaffold_kfold(self, n_splits: int = 5, smiles_col: str = 'Canonical_Smiles'):
        """
        Splits a dataset into K scaffold-based folds and saves train/val CSVs for each fold.

        Args:
            n_splits (int): Number of folds to create.
            smiles_col (str): Column name containing SMILES strings for scaffold grouping.
        """
        df = pd.read_csv(self.train_path)
        folds = self.scaffold_k_fold_split(df, n_splits=n_splits, smiles_col=smiles_col, seed=self.seed)

        print(f"\nScaffold KFold splitting '{os.path.basename(self.train_path)}' into {n_splits} folds...")

        for i, (train_index, val_index) in enumerate(folds):
            fold_train_df = df.iloc[train_index]
            fold_val_df = df.iloc[val_index]

            fold_train_path = os.path.join(self.save_dir, f'fold_{i}_train.csv')
            fold_val_path = os.path.join(self.save_dir, f'fold_{i}_validation.csv')
            
            self.path_train.append(fold_train_path)
            self.path_val.append(fold_val_path)

            fold_train_df.to_csv(fold_train_path, index=False)
            fold_val_df.to_csv(fold_val_path, index=False)

        print("\nProcess complete. All scaffold-based fold CSV files have been created.")

    def create_kfold_csv_splits(self, n_splits: int = 5):
        """
        Reads a CSV file, splits it into K folds for cross-validation, and saves
        each fold's training and validation set as a separate CSV file.

        Args:
            input_csv_path (str): The path to the input CSV file to be split.
            output_dir (str): The directory where the fold CSV files will be saved.
            n_splits (int): The number of folds to create.
            seed (int): A random seed for reproducibility of the shuffle.
        """

        df = pd.read_csv(self.train_path)
        kf = KFold(n_splits=n_splits, shuffle=True, random_state = self.seed)

        print(f"\nSplitting '{os.path.basename(self.train_path)}' into {n_splits} folds...")

        for i, (train_index, val_index) in enumerate(kf.split(df)):
            fold_train_df = df.iloc[train_index]
            fold_val_df = df.iloc[val_index]

            fold_train_path = os.path.join(self.save_dir, f'fold_{i}_train.csv')
            fold_val_path = os.path.join(self.save_dir, f'fold_{i}_validation.csv')
            
            self.path_train.append(fold_train_path)
            self.path_val.append(fold_val_path)

            fold_train_df.to_csv(fold_train_path, index=False)
            fold_val_df.to_csv(fold_val_path, index=False)

        print("\nProcess complete. All fold CSV files have been created.")

    def run_fine_tuning(self, train_df, save_dir, scaffolding = False, val_df = None):
        
        if scaffolding:
            split_method = "scaffold"
            kfold = 5
        else:
            split_method = "random"
            kfold = 1

        trainer = unimol_tools.MolTrain(
            task='regression',
            data_type='molecule',
            epochs=100,
            learning_rate=self.lr,
            batch_size=self.bs,
            early_stopping=15,
            metrics='pearsonr', 
            split= split_method,
            kfold= kfold, 
            save_path= save_dir,
            smiles_col='Canonical_Smiles',
            target_cols=['Inhibition'],
            use_cuda=True,
            use_amp=True,
            model_name='unimolv1'
        )
        if val_df is not None:
            print("manual Validation Provided")
            trainer.fit(train_df, df_val=val_df)
        else:
            trainer.fit(train_df)

    def make_predictions(self, df_test, load_dir, clipping = False):
        print(f"--- Generating predictions from model in: {self.save_dir} ---")

        predictor = unimol_tools.predict.MolPredict(load_model = load_dir)
        test_predictions = predictor.predict(df_test)
        if test_predictions.ndim == 2: 
            test_predictions = test_predictions.mean(axis=1)
        
        if clipping:
            test_predictions.clip(lower=0, inplace=True)

        df_test["Inhibition"] = test_predictions

        return df_test

if __name__ == "__main__":
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dir_name = "Noisy_label_reduction2"
    train_path = os.path.join(current_dir, 'filtered_train.csv')
    test_path = os.path.join(current_dir, 'test.csv')
    model_save_directory = os.path.join(current_dir, dir_name)
    solution = Solution(
        train_path=train_path,
        test_path=test_path,
        save_dir=model_save_directory,
        seed = 42
    )

    # solution.main()    

    df_test = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\noisy_label_reduced\exp1_TDC_prob.csv")
    current_dir = os.path.dirname(os.path.abspath(__file__))
    dir_name = "noisy_label_reduced"

    dfs_tests = []
    for i in range(5):
        model_dir = os.path.join(current_dir, dir_name, f"Model{i}")
        preds = solution.make_predictions(df_test=df_test, load_dir=model_dir)["Inhibition"]
        dfs_tests.append(preds)

    n = len(dfs_tests)
    avg = pd.Series(0.0, index = dfs_tests[0].index)
    for s in dfs_tests:
        avg += s
    avg /= n

    print(avg)
    df_test["Inhibition"] = avg
    df_test.to_csv("exp1_TDC_inhibit.csv", index = False)


# Testing ####
###############################################################################
# def canonical_smile(smi):
#     try:
#         return Chem.MolToSmiles(Chem.MolFromSmiles(smi), canonical=True)
#     except:
#         return smi
    
# df_test = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\test_with_rdkit_prob.csv")
# df_test["Canonical_Smiles"] = df_test["Canonical_Smiles"].apply(canonical_smile)

# df_negative = df_test[df_test["TDC_prob"] < 0.1][["ID", "Canonical_Smiles"]].copy().reset_index(drop = True)
# df_positive = df_test[df_test["TDC_prob"] > 0.9][["ID", "Canonical_Smiles"]].copy().reset_index(drop = True)

# # Get the IDs of already selected samples
# excluded_ids = pd.concat([df_negative["Canonical_Smiles"], df_positive["Canonical_Smiles"]])
# df_neutral = df_test[~df_test["Canonical_Smiles"].isin(excluded_ids)][["ID", "Canonical_Smiles"]].copy().reset_index(drop=True)

# # print(df_negative) #56 negative non-inhibitors
# # print(df_positive) #44 positive inhibitors
# # print(df_neutral) # 0 realized testing set is strictly adhering to TDC complied inhibitor and non-inhibitors.
# path_neg = r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\multiple_expert2\negative_specialist"
# path_pos = r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\multiple_expert2\positive_specialist"

# results = []

# for df_test, model_path in zip([df_negative, df_positive], [path_neg, path_pos]):
#     current_dir = os.path.dirname(os.path.abspath(__file__))
#     dir_name = "multiple_experts"
#     test_path = os.path.join(current_dir, 'test.csv')
#     train_path = os.path.join(current_dir, dir_name, "df_neutral.csv")
#     model_save_directory = os.path.join(current_dir, dir_name, 'neutral_generalist')
#     solution = Solution(
#         train_path=train_path,
#         test_path=test_path,
#         save_dir=model_save_directory,
#         seed = 42
#     )

#     dfs_tests = []
#     for i in range(5):
#         model_dir = os.path.join(model_path, f"Model{i}")
#         preds = solution.make_predictions(df_test=df_test, load_dir=model_dir)["Inhibition"]
#         dfs_tests.append(preds)

#     n = len(dfs_tests)
#     avg = pd.Series(0.0, index = dfs_tests[0].index)
#     for s in dfs_tests:
#         avg += s
#     avg /= n

#     print(avg)
#     results.append(avg)

# df_negative["Inhibition"] = results[0]
# df_positive["Inhibition"] = results[1]

# final_test = pd.concat([df_negative, df_positive], axis = 0)[["ID", "Inhibition"]].sort_values(by = "ID")
# final_test.to_csv("Fianl_Submission_of_multiple_experts_model.csv", index = False)
    
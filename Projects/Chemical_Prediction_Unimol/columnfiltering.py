import pandas as pd
import numpy as np
import xgboost as xgb
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import root_mean_squared_error
from sklearn.model_selection import KFold
from scipy.stats import pearsonr
import os
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.Chem import Descriptors
from rdkit.Chem.Scaffolds import MurckoScaffold
from rdkit import DataStructs
from rdkit import RDLogger
from sklearn.feature_selection import VarianceThreshold
import matplotlib.pyplot as plt
import seaborn as sns

RDLogger.DisableLog('rdApp.*')
os.environ["TOKENIZERS_PARALLELISM"] = "false"

class xgbpipeline():
    def __init__(self, trainPath, rdkitcsv, dir_name = None, testcase = None):
        self.OOFtrain = pd.read_csv(trainPath)
        self.rdkitcsv =  pd.read_csv(rdkitcsv)
        self.test = pd.read_csv(testcase) if testcase is not None else None
        self.dir_name = dir_name
        self.models_config = {}
        self.final_indices = None
        self.y_scaler = False
        result = [1] + [0] * 29  # length 30 list
        self.params = {
            'objective': 'reg:pseudohubererror', 
            'eval_metric': 'rmse',               
            'learning_rate': 0.05,
            'max_depth': 6,
            'subsample': 0.8,
            'colsample_bytree': 0.8,
            'reg_lambda': 0.5,
            'min_child_weight': 1,
            'tree_method': 'hist',
            'seed': 42,
            'monotone_constraints': f"({','.join(map(str, result))})",
        }
        self.num_boost_round = 2000
        self.early_stopping_rounds = 50

    def main(self):
        def canonical_smile(smi):
            try:
                return Chem.MolToSmiles(Chem.MolFromSmiles(smi), canonical=True)
            except:
                return smi

        # --- 1. Data Preparation ---
        self.OOFtrain["Canonical_Smiles"] = self.OOFtrain["Canonical_Smiles"].apply(canonical_smile)
        df_train = pd.merge(self.OOFtrain, self.rdkitcsv, on="Canonical_Smiles", how="left")
        y_true = df_train.pop("Inhibition_true")

        baseline_score = root_mean_squared_error(y_true, df_train["Inhibition"])
        print("\n" + "="*50)
        print(f"🎯 Baseline Score (Previous Model vs. Truth): {baseline_score:.5f}")
        print("="*50 + "\n")
        
        # --- 2. Feature Selection ---
        initial_features = [col for col in df_train.columns if col not in ["ID", "Canonical_Smiles","split", "Unnamed: 0"]]
        df_features_only = df_train[initial_features]

        variance_indices = self.select_features_by_variance(df_features_only)
        correlation_indices = self.select_features_by_correlation(df_features_only, variance_indices)
        final_selected_indices = self.rank_features_by_importance(df_features_only, y_true, correlation_indices, n_features=30)
        
        # Get the column NAMES from the final indices
        final_selected_features = df_features_only.columns[final_selected_indices].tolist()
        
        # Create the final dataframe for training with ONLY the selected features
        df_final_selected = df_train[['ID', 'Canonical_Smiles'] + final_selected_features]

        sns.scatterplot(x=y_true, 
                        y=df_train["Inhibition"],
                        hue = df_train["TDC_conf_true_inhibitor"],
                        palette="coolwarm",
                        alpha = 0.7,
                        )
        plt.plot([0, 100], [0, 100], 'r--') # Add a line for perfect predictions
        plt.xlabel("True Inhibition")
        plt.ylabel("Unimol Baseline Prediction")
        plt.title("Baseline Performance & Bias")
        plt.show()

        # --- 3. Model Training ---
        self.train_with_scaffold_cv(df_final_selected, y_true)
        
        # --- 4. Prediction on Test Set ---
        if self.test is not None:
            df_test_selected = self.test[['ID', 'Canonical_Smiles'] + final_selected_features]
            self.xgb_predict(df_test_selected)
            
            """
            Index(['ID', 'Canonical_Smiles', 'Inhibition', 'AUTOCORR2D_1', 'AUTOCORR2D_2',
        'AUTOCORR2D_3', 'AUTOCORR2D_4', 'AUTOCORR2D_5', 'AUTOCORR2D_6',
        'AUTOCORR2D_7',
        ...
        'fr_sulfonamd', 'fr_sulfone', 'fr_term_acetylene', 'fr_tetrazole',
        'fr_thiazole', 'fr_thiocyan', 'fr_thiophene', 'fr_unbrch_alkane',
        'fr_urea', 'qed'],
            dtype='object', length=223)
            """
            

    def plot_feature_importance(self, importance_df, n_top_features=30):
        """
        Creates and displays a bar plot of the top N feature importances
        and prints the list to the console.
        """
        # Select the top N features for plotting and printing
        top_df = importance_df.head(n_top_features)

        # --- START: NEW CODE BLOCK FOR PRINTING ---
        print("\n" + "="*70)
        print(f"Top {n_top_features} Most Important Features (Name and Value):")
        print("="*70)
        # .to_string() provides a clean, copy-pasteable format
        print(top_df.to_string(index=False))
        print("="*70 + "\n")
        # --- END: NEW CODE BLOCK ---

        # The plotting code remains the same
        plt.figure(figsize=(12, 10))
        sns.barplot(x="Importance", y="Feature", data=top_df, orient='h')
        
        plt.title(f'Top {n_top_features} Feature Importances')
        plt.xlabel('Importance (Gain)')
        plt.ylabel('Feature')
        plt.grid(axis='x', linestyle='--', alpha=0.6)
        plt.tight_layout()
        
        plt.show()

    def select_features_by_variance(self, df_x, threshold=0.01):
        """Removes low-variance features and returns their integer indices."""
        selector = VarianceThreshold(threshold=threshold)
        selector.fit(df_x)
        
        # Get the integer indices of the columns to keep
        retained_indices = selector.get_support(indices=True)
        
        print(f"Variance Threshold: Removed {df_x.shape[1] - len(retained_indices)} features. Retaining {len(retained_indices)}.")
        return retained_indices

    def select_features_by_correlation(self, df_x, current_indices, threshold=0.95):
        """
        Takes a dataframe and a list of current valid indices.
        Removes highly correlated features and returns an updated list of indices.
        """
        print(f"Correlation Threshold: Starting with {len(current_indices)} features.")
        
        # Work on a subset of the data defined by the current indices
        df_subset = df_x.iloc[:, current_indices]
        corr_matrix = df_subset.corr().abs()
        upper = corr_matrix.where(np.triu(np.ones(corr_matrix.shape), k=1).astype(bool))
        
        # Find names of columns to drop *from the subset*
        to_drop_names = [column for column in upper.columns if any(upper[column] > threshold)]
        
        # Get the names of columns to keep
        retained_names = [col for col in df_subset.columns if col not in to_drop_names]
        
        # Map retained names back to their original indices
        retained_indices = [df_x.columns.get_loc(col) for col in retained_names]
        
        print(f"Correlation Threshold: Dropped {len(to_drop_names)} features. Retaining {len(retained_indices)}.")
        return retained_indices

    def rank_features_by_importance(self, df_x, y, current_indices, n_features=40):
        """
        Takes a dataframe and current indices. Ranks features using xgb.train,
        displays a plot, and returns the top N integer indices.
        """
        print(f"Ranking features with xgb.train and selecting top {n_features}...")
        
        df_subset = df_x.iloc[:, current_indices]
        dtrain_rank = xgb.DMatrix(df_subset, label=y)
        
        ranking_params = {
            'objective': 'reg:pseudohubererror',
            'eval_metric': 'mae',
            'learning_rate': 0.1, 
            'max_depth': 5, 
            'seed': 42
        }
        
        ranker_model = xgb.train(
            params=ranking_params, dtrain=dtrain_rank,
            num_boost_round=250, verbose_eval=False
        )
        
        importances = ranker_model.get_score(importance_type='gain')
        
        importance_df = pd.DataFrame({
            'Feature': list(importances.keys()),
            'Importance': list(importances.values())
        }).sort_values(by='Importance', ascending=False)
        
        # --- NEW LINE ADDED HERE ---
        # Call the plotting function to show the graph
        self.plot_feature_importance(importance_df, n_top_features=n_features)
        
        top_feature_names = importance_df['Feature'].head(n_features).tolist()
        final_selected_indices = [df_x.columns.get_loc(col) for col in top_feature_names]
        
        print("\n--- Top 10 Most Important Features ---")
        print(importance_df.head(10))
        print(f"----------------------------------------\nSelected top {len(final_selected_indices)} features for the model.\n")
        
        return final_selected_indices

    def train_with_scaffold_cv(self, df_x, y, smiles_col='Canonical_Smiles'):
        x_cols = [col for col in df_x.columns if col not in ["ID","Canonical_Smiles"]]

        y_original = y.copy()
        y_scaled = y.copy()

        folds = self.scaffold_k_fold_split(df_x, n_splits=5, smiles_col=smiles_col) 
        models = []
        fold_scores = []
        scalers = []
        oof_predictions = np.zeros(len(df_x))
        y_scaler = False
        scale_factor = 1.0

        if y_original.max() > 1:
            y_scaled /= 100
            y_scaler = True
            scale_factor = 100
            self.y_scaler = True

        for fold_num, (train_idx, val_idx) in enumerate(folds):
            X_train_fold, y_train_fold = df_x.iloc[train_idx], y_scaled.iloc[train_idx]
            X_valid_fold, y_valid_fold = df_x.iloc[val_idx], y_scaled.iloc[val_idx]
            
            scaler = StandardScaler()
            X_train_scaled = X_train_fold.copy()
            X_valid_scaled = X_valid_fold.copy()
            
            X_train_scaled[x_cols] = scaler.fit_transform(X_train_fold[x_cols])
            X_valid_scaled[x_cols] = scaler.transform(X_valid_fold[x_cols])
            scalers.append(scaler)

            dtrain = xgb.DMatrix(X_train_scaled[x_cols], label=y_train_fold)
            dvalid = xgb.DMatrix(X_valid_scaled[x_cols], label=y_valid_fold)
            watchlist = [(dtrain, 'train'), (dvalid, 'valid')]
            
            model = xgb.train(
                params=self.params,
                dtrain=dtrain,
                num_boost_round=self.num_boost_round,
                evals=watchlist,
                # custom_metric=self.xgb_eval_metric,
                # maximize=True,
                early_stopping_rounds=self.early_stopping_rounds,
                verbose_eval=40 # Quieter for the example
            )
            
            val_pred = model.predict(dvalid, iteration_range=(0, model.best_iteration))
            val_pred_orig = val_pred * scale_factor
            oof_predictions[val_idx] = val_pred_orig # Store OOF preds
            
            y_valid_orig = y_original.iloc[val_idx]

            # score = self.cp_calc(y_valid_orig, val_pred_orig)
            score = root_mean_squared_error(y_valid_orig, val_pred_orig)
            fold_scores.append(score)
            print(f"✅ Fold {fold_num + 1} Score: {score:.5f}")
            
            models.append(model)
        
        cv_mean = np.mean(fold_scores)        
        self.OOFtrain["XBG_OOF_result"] = oof_predictions 
        self.OOFtrain.to_csv(os.path.join(os.path.dirname(__file__), self.dir_name, f"Results_of_final_xgb_score{cv_mean}.csv"), index=False)
        self.models_config = {"Model" : models, "Scaler": scalers, "Score" : fold_scores, "Y_scaler" : y_scaler, "Mean_Score" : cv_mean}
    
    def xgb_predict(self, df_test):
        df_test_original = df_test.copy()
        x_cols = [col for col in df_test.columns if col not in ["ID","Canonical_Smiles"]]

        all_fold_predictions = []

        for i, model in enumerate(self.models_config["Model"]):
            scaler = self.models_config["Scaler"][i]
            test_scaled_fold = df_test_original.copy()
            test_scaled_fold[x_cols] = scaler.transform(df_test_original[x_cols])
            dtest_fold = xgb.DMatrix(test_scaled_fold[x_cols])
            pred_test = model.predict(dtest_fold)
            all_fold_predictions.append(pred_test)
            
            # print(pred_test)
        avg_predictions = np.mean(all_fold_predictions, axis=0)

        if self.models_config["Y_scaler"]:
            avg_predictions *= 100

        submission_df = pd.DataFrame({
            "ID" : df_test_original["ID"],
            "Inhibition" : avg_predictions,
        })

        mean_score = self.models_config["Mean_Score"]
        path = os.path.join(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025", self.dir_name, f"score_{mean_score}_test_prediction.csv")
        submission_df.to_csv(path, index=False)
        print(submission_df.describe())

    def scaffold_k_fold_split(self, df_x, n_splits=5, smiles_col='Canonical_Smiles'):
        def generate_scaffold_groups(df_x):
            scaffolds = {}
            for idx, smiles in enumerate(df_x[smiles_col]):
                mol = Chem.MolFromSmiles(smiles)
                if mol is None:
                    raise Exception("Not a smile")
                scaffold = Chem.MolToSmiles(MurckoScaffold.GetScaffoldForMol(mol))

                if not scaffold:
                    scaffold = smiles

                scaffolds.setdefault(scaffold, []).append(idx)
            return list(scaffolds.values())

        scaffold_groups = generate_scaffold_groups(df_x)
        kf = KFold(n_splits=n_splits, shuffle=True)
        folds = []
        scaffold_groups = np.array(scaffold_groups, dtype=object)

        for train_group_idx, val_group_idx in kf.split(scaffold_groups):
            train_idx = [i for group in scaffold_groups[train_group_idx] for i in group]
            val_idx   = [i for group in scaffold_groups[val_group_idx] for i in group]
            folds.append((train_idx, val_idx))
    
        return folds

if __name__ == "__main__":
    trainOOFPath = r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\noisy_label_reduced\OOF_conf_included.csv"
    rdkitcsv = r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\noisy_label_reduced\rdkitcolumns.csv" 
    dir_name = r"noisy_label_reduced"
    testPath = r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\noisy_label_reduced\test_rdkit_features_attached.csv"
    pipeline2 = xgbpipeline(trainOOFPath, rdkitcsv, dir_name=dir_name, testcase=testPath)
    pipeline2.main()

##########################################################################################################################

class rdkit_xgboost_csv():
    def __init__(self, unifiedPath):
        self.unifiedPath = unifiedPath
        self.rdkitcsv = pd.read_csv(self.unifiedPath)
        self.descriptors = []
        self.kept_names = []

    def produce_rdkitcsv(self): 
        self.get_molecular_descriptors()
        smiles_list = list(self.rdkitcsv["Canonical_Smiles"])
        np_features = self.smiles_to_features(smiles_list, self.descriptors)
        np_xgb = self.clean_missing_cols(np_features, 0.8)
        np_extra = self.clean_features(np_xgb)
        
        df_extra= pd.DataFrame(np_extra, columns=self.kept_names)
        rdkit_features_df = pd.concat([self.rdkitcsv, df_extra], axis = 1)
        rdkit_features_df.to_csv(r"_data/dacon/BoostUpAI2025/ManualScaffold_seed42/rdkitcolumns.csv", index=False)

    def get_molecular_descriptors(self, max_autocorr=10):
        """Get molecular descriptors - either hardcoded list or auto-discovered"""

        descriptor_list_all = []
        test_mol = Chem.MolFromSmiles('Cl.OC1(Cc2cccc(Br)c2)CCNCC1')

        # Collect all valid descriptors first
        for name in dir(Descriptors):  # 返回 Descriptors 模块下所有的属性名称列表（字符串），包括：描述符函数名（如 MolWt, MolLogP, TPSA 等）、常量、类、方法等
            if not name.startswith('_'):
                try:
                    func = getattr(Descriptors, name)  # 从 Descriptors 模块中根据字符串变量 name 获取实际的函数/对象。
                    if callable(func):  # 判断 func 是否为可调用对象（函数、方法等）
                        result = func(test_mol)
                        if isinstance(result, (int, float)) and not np.isnan(result):
                            descriptor_list_all.append((name, func))
                except:
                    pass

        print(f"🔍 Total discovered descriptors before filtering: {len(descriptor_list_all)}")

        # Sort AUTOCORR2D descriptors by their numeric suffix
        autocorr_descriptors = [
            (name, func)
            for name, func in descriptor_list_all
            if name.startswith('AUTOCORR2D_')
        ]
        autocorr_descriptors.sort(key=lambda x: int(x[0].split('_')[-1]))

        # Select only the lowest-numbered ones
        limited_autocorr = autocorr_descriptors[:max_autocorr]

        # Include all other descriptors
        other_descriptors = [
            (name, func)
            for name, func in descriptor_list_all
            if not name.startswith('AUTOCORR2D_')
        ]

        # Final descriptor list
        descriptor_list = limited_autocorr + other_descriptors

        print(f"✅ Auto-discovered {len(descriptor_list)} descriptors (limited to {max_autocorr} AUTOCORR2D):")
        names = [name for name, _ in descriptor_list]
        print("  " + ", ".join(names))

        feature_names = [name for name, _ in descriptor_list]
        self.descriptors = descriptor_list
        return descriptor_list, feature_names

    def smiles_to_features(self, smiles_list, descriptor_functions):
        """ 
        Convert SMILES strings to raw feature matrix
        https://www.kaggle.com/code/richolson/smiles-rdkit-lgbm-ftw 
        """

        features = []
        total = len(smiles_list)

        print(f"Processing {total} SMILES...", end="", flush=True)

        for i, smiles in enumerate(smiles_list):
            # Progress indicator every 1000 molecules or at milestones
            if i > 0 and (i % 1000 == 0 or i == total - 1):
                print(f" {i+1}/{total}", end="", flush=True)

            mol_features = []
            try:
                mol = Chem.MolFromSmiles(smiles)
                if mol is None:
                    # Invalid SMILES - fill with NaN
                    mol_features = [np.nan] * len(descriptor_functions)
                else:
                    # Calculate each descriptor
                    for name, func in descriptor_functions:
                        try:
                            value = func(mol)
                            # Handle problematic values
                            if np.isinf(value) or abs(value) > 1e10:
                                value = np.nan
                            mol_features.append(value)
                        except:
                            # Descriptor calculation failed
                            mol_features.append(np.nan)
            except:
                # Complete failure - fill entire row with NaN
                mol_features = [np.nan] * len(descriptor_functions)

            features.append(mol_features)

        print(" ✅", flush=True)
        result = np.array(features, dtype=float)
        print("fetched values: ", result)
        return result

    def clean_features(self, X):
        """Handle NaN/inf values and impute missing data"""
        # Create a copy to avoid modifying the original
        print(f"🧪 Before cleaning: {X.shape}")

        X_clean = X.copy()

        X_clean[np.isinf(X_clean)] = np.nan

        # Count and report missing values
        missing = np.isnan(X_clean).sum()
        print(f"🧹 Cleaned {missing:,} missing values ({missing/X_clean.size*100:.1f}%)")

        # Median imputation
        for i in range(X_clean.shape[1]):
            col = X_clean[:, i]
            if np.isnan(col).any():
                X_clean[np.isnan(col), i] = np.nanmedian(col) if not np.isnan(np.nanmedian(col)) else 0
                n_nan = np.isnan(col).sum()
                n_unique = len(np.unique(col[~np.isnan(col)]))
                print(f"Col {i}: NaN={n_nan}, Unique={n_unique}")

        return X_clean
    
    def clean_missing_cols(self, arr, threshold):
        r_missing = np.isnan(arr).mean(axis=0)  # axis=0 means column-wise
        cols_to_keep = np.where(r_missing <= threshold)[0]
        descriptor_names = [name for name, _ in self.descriptors]
        self.kept_names = [descriptor_names[i] for i in cols_to_keep]
        return arr[:, cols_to_keep]

####------------- yielding unified rdkit params ________________
# if __name__ == "__main__":
#     unifiedPath = r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\ManualScaffold_seed42\unified_smiles.csv"
#     processor = rdkit_xgboost_csv(unifiedPath)
#     processor.produce_rdkitcsv()
###-------------------------------------------------------------


    
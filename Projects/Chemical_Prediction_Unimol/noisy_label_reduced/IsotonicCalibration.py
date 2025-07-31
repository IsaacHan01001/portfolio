import pandas as pd
from sklearn.isotonic import IsotonicRegression
import numpy as np

# def calibrate():
#     # --- STEP 1: DEFINE YOUR FILE PATHS ---

#     # This is the file with out-of-fold predictions from your training run.
#     # It MUST contain the true labels (e.g., 'Inhibition_true') and your model's predictions (e.g., 'XGB_OOF_Result').
#     oof_file_path = r'C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\noisy_label_reduced\Results_of_final_xgb_score17.03014127895512.csv'

#     # This is the final submission file you want to correct.
#     # It MUST contain the 'ID' and your model's predictions (e.g., 'Inhibition').
#     submission_to_correct_path = r'C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\noisy_label_reduced\LegacyFile\Clipped_Score_0.7054230285823235_time_29072025_1408_Submission.csv'

#     # This will be the name of your new, improved submission file.
#     calibrated_submission_path = 'submission_CALIBRATED2ndtime.csv'


#     # --- STEP 2: LOAD THE DATA ---

#     try:
#         df_oof = pd.read_csv(oof_file_path)
#         df_submission = pd.read_csv(submission_to_correct_path)
#     except FileNotFoundError as e:
#         print(f"Error: Could not find a file. Please check your paths.")
#         print(e)
#         exit()

#     # --- VALIDATE COLUMN NAMES ---
#     # Make sure you have the right column names. Adjust these if yours are different.
#     oof_prediction_col = 'Inhibition'
#     true_label_col = 'Inhibition_true'
#     submission_prediction_col = 'Inhibition'

#     if not all(col in df_oof.columns for col in [oof_prediction_col, true_label_col]):
#         print(f"Error: OOF file is missing required columns. Expected '{oof_prediction_col}' and '{true_label_col}'.")
#         exit()

#     if submission_prediction_col not in df_submission.columns:
#         print(f"Error: Submission file is missing the prediction column '{submission_prediction_col}'.")
#         exit()


#     # --- STEP 3: TRAIN THE CALIBRATOR (THE CORRECT ORDER) ---

#     print("Training the Isotonic Regression calibrator...")

#     # The X variable is the feature we are learning FROM (your model's biased predictions).
#     X_cal = df_oof[oof_prediction_col].clip(lower=0, upper=100)

#     # The y variable is the target we are learning TO (the ground truth).
#     y_cal = df_oof[true_label_col]

#     # Create and fit the calibrator model
#     # It learns the function: f(Biased_Prediction) -> True_Value
#     iso_reg = IsotonicRegression(y_min=0, y_max=100, out_of_bounds="clip")
#     iso_reg.fit(X_cal, y_cal)

#     print("Calibration model trained successfully.")


#     # --- STEP 4: APPLY THE CALIBRATION TO YOUR SUBMISSION FILE ---

#     # Get the original, biased predictions from your submission file
#     original_test_predictions = df_submission[submission_prediction_col]

#     # Use the trained calibrator to transform them into new, corrected predictions
#     calibrated_test_predictions = iso_reg.transform(original_test_predictions)

#     # Create the new submission dataframe
#     df_calibrated_submission = pd.DataFrame({
#         'ID': df_submission['ID'],
#         'Inhibition': calibrated_test_predictions
#     })


#     # --- STEP 5: SAVE AND ANALYZE THE FINAL RESULT ---

#     df_calibrated_submission.to_csv(calibrated_submission_path, index=False)

#     print(f"\nCalibration complete! New submission file saved to: {calibrated_submission_path}")

#     print("\n--- Original Submission Stats ---")
#     print(original_test_predictions.describe())

#     print("\n--- Calibrated Submission Stats ---")
#     print(df_calibrated_submission['Inhibition'].describe())

# calibrate()

# def weighted_calibration(weight, df1, df2):
#     return df1["Inhibition"]

sub = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\noisy_label_reduced\LegacyFile\Score_0.7054230285823235_time_29072025_1408_Submission.csv")
train = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\noisy_label_reduced\Results_of_final_xgb_score17.03014127895512.csv")
y_pred = sub["Inhibition"]
y_true = train["Inhibition_true"]
y_pred = np.clip((y_pred - y_pred.mean()) / y_pred.std() * y_true.std() + y_true.mean(), 0, 100)
sub["Inhibition"] = y_pred
sub.to_csv("final_clipped.csv", index=False)
print(sub.describe())
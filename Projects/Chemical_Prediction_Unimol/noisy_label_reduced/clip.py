import pandas as pd
import os
curr = os.path.dirname(__file__)
reading = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\noisy_label_reduced\test_rdkit_features_attached.csv")
print(reading.columns)

result = [1 if col == 'Inhibition' else 0 for col in reading.columns][2:]
import numpy as np

np.save("monotone_constraints.npy", result)
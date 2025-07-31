import pandas as pd

rdkit = pd.read_csv(r"C:\Users\Isaac_Han\Desktop\CS\IBM_RedHat\_data\dacon\BoostUpAI2025\ManualScaffold_seed42\rdkit_prob.csv")

print(rdkit["Inhibitor_probability"][:50])
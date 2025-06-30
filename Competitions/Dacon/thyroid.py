import numpy as np
import pandas as pd
from sklearn.model_selection import StratifiedKFold
from sklearn.preprocessing import OneHotEncoder, StandardScaler
from sklearn.utils.class_weight import compute_class_weight
from sklearn.metrics import f1_score
from tensorflow.keras.models import Model
from tensorflow.keras.layers import Input, Dense, Dropout, BatchNormalization, LeakyReLU
from tensorflow.keras.optimizers import Adam
from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau
import matplotlib.pyplot as plt

# Load data
path = "./_data/dacon/thyroidCancer/"
train = pd.read_csv(path+"train.csv", index_col=0)
test = pd.read_csv(path+"test.csv", index_col=0)
submission = pd.read_csv(path+"sample_submission.csv")
y = train.pop("Cancer")

# Encode categoricals
categorical_cols = train.columns[[1, 2, 3, 4, 5, 6, 7, 8, 9]]

# import inspect
# print(inspect.signature(OneHotEncoder))
# exit()

ohe = OneHotEncoder(sparse=False, handle_unknown='ignore')

train_ohe = pd.DataFrame(ohe.fit_transform(train[categorical_cols]), index=train.index)
test_ohe = pd.DataFrame(ohe.transform(test[categorical_cols]), index=test.index)

train = train.drop(categorical_cols, axis=1).join(train_ohe)
test = test.drop(categorical_cols, axis=1).join(test_ohe)

# Normalize numerics
numeric_cols = train.columns.difference(train_ohe.columns)
scaler = StandardScaler()
train[numeric_cols] = scaler.fit_transform(train[numeric_cols])
test[numeric_cols] = scaler.transform(test[numeric_cols])

# Compute class weights
class_weights = compute_class_weight(class_weight="balanced", classes=np.unique(y), y=y)
class_weights = dict(enumerate(class_weights))

# Define model
def build_model(input_dim):
    inputs = Input(shape=(input_dim,))
    x = Dense(256)(inputs)
    x = LeakyReLU()(x)
    x = BatchNormalization()(x)
    x = Dropout(0.4)(x)

    x = Dense(128)(x)
    x = LeakyReLU()(x)
    x = BatchNormalization()(x)

    x = Dense(64)(x)
    x = LeakyReLU()(x)
    x = BatchNormalization()(x)

    x = Dropout(0.3)(x)
    x = Dense(32, activation='relu')(x)

    outputs = Dense(1, activation='sigmoid')(x)
    model = Model(inputs, outputs)

    model.compile(optimizer=Adam(0.001), loss='binary_crossentropy', metrics=['accuracy'])
    return model

# Stratified K-Fold (using only first split)
skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
for train_idx, val_idx in skf.split(train, y):
    x_train, x_val = train.iloc[train_idx], train.iloc[val_idx]
    y_train, y_val = y.iloc[train_idx], y.iloc[val_idx]
    break  # use only first fold

# Callbacks
es = EarlyStopping(monitor='val_loss', patience=40, restore_best_weights=True)
lr = ReduceLROnPlateau(monitor='val_loss', factor=0.5, patience=10, verbose=1)

# Train model
model = build_model(x_train.shape[1])
history = model.fit(
    x_train, y_train,
    validation_data=(x_val, y_val),
    epochs=1000,
    batch_size=20,
    callbacks=[es, lr],
    class_weight=class_weights,
    verbose=1
)

# Threshold optimization
val_pred_proba = model.predict(x_val)
thresholds = np.arange(0.1, 0.9, 0.01)
best_thresh, best_f1 = 0.5, 0

for t in thresholds:
    pred = (val_pred_proba > t).astype(int)
    f1 = f1_score(y_val, pred)
    if f1 > best_f1:
        best_f1, best_thresh = f1, t

print(f"Best threshold: {best_thresh:.2f} — F1: {best_f1:.4f}")

# Predict test set
test_pred = (model.predict(test) > best_thresh).astype(int)
submission["Cancer"] = test_pred
submission.to_csv(path + f"Model_Threshold_{best_f1:.4f}.csv", index=False)


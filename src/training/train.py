import os
import joblib
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.metrics import roc_auc_score, average_precision_score
from xgboost import XGBClassifier

SEED = 42
DATA_PATH = "data/creditcard.csv"
MODEL_DIR = "models"
MODEL_PATH = os.path.join(MODEL_DIR, "xgb_fraud.joblib")

def main():
    df = pd.read_csv(DATA_PATH)

    X = df.drop(columns = ["Class"])
    y = df["Class"]

    X_tr, X_te, y_tr, y_te = train_test_split(
        X, y, test_size=0.20, random_state=SEED, stratify = y
    )

    neg, pos = np.bincount(y_tr)
    spw = neg / pos

    model = XGBClassifier(
        n_estimators = 400,
        max_depth = 6,
        learning_rate = 0.05,
        subsample = 0.9,
        colsample_bytree = 0.9,
        reg_lambda = 2.0,
        tree_method = "hist",
        random_state = SEED,
        scale_pos_weight = spw,
        n_jobs = 1,
        eval_metrics = "auc",
    )

    model.fit(X_tr, y_tr)

    proba = model.predict_proba(X_te)[:, 1]
    roc_auc = roc_auc_score(y_te, proba)
    avg_prec = average_precision_score(y_te, proba)

    os.makedirs(MODEL_DIR, exist_ok = True)
    joblib.dump({"model": model, "features": X.columns.tolist()}, MODEL_PATH)

    print({
        "roc_auc": float(roc_auc),
        "avg_precision": float(avg_prec),
        "model_path": MODEL_PATH,
        "train_samples": int(len(y_tr)),
        "test_samples": int(len(y_te)),
        "scale_pos_weight": float(spw),
    })

if __name__ == '__main__':
    main()
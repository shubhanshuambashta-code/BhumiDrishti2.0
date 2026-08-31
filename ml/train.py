#!/usr/bin/env python3
"""
Train a starter XGBoost model on the demo dataset and save as a joblib artifact.
Saves a dict: {'model': model, 'pipeline': pipeline}
"""
import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.compose import ColumnTransformer
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import xgboost as xgb
import joblib

CATEGORICALS = ['project_type', 'department', 'state', 'district', 'acquisition_method', 'approval_status', 'current_stage']
NUMERICALS = ['land_area_hectares','affected_families','pending_approvals','compensation_pending_percentage','possession_percentage','elapsed_days','legal_disputes','r_and_r_pending_families']


def load_data(path):
    df = pd.read_csv(path)
    # basic cleaning
    df[CATEGORICALS] = df[CATEGORICALS].fillna('Unknown')
    df[NUMERICALS] = df[NUMERICALS].fillna(0)
    return df


def build_pipeline():
    num_pipe = Pipeline(steps=[('imputer', SimpleImputer(strategy='median'))])
    cat_pipe = Pipeline(steps=[('imputer', SimpleImputer(strategy='constant', fill_value='Unknown')),
                               ('ohe', OneHotEncoder(handle_unknown='ignore'))])
    preproc = ColumnTransformer(transformers=[
        ('num', num_pipe, NUMERICALS),
        ('cat', cat_pipe, CATEGORICALS)
    ], remainder='drop')
    return preproc


def main(data, out):
    df = load_data(data)
    X = df[NUMERICALS + CATEGORICALS]
    y = df['delayed']

    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, random_state=42, stratify=y)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, random_state=42, stratify=y_temp)

    preproc = build_pipeline()
    X_train_t = preproc.fit_transform(X_train)
    X_val_t = preproc.transform(X_val)
    X_test_t = preproc.transform(X_test)

    model = xgb.XGBClassifier(n_estimators=200, max_depth=6, use_label_encoder=False, eval_metric='logloss')
    model.fit(X_train_t, y_train, eval_set=[(X_val_t, y_val)], early_stopping_rounds=20, verbose=False)

    # evaluate
    y_pred = model.predict(X_test_t)
    y_proba = model.predict_proba(X_test_t)[:,1]
    metrics = {
        'accuracy': float(accuracy_score(y_test, y_pred)),
        'precision': float(precision_score(y_test, y_pred)),
        'recall': float(recall_score(y_test, y_pred)),
        'f1': float(f1_score(y_test, y_pred)),
        'roc_auc': float(roc_auc_score(y_test, y_proba))
    }
    print('Evaluation metrics:', metrics)

    # save model+pipeline
    artifact = {'model': model, 'pipeline': preproc, 'metrics': metrics}
    joblib.dump(artifact, out)
    print('Saved model artifact to', out)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data', type=str, default='data/projects_demo.csv')
    parser.add_argument('--out', type=str, default='ml/models/model_v1.joblib')
    args = parser.parse_args()
    main(args.data, args.out)

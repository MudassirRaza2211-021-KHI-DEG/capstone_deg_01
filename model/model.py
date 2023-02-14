import logging
import os
import pickle

import numpy as np
import sklearn
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import f1_score, precision_score, recall_score
from sklearn.model_selection import train_test_split


def train_model(
    x: np.ndarray,
    y: np.ndarray,
    save_model: bool = False,
    model_dir: str = "./",
):
    x_train, x_test, y_train, y_test = train_test_split(
        x, y, test_size=0.1, random_state=42
    )
    model = RandomForestClassifier(random_state=42)
    logging.info("Fitting the model")
    model.fit(x_train, y_train)
    logging.info("Evaluating the model")
    score = evaluate_model(model, x_test, y_test)
    logging.info(score)
    if save_model:
        model_path = os.path.join(model_dir, "model.pkl")
        with open(model_path, "wb") as f:
            pickle.dump(model, f)
            logging.info("Saving the model")
    return model


def evaluate_model(
    model: sklearn.base.ClassifierMixin, x_test: np.ndarray, y_test: np.ndarray
):
    y_pred = model.predict(x_test)
    score = {
        "f1": f1_score(y_test, y_pred),
        "precision": precision_score(y_test, y_pred),
        "recall": recall_score(y_test, y_pred),
    }
    return score

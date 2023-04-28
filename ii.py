import pandas as pd
import numpy as np
from sklearn.neural_network import BernoulliRBM
from sklearn.pipeline import Pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder

def predict_diagnosis(age, gender, allergy, complication, difficulty, diagnosis):
    df = pd.read_csv("dataset.csv", delimiter=";")
    le = LabelEncoder()
    df = df.apply(le.fit_transform)

    y = df['diagnosis']
    x_train, x_test, y_train, y_test = train_test_split(df.drop('diagnosis', axis=1), y, test_size=0.2)

    # Check if all labels are present in LabelEncoder object
    le.fit(y)
    if 33 not in le.classes_:
        return "Ошибка исполнения. Проверьте dataset.csv на соответствие."

    # Define the pipeline with BernoulliRBM and LogisticRegression
    rbm = BernoulliRBM(n_components=200, learning_rate=0.01, n_iter=100)
    logistic = LogisticRegression(C=6000, penalty='l2')
    classifier = Pipeline([("rbm", rbm), ("logistic", logistic)])
    classifier.fit(x_train, y_train)

    # Encode input values
    values_encoded = np.array([int(age), gender, allergy, complication, difficulty], dtype=object)
    values_encoded[0] = le.transform([values_encoded[0]])[0] # Fix for age parameter
    values_encoded = le.transform(values_encoded).flatten()

    # Check if all values for encoding are present in le
    if len(np.unique(values_encoded)) != len(le.classes_):
        return "Ошибка формата данных"

    d_samples = np.random.binomial(1, 0.5, size=(10, 5))
    d_samples[:, :-1] = values_encoded
    d_weights = rbm.transform(d_samples)
    x = np.hstack([d_weights, d_samples[:, :-1]])
    y_pred_proba = logistic.predict_proba(x)
    diagnosis_index = le.transform([diagnosis])[0]
    return f"Ответ: {y_pred_proba[0][diagnosis_index]}"

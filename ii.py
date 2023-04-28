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
    df['gender'] = le.fit_transform(df['gender'])
    df['allergy'] = le.fit_transform(df['allergy'])
    df['complication'] = le.fit_transform(df['complication'])
    df['difficulty'] = le.fit_transform(df['difficulty'])
    y = df['diagnosis']
    le.fit(y)
    y = le.transform(y)
    x_train, x_test, y_train, y_test = train_test_split(df.drop('diagnosis', axis=1), y, test_size=0.2)

    # Define the pipeline with BernoulliRBM and LogisticRegression
    rbm = BernoulliRBM(n_components=200, learning_rate=0.01, n_iter=100)
    logistic = LogisticRegression(C=6000, penalty='l2')
    classifier = Pipeline([("rbm", rbm), ("logistic", logistic)])
    classifier.fit(x_train, y_train)
    values = [[age, gender, allergy, complication, difficulty]]
    arr = values[0:4]
    arr[0].append(diagnosis)
    values_encoded = le.transform(arr)
    d_samples = np.random.binomial(1, 0.5, size=(10, 5))
    d_samples[:, :-1] = values_encoded
    d_weights = rbm.transform(d_samples)
    x = np.hstack([d_weights, d_samples[:, :-1]])
    y_pred_proba = logistic.predict_proba(x)
    diagnosis_index = le.transform([diagnosis])[0]
    return y_pred_proba[0][diagnosis_index]


diagnosis_proba = predict_diagnosis(age=35, gender='Мужской', allergy='Пыльца', complication='Отсутствует',
                                    difficulty='Средний', diagnosis='Грипп')
print(diagnosis_proba)

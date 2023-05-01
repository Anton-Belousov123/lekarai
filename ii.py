import pandas as pd
from sklearn.feature_extraction import DictVectorizer
from sklearn.tree import DecisionTreeClassifier


def predict_diagnosis(age, gender, allergy, complications, difficulty, diagnosis):
    new_object = {'age': int(age), 'gender': gender, 'allergy': allergy,
                  'complication': complications,
                  'difficulty': difficulty}

    df = pd.read_csv('dataset.csv', sep=';')

    vec = DictVectorizer()
    X = vec.fit_transform(df.drop('diagnosis', axis=1).to_dict('records'))

    y = df['diagnosis']

    model = DecisionTreeClassifier()
    model.fit(X, y)

    new_object_vec = vec.transform([new_object])
    predicted_diagnosis = model.predict(new_object_vec)
    return f"Ваш ответ: {diagnosis}\nДиагноз: {predicted_diagnosis[0]}"
    
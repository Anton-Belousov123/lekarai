import tkinter as tk

import numpy as np
import pandas as pd

from ii import predict_diagnosis
from tkinter import messagebox


class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master
        self.pack()
        self.create_widgets()

    def update_entry_text(self, *args):
        difficulty_text = ""
        if self.difficulty_var.get() == "1":
            difficulty_text = "Легкий"
        elif self.difficulty_var.get() == "2":
            difficulty_text = "Средний"
        elif self.difficulty_var.get() == "3":
            difficulty_text = "Тяжелый"

        df = pd.read_csv("dataset.csv", delimiter=";")
        random_row = df.loc[df['difficulty'] == difficulty_text].sample(n=1, random_state=np.random.randint(100))
        self.age = random_row['age'].to_string(index=False)
        self.gender = random_row['gender'].to_string(index=False)
        self.allergy = random_row['allergy'].to_string(index=False)
        self.complications = random_row['complication'].to_string(index=False)
        self.age_entry.delete(0, tk.END)
        self.age_entry.insert(0, self.age)
        self.gender_entry.delete(0, tk.END)
        self.gender_entry.insert(0, self.gender)
        self.allergy_entry.delete(0, tk.END)
        self.allergy_entry.insert(0, self.allergy)
        self.complications_entry.delete(0, tk.END)
        self.complications_entry.insert(0, self.complications)
    def create_widgets(self):
        df = pd.read_csv("dataset.csv", delimiter=";")
        random_row = df.loc[df['difficulty'] == 'Легкий'].sample(n=1, random_state=np.random.randint(100))
        self.age = random_row['age'].to_string(index=False)
        self.gender = random_row['gender'].to_string(index=False)
        self.allergy = random_row['allergy'].to_string(index=False)
        self.complications = random_row['complication'].to_string(index=False)

        # создаем текстовые метки и поля ввода для данных о пациенте
        tk.Label(self, text="Возраст пациента:").grid(row=0, column=0, sticky=tk.W)
        self.age_entry = tk.Entry(self)
        self.age_entry.insert(0, self.age)
        self.age_entry.grid(row=0, column=1)

        tk.Label(self, text="Пол пациента:").grid(row=1, column=0, sticky=tk.W)
        self.gender_entry = tk.Entry(self)
        self.gender_entry.insert(0, self.gender)
        self.gender_entry.grid(row=1, column=1)

        tk.Label(self, text="Аллергия на препараты:").grid(row=2, column=0, sticky=tk.W)
        self.allergy_entry = tk.Entry(self)
        self.allergy_entry.insert(0, self.allergy)
        self.allergy_entry.grid(row=2, column=1)

        tk.Label(self, text="Осложнения:").grid(row=3, column=0, sticky=tk.W)
        self.complications_entry = tk.Entry(self)
        self.complications_entry.insert(0, self.complications)
        self.complications_entry.grid(row=3, column=1)

        # создаем кнопки для выбора уровня сложности и запуска программы
        tk.Label(self, text="Выберите уровень сложности:").grid(row=4, column=0, sticky=tk.W)
        self.difficulty_var = tk.StringVar(value="1")
        self.difficulty_var.trace("w", self.update_entry_text)
        tk.Radiobutton(self, text="Легкий", variable=self.difficulty_var, value="1").grid(row=5, column=0, sticky=tk.W)
        tk.Radiobutton(self, text="Средний", variable=self.difficulty_var, value="2").grid(row=6, column=0, sticky=tk.W)
        tk.Radiobutton(self, text="Тяжелый", variable=self.difficulty_var, value="3").grid(row=7, column=0, sticky=tk.W)
        tk.Label(self, text="Диагноз:").grid(row=8, column=0, columnspan=2)
        self.user_diagnos = tk.Entry(self)
        self.user_diagnos.grid(row=9, column=0, columnspan=2)

        self.submit_button = tk.Button(self, text="Проверить диагноз", command=self.submit_data)
        self.submit_button.grid(row=10, column=0, columnspan=2)

        self.diagnosis_label = tk.Label(self, text="")
        self.diagnosis_label.grid(row=9, column=0, columnspan=2)

    def submit_data(self):
        # получаем данные о пациенте из полей ввода
        age = self.age_entry.get()
        gender = self.gender_entry.get()
        allergy = self.allergy_entry.get()
        complications = self.complications_entry.get()
        diagnosis = self.user_diagnos.get()

        # получаем выбранный уровень сложности
        difficulty = int(self.difficulty_var.get())

        # передаем данные в функцию для определения диагноза
        diagnosis = predict_diagnosis(age, gender, allergy, complications, difficulty, diagnosis)
        messagebox.showinfo(title=diagnosis, message=diagnosis)
        # выводим диагноз на метку
        #self.diagnosis_label.config(text=diagnosis)

# создаем окно и запускаем приложение
root = tk.Tk()
app = Application(master=root)
app.mainloop()

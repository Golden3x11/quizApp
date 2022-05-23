from tkinter import *
from tkinter.messagebox import *
from customtkinter import *

import app
import quiz


class QuizPage(CTkFrame):
    def __init__(self, master):
        try:
            self.quiz = quiz.Quiz()
            self.master = master
            super().__init__(master, fg_color='#CBF3F0')

            self.rowconfigure(0, weight=1)
            self.rowconfigure(1, weight=1)
            self.rowconfigure(2, weight=1)
            self.rowconfigure((3, 4), weight=6)
            self.columnconfigure((0, 1), weight=1)
            self.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

            self.question_text_label = CTkLabel(self, text='', wraplength=800,
                                                text_font=(app.App.FONT, -45, 'bold'))
            self.question_text_label.grid(row=1, column=0, columnspan=2, pady=20, padx=20, sticky='n')

            self.frame_b = CTkFrame(self, fg_color='#FFBF69')
            self.frame_b.rowconfigure((0, 1), weight=5)
            self.frame_b.columnconfigure(0, weight=2)
            self.frame_b.columnconfigure(1, weight=2)
            self.frame_b.grid(row=3, rowspan=2, column=0, columnspan=2, sticky="nsew", padx=15, pady=15)

            self.choices_button = []
            for i in range(2):
                for j in range(2):
                    b = CTkButton(self.frame_b, text='', fg_color='#FF9F1C', hover_color='#FFB347',
                                  command=self.make_lambda(
                                      len(self.choices_button)), text_font=(app.App.FONT, -20))
                    b.grid(row=i, column=j, pady=10, padx=10, sticky='nsew')
                    self.choices_button.append(b)

            for i, choice in enumerate(self.choices_button, start=1):
                self.master.bind(f"<KeyPress-{i}>", self.make_lambda_event(i - 1))

            self.display_question(self.quiz.get_new_question())
            self.is_correct_label = CTkLabel(self, text='', text_font=(app.App.FONT, -30, 'bold'))
            self.is_correct_label.grid(column=0, columnspan=2, row=2)

            self.user_frame = CTkFrame(self, height=100, fg_color='#9CE8E3')
            self.user_frame.grid(row=0, column=0, columnspan=2,
                                 sticky=tkinter.NSEW)
            self.user_frame.columnconfigure((0, 1), weight=20)
            self.user_info_label = CTkLabel(self.user_frame, text='', text_font=('Corbel', -15, 'bold'))
            self.user_info_label.grid(row=0, column=0)
            self.score_label = CTkLabel(self.user_frame, text='', text_font=('Corbel', -15, 'bold'))
            self.score_label.grid(row=0, column=1)
            self.display_user_info()
            self.tkraise()
        except ConnectionError:
            showerror('Error', 'Question not loaded probably no internet connection')

    def make_lambda(self, x):
        return lambda: (self.check_answer(x))

    def make_lambda_event(self, x):
        return lambda event: (self.check_answer(x))

    def display_user_info(self):
        self.user_info_label.config(
            text=f'USER: {app.App.get_USER().login}\nBEST SCORE: {app.App.get_USER().best_score}')
        self.score_label.config(text=f'YOUR SCORE: {self.quiz.score}')

    def display_question(self, question):
        print('Correct answer: ', question.correct_answer)

        self.question_text_label.config(text=question.text_of_question)

        for i, choice in enumerate(question.choices, start=0):
            self.choices_button[i].config(text=f'{choice} ({i + 1})')

    def check_answer(self, answer):
        self.is_correct_label = CTkLabel(self, text='', text_font=(app.App.FONT, -30, 'bold'))
        self.is_correct_label.grid(column=0, columnspan=2, row=2)

        try:
            if self.quiz.check_answer(answer):
                self.display_user_info()
                self.is_correct_label.config(text='Correct answer', fg_color='#4CC241')
                self.after(1000, self.is_correct_label.destroy)
                try:
                    self.display_question(self.quiz.get_new_question())
                except ConnectionError:
                    showerror('Error', 'Question not loaded probably no internet connection')
            else:
                self.is_correct_label.config(
                    text=f'Incorrect answer!\n Right one: {self.quiz.current_question.correct_answer}', fg_color='#F75B38')
                showinfo("Result", f"Your result: {self.quiz.score}\nBest result: {app.App.get_USER().best_score}")
                self.master.unbind('<Return>')
                for i in range(1, 5):
                    self.master.unbind(f"<KeyPress-{i}>")
                self.master.frame.tkraise()
        except ConnectionError:
            showerror('Error', 'No data base Connection')
            self.master.frame.tkraise()

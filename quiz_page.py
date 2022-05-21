from tkinter import *
from tkinter.messagebox import *
from customtkinter import *

import app
import main_page
import quiz


class QuizPage(CTkFrame):
    def __init__(self, master):
        try:
            self.quiz = quiz.Quiz()
            self.master = master
        except ConnectionError:

            showerror('Error', 'Question not loaded probably no internet connection')
        super().__init__(master)
        self.rowconfigure(0, weight=5)
        self.rowconfigure((1, 2, 3, 4, 5, 6), weight=1)
        self.columnconfigure((0, 2), weight=5)
        self.columnconfigure(1, weight=15)
        self.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        self.question_text_label = CTkLabel(self, text='', wraplength=800,
                                            text_font=(app.FONT, -50, 'bold'))
        self.question_text_label.grid(row=0, column=0, columnspan=3, pady=20, padx=20, sticky='n')

        self.user_answer = StringVar(self, '-1')
        self.choices_radiobutton = []
        for i in range(4):
            rb = CTkRadioButton(self, text='', variable=self.user_answer, value=i)
            rb.grid(row=i + 1, column=1, pady=20, padx=20, sticky='n')
            self.choices_radiobutton.append(rb)

        self.check_answer_button = CTkButton(self, text='Check', command=self.check_answer,
                                             text_font=(app.FONT, -30, 'bold'))
        self.check_answer_button.grid(row=6, column=2, pady=20, padx=20, sticky='n')

        self.master.bind('<Return>', lambda event: self.check_answer())
        for i, choice in enumerate(self.choices_radiobutton, start=1):
            def make_lambda(x):
                return lambda event: x.select()

            self.master.bind(f"<KeyPress-{i}>", make_lambda(choice))

        self.display_question(self.quiz.get_question())

    def display_question(self, question):
        print('Correct answer: ', question.correct_answer)
        # question text
        self.question_text_label.config(text=question.text_of_question)

        for i, choice in enumerate(question.choices, start=0):
            self.choices_radiobutton[i].config(text=f'{choice} ({i + 1})')

    def check_answer(self):
        self.is_correct_label = CTkLabel(self, text='', text_font=(app.FONT, -30, 'bold'))
        self.is_correct_label.grid(column=1, row=6)
        if self.user_answer.get() != '-1':
            if self.quiz.check_answer(self.user_answer.get()):
                self.is_correct_label.config(text='Correct answer', fg_color='green')
                self.after(1000, self.is_correct_label.destroy)
                self.user_answer.set('-1')
                self.display_question(self.quiz.get_question())
            else:
                self.is_correct_label.config(
                    text=f'Incorrect answer!\n Right one: {self.quiz.current_question.correct_answer}', fg_color='red')
                showinfo("Result", f"Your result: {self.quiz.score}\nBest result: {app.USER.best_score}")
                self.master.unbind('<Return>')
                for i in range(1, 5):
                    self.master.unbind(f"<KeyPress-{i}>")
                main_page.MainPage(self.master)

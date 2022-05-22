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
        except ConnectionError:
            master.frame.tkrise()
            showerror('Error', 'Question not loaded probably no internet connection')
        super().__init__(master, fg_color='#FCF7FF')

        self.rowconfigure(0, weight=1)
        self.rowconfigure(1, weight=5)
        self.rowconfigure((1, 2, 3, 4, 5, 6), weight=2)
        self.columnconfigure((0, 2), weight=5)
        self.columnconfigure(1, weight=15)
        self.grid(row=0, column=0, sticky="nsew", padx=15, pady=15)

        self.question_text_label = CTkLabel(self, text='', wraplength=800,
                                            text_font=(app.App.FONT, -45, 'bold'))
        self.question_text_label.grid(row=1, column=0, columnspan=3, pady=20, padx=20, sticky='n')

        self.user_answer = StringVar(self, '-1')
        self.choices_radiobutton = []
        for i in range(4):
            rb = CTkRadioButton(self, text='', variable=self.user_answer, value=i)
            rb.grid(row=i + 2, column=1, pady=20, padx=20, sticky='n')
            self.choices_radiobutton.append(rb)

        self.check_answer_button = CTkButton(self, text='Check', command=self.check_answer,
                                             text_font=(app.App.FONT, -30, 'bold'))
        self.check_answer_button.grid(row=7, column=2, pady=20, padx=20, sticky='n')

        self.master.bind('<Return>', lambda event: self.check_answer())
        for i, choice in enumerate(self.choices_radiobutton, start=1):
            def make_lambda(x):
                return lambda event: x.select()

            self.master.bind(f"<KeyPress-{i}>", make_lambda(choice))

        self.display_question(self.quiz.get_new_question())
        self.is_correct_label = None

        self.user_frame = CTkFrame(self, height=100, fg_color='#B0A8B9')
        self.user_frame.grid(row=0, column=0, columnspan=3,
                             sticky=tkinter.NSEW)
        self.user_frame.columnconfigure((0, 1), weight=20)
        self.user_info_label = CTkLabel(self.user_frame, text='', text_font=('Corbel', -15, 'bold'))
        self.user_info_label.grid(row=0, column=0)
        self.score_label = CTkLabel(self.user_frame, text='', text_font=('Corbel', -15, 'bold'))
        self.score_label.grid(row=0, column=1)
        self.display_user_info()

    def display_user_info(self):
        self.user_info_label.config(text=f'USER: {app.App.get_USER().login}\nBEST SCORE: {app.App.get_USER().best_score}')
        self.score_label.config(text=f'YOUR SCORE: {self.quiz.score}')

    def display_question(self, question):
        print('Correct answer: ', question.correct_answer)

        self.question_text_label.config(text=question.text_of_question)

        for i, choice in enumerate(question.choices, start=0):
            self.choices_radiobutton[i].config(text=f'{choice} ({i + 1})')

    def check_answer(self):
        self.is_correct_label = CTkLabel(self, text='', text_font=(app.App.FONT, -30, 'bold'))
        self.is_correct_label.grid(column=1, row=7)
        if self.user_answer.get() != '-1':
            if self.quiz.check_answer(self.user_answer.get()):
                self.display_user_info()
                self.is_correct_label.config(text='Correct answer', fg_color='green')
                self.after(1000, self.is_correct_label.destroy)
                self.user_answer.set('-1')
                self.display_question(self.quiz.get_new_question())
            else:
                self.is_correct_label.config(
                    text=f'Incorrect answer!\n Right one: {self.quiz.current_question.correct_answer}', fg_color='red')
                showinfo("Result", f"Your result: {self.quiz.score}\nBest result: {app.App.get_USER().best_score}")
                self.master.unbind('<Return>')
                for i in range(1, 5):
                    self.master.unbind(f"<KeyPress-{i}>")
                self.master.frame.tkraise()

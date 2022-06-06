from tkinter import *
from tkinter.messagebox import *
from customtkinter import *
from requests.exceptions import HTTPError

import app
import quiz


class QuizPage(CTkFrame):
    def __init__(self, master):
        try:
            self.quiz = quiz.Quiz(app.App.get_USER())  # create the quiz brain instance
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

            self.frame_buttons = CTkFrame(self, fg_color='#FFBF69')  # frame with answer buttons
            self.frame_buttons.rowconfigure((0, 1), weight=5)
            self.frame_buttons.columnconfigure(0, weight=2)
            self.frame_buttons.columnconfigure(1, weight=2)
            self.frame_buttons.grid(row=3, rowspan=2, column=0, columnspan=2, sticky="nsew", padx=15, pady=15)

            self.choices_button = []
            for i in range(2):  # create answer buttons always 2 rows
                for j in range(2):
                    b = CTkButton(self.frame_buttons, text='', fg_color='#FF9F1C', hover_color='#FFB347',
                                  command=self.make_lambda(
                                      len(self.choices_button)), text_font=(app.App.FONT, -18))
                    b.grid(row=i, column=j, pady=10, padx=10, sticky='nsew')
                    self.choices_button.append(b)

            for i, choice in enumerate(self.choices_button, start=1):  # binds to chose answer
                self.master.bind(f"<KeyPress-{i}>", self.make_lambda_event(i - 1))

            self.display_question(self.quiz.get_new_question())  # change displayed question

            self.is_correct_label = CTkLabel(self, text='', text_font=(app.App.FONT, -30, 'bold'))
            self.is_correct_label.grid(column=0, columnspan=2, row=2)

            self.user_frame = CTkFrame(self, height=100, fg_color='#9CE8E3')  # frame with user info
            self.user_frame.grid(row=0, column=0, columnspan=2, sticky=tkinter.NSEW)
            self.user_frame.columnconfigure((0, 1), weight=20)

            self.user_info_label = CTkLabel(self.user_frame, text='', text_font=('Corbel', -15, 'bold'))
            self.user_info_label.grid(row=0, column=0)
            self.score_label = CTkLabel(self.user_frame, text='', text_font=('Corbel', -15, 'bold'))
            self.score_label.grid(row=0, column=1)

            self.display_user_info()

            self.tkraise()  # raise this frame above the main welcoming frame
        except HTTPError as e:
            showerror('Error', e)
        except ConnectionError as e:
            showerror('Error', e)

    def clear_is_correct_label(self):
        self.is_correct_label.config(text='', fg_color=None)

    def make_lambda(self, x):  # to use argument in lambda statement
        return lambda: (self.check_answer(x))

    def make_lambda_event(self, x):
        return lambda event: (self.check_answer(x))

    def display_user_info(self):  # we update user info bar
        self.user_info_label.config(
            text=f'USER: {app.App.get_USER().login}\nBEST SCORE: {app.App.get_USER().best_score}')
        self.score_label.config(text=f'YOUR SCORE: {self.quiz.score}')

    def display_question(self, question):
        self.question_text_label.config(text=question.text_of_question)  # update text of question

        for i, choice in enumerate(question.choices, start=0):
            self.choices_button[i].config(text=f'{choice} ({i + 1})')  # update answer buttons

    def check_answer(self, answer):

        try:
            if self.quiz.check_answer(answer):  # if not correct database actions
                self.display_user_info()
                self.is_correct_label.config(text='Correct answer', fg_color='#4CC241')
                self.after(1000, self.clear_is_correct_label)
                try:
                    self.display_question(self.quiz.get_new_question())
                except HTTPError as e:
                    showerror('Error', e)
                except ConnectionError as e:
                    showerror('Error', e)
            else:
                self.is_correct_label.config(
                    text=f'Incorrect answer!\n Right one: {self.quiz.current_question.correct_answer}',
                    fg_color='#F75B38')
                showinfo("Result", f"Your result: {self.quiz.score}\nBest result: {app.App.get_USER().best_score}")

                for i in enumerate(self.choices_button, start=1):
                    self.master.unbind(f"<KeyPress-{i}>")
                self.master.frame.tkraise()  # raise main frame

        except ConnectionError:
            showerror('Error', 'No data base Connection')
            self.master.frame.tkraise()  # raise main frame

import time
from tkinter import *
from tkinter.messagebox import *

import mainpage
import quiz
import app


class QuizGUI:
    def __init__(self):
        try:
            self.quiz = quiz.Quiz()
        except ConnectionError:
            mainpage.MainGUI()
            showerror('Error', 'Question not loaded probably no internet connection')
        else:
            self.root = Tk()
            self.root.geometry("{}x{}+{}+{}".format(app.WIDTH, app.HEIGHT, app.POSITION_W, app.POSITION_H))
            self.root.resizable(False, False)
            self.root.title('Quiz App')

            self.question_text = None
            self.is_correct_label = None

            self.user_info_label = None
            self.score_label = None
            self.frame = Frame(self.root, width=app.WIDTH, height=app.HEIGHT)
            self.frame.place(x=0, y=0)
            self.frame_user = Frame(self.frame, width=890, height=50)
            self.frame_user.place(x=5, y=0)

            self.create_user_info_bar()
            self.display_user_info()

            self.frame_question = Frame(self.frame, width=890, height=550, bg='white')
            self.frame_question.place(x=5, y=50)

            self.user_answer = StringVar()

            self.question_text_label, self.choices_buttons = self.create_quiz_template()

            self.check_answer_button = Button(self.frame_question, text='Check', command=self.check_answer, bg="red", fg="white",
                                              font=(app.FONT, 18, " bold"))
            self.check_answer_button.place(x=700, y=450)

            self.root.bind('<Return>', lambda event: self.check_answer())
            for i, choice in enumerate(self.choices_buttons, start=1):
                def make_lambda(x):
                    return lambda event: x.select()

                self.root.bind(f"<KeyPress-{i}>", make_lambda(choice))

            self.display_question(self.quiz.get_question())

            self.root.mainloop()

    def create_user_info_bar(self):
        self.user_info_label = Label(self.frame_user, text='', font=(app.FONT, 15))
        self.user_info_label.place(x=0, y=20, anchor='w')
        self.score_label = Label(self.frame_user, text='', font=(app.FONT, 18))
        self.score_label.place(x=app.WIDTH - 10, y=20, anchor='e')

    def display_user_info(self):
        self.user_info_label['text'] = f'{app.USER.login}\nBest score: {app.USER.best_score}'
        self.score_label['text'] = f'Your score: {self.quiz.score}'

    def create_quiz_template(self):
        self.question_text = Label(self.frame_question, text="", wraplength=750, font=(app.FONT, 25, 'bold'),
                                   fg='black')
        self.question_text.place(x=100, y=70)

        y_position = 220
        choices = []
        for _ in range(4):
            radio_button = Radiobutton(self.frame_question, text="", variable=self.user_answer, value="",
                                       font=(app.FONT, 14))
            radio_button.place(x=200, y=y_position)
            choices.append(radio_button)
            y_position += 40

        return self.question_text, choices

    def display_question(self, question):
        print('Correct answer: ', question.correct_answer)
        # question text
        self.question_text_label['text'] = question.text_of_question

        for i, choice in enumerate(question.choices, start=0):
            self.choices_buttons[i]['text'] = f'{choice} ({i + 1})'
            self.choices_buttons[i]['value'] = choice

    def check_answer(self):
        self.is_correct_label = Label(self.frame_question, text='', fg='red', bg='white', font=(app.FONT, 15, " bold"))
        self.is_correct_label.place(x=445, y=390)

        if self.quiz.check_answer(self.user_answer.get()):
            self.display_user_info()
            self.is_correct_label['fg'] = 'green'
            self.is_correct_label['text'] = 'Correct answer'
            self.root.after(1000, self.is_correct_label.destroy)
            self.display_question(self.quiz.get_question())
        else:
            self.is_correct_label['fg'] = 'red'
            self.is_correct_label[
                'text'] = f'Incorrect answer!\n Right one: {self.quiz.current_question.correct_answer}'
            showinfo("Result", f"Your result: {self.quiz.score}\nBest result: {app.USER.best_score}")
            self.root.destroy()
            mainpage.MainGUI()

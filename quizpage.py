import time
from tkinter import *
from tkinter.messagebox import *
import quiz
import app


def create_quiz_template():
    question_text = Label(frame, text="", wraplength=750, font=(app.FONT, 25, 'bold'),
                          fg='black')
    question_text.place(x=100, y=70)

    y_position = 200
    choices = []
    for _ in range(4):
        radio_button = Radiobutton(frame, text="", variable=user_answer, value="",
                                   font=(app.FONT, 14))
        radio_button.place(x=200, y=y_position)
        choices.append(radio_button)
        y_position += 40

    return question_text, choices


def display_question(question):
    print(question.correct_answer)
    # question text
    question_text_label['text'] = question.text_of_question

    for i, choice in enumerate(question.choices, start=0):
        choices_buttons[i]['text'] = choice
        choices_buttons[i]['value'] = choice


def check_answer():
    is_correct_label = Label(frame, text='', fg='red', bg='white', font=(app.FONT, 15, " bold"))
    is_correct_label.place(x=445, y=390)

    if quiz.check_answer(user_answer.get()):
        is_correct_label['fg'] = 'green'
        is_correct_label['text'] = 'Correct answer'
        root.after(1000, is_correct_label.destroy)
        display_question(quiz.get_question())
    else:
        is_correct_label['fg'] = 'red'
        is_correct_label['text'] = f'Incorrect answer!\n Right one: {quiz.current_question.correct_answer}'
        showinfo("Result", f"Your result: {quiz.score}\nBest result: {app.USER.best_score}")
        root.destroy()


# GUI
quiz = quiz.Quiz()
root = Tk()
root.geometry("{}x{}+{}+{}".format(app.WIDTH, app.HEIGHT, app.POSITION_W, app.POSITION_H))
root.resizable(False, False)
root.title('Quiz App')

frame = Frame(root, width=890, height=550, bg='white')
frame.place(x=5, y=50)

user_answer = StringVar()

question_text_label, choices_buttons = create_quiz_template()

check_answer_button = Button(frame, text='Check', command=check_answer, bg="red", fg="white",
                             font=(app.FONT, 18, " bold"))
check_answer_button.place(x=700, y=450)

display_question(quiz.get_question())


root.mainloop()

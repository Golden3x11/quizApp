from tkinter import *
from customtkinter import *
import app


class MainGui(CTk):
    def __init__(self):
        super().__init__()
        self.title('Quiz App')
        app.POSITION_W = int(self.winfo_screenwidth() / 2 - app.WIDTH / 2)
        app.POSITION_H = int(self.winfo_screenheight() / 2 - app.HEIGHT / 2)
        self.geometry("{}x{}+{}+{}".format(app.WIDTH, app.HEIGHT, app.POSITION_W, app.POSITION_H))

        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

        self.frame = CTkFrame(self)
        self.frame.grid(row=0, column=1, sticky="nswe", padx=25, pady=25)
        self.quiz_img = CTkLabel(self.frame, text='QuizApp')
        self.img.grid(row=0, column=1)

        self.start_button = CTkButton(self.frame, height=30, text='START')
        self.start_button.grid(row=1, column=0)


if __name__ == "__main__":
    app = MainGui()
    app.mainloop()

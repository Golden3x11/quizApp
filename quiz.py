import html
import random
import requests

import app


class Question:
    def __init__(self, text_of_question, correct_answer, choices):
        self.__text_of_question = text_of_question
        self.__correct_answer = correct_answer
        self.__choices = choices  # all possible answers

    def get_text_and_choices(self):  # function that returns question and possible answers
        return self.__text_of_question, self.__choices

    @property
    def correct_answer(self):
        return self.__correct_answer

    @property
    def choices(self):
        return self.__choices

    @property
    def text_of_question(self):
        return self.__text_of_question

    def is_answer_correct(self, answer_index):  # checking if answer under this index is correct
        return self.__correct_answer == self.choices[answer_index]


class Game:  # class where some general game info are stored
    def __init__(self, user):
        self._user = user
        self._score = 0

    @property
    def score(self):
        return self._score

    def change_score(self):
        self._score += 2


class Quiz(Game):
    def __init__(self, user, difficulty=None, chunk_of_questions=10):
        super(Quiz, self).__init__(user)
        self.__current_question: Question = None
        self.__difficulty = difficulty
        self.__parameters = {  # dict of parameters for json api get
            'amount': chunk_of_questions,  # chunk of question is how many questions we get from api
            'type': 'multiple'
        }
        if difficulty is not None:
            self.__parameters['difficulty'] = difficulty
        self.__questions = []
        self.__token = None
        self.__load_questions()

    def __load_questions(self):
        try:
            if self.__token is None:
                response = requests.get(url="https://opentdb.com/api_token.php?command=request")
                if response.status_code != 200:
                    response.raise_for_status()
                token = response.json()["token"]
                self.__parameters['token'] = token

            response = requests.get(url="https://opentdb.com/api.php", params=self.__parameters)  # json api get
            if response.status_code != 200:
                response.raise_for_status()
            response_code = response.json()["response_code"]
            if response_code in ['1', '2', '3']:
                raise ConnectionError
            elif response_code == '4':
                self.__token = None
                self.__load_questions()
        except requests.exceptions.RequestException as e:
            raise ConnectionError(e)

        questions = response.json()["results"]  # getting questions from api

        for question in questions:
            choices = []  # all possible answers
            text_of_question = html.unescape(question['question'])
            correct_answer = html.unescape(question['correct_answer'])
            choices.append(correct_answer)

            other_answers = question["incorrect_answers"]
            for answer in other_answers:
                choices.append(html.unescape(answer))

            random.shuffle(choices)  # sort of answers
            self.__questions.append(Question(text_of_question, correct_answer, choices))

    @property
    def current_question(self):
        return self.__current_question

    def get_new_question(self) -> Question:
        self.__current_question = self.__questions.pop()
        print('Correct answer: ', self.current_question.correct_answer)  # this quiz is really hard to be honest

        if not self.__questions:
            self.__load_questions()
        return self.__current_question

    def change_score(self):
        self._score += 1

    def check_answer(self, id_answer):
        if self.__current_question.is_answer_correct(int(id_answer)):
            self.change_score()
            return True
        else:
            self.__questions.clear()
            if self._user.best_score < self.score:
                self._user.best_score = self.score
                app.App.get_db().update_best_result(self._user, self.score)

            app.App.get_db().add_result_to_db(self._user, self.score)
            return False

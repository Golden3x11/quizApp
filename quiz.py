import html
import random
import requests

import app
import database_connection


class Question:
    def __init__(self, text_of_question, correct_answer, choices):
        self.__text_of_question = text_of_question
        self.__correct_answer = correct_answer
        self.__choices = choices

    def get_text_and_choices(self):
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

    def isAnswerCorrect(self, answer):
        return answer == self.__correct_answer


class Quiz:
    def __init__(self, difficulty=None, chunk_of_questions=10):
        self.__user = app.App.get_USER()
        self.__current_question: Question = Question('', '', [])
        self.__score = 0
        self.__difficulty = difficulty
        self.__parameters = {
            'amount': chunk_of_questions,
            'type': 'multiple'
        }
        if difficulty is not None:
            self.__parameters['difficulty'] = difficulty
        self.__questions = []
        self.__load_questions()

    def __load_questions(self):
        try:
            response = requests.get(url="https://opentdb.com/api.php", params=self.__parameters)
        except requests.exceptions.RequestException as e:
            raise ConnectionError(e)
        questions = response.json()["results"]

        for question in questions:
            choices = []
            text_of_question = html.unescape(question['question'])
            correct_answer = html.unescape(question['correct_answer'])
            choices.append(correct_answer)

            other_answers = question["incorrect_answers"]
            for answer in other_answers:
                choices.append(html.unescape(answer))

            random.shuffle(choices)
            self.__questions.append(Question(text_of_question, correct_answer, choices))

    @property
    def score(self):
        return self.__score

    @property
    def current_question(self):
        return self.__current_question

    def get_new_question(self) -> Question:
        self.__current_question = self.__questions.pop()
        if not self.__questions:
            self.__load_questions()
        return self.__current_question

    def check_answer(self, id_answer):
        if self.__current_question.isAnswerCorrect(self.__current_question.choices[int(id_answer)]):
            self.__score += 1
            return True
        else:
            self.__questions.clear()
            if self.__user.best_score < self.score:
                self.__user.best_score = self.score
                database_connection.update_best_result(self.__user, self.score)

            database_connection.add_result_to_db(self.__user, self.score)
            return False

import html
from random import shuffle
import requests


class Question:
    def __init__(self, question: str, correct_answer: str, choices: list):
        self.text_of_question = question
        self.correct_answer = correct_answer
        self.choices = choices

    def get_text_and_choices(self):
        return self.text_of_question, self.choices

    def isAnswerCorrect(self, answer):
        return answer == self.correct_answer


class Quiz:
    def __init__(self, difficulty=None, chunk_of_questions=10):
        self.current_question: Question = Question('', '', [])
        self.score = 0
        self.difficulty = difficulty
        self.parameters = {
            'amount': chunk_of_questions,
            'type': 'multiple'
        }
        if difficulty is not None:
            self.parameters['difficulty'] = difficulty
        self.questions = []
        self.load_questions()

    def load_questions(self):
        response = requests.get(url="https://opentdb.com/api.php", params=self.parameters)
        questions = response.json()["results"]

        for question in questions:
            choices = []
            text_of_question = html.unescape(question['question'])
            correct_answer = html.unescape(question['correct_answer'])
            choices.append(correct_answer)

            incorrect_answers = question["incorrect_answers"]
            for incorrect_answer in incorrect_answers:
                choices.append(html.unescape(incorrect_answer))
                
            shuffle(choices)
            self.questions.append(Question(text_of_question, correct_answer, choices))

    def get_score(self):
        return self.score

    def get_question(self) -> Question:
        self.current_question = self.questions.pop()
        if not self.questions:
            self.load_questions()
        return self.current_question

    def check_answer(self, answer):
        if self.current_question.isAnswerCorrect(answer):
            self.score += 1
            return True
        else:
            self.questions.clear()
            return False


# quiz = Quiz()
# while True:
#     question = quiz.get_question()
#     text, choices = question.get_text_and_choices()
#
#     print(text)
#     print(*enumerate(choices))
#     print(question.correct_answer)
#     x = int(input())
#     print(quiz.collect_answer(choices[x]))


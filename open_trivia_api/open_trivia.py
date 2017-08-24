from urllib2 import Request, urlopen, URLError
import ast

class TriviaCategory(object):
	ANY = ""
	GENERAL_KNOWLEDGE = 9
	BOOKS = 10
	FILM = 11
	MUSIC = 12
	MUSICALS_AND_THEATRE = 13
	TELEVISION = 14
	VIDEO_GAMES = 15
	BOARD_GAMES = 16
	SCIENCE_AND_NATURE = 17
	COMPUTERS = 18
	MATH = 19
	MYTHOLOGY = 20
	SPORTS = 21
	GEOGRAPHY = 22
	HISTORY = 23
	POLITICS = 24
	ART = 25
	CELEBRITIES = 26
	ANIMALS = 27
	VEHICLES = 28
	COMICS = 29
	GADGETS = 30
	JAPANESE_ANIME_AND_MANGA = 31
	CARTOON_AND_ANIMATIONS = 32


class Difficulty(object):
	ANY = ""
	EASY = "easy"
	MEDIUM = "medium"
	HARD = "hard"


class TriviaType(object):
	ANY = ""
	MULTIPLE_CHOICE = "multiple"
	TRUE_OR_FALSE = "boolean"


class TriviaQuestion(object):

	def __init__(self, category, question_type, question, difficulty, correct_answer, incorrect_answers):
		self.__category = category
		self.__type = question_type
		self.__question = question
		self.__difficulty = difficulty
		self.__correct_answer = correct_answer
		self.__incorrect_answers = incorrect_answers

	def __set_category(self, category):
		self.__category = category

	def get_category(self):
		return self.__category

	def __set_type(self, t):
		self.__type = t

	def get_type(self):
		return self.__type

	def __set_question(self, question):
		self.__question = question

	def get_question(self):
		return self.__question

	def set_difficulty(self, difficulty):
		self.__difficulty = difficulty

	def get_difficulty(self):
		return self.__difficulty

	def __set_correct_answer(self, correct_answer):
		self.__correct_answer = correct_answer

	def get_correct_answer(self):
		return self.__correct_answer

	def __set_incorrect_answers(self, incorrect_answers):
		self.__incorrect_answers = incorrect_answers

	def get_incorrect_answers(self):
		return self.__incorrect_answers


class OpenTrivia(object):

	def __init__(self, amount = "", category = "", question_type = "", difficulty = ""):
		url_address = "https://opentdb.com/api.php?amount=" + str(amount) + "&category=" + str(category) + "&type=" + str(question_type) + "&difficulty=" + str(difficulty)
		reqeust = Request(url_address)
		response = urlopen(reqeust)
		trivia_data = ast.literal_eval(response.read())
		self.__trivia_questions = self.__initialize_trivia_questions(trivia_data)

	def __initialize_trivia_questions(self, trivia_data):
		questions = []
		questions_data = trivia_data["results"]
		for question_data in questions_data:
			questions.append(TriviaQuestion(question_data["category"], question_data["type"], question_data["question"],
											 question_data["difficulty"], question_data["correct_answer"], question_data["incorrect_answers"]))
		return questions

	def get_trivia_questions(self):
		return self.__trivia_questions


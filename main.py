from kivy.app import App
from kivy.core.window import Window
from kivy.utils import get_color_from_hex
from kivy.core.text import LabelBase
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.uix.screenmanager import ScreenManager, Screen, SlideTransition
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.behaviors import ButtonBehavior
from kivy.properties import ObjectProperty, NumericProperty
from kivy.network.urlrequest import UrlRequest
from kivy.clock import Clock
from uix.buttons import AnswerButton, PurpleButton
from uix.popups import ScorePopup, ZeroPopup, ErrorPopup, NetworkErrorPopup
from scores_tracking import ScoresTracking

from random import randint
import time


class StartScreen(Screen):
	pass

class QuestionScreen(Screen):

	def __init__(self, **kwargs):
		super(QuestionScreen, self).__init__(**kwargs)
		self.button_choices = []
		self.question_number = 0
		self.score = 0
		self.trivia_questions = []
		try:
			self.trivia_info()
		except:
			NetworkErrorPopup().open()

	def trivia_info(self):
		url_request = ("https://opentdb.com/api.php?amount=" + str(25) + "&category=" + str(15) + "&type=" + str("multiple"))
		req = UrlRequest(url_request, self.get_trivia_data)

	def get_trivia_data(self, reqeust, response):
		questions_data = response["results"]
		for question_data in questions_data:
			data = {}
			data["question"] = question_data["question"]
			data["correct_answer"] = question_data["correct_answer"]
			data["incorrect_answers"] = question_data["incorrect_answers"]
			self.trivia_questions.append(data)
		self.update_screen()

	def initialize_answer_choice_labels(self):
		self.button_choices = [self.button_a, self.button_b, self.button_c, self.button_d]
		letter = 65
		for button_choice in self.button_choices:
			button_choice.answer_choice_label.text = str(chr(letter)) + ". "
			button_choice.icon_label.text = ""
			button_choice.refresh_color()
			letter += 1

	def update_screen(self, timer = 0):
		self.question_label.text = str(self.question_number + 1) + ". "
		self.question_label.text += self.replace_weird_characters(self.trivia_questions[self.question_number]["question"])
		self.place_answers()

	def place_answers(self):
		answer_choices = self.trivia_questions[self.question_number]["incorrect_answers"] + [self.trivia_questions[self.question_number]["correct_answer"]]
		self.initialize_answer_choice_labels()
		i = 3
		while(len(answer_choices) > 0):
			rand_num = randint(0,i)
			self.button_choices[i].answer_choice_label.text += self.replace_weird_characters(answer_choices[rand_num])
			answer_choices.pop(rand_num)
			i -= 1

	def check_answer(self, answer_choice_button):
		user_answer = answer_choice_button.answer_choice_label.text[3:]
		correct_answer = self.replace_weird_characters(self.trivia_questions[self.question_number]["correct_answer"])
		is_correct = (user_answer == correct_answer)
		if(is_correct):
			answer_choice_button.icon_label.text = "%"
			answer_choice_button.correct_color()
			self.score += 1
			self.question_number += 1
			if(self.question_number % 2 == 0):
				self.trivia_info()
			Clock.schedule_once(self.update_screen, 0.7)
			return "correct"
		else:
			answer_choice_button.icon_label.text = "X"
			answer_choice_button.incorrect_color()
			self.find_correct_answer()
			return "incorrect"
		return is_correct

	def find_correct_answer(self, time = 0):
		correct_answer = self.replace_weird_characters(self.trivia_questions[self.question_number]["correct_answer"])
		for button_choice in self.button_choices:
			answer_choice_text = button_choice.answer_choice_label.text[3:]
			if(answer_choice_text == correct_answer):
				button_choice.icon_label.text = "%"
				button_choice.correct_color()

	def get_score(self):
		return self.score

	def replace_weird_characters(self, word):
		word = word.replace("&#039;", "'")
		word = word.replace("&quot;", "\"")
		return word


class ScoresScreen(Screen):

	def __init__(self, **kwargs):
		super(ScoresScreen, self).__init__(**kwargs)
		try:
			self.initialize_scores()
		except:
			NetworkErrorPopup().open()

	def initialize_scores(self):
		self.scores_layout.cols = 3
		self.scores_layout.add_widget(Label(text = "Rank"))
		self.scores_layout.add_widget(Label(text = "Name"))
		self.scores_layout.add_widget(Label(text = "Score"))
		scores_data = ScoresTracking().get_scores_data()
		rank = 1
		for data in scores_data:
			self.scores_layout.add_widget(Label(text = ("%d." %rank)))
			self.scores_layout.add_widget(Label(text = data["Name"]))
			self.scores_layout.add_widget(Label(text = str(data["Score"])))
			rank += 1


class FinalScoreScreen(Screen):

	def __init__(self, final_score, **kwargs):
		super(FinalScoreScreen, self).__init__(**kwargs)
		self.final_score = final_score
		self.has_entered = False

	def enter_entry(self):
		if(self.final_score == 0):
			ZeroPopup().open()
		elif(self.has_entered):
			ErrorPopup().open()
		else:
			score_popup = ScorePopup(on_dismiss = self.enter_data)
			score_popup.open()
			self.has_entered = True

	def enter_data(self, popup):
		ScoresTracking(popup.name.text, self.final_score).start()
		#ScoresTracking().update_scores(popup.name.text, self.final_score)


class TriviaScreenManager(ScreenManager):

	def __init__(self, **kwargs):
		super(TriviaScreenManager, self).__init__(**kwargs)
		self.start_screen = None
		self.question_screen = None
		self.scores_screen = None
		self.final_score_screen = None
		self.final_score = NumericProperty()
		self.new_start_screen()

	def new_start_screen(self, timer = 0):
		self.remove_existing_child_widgets()
		name = "start_screen"
		self.start_screen = StartScreen(name = name)
		self.add_widget(self.start_screen)
		self.transition = SlideTransition(direction = "left")
		self.current = "start_screen"

	def new_question_screen(self):
		self.remove_existing_child_widgets()
		name = "question_screen"
		self.question_screen = QuestionScreen(name = name)
		self.add_widget(self.question_screen)
		self.current = name

	def new_scores_screen(self):
		self.remove_existing_child_widgets()
		name = "scores_screen"
		self.scores_screen = ScoresScreen(name = name)
		self.add_widget(self.scores_screen)
		self.transition = SlideTransition(direction = "right")
		self.current = name

	def new_final_score_screen(self, timer = 0):
		self.remove_existing_child_widgets()
		name = "final_score_screen"
		self.final_score_screen = FinalScoreScreen(final_score = self.final_score, name = name)
		self.add_widget(self.final_score_screen)
		self.current = name

	def check_answers(self, answer_choice_button):
		game_status = self.question_screen.check_answer(answer_choice_button)
		if(game_status == "finished"):
			self.final_score = self.question_screen.get_score()
			Clock.schedule_once(self.new_final_score_screen, 0.7)
		if(game_status == "incorrect"):
			self.final_score = self.question_screen.get_score()
			Clock.schedule_once(self.new_final_score_screen, 0.7)

	def remove_existing_child_widgets(self):
		if(self.start_screen in self.children):
			self.remove_widget(self.start_screen)
		if(self.question_screen in self.children):
			self.remove_widget(self.question_screen)
		if(self.scores_screen in self.children):
			self.remove_widget(self.scores_screen)
		if(self.final_score_screen in self.children):
			self.remove_widget(self.final_score_screen)

	"""def enter_player_name(self):
		score_popup = ScorePopup(on_dismiss = self.enter_data)
		score_popup.open()

	def enter_data(self, popup):
		ScoresTracking().update_scores(popup.name.text, self.final_score)"""


class TriviaApp(App):

	def on_pause(self):
		return True

	def open_settings(self):
		pass

if __name__ == '__main__':
	Window.clearcolor = get_color_from_hex("#383e4e")
	LabelBase.register(name = "Montserrat", fn_regular = "fonts/Montserrat-Bold.otf", fn_bold = "fonts/Montserrat-ExtraBold.otf")
	LabelBase.register(name = "Modern Pictograms", fn_regular = "fonts/modernpics.ttf")
	TriviaApp().run()




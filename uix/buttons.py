from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.graphics import Rectangle, Color
from kivy.properties import OptionProperty, ObjectProperty, ListProperty
from kivy.uix.label import Label

class AnswerButton(ButtonBehavior, BoxLayout):

	background_color = ListProperty([1,1,1])

	def rgb(self, red, green, blue):
		max_value = 255.0
		return [red/max_value, green/max_value, blue/max_value]

	def correct_color(self):
		self.background_color = self.rgb(0, 188, 140)

	def incorrect_color(self):
		self.background_color = self.rgb(231, 76, 60)

	def refresh_color(self):
		self.background_color =self.rgb(19, 19, 25) if self.state == "down" else self.rgb(24, 24, 34)


class PurpleButton(Button):

	def __init__(self, **kwargs):
		super(PurpleButton, self).__init__(**kwargs)
		self.background_normal = ""
		self.background_down = ""
		#self.background_color = self.rgba(19,19,25,1) if self.state == "down" else self.rgba(24,24,34,1)

	def rgba(self, red, green, blue, alpha):
		max_value = 255.0
		return [red/max_value, green/max_value, blue/max_value, alpha]
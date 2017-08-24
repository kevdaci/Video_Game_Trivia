from kivy.uix.modalview import ModalView
from kivy.graphics import Rectangle, Color


class MyPopup(ModalView):

	def __init__(self, **kwargs):
		super(MyPopup, self).__init__(**kwargs)
		self.size_hint = [0.8, 0.4]
		self.background = ""
		self.auto_dismiss = False


class ScorePopup(MyPopup):

	def __init__(self, **kwargs):
		super(ScorePopup, self).__init__(**kwargs)


class ZeroPopup(MyPopup):

	def __init__(self, **kwargs):
		super(ZeroPopup, self).__init__(**kwargs)


class ErrorPopup(MyPopup):

	def __init__(self, **kwargs):
		super(ErrorPopup, self).__init__(**kwargs)


class NetworkErrorPopup(ErrorPopup):

	def __init__(self, **kwargs):
		super(NetworkErrorPopup, self).__init__(**kwargs)

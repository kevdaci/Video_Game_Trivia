import threading
import gspread
from oauth2client.service_account import ServiceAccountCredentials

#class ScoresTracking(object):
class ScoresTracking(threading.Thread):

	scope = ["https://spreadsheets.google.com/feeds"]
	creds = ServiceAccountCredentials.from_json_keyfile_name("client_secret.json", scope)
	client = gspread.authorize(creds)
	sheet = client.open("VideoGameTriviaApp").sheet1

	def __init__(self, name=None, score=None):
		threading.Thread.__init__(self);
		self.name = name
		self.score = score

	def run(self):
		self.update_scores(self.name, self.score)

	def update_scores(self, name, score):
		records = self.sheet.get_all_records()
		index_new_score = self.__sort_cells(records, [score, name])
		start_row = 2
		if(index_new_score != -1):
			self.sheet.insert_row([name, score], index_new_score + start_row)
		self.sheet.resize(rows = 51)

	def __sort_cells(self, records, new_entry):
		pair_values = []
		index = -1
		for record in records:
			pair_values.append([record["Score"], record["Name"]])
		pair_values.append(new_entry)
		pair_values.sort()
		pair_values = pair_values [::-1]
		try:
			index = pair_values.index(new_entry)
		except:
			index = -1
		return index

	def get_scores_data(self):
		return self.sheet.get_all_records()
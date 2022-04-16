from datetime import datetime


class ReleaseDate():

	@classmethod
	def date_string_to_object(self, date: str) -> datetime.date:
		return datetime\
        		.strptime(date, '%Y-%m-%d')\
        		.date()

	@classmethod
	def date_object_to_string(self, date: datetime.date) -> str:
		return date.strftime('%Y-%m-%d')
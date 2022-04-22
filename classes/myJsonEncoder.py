from json import JSONEncoder
import datetime

class MyJsonEncoder(JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime.date):
            return f"{obj.day}.{obj.month}"
        else:
            return obj.__dict__    
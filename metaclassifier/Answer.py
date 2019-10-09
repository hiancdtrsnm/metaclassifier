
class Answer(object):

    def __init__(self, answer: str, extra_data:dict):
        self.answer = answer
        self.extra_data = extra_data

    def to_dict(self):
        return {
            'answer': self.answer,
            'extra_data': self.extra_data
        }

    def __str__(self):
        return str(self.to_dict())

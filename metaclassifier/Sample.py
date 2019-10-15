from typing import Set, List
from .Answer import Answer


class Sample(object):

    def __init__(self, id: str, text: str, options: List[str], writter):
        self.id = id
        self.text = text
        self.options = options
        self._options_set = set(options)
        if len(options) != len(self._options_set):
            raise Exception('The option list most not contain repeat options')

        self.writter = writter

        self.answers: List[Answer] = []

    def save(self, option: str, **kwargs):
        if option not in self._options_set:
            raise Exception('The selected option most be in the options set')

        ans = Answer(option, kwargs)
        self.answers.append(ans)

        self.writter.save(self)

    def to_dict(self)->dict:
        return {
            'text':self.text,
            'answers': [ans.to_dict() for ans in self.answers],
            'id': self.id
        }

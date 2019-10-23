from typing import Set, List, Dict, Any
from .Answer import Answer

class RepeatedOptions(Exception):
    pass

class BadContainerClass(Exception):
    pass

class Sample(object):

    def __init__(self, id: str, text: str, options: List[str], writter, additional_data: Dict[str, Any]={}):
        self.id = id
        self.text = text
        self.options = options
        self._options_set = set(options)
        if len(options) != len(self._options_set):
            raise RepeatedOptions('The option list most not contain repeat options')

        self.writter = writter

        self.answers: List[Answer] = []

        self.additional_data = additional_data

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
            'id': self.id,
            'additional_data': self.additional_data
        }

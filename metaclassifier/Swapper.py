from typing import List
import random
from .Sample import Sample
from hashlib import md5
import json
from os.path import exists
from typing import Dict

class Swapper(object):
    def __init__(self, texts: List[str], options: List[str], destination: str):

        self.destination = destination
        self.samples: Dict[str, Sample] = {}
        self.options = options
        for text in texts:
            hash_digest = md5(text.encode()).hexdigest()
            self.samples[hash_digest] = Sample(hash_digest, text, options,
                                               self)

        self.finished = {}

        if exists(destination):
            self.done = json.load(open(destination))
            for s in self.done:
                self.samples.pop(s['id'])


    def get_sample(self)->Sample:

        with_annotation = [s for s in self.samples.values() if len(s.answers) > 0]

        prob = min(1, len(with_annotation)/100)

        if random.random() < prob:
            return random.choice(tuple(self.samples.values()))

        return random.choice(tuple(self.samples.values()))

    def save(self, sample: Sample):

        if sample.id in self.samples and len(sample.answers) >= 2:
            self.samples.pop(sample.id)

        self.finished[sample.id] = sample
        json.dump(list(map(lambda x: x.to_dict(), self.finished.values())),
                  open(self.destination, 'w'),
                  indent=2,
                  default=str,
                  ensure_ascii=False)

    @staticmethod
    def load_from_dict(data: dict):
        return Swapper(**data)

    @staticmethod
    def load_from_yaml(data: dict):
        path = data.pop('source')
        data['texts'] = [line for line in open(path)]
        return Swapper(**data)

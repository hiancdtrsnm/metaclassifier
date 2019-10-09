from typing import List
import random
from .Sample import Sample
from hashlib import md5
import json
from os.path import exists


class Swapper(object):
    def __init__(self, texts: List[str], options: List[str], destination: str):

        self.destination = destination
        self.samples = {}
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
        return random.choice(tuple(self.samples.values()))

    def save(self, sample: Sample):

        if sample.id in self.samples:
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
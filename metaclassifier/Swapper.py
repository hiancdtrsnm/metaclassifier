from typing import List
import random
from .Sample import Sample
from hashlib import md5
import json
from os.path import exists
from typing import Dict
from collections import Counter

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
        counter = 0
        if exists(destination):
            self.done = json.load(open(destination))
            for s in self.done:
                try:
                    # Sustituir this for organizative method
                    c = Counter(map(lambda x: x['answer'], s['answers']))
                    if max(c.values()) >= 2:
                        counter += 1
                        self.samples.pop(s['id'])
                except KeyError as e:
                    print(e)
                    print('Error removing id: '+ s['id'] + '\n' , s)

        print('Skiped samples: ', counter)


    def get_sample(self)->Sample:

        with_annotation = [s for s in self.samples.values() if len(s.answers) > 0]

        prob = min(1, len(with_annotation)/100)

        if random.random() < prob:
            return random.choice(tuple(self.samples.values()))

        return random.choice(tuple(self.samples.values()))

    def save(self, sample: Sample):

        # This most be separeted
        c = Counter(map(lambda x: x.answer, sample.answers))
        if max(c.values()) >= 2:
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
        data['texts'] = [json.loads(line) for line in open(path) if line]
        return Swapper(**data)

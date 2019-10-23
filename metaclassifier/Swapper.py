from typing import List, Dict, Any
import random
from .Sample import Sample
from hashlib import md5, sha1
import json
from os.path import exists

COINCIDENT_ANSWERS = 2
MAX_ANSWERS = 100

# TODO: por optimizar la clase, mirar los comentarios de abajo
# en el metodo save se guarda todo cada vez que hay un cambio
# se samplea sobre todas las muestras, cuando haya muchas hay que expandir
# los generadores y luego samplear que es lento
# mover las llaves a sha1 para evitar colisiones
class Swapper(object):
    def __init__(self, texts: List[str], options: List[str], destination: str, aditional_datas: List[Dict[str, Any]]=[]):

        self.destination = destination
        self.samples: Dict[str, Sample] = {}
        self.options = options
        for n, text in enumerate(texts):
            hash_digest = md5(text.encode()).hexdigest()
            try:
                adat = aditional_datas[n]
            except:
                adat = {}
            self.samples[hash_digest] = Sample(hash_digest, text, options,
                                               self, adat)

        self.finished = {}

        if exists(destination):
            self.done = json.load(open(destination))
            for s in self.done:
                try:
                    self.samples.pop(s['id'])
                except KeyError:
                    print('Error removing id: '+ s['id'] + '\n' , s)


    def get_sample(self)->Sample:

        with_annotation = [s for s in self.samples.values() if len(s.answers) > 0]

        prob = min(1, len(with_annotation)/100)

        if random.random() < prob:
            return random.choice(tuple(self.samples.values()))

        return random.choice(tuple(self.samples.values()))

    def save(self, sample: Sample):

        if sample.id in self.samples:
            try:
                max_ans = int(sample.additional_data['max_answers'])
            except (KeyError, TypeError):
                max_ans = MAX_ANSWERS
            if len(sample.answers) >= max_ans:
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
        try:
            path = data.pop('info')
            data['aditional_datas'] =  [json.loads(line.strip()) for line in open(path)]
        except KeyError:
            pass
        return Swapper(**data)
import json
from .Swapper import Swapper
from fire import Fire

class CLI:
    @staticmethod
    def console(json_path):

        data = json.load(open(json_path))

        sp = Swapper.load_from_dict(data)

        while sp.samples:

            sample = sp.get_sample()

            print(sample.text)

            print('\nchoose one option:\n\n')

            ans = input(' '.join((f'({i}) {option}' for i, option in enumerate(sample.options))) + '\n')
            if not ans.isnumeric():
                print('Your choice is not numeric')
                continue
            index = int(ans)
            if 0 <= index < len(sample.options):
                sample.save(sample.options[index])


Fire(CLI)
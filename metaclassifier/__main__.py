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


    @staticmethod
    def webapp(json_path, web_server_config: str=None):
        web_config: dict = {'host': '0.0.0.0', 'port': 8000, 'reload':True}
        if web_server_config is not None:
            raise NotImplementedError('But not quite yet')



        data = json.load(open(json_path))

        sp = Swapper.load_from_dict(data)

        from .webapp import run_web

        run_web(sp, **web_config)








Fire(CLI)
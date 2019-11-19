import yaml
from typing import Dict, Any
from .Swapper import Swapper
config: Dict[str, Any] = {}
swapper: Swapper = None


def load_config(path):
    global config
    config = yaml.load(open(path).read())
    load_swapper(config['swapper'])
    return config

def load_swapper(config):
    global swapper
    swapper = Swapper.load_from_yaml(config)
    return swapper
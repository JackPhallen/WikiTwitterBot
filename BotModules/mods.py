from BotModules.txt import txt
from BotModules.wikifeat import wikifeat
from BotModules.wikirandom import wikirandom
from BotModules.wikievent import wikievent

# Add reference to module init
init = {
    "txt": txt.init,
    "wikifeat": wikifeat.init,
    "wikirandom": wikirandom.init,
    "wikievent": wikievent.init
}

# Add reference to module getter
get = {
    "txt": txt.get,
    "wikifeat": wikifeat.get,
    "wikirandom": wikirandom.get,
    "wikievent": wikievent.get
}


def activate(module, config):
    '''
    Initiates module and returns getter to BotConfig
    :param module: module to activate
    :param config: configuration to module
    :return: module getter
    '''
    global init
    global get
    init[module](config)
    return get[module]


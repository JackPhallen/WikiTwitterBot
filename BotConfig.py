import configparser
from BotModules import mods
class BotConfig:

    # Some things are better off not in the properties file...
    tweetformat = "Subject: {}\n\n{}"

    modules = {}

    def __init__(self, file):
        self.__dict__ = {}
        self._init(file)

    def _init(self, file):
        '''
        Fetches properties from file and sets them as BotConfig attributes
        :param file: properties file
        '''
        config = configparser.ConfigParser()
        config.read(file)
        # Get list of proprties to set
        required_props = config['dev']['RequiredProps'].split(",")
        modules = config['dev']['Modules'].split(",")
        for module in modules:
            self._set_module(module, config[module])
        # Set zone, allows for multiple sets of properties in file
        zone = config['dev']['Zone']
        # Check for all required properties
        for prop in required_props:
            if prop not in config[zone]:
                raise Exception("Config Error: Missing '%s' in '%s' " % (prop, file))
        for prop in config[zone]:
            self._set_prop(prop, config[zone][prop])

    def _set_prop(self, key, value):
        '''
        Sets attributes of self
        :param key: attribute key
        :param value: attribute value
        '''
        self.__dict__[key] = value

    def _set_module(self, module, config):
        '''
        Initiate each module and add to config module dictionary
        :param module: module to activate
        :param config: config for module
        '''
        self.modules[module] = mods.activate(module, config)


import os
import yaml


TEMPLATE_VARS = {
    'cwd': os.getcwd()
}


class ConfigDict(object):
    def __init__(self, yaml_dict):
        self.dict = yaml_dict

    def __repr__(self):
        return repr(self.dict)

    def __str__(self):
        return str(self.dict)

    def __getattr__(self, attr):
        try:
            val = self.dict[attr]

            for var in TEMPLATE_VARS:
                if isinstance(val, str) and ("{{%s}}" % var) in val:
                    val = val.replace("{{%s}}" % var, TEMPLATE_VARS[var])

            if isinstance(val, dict):
                val = ConfigDict(val)

            return val
        except KeyError:
            raise AttributeError

    def get(self, attr):
        return self.__getattr__(attr)


def load(config_path):
    with open(config_path, 'r') as config_file:
        return ConfigDict(yaml.safe_load(config_file))

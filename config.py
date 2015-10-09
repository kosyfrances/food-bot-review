#  Defining a re-usable configuration method in this file
# Imports are done in places where they are needed


class Config:
    """
    Making this class look like a dictionary
    so we can manipulate configuration values the way we want
    """
    config_dict = {}

    @staticmethod
    def __getitem__(*args, **kwargs):
        return Config.config_dict.__getitem__(*args, **kwargs)

    @staticmethod
    def __setitem__(*args, **kwargs):
        return Config.config_dict.__setitem__(*args, **kwargs)

    @staticmethod
    def __iter__(*args, **kwargs):
        """
        This makes this class iterable like a dictionary
        """
        return Config.config_dict.__iter__(*args, **kwargs)

    @staticmethod
    def load_yaml(config_file):
        import yaml

        Config.config_dict.update(yaml.load(file(config_file, 'r')))

    @staticmethod
    def update(*args, **kwargs):
        """
        To update the config_dict
        """
        return Config.config_dict.update(*args, **kwargs)

    @staticmethod
    def load_os_environ_vars(startswith_string):
        """
        Load all production environmental variables that begin with
        the specific identifier we want to avoid messing up other files
        """
        import os

        environment_vars = {}
        for var in os.environ:
            if var.startswith(startswith_string):
                new_var = var[len(startswith_string):]
                environment_vars[new_var] = os.environ[var]

        Config.config_dict.update(environment_vars)

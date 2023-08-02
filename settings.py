import sys


PROMPT = None
RESPONSE_FORMAT = None
TEMPERATURE = None
LANGUAGE = None
FILENAME = None


def split_parameters(obj: str):
    return obj.split('=')


def load_settings():
    global PROMPT, RESPONSE_FORMAT, TEMPERATURE, LANGUAGE, FILENAME
    argv = sys.argv[1:]
    parameters_dict = dict(map(split_parameters, argv))

    PROMPT = parameters_dict.get('prompt')
    RESPONSE_FORMAT = parameters_dict.get('response_format')
    TEMPERATURE = parameters_dict.get('temperature', 1)
    FILENAME = parameters_dict.get('filename')
    LANGUAGE = parameters_dict.get('language')
    return Settings(FILENAME,
                    PROMPT,
                    RESPONSE_FORMAT,
                    LANGUAGE,
                    TEMPERATURE)


class Settings:
    def __init__(self,
                 filename: str,
                 prompt: str,
                 response_format: str,
                 language: str,
                 temperature: int = 1):
        self.FILENAME = filename
        self.PROMPT = prompt
        self.RESPONSE_FORMAT = response_format
        self.LANGUAGE = language
        self.TEMPERATURE = temperature


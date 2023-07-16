import os
from dotenv import load_dotenv

load_dotenv()


class Environment:
    """
        Environment is the main access port to .env variables.
    """
    CLASSIFIER_MODEL_PATH = os.getenv('CLASSIFIER_MODEL_PATH')
    CLASSIFIER_HOST = os.getenv('CLASSIFIER_HOST')
    CLASSIFIER_PORT = int(os.getenv('CLASSIFIER_PORT'))

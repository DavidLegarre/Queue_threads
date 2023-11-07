import random
import string
import time

from decorator import TokenCounter, token_limit

LIMIT = 5
tokenCounter = TokenCounter(LIMIT)


# Def wrapper counter


def get_random_string(length: int = 6):
    # choose from all lowercase letter
    letters = string.ascii_lowercase
    result_str = ''.join(random.choice(letters) for i in range(length))
    return result_str


@token_limit(tokenCounter)
def classify():
    c_id = get_random_string()
    print(f"Classifying {c_id}")
    time.sleep(1)
    print(f"Classified {c_id}")


def worker_function():
    classify()

import threading


class TokenCounter:
    def __init__(self, limit):
        self.limit = limit
        self.count = 0
        self.event = threading.Event()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def count_tokens(self):
        self.count += 1
        if self.count > self.limit:
            self.event.set()
        print(f"The count right now is: {self.count}")


def token_limit(counter: TokenCounter):
    def decorator(func):
        def wrapped(*args, **kwargs):
            func(*args, **kwargs)
            counter.count_tokens()

        return wrapped

    return decorator

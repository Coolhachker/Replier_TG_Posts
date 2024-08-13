class Exceptions:
    class ExceptionOnUnFoundChannelInDb(Exception):
        def __init__(self, message):
            super().__init__(message)

    class ExceptionOnUnsuitablePost(Exception):
        def __init__(self, message):
            super().__init__(message)
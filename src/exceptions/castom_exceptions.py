class Exceptions:
    class ExceptionOnUnFoundChannelInDb(Exception):
        def __init__(self, message):
            super().__init__(message)

    class ExceptionOnUnsuitablePost(Exception):
        def __init__(self, message):
            super().__init__(message)

    class ExceptionOnDateOfPost(Exception):
        def __init__(self, message):
            super().__init__(message)

    class UnSuccessfulResponseRMQ(Exception):
        def __init__(self, message):
            super().__init__(message)
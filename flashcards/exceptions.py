class FlashcardsException(Exception):
    pass


class NoEditsMadeException(FlashcardsException):
    pass


class InstructionsRemovedException(FlashcardsException, ValueError):
    pass

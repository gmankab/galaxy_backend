import typing


class NotPassed(Exception):
    def __init__(
        self,
        msg: str = '',
    ):
        self.msg = msg


cor_str = typing.Callable[[], typing.Coroutine[None, None, str]]


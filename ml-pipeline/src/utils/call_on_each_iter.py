
from typing import Callable, Iterable

def call_on_each_iter[T](callable: Callable[[], T]) -> Iterable[T]:
    """
    A generator that continuously calls and yields the result of this function.
    """
    while True:
        yield callable()

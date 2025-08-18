from collections.abc import Sequence
from typing import Callable, Iterable  

def get_predictions[I, T](model: Callable[[I], T], dataset: Sequence[I]) -> Iterable[T]:
    for batch in dataset:
        yield model(batch)


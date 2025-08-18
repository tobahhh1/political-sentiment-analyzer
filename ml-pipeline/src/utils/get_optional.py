
from typing import Optional

def get_optional[T](x: Optional[T], fail_msg: str = "Expected non-None value") -> T:
    assert x is not None, fail_msg
    return x

if __name__ != "__main__": from .operator_enum import Operator, MathKeyword, Other
else: from operator_enum import Operator, MathKeyword, Other
from typing import List, Tuple, Union
from decimal import Decimal


def Parser(lexed_list: List[Tuple[Union[Operator, MathKeyword, Other], Union[Decimal, str]]]) -> Decimal:
    leftbracket_ptrlist: List[int] = list()
    for lexed_tuple in lexed_list:
        
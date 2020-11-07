from operator_enum import Operator, MathKeyword, Other
from exception import ParserException
from typing import List, Tuple, Union, cast
from decimal import Decimal

TupleType = Tuple[Union[Operator, MathKeyword, Other], Union[Decimal, str]]
LexedType = List[TupleType]

def OperatorFinder(parsed_list: LexedType, checkOperator_list: List[Union[Operator, MathKeyword, Other]]) -> bool:
	for parsed_list_value in parsed_list:
		for checkOperator_list_value in checkOperator_list:
			if parsed_list_value[0] == checkOperator_list_value: return True

	return False

def Calcurate(parsed_list: LexedType) -> None:
	if len(parsed_list) == 0: raise ParserException()

	parsed_list_ptr: int = 0
	while OperatorFinder(parsed_list, [Operator.Multi, Operator.Divide, Operator.Modulo]):
		parsed_list_value = parsed_list[parsed_list_ptr]

		if parsed_list_value[0] == Operator.Multi:
			left_value = parsed_list[parsed_list_ptr - 1]
			right_value = parsed_list[parsed_list_ptr + 1]

			# [0] [*] [0] [*] ...
			#  ^  (^)
			parsed_list[parsed_list_ptr - 1] = (Other.Value, Decimal(0))

			# [1] [*] [0] [*] ...
			#      ^
			parsed_list.pop(parsed_list_ptr)
			# [1] [0] [*] ...
			#      ^
			parsed_list.pop(parsed_list_ptr)

			# [1] [*] ...
			#  ^
			parsed_list_ptr -= 1
		elif parsed_list_value[0] == Operator.Divide:
			left_value = parsed_list[parsed_list_ptr - 1]
			right_value = parsed_list[parsed_list_ptr + 1]

			# [0] [/] [0] [/] ...
			#  ^  (^)
			parsed_list[parsed_list_ptr - 1] = (Other.Value, Decimal(0))

			# [1] [/] [0] [/] ...
			#      ^
			parsed_list.pop(parsed_list_ptr)
			# [1] [0] [/] ...
			#      ^
			parsed_list.pop(parsed_list_ptr)

			# [1] [/] ...
			#  ^
			parsed_list_ptr -= 1
		elif parsed_list_value[0] == Operator.Modulo:
			left_value = parsed_list[parsed_list_ptr - 1]
			right_value = parsed_list[parsed_list_ptr + 1]

			# [0] [%] [0] [%] ...
			#  ^  (^)
			parsed_list[parsed_list_ptr - 1] = (Other.Value, Decimal(0))

			# [1] [%] [0] [%] ...
			#      ^
			parsed_list.pop(parsed_list_ptr)
			# [1] [0] [%] ...
			#      ^
			parsed_list.pop(parsed_list_ptr)

			# [1] [%] ...
			#  ^
			parsed_list_ptr -= 1

		parsed_list_ptr += 1

	parsed_list_ptr = 0
	while OperatorFinder(parsed_list, [Operator.Plus, Operator.Minus]):
		parsed_list_value = parsed_list[parsed_list_ptr]

		if parsed_list_value[0] == Operator.Plus:
			left_value = parsed_list[parsed_list_ptr - 1]
			right_value = parsed_list[parsed_list_ptr + 1]

			# [0] [+] [0] [+] ...
			#  ^  (^)
			parsed_list[parsed_list_ptr - 1] = (Other.Value, Decimal(0))

			# [1] [+] [0] [+] ...
			#      ^
			parsed_list.pop(parsed_list_ptr)
			# [1] [0] [+] ...
			#      ^
			parsed_list.pop(parsed_list_ptr)

			# [1] [+] ...
			#  ^
			parsed_list_ptr -= 1
		elif parsed_list_value[0] == Operator.Minus:
			left_value = parsed_list[parsed_list_ptr - 1]
			right_value = parsed_list[parsed_list_ptr + 1]

			# [0] [-] [0] [-] ...
			#  ^  (^)
			parsed_list[parsed_list_ptr - 1] = (Other.Value, Decimal(0))

			# [1] [-] [0] [-] ...
			#      ^
			parsed_list.pop(parsed_list_ptr)
			# [1] [0] [-] ...
			#      ^
			parsed_list.pop(parsed_list_ptr)

			# [1] [-] ...
			#  ^
			parsed_list_ptr -= 1

		parsed_list_ptr += 1

	print(parsed_list)
	print()
	if len(parsed_list) != 1: raise ParserException("Couldn't Calculation")

# Reference list argument, output the result into list argument by using it
# In other words, it's used as a pointer
def Analyzer(lexed_lists: Union[List[Union[LexedType, TupleType]], TupleType]) -> None:
	for lexed_value in lexed_lists:
		if type(lexed_value) is list:
			Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))

	Calcurate(cast(LexedType, lexed_lists))

def Parser(lexed_lists: List[Union[LexedType, TupleType]]) -> Decimal:
	Analyzer(lexed_lists)
	print(lexed_lists)

	if len(lexed_lists) != 1: raise ParserException("Unknown error")

	return cast(Decimal, lexed_lists[0][1])


if __name__ == "__main__":
	a = range(10)
	for b in a:
		pass

	from lexer import Lexer
	test_text: str = "((2) + 20 * (-4 / 2)) - 6"
	lexed_lists = Lexer(test_text)
	print(lexed_lists)
	print()
	print("<-Parser test->")
	print(Parser(lexed_lists))

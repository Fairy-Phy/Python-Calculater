from operator_enum import Operator, MathKeyword, Other
from exception import ParserException
from typing import List, Tuple, Union, cast

TupleType = Tuple[Union[Operator, MathKeyword, Other], Union[float, str]]
LexedType = List[TupleType]

def OperatorFinder(parsed_list: LexedType, checkOperator_list: List[Union[Operator, MathKeyword, Other]]) -> bool:
	for parsed_list_value in parsed_list:
		for checkOperator_list_value in checkOperator_list:
			if parsed_list_value[0] == checkOperator_list_value: return True

	return False


"""
担当を分けるため計算はCalcuratorに
関数化して入れる
"""
def Calcurate(parsed_list: LexedType) -> None:
	if len(parsed_list) == 0: raise ParserException()

	parsed_list_ptr: int = 0
	while OperatorFinder(parsed_list, [Operator.Factorial]):
		parsed_list_value = parsed_list[parsed_list_ptr]

		if parsed_list_value[0] == Operator.Factorial:
			left_value = parsed_list[parsed_list_ptr - 1]

			# [0] [!] [*] [0] ...
			#  ^  (^)
			parsed_list[parsed_list_ptr - 1] = (Other.Value, float(0))

			# [1] [!] [*] [0] ...
			#      ^
			parsed_list.pop(parsed_list_ptr)

			# [1] [*] [0] ...
			#  ^
			parsed_list_ptr -= 1

		parsed_list_ptr += 1

	parsed_list_ptr = 0
	while OperatorFinder(parsed_list, [Operator.Pow]):
		parsed_list_value = parsed_list[parsed_list_ptr]

		if parsed_list_value[0] == Operator.Pow:
			left_value = parsed_list[parsed_list_ptr - 1]
			right_value = parsed_list[parsed_list_ptr + 1]

			# [0] [^] [0] [^] ...
			#  ^  (^)
			parsed_list[parsed_list_ptr - 1] = (Other.Value, float(0))

			# [1] [^] [0] [^] ...
			#      ^
			parsed_list.pop(parsed_list_ptr)
			# [1] [0] [^] ...
			#      ^
			parsed_list.pop(parsed_list_ptr)

			# [1] [^] ...
			#  ^
			parsed_list_ptr -= 1

		parsed_list_ptr += 1

	parsed_list_ptr = 0
	while OperatorFinder(parsed_list, [Operator.Multi, Operator.Divide, Operator.Modulo]):
		parsed_list_value = parsed_list[parsed_list_ptr]

		if parsed_list_value[0] == Operator.Multi:
			left_value = parsed_list[parsed_list_ptr - 1]
			right_value = parsed_list[parsed_list_ptr + 1]

			# [0] [*] [0] [*] ...
			#  ^  (^)
			parsed_list[parsed_list_ptr - 1] = (Other.Value, float(0))

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
			parsed_list[parsed_list_ptr - 1] = (Other.Value, float(0))

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
			parsed_list[parsed_list_ptr - 1] = (Other.Value, float(0))

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
			parsed_list[parsed_list_ptr - 1] = (Other.Value, float(0))

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
			parsed_list[parsed_list_ptr - 1] = (Other.Value, float(0))

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

	if len(parsed_list) != 1: raise ParserException("Couldn't Calculation")

	# parsed_list = parsed_list[0]
	# It should returns a Tuple, but omitted it because it results in a List

# Reference list argument, output the result into list argument by using it
# In other words, it's used as a pointer
def Analyzer(lexed_lists: List[Union[LexedType, TupleType]]) -> None:
	lexed_lists_index: int = 0
	while lexed_lists_index < len(lexed_lists):
		lexed_value = lexed_lists[lexed_lists_index]

		if type(lexed_value) is list:
			if lexed_lists_index != 0:
				prev_lexed_value = lexed_lists[lexed_lists_index - 1]
				if type(prev_lexed_value) is tuple:
					prev_lexed_value = cast(TupleType, prev_lexed_value)

					"""
					正しくやるためには少し考えなければならない
					今のままでは計算したあとに計算ができない
					リスト内のカンマを見つけ、区切り再帰をする
					そうすることでリストが1つのValueになる
					そこから改めて計算するのが一番良いはずだ
					"""
					if prev_lexed_value[0] == MathKeyword.Sqrt:
						lexed_value = cast(LexedType, lexed_value)
						if lexed_value[0][0] != Other.Value: raise ParserException()

						prev_lexed_value = (Other.Value, float(0))
						lexed_lists.pop(lexed_lists_index)

						lexed_lists_index -= 1
					elif prev_lexed_value[0] == MathKeyword.Log10: pass
					elif prev_lexed_value[0] == MathKeyword.Log: pass

					elif prev_lexed_value[0] == MathKeyword.Sin: pass
					elif prev_lexed_value[0] == MathKeyword.Asin: pass
					elif prev_lexed_value[0] == MathKeyword.Cos: pass
					elif prev_lexed_value[0] == MathKeyword.Acos: pass
					elif prev_lexed_value[0] == MathKeyword.Tan: pass
					elif prev_lexed_value[0] == MathKeyword.Atan: pass

					elif prev_lexed_value[0] == MathKeyword.Permutation: pass
					elif prev_lexed_value[0] == MathKeyword.Combination: pass
					else: Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))
				else: Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))
			else: Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))

		lexed_lists_index += 1

	Calcurate(cast(LexedType, lexed_lists))

def Parser(lexed_lists: List[Union[LexedType, TupleType]]) -> float:
	Analyzer(lexed_lists)

	if len(lexed_lists) != 1: raise ParserException("Unknown error")

	return cast(float, lexed_lists[0][1])


if __name__ == "__main__":
	from lexer import Lexer

	test_text: str = "((2^4) + 20! * (-4 / 2)) - 6"

	print("<-Lexer Phase->")
	lexed_lists = Lexer(test_text)
	print(lexed_lists)
	print()
	print("<-Parser Phase->")
	print("Result:", Parser(lexed_lists))

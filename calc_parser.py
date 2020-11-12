from calcurator import Permutation, Combination
from operator_enum import Operator, MathKeyword, Other
from exception import ParserException
from typing import List, Tuple, Union, cast, Any
import math

TupleType = Tuple[Union[Operator, MathKeyword, Other], Union[float, str]]
LexedType = List[TupleType]

def OperatorFinder(parsed_list: LexedType, checkOperator_list: List[Union[Operator, MathKeyword, Other]]) -> List[int]:
	result_list: List[int] = list()

	list_index: int = 0
	for parsed_list_value in parsed_list:
		for checkOperator_list_value in checkOperator_list:
			if parsed_list_value[0] == checkOperator_list_value: result_list.append(list_index)
		list_index += 1

	return result_list

def Calcurate(parsed_list: LexedType) -> None:
	if len(parsed_list) == 0: return

	parsed_list_ptr: int = 0
	while OperatorFinder(parsed_list, [Operator.Factorial]):
		parsed_list_value = parsed_list[parsed_list_ptr]

		if parsed_list_value[0] == Operator.Factorial:
			left_value = parsed_list[parsed_list_ptr - 1]

			# [0] [!] [*] [0] ...
			#  ^  (^)
			parsed_list[parsed_list_ptr - 1] = (Other.Value, math.factorial(cast(float, left_value[1])))

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
			parsed_list[parsed_list_ptr - 1] = (Other.Value, math.pow(cast(float, left_value[1]), cast(float, right_value[1])))

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
			parsed_list[parsed_list_ptr - 1] = (Other.Value, cast(float, left_value[1]) * cast(float, right_value[1]))

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
			parsed_list[parsed_list_ptr - 1] = (Other.Value, cast(float, left_value[1]) / cast(float, right_value[1]))

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
			parsed_list[parsed_list_ptr - 1] = (Other.Value, cast(float, left_value[1]) % cast(float, right_value[1]))

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
			parsed_list[parsed_list_ptr - 1] = (Other.Value, cast(float, left_value[1]) + cast(float, right_value[1]))

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
			parsed_list[parsed_list_ptr - 1] = (Other.Value, cast(float, left_value[1]) - cast(float, right_value[1]))

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

					if prev_lexed_value[0] == MathKeyword.Sqrt:
						index_list = OperatorFinder(cast(LexedType, lexed_value), [Other.Comma])
						if index_list:
							first_index = index_list[0]
							if not first_index: raise ParserException("First argument does not exist.")

							first_list = lexed_value[:first_index]
							Analyzer(cast(List[Union[LexedType, TupleType]], first_list))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.sqrt(cast(float, first_list[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
						else:
							Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.sqrt(cast(float, lexed_value[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
					elif prev_lexed_value[0] == MathKeyword.Log10:
						index_list = OperatorFinder(cast(LexedType, lexed_value), [Other.Comma])
						if index_list:
							first_index = index_list[0]
							if not first_index: raise ParserException("First argument does not exist.")

							first_list = lexed_value[:first_index]
							Analyzer(cast(List[Union[LexedType, TupleType]], first_list))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.log10(cast(float, first_list[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
						else:
							Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.log10(cast(float, lexed_value[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
					elif prev_lexed_value[0] == MathKeyword.Log:
						index_list = OperatorFinder(cast(LexedType, lexed_value), [Other.Comma])
						if index_list:
							first_index = index_list[0]
							if not first_index: raise ParserException("First argument does not exist.")
							if first_index + 1 == len(lexed_value): raise ParserException("Second argument does not exist.")

							first_list = lexed_value[:first_index]
							second_list = lexed_value[first_index + 1:]
							Analyzer(cast(List[Union[LexedType, TupleType]], first_list))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.log(cast(float, first_list[0][1]), cast(float, second_list[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
						else: raise ParserException("Second argument does not exist.")

					elif prev_lexed_value[0] == MathKeyword.Sin:
						index_list = OperatorFinder(cast(LexedType, lexed_value), [Other.Comma])
						if index_list:
							first_index = index_list[0]
							if not first_index: raise ParserException("First argument does not exist.")

							first_list = lexed_value[:first_index]
							Analyzer(cast(List[Union[LexedType, TupleType]], first_list))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.sin(cast(float, first_list[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
						else:
							Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.sin(cast(float, lexed_value[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
					elif prev_lexed_value[0] == MathKeyword.Asin:
						index_list = OperatorFinder(cast(LexedType, lexed_value), [Other.Comma])
						if index_list:
							first_index = index_list[0]
							if not first_index: raise ParserException("First argument does not exist.")

							first_list = lexed_value[:first_index]
							Analyzer(cast(List[Union[LexedType, TupleType]], first_list))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.asin(cast(float, first_list[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
						else:
							Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.asin(cast(float, lexed_value[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
					elif prev_lexed_value[0] == MathKeyword.Cos:
						index_list = OperatorFinder(cast(LexedType, lexed_value), [Other.Comma])
						if index_list:
							first_index = index_list[0]
							if not first_index: raise ParserException("First argument does not exist.")

							first_list = lexed_value[:first_index]
							Analyzer(cast(List[Union[LexedType, TupleType]], first_list))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.cos(cast(float, first_list[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
						else:
							Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.cos(cast(float, lexed_value[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
					elif prev_lexed_value[0] == MathKeyword.Acos:
						index_list = OperatorFinder(cast(LexedType, lexed_value), [Other.Comma])
						if index_list:
							first_index = index_list[0]
							if not first_index: raise ParserException("First argument does not exist.")

							first_list = lexed_value[:first_index]
							Analyzer(cast(List[Union[LexedType, TupleType]], first_list))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.acos(cast(float, first_list[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
						else:
							Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.acos(cast(float, lexed_value[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
					elif prev_lexed_value[0] == MathKeyword.Tan:
						index_list = OperatorFinder(cast(LexedType, lexed_value), [Other.Comma])
						if index_list:
							first_index = index_list[0]
							if not first_index: raise ParserException("First argument does not exist.")

							first_list = lexed_value[:first_index]
							Analyzer(cast(List[Union[LexedType, TupleType]], first_list))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.tan(cast(float, first_list[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
						else:
							Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.tan(cast(float, lexed_value[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
					elif prev_lexed_value[0] == MathKeyword.Atan:
						index_list = OperatorFinder(cast(LexedType, lexed_value), [Other.Comma])
						if index_list:
							first_index = index_list[0]
							if not first_index: raise ParserException("First argument does not exist.")

							first_list = lexed_value[:first_index]
							Analyzer(cast(List[Union[LexedType, TupleType]], first_list))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.atan(cast(float, first_list[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
						else:
							Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, math.atan(cast(float, lexed_value[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)

					elif prev_lexed_value[0] == MathKeyword.Permutation:
						index_list = OperatorFinder(cast(LexedType, lexed_value), [Other.Comma])
						if index_list:
							first_index = index_list[0]
							if not first_index: raise ParserException("First argument does not exist.")
							if first_index + 1 == len(lexed_value): raise ParserException("Second argument does not exist.")

							first_list = lexed_value[:first_index]
							second_list = lexed_value[first_index + 1:]
							Analyzer(cast(List[Union[LexedType, TupleType]], first_list))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, Permutation(cast(float, first_list[0][1]), cast(float, second_list[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
						else: raise ParserException("Second argument does not exist.")
					elif prev_lexed_value[0] == MathKeyword.Combination:
						index_list = OperatorFinder(cast(LexedType, lexed_value), [Other.Comma])
						if index_list:
							first_index = index_list[0]
							if not first_index: raise ParserException("First argument does not exist.")
							if first_index + 1 == len(lexed_value): raise ParserException("Second argument does not exist.")

							first_list = lexed_value[:first_index]
							second_list = lexed_value[first_index + 1:]
							Analyzer(cast(List[Union[LexedType, TupleType]], first_list))
							lexed_lists.insert(lexed_lists_index, cast(Any, (Other.Value, Combination(cast(float, first_list[0][1]), cast(float, second_list[0][1])))))  # Any is TupleType
							lexed_lists.pop(lexed_lists_index + 1)
							lexed_lists_index -= 1
							lexed_lists.pop(lexed_lists_index)
						else: raise ParserException("Second argument does not exist.")
					else:
						Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))
						lexed_lists.insert(lexed_lists_index, cast(Any, lexed_value[0]))  # Any is TupleType
						lexed_lists.pop(lexed_lists_index + 1)
				else:
					Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))
					lexed_lists.insert(lexed_lists_index, cast(Any, lexed_value[0]))  # Any is TupleType
					lexed_lists.pop(lexed_lists_index + 1)
			else:
				Analyzer(cast(List[Union[LexedType, TupleType]], lexed_value))
				lexed_lists.insert(lexed_lists_index, cast(Any, lexed_value[0]))  # Any is TupleType
				lexed_lists.pop(lexed_lists_index + 1)

		lexed_lists_index += 1

	Calcurate(cast(LexedType, lexed_lists))

def Parser(lexed_lists: List[Union[LexedType, TupleType]]) -> float:
	Analyzer(lexed_lists)

	if len(lexed_lists) != 1: raise ParserException("Unknown error")

	return cast(float, lexed_lists[0][1])


if __name__ == "__main__":
	from lexer import Lexer

	test_text: str = "sqrt(2)"

	print("<-Lexer Phase->")
	lexed_lists = Lexer(test_text)
	print(lexed_lists)
	print()
	print("<-Parser Phase->")
	print("Result:", Parser(lexed_lists))

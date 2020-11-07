from operator_enum import Operator, MathKeyword, Other
from exception import LexerException
from typing import List, Tuple, Union, Any, cast
from decimal import Decimal

TupleType = Tuple[Union[Operator, MathKeyword, Other], Union[Decimal, str]]
ResultType = List[TupleType]

def get_nestlist(ptr_list: List[int], value_list: List[Any]) -> List[Any]:
	result_list: List[Any] = value_list
	for ptr in ptr_list:
		result_list = result_list[ptr]

	return result_list

# Tuple is
# Item1 -> Enum Type
# Item2 -> Value(operator is raw string)
def Lexer(text: str) -> List[Union[ResultType, TupleType]]:
	result_list: List[Union[ResultType, TupleType]] = list()

	current_layerlist: ResultType = list()
	current_layer_ptrlist: List[int] = [-1]
	text_ptr: int = 0
	while True:
		text_charint: int = ord(text[text_ptr] if text_ptr < len(text) else '\0')

		if text_charint == 32: pass
		elif text_charint == 40:
			if len(current_layerlist) != 0 and current_layer_ptrlist[-1] == -1:
				result_list.extend(current_layerlist)
				current_layerlist = list()
			elif len(current_layerlist) != 0:
				nestlist = get_nestlist(current_layer_ptrlist[1:], result_list)
				nestlist.extend(current_layerlist)
				current_layerlist = list()

			if current_layer_ptrlist[-1] == -1:
				current_layer_ptrlist.append(len(result_list))
				result_list.append(list())
			else:
				nestlist = get_nestlist(current_layer_ptrlist[1:], result_list)
				current_layer_ptrlist.append(len(nestlist))
				nestlist.append(list())
		elif text_charint == 41:
			if current_layer_ptrlist[-1] == -1: raise LexerException("Not found left bracket")
			nestlist = get_nestlist(current_layer_ptrlist[1:], result_list)
			nestlist.extend(current_layerlist)

			current_layer_ptrlist.pop(-1)
			current_layerlist = list()
		elif text_charint == 43:
			if (current_layerlist[-1][0] if len(current_layerlist) != 0 else Other.Unknown) != Other.Value:
				if current_layer_ptrlist[-1] == -1:
					if type(result_list[-1] if len(result_list) != 0 else (Other.Unknown, '')) is not list: pass
					else: current_layerlist.append((Operator.Plus, chr(text_charint)))
				else:
					nestlist = get_nestlist(current_layer_ptrlist[1:], result_list)
					if type(nestlist[-1] if len(nestlist) != 0 else (Other.Unknown, '')) is not list: pass
					else: current_layerlist.append((Operator.Plus, chr(text_charint)))
			else: current_layerlist.append((Operator.Plus, chr(text_charint)))
		elif text_charint == 45:
			if (current_layerlist[-1][0] if len(current_layerlist) != 0 else Other.Unknown) != Other.Value:
				if current_layer_ptrlist[-1] == -1:
					if type(result_list[-1] if len(result_list) != 0 else (Other.Unknown, '')) is not list: current_layerlist.append((Other.ValueMinus, chr(text_charint)))
					else: current_layerlist.append((Operator.Minus, chr(text_charint)))
				else:
					nestlist = get_nestlist(current_layer_ptrlist[1:], result_list)
					if type(nestlist[-1] if len(nestlist) != 0 else (Other.Unknown, '')) is not list: current_layerlist.append((Other.ValueMinus, chr(text_charint)))
					else: current_layerlist.append((Operator.Minus, chr(text_charint)))
			else: current_layerlist.append((Operator.Minus, chr(text_charint)))
		elif text_charint == 42: current_layerlist.append((Operator.Multi, chr(text_charint)))
		elif text_charint == 47: current_layerlist.append((Operator.Divide, chr(text_charint)))
		elif text_charint == 37: current_layerlist.append((Operator.Modulo, chr(text_charint)))
		elif text_charint == 94: current_layerlist.append((Operator.Pow, chr(text_charint)))
		elif text_charint == 33:
			if (current_layerlist[-1][0] if len(current_layerlist) != 0 else Other.Unknown) != Other.Value: raise LexerException("Previous value is not Number")
			current_layerlist.append((Operator.Factorial, chr(text_charint)))
		elif (text_charint >= 48 and text_charint <= 57) or text_charint == 46:
			prev_value = current_layerlist[-1][0] if len(current_layerlist) != 0 else Other.Unknown
			if prev_value == Other.Value: raise LexerException("Previous value is Number")
			elif prev_value == Operator.Factorial: raise LexerException("Previous value is Factorial")

			value: str = cast(str, current_layerlist.pop(-1)[1] if prev_value == Other.ValueMinus else "")
			value += chr(text_charint)

			text_ptr += 1
			text_charint = ord(text[text_ptr] if text_ptr < len(text) else '\0')
			while (text_charint >= 48 and text_charint <= 57) or text_charint == 46:
				value += chr(text_charint)

				text_ptr += 1
				text_charint = ord(text[text_ptr] if text_ptr < len(text) else '\0')

			if text_charint != 0: text_ptr -= 1
			current_layerlist.append((Other.Value, Decimal(value)))
		elif text_charint == 0:
			current_layerlist.append((Other.ETX, '\0'))
			if len(current_layer_ptrlist) != 1: raise LexerException("Not found right bracket")
			result_list.extend(current_layerlist)
			break
		else: current_layerlist.append((Other.Unknown, chr(text_charint)))

		text_ptr += 1

	result_list.pop(-1)
	return result_list


if __name__ == "__main__":
	print("<-get_nestlist test->")
	a: List[Any] = [[1, [0]], 0]
	b: List[Any] = [0, 1]
	print(id(get_nestlist(b, a)))
	print(id(a[0][1]))

	print("<-Lexer test->")
	test_text: str = "((+2) + 20! * (-4 / 2)) - 6"

	def allfor_lists(lists: List[Any]) -> None:
		for list_value in lists:
			if type(list_value) is list:
				print("Left Bracket")
				allfor_lists(list_value)
				print("Right Bracket")
			else: print(list_value)

	allfor_lists(Lexer(test_text))

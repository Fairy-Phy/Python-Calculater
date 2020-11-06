if __name__ != "__main__": from .operator_enum import Operator, MathKeyword, Other
else: from operator_enum import Operator, MathKeyword, Other
from typing import List, Tuple, Union, TypeVar, Any
from decimal import Decimal


ResultType = TypeVar("ResultType", bound=List[Tuple[Union[Operator, MathKeyword, Other], Union[Decimal, str]]])

def get_nestlist(ptr_list: List[int], value_list: List[Any]) -> List[Any]:
	result_list: List[Any] = value_list
	for ptr in ptr_list:
		result_list = result_list[ptr]
	
	return result_list

# 
# Tuple is
# Item1 -> Enum Type
# Item2 -> Value(operator is raw string)
# 
def Lexer(text: str) -> List[Union[List[ResultType], ResultType]]:
	result_list: List[Union[List[ResultType], ResultType]] = list()
	
	current_layerlist: ResultType = list()
	current_layer_ptrlist: List[int] = [-1]
	text_ptr: int = 0
	while True:
		text_charint: int = ord(text[text_ptr] if text_ptr < len(text) else '\0')

		if text_charint == 32: pass
		elif text_charint == 40:
		    if len(current_layerlist) != 0:
		        result_list.extend(current_layerlist)
		        current_layerlist = list()

		    if len(current_layer_ptrlist) == 1:
		    	current_layer_ptrlist.append(len(result_list))
		    	result_list.append(list())
		    else:
		    	result_list[current_layer_ptrlist[1]].append(list())
		    	current_layer_ptrlist.append(len(result_list))
		elif text_charint == 41:
		    if current_layer_ptrlist[-1] == -1: raise Exception("not found left bracket")
		    get_nestlist(current_layer_ptrlist[1:], result_list).extend(current_layerlist)
		    current_layer_ptrlist.pop(-1)
		    current_layerlist = list()
		elif text_charint == 43: current_layerlist.append((Operator.Plus, chr(text_charint)))
		elif text_charint == 45:
		    next_charint: int = ord(text[text_ptr + 1] if text_ptr < len(text) else '\0')
		    if  (current_layerlist[-1][0] if len(current_layerlist) != 0 else Other.Unknown) != Other.Value and ((next_charint >= 48 and next_charint <= 57) or next_charint == 46): result_list.append((Other.ValueMinus, chr(text_charint)))
		    else: result_list.append((Operator.Minus, chr(text_charint)))
		elif text_charint == 42: current_layerlist.append((Operator.Multi, chr(text_charint)))
		elif text_charint == 47: current_layerlist.append((Operator.Divide, chr(text_charint)))
		elif text_charint == 37: current_layerlist.append((Operator.Modulo, chr(text_charint)))
		elif text_charint == 94: current_layerlist.append((Operator.Pow, chr(text_charint)))
		elif text_charint == 33: current_layerlist.append((Operator.Factorial, chr(text_charint)))
		elif (text_charint >= 48 and text_charint <= 57) or text_charint == 46:
			value: str = current_layerlist.pop(-1)[1] if (current_layerlist[-1][0] if len(current_layerlist) != 0 else Other.Unknown) == Other.ValueMinus else ""
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
			if len(current_layer_ptrlist) != 1: raise Exception("Not found right bracket")
			result_list.extend(current_layerlist)
			break
		else: current_layerlist.append((Other.Unknown, chr(text_charint)))
		    
		text_ptr += 1
	
	return result_list


if __name__ == "__main__":
	test_text: str = "((123456789) + 20.4 * (-4 / .7)) - 6"
	print(ord("a"))
	print(ord("z"))
	a = [[1, [0]], 0]
	b = [0, 1]
	print(id(get_nestlist(b, a)))
	print(id(a[0][1]))
	print(test_text[0:3])
	for result in Lexer(test_text):
	    print(result)

if __name__ != "__main__": from .operator_enum import Operator, MathKeyword, Other
else: from operator_enum import Operator, MathKeyword, Other
from typing import List, Tuple, Union
from decimal import Decimal

# 
# Tuple is
# Item1 -> Enum Type
# Item2 -> Value(operator is raw string)
# 
def Lexer(text: str) -> List[Tuple[Union[Operator, MathKeyword, Other], Union[Decimal, str]]]:
	result_list: List[Tuple[Union[Operator, MathKeyword, Other], Union[Decimal, str]]] = list()

	text_ptr: int = 0
	while True:
		text_charint: int = ord(text[text_ptr] if text_ptr < len(text) else '\0')

		if text_charint == 32: pass
		elif text_charint == 40: result_list.append((Operator.LeftBracket, chr(text_charint)))
		elif text_charint == 41: result_list.append((Operator.RightBracket, chr(text_charint)))
		elif text_charint == 43: result_list.append((Operator.Plus, chr(text_charint)))
		elif text_charint == 45: result_list.append((Operator.Minus, chr(text_charint)))
		elif text_charint == 42: result_list.append((Operator.Multi, chr(text_charint)))
		elif text_charint == 47: result_list.append((Operator.Divide, chr(text_charint)))
		elif text_charint == 37: result_list.append((Operator.Modulo, chr(text_charint)))
		elif text_charint == 94: result_list.append((Operator.Pow, chr(text_charint)))
		elif text_charint == 33: result_list.append((Operator.Factorial, chr(text_charint)))
		elif (text_charint >= 48 and text_charint <= 57) or text_charint == 46:
			value: str = chr(text_charint)

			text_ptr += 1
			text_charint = ord(text[text_ptr] if text_ptr < len(text) else '\0')
			while (text_charint >= 48 and text_charint <= 57) or text_charint == 46:
				value += chr(text_charint)

				text_ptr += 1
				text_charint = ord(text[text_ptr] if text_ptr < len(text) else '\0')

			if text_charint != 0: text_ptr -= 1
			result_list.append((Other.Value, Decimal(value)))
		elif text_charint == 0:
			result_list.append((Other.ETX, '\0'))
			break
		else: result_list.append((Other.Unknown, chr(text_charint)))

		text_ptr += 1

	return result_list


if __name__ == "__main__":
	test_text: str = "(0123456789) + 20.4 * 4 / 7"
	print(Lexer(test_text))

from enum import Enum

class Operator(Enum):
	Plus = "+"
	Minus = "-"
	Multi = "*"
	Divide = "/"
	Modulo = "%"
	Pow = "^"

	Factorial = "!"

class MathKeyword(Enum):
	PI = "pi"
	E = "e"

	Sqrt = "sqrt"  # x
	Log10 = "log10"  # x
	Log = "log"  # x, base

	Sin = "sin"  # x
	Asin = "asin"  # x
	Cos = "cos"  # x
	Acos = "acos"  # x
	Tan = "tan"  # x
	Atan = "atan"  # x

	Permutation = "P"  # left, right
	Combination = "C"  # left, right

class Other(Enum):
	ValueMinus = 0
	Value = 1
	Comma = 2
	ETX = 3
	Unknown = 4

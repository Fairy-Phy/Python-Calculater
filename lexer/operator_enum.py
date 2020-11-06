from enum import Enum

class Operator(Enum):
	Plus = "+"
	Minus = "-"
	Multi = "*"
	Divide = "/"
	Modulo = "%"
	Pow = "^"

	Factorial = "!"

	LeftBracket = "("
	RightBracket = ")"

class MathKeyword(Enum):
	PI = "pi"
	E = "e"
	Euler = "euler"

	Sqrt = "sqrt"
	Log10 = "log10"
	Log = "log"

	Sin = "sin"
	Asin = "asin"
	Cos = "cos"
	Acos = "acos"
	Tan = "tan"
	Atan = "atan"

	Permutation = "P"
	Combination = "C"

class Other(Enum):
	ValueMinus = 0
	Value = 1
	ETX = 2
	Unknown = 3

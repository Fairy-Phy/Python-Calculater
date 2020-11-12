import math

def Permutation(left: float, right: float) -> float:
	return math.factorial(left) / math.factorial(left - right)

def Combination(left: float, right: float) -> float:
	return Permutation(left, right) / math.factorial(right)

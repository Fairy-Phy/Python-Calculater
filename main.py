# Copyright 2020 (Fairy)Phy

from calc_parser import Parser
from lexer import Lexer
import traceback


version: str = "0.2"
debug: bool = False

if __name__ == "__main__":
	print("Python Calculator Varsion", version)
	print()
	print("Please enter a formula.\nType \"help\" for check usage. \"exit\" for exit.")

	while True:
		formula_text = input("> ")

		if formula_text == "":
			print("Please enter a formula.")
		elif formula_text == "help":
			print("<Example>")
			print("log(3! * ((sqrt(3^2 / 3) / sin(pi / 3)) + 4) - 9, 3)")
			print("Result: 3.0")
			print("If there are brackets, they are calculated from the brackets first.")
			print()
			print("<Operator>")
			print("a+b -> Plus")
			print("a-b -> Minus")
			print("a*b -> Multi")
			print("a/b -> Divide")
			print("a%b -> Modulo")
			print("a^b -> Power")
			print("x! -> Factorial")
			print()
			print("<Math keyword>")
			print("pi -> return mathematical constant π = 3.141592...")
			print("e -> return mathematical constant e = 2.718281...")
			print("sqrt(x) -> return square root of x")
			print("log10(x) -> return base-10 logarithm of x")
			print("log(x, base) -> return logarithm of x to the given base")
			print("sin(x) -> return sine of x radians")
			print("cos(x) -> return cosine of x radians")
			print("tan(x) -> return tangent of x radians")
			print("asin(x) -> return arc sine of x, in radians. result is between -pi/2 and pi/2")
			print("acos(x) -> return arc cosine of x, in radians. result is between 0 and pi")
			print("atan(x) -> return arc tangent of x, in radians. result is between -pi/2 and pi/2")
			print("P(n, r) -> return permutation (nPr)")
			print("C(n, r) -> return combination (nCr)")
			pass
		elif formula_text == "exit":
			print("Bye")
			from time import sleep
			sleep(3)
			break
		elif formula_text == "debug":
			if debug:
				debug = False
				print("debug switched to False")
			else:
				debug = True
				print("debug switched to True")
		else:
			try:
				lexed_lists = Lexer(formula_text)
				if debug: print("lexed_lists:", lexed_lists)
				result = Parser(lexed_lists)
				print("Result:", result)
			except Exception as error:
				print("An error occurred during the calculation.")
				if debug: traceback.print_exc()
				else: print(error)


from typing import Callable

def precompute_truth_table( bits : int, logic_solve : Callable[ [str], str ] ) -> None:
	truth_table : dict = dict()
	total : int = (2 ** bits)
	total_bits = len(bin( total )[2:])
	for counter in range( total ):
		value : str = bin(counter)[2:]
		padding : str = '0' * (total_bits - len(value) - 1)
		binary : str = padding + value
		truth_table[binary] = logic_solve( binary )
	return truth_table

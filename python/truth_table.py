
from __future__ import annotations
from typing import Callable

def precompute_truth_table( in_bits : int, out_bits : int, logic_solve : Callable[ [str], str ] ) -> None:
	truth_table : dict = dict()
	total : int = (2 ** in_bits)
	total_bits = len(bin( total )[2:])
	for counter in range( total ):
		value : str = bin(counter)[2:]
		padding : str = '0' * (total_bits - len(value) - 1)
		binary : str = padding + value
		output : str = logic_solve( binary )
		if len(output) != out_bits:
			raise ValueError(f'Logic Solve did not return {out_bits} total bits!')
		truth_table[binary] = output
	return truth_table

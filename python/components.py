
from __future__ import annotations
from truth_table import precompute_truth_table

class Component:
	'''
	Individual inputs/outputs are separated by spaces.
	&N& represents the total bits, &B& represents a single bit.
	'''
	in_bits : int
	out_bits : int
	truth_table : dict[str, str]

	def __init__(self, bits : int) -> Component:
		self.in_bits = bits
		self.precompute_tt()

	def logic_solve( self, binary : str ) -> str:
		raise NotImplementedError

	def precompute_tt( self ) -> None:
		self.truth_table = precompute_truth_table( self.in_bits, self.out_bits, self.logic_solve )

	def calculate( self, binary : str ) -> str:
		output : str = self.truth_table.get(binary)
		assert output, 'Binary was not found in output truth table.'
		return output

class ANDComponent(Component):
	in_bits : int = 1
	out_bits : int = 1

	def logic_solve( self, binary : str ) -> str:
		if binary.find('0') == -1: return '1'
		return '0'

class ORComponent(Component):
	in_bits : int = 1
	out_bits : int = 1

	def logic_solve( self, binary : str ) -> str:
		if binary.find('1') != -1:
			return '1'
		return '0'

class NORComponent(Component):
	in_bits : int = 1
	out_bits : int = 1

	def logic_solve( self, binary : str ) -> str:
		if binary.find('1') == -1: return '1'
		return '0'

class XORComponent(Component):
	in_bits : int = 1
	out_bits : int = 1

	def logic_solve( self, binary : str ) -> str:
		if binary.find('0') != -1 and binary.find('1') != -1:
			return '1'
		return '0'

class NANDComponent(Component):
	in_bits : int = 1
	out_bits : int = 1

	def logic_solve( self, binary : str ) -> str:
		if binary == '1' * self.bits:
			return '1'
		return '0'

class XNORComponent(Component):
	in_bits : int = 1
	out_bits : int = 1

	def logic_solve( self, binary : str ) -> str:
		if binary == ('1' * self.bits) or binary == ('0' * self.bits):
			return '1'
		return '0'

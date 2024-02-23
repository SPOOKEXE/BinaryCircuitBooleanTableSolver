
from __future__ import annotations

class Component:
	'''
	Individual inputs/outputs are separated by spaces.
	[N] represents the total bits, [B] represents a single bit.
	'''
	bits : int
	inputs : str
	outputs : str
	truth_table : dict[str, str]

	def __init__(self, bits : int) -> Component:
		self.bits = bits
		self.precompute_truth_table()

	def logic_solve( self, binary : str ) -> str:
		raise NotImplementedError

	def precompute_truth_table( self ) -> None:
		self.truth_table = dict()
		total : int = 2 ** self.bits
		total_bits = len(bin( total )[2:])
		for counter in range( total ):
			value : str = bin(counter)[2:]
			padding : str = '0' * (total_bits - len(value) - 1)
			binary : str = padding + value
			self.truth_table[binary] = self.logic_solve( binary )

	def calculate( self, binary : str ) -> str:
		output : str = self.truth_table.get(binary)
		assert output, 'Binary was not found in output truth table.'
		return output

class ANDComponent(Component):
	bits : int = 1
	inputs : str = "[N]"
	outputs : str = "[B]"
	cost : int = 1

	def logic_solve( self, binary : str ) -> str:
		if binary.find('0') == -1: return '1'
		return '0'

class ORComponent(Component):
	bits : int = 1
	inputs : str = "&N&"
	outputs : str = "&B&"
	cost : int = 1

	def logic_solve( self, binary : str ) -> str:
		if binary.find('1') != -1:
			return '1'
		return '0'

class NORComponent(Component):
	bits : int = 1
	inputs : str = "&N&"
	outputs : str = "&B&"
	cost : int = 2

	def logic_solve( self, binary : str ) -> str:
		if binary.find('1') == -1: return '1'
		return '0'

class XORComponent(Component):
	bits : int = 1
	inputs : str = "&N&"
	outputs : str = "&B&"
	cost : int = 2

	def logic_solve( self, binary : str ) -> str:
		if binary.find('0') != -1 and binary.find('1') != -1:
			return '1'
		return '0'

class NANDComponent(Component):
	bits : int = 1
	inputs : str = "&N&"
	outputs : str = "&B&"
	cost : int = 2

	def logic_solve( self, binary : str ) -> str:
		if binary == '1' * self.bits:
			return '1'
		return '0'

class XNORComponent(Component):
	bits : int = 1
	inputs : str = "&N&"
	outputs : str = "&B&"
	cost : int = 2

	def logic_solve( self, binary : str ) -> str:
		if binary == ('1' * self.bits) or binary == ('0' * self.bits):
			return '1'
		return '0'

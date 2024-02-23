
from string import ascii_uppercase

def sum_of_products( truth_table : dict[str, str] ) -> tuple[int, str]:
	symbols : int = ascii_uppercase[:len(list(truth_table.keys())[0])]
	binops : list[str] = []
	for key in truth_table.keys():
		letters = [ ascii_uppercase[i] + (c == '0' and '\'' or '') for i, c in enumerate(key) ]
		# print(key, letters)
		value : str = ''.join(letters)
		if value.find("'") != -1:
			value = '(' + value + ')'
		binops.append( value )
	return symbols, ' + '.join(binops)

if __name__ == '__main__':

	items, boolean = sum_of_products({
		"0000" : "010",
		"0001" : "001",
		"0010" : "001",
		"0011" : "001",
		"0100" : "100",
		"0101" : "010",
		"0110" : "001",
		"0111" : "001",
		"1000" : "100",
		"1001" : "010",
		"1010" : "001",
		"1011" : "100",
		"1100" : "100",
		"1101" : "100",
		"1110" : "100",
		"1111" : "010",
	})

	print(items)
	print(boolean)


import numpy as np
import json
import re

from string import ascii_uppercase
from typing import Callable

def bin_to_bool_expression( binary_in : str ) -> str:
	items : list[str] = [ ascii_uppercase[i] if c == '1' else f'NOT({ascii_uppercase[i]})' for i, c in enumerate(binary_in) ]
	value : str = ' AND '.join(items)
	return binary_in == '1111' and value or f'{value}'

def truth_table_single_output( truth_table_rows : list[str], output : str ) -> list[str]:
	'''
	A | B | C | D | Z1
	------------------
	0 | 0 | 0 | 0 | 1
	0 | 0 | 0 | 1 | 0
	0 | 0 | 1 | 0 | 1

	truth_table_rows = ['0000', '0001', '0010']
	output = '101

	returns ["(A'B'C'D') AND NOT(A'B'C'D) AND (A'B'CD')", "",]
	'''
	expressions : list[str] = []
	for i, row in enumerate(truth_table_rows):
		expr : str = '(' + bin_to_bool_expression( row ) + ')'
		if output[i] == '0': expr = 'NOT' + expr
		expressions.append(expr)
	return expressions

def truth_table_multi_output( truth_table_rows : list[str], outputs : list[str] ) -> list[list[str]]:
	'''
	A | B | C | D | Z1 | Z2
	-----------------------
	0 | 0 | 0 | 0 | 1  | 1
	0 | 0 | 0 | 1 | 0  | 0
	0 | 0 | 1 | 0 | 1  | 0

	truth_table_rows = ['0000', '0001', '0010']
	outputs = ['101', '100']

	RETURNS [
		[
			'NOT(A) AND NOT(B) AND NOT(C) AND NOT(D)',
			'NOT(NOT(A) AND NOT(B) AND NOT(C) AND D)',
			'NOT(A) AND NOT(B) AND C AND NOT(D)'
		],
		[
			'NOT(A) AND NOT(B) AND NOT(C) AND NOT(D)',
			'NOT(NOT(A) AND NOT(B) AND NOT(C) AND D)',
			'NOT(NOT(A) AND NOT(B) AND C AND NOT(D)'
		]
	]
	'''
	cache : dict[str, str] = dict()
	for row in truth_table_rows:
		if cache.get(row) != None: continue
		expr : str = '' + bin_to_bool_expression( row ) + ''
		cache[row] = expr
	completed : list[str] = list()
	for output in outputs:
		compiled : list[str] = list()
		for index, char in enumerate(output):
			row : str = truth_table_rows[index]
			expr = cache.get(row)
			if char == '0': expr = 'NOT(' + expr + ')'
			compiled.append(expr)
		completed.append( compiled )
	return completed

PARENTHESIS_VALUE_REGEX = r'\(([^)]+)'

SIMPLIFY_REGEX_TUPLES : tuple[ str, Callable[[tuple], str], Callable[[tuple], str] ] = [
	(
		# NOT(NOT(*)) -> (*)
		r'NOT\(NOT\((.*?)\)\)',
		lambda values : ''.join(values),
		lambda value : re.match(r'(?<=NOT\()NOT\(([A-Z])\)(?=\))', value) or re.match(r'NOT\(NOT\((.)\) AND NOT\((.)\)\)', value) != None
	),
	(
		# NOT(A) AND NOT(B) AND NOT(C) -> NOT(A OR B OR C)
		r'(?<=NOT\()[A-Z](?=\))',
		lambda values : 'NOT(' + (' OR '.join(values)) + ')',
		lambda value : re.fullmatch(r'(?<=NOT\()[A-Z](?=\))', value) or re.match(r'NOT\(NOT\((.)\) AND NOT\((.)\)\)', value) != None
	),
	(
		# NOT(NOT(A) AND NOT(B) AND NOT(C) AND NOT(D)) -> NOT( NOT(A OR B) ) -> (A OR B) # IGNORE NOT(NOT(*)) PART
		r'(?<=NOT\()[A-Z](?=\))',
		lambda values : ' OR '.join(values), # skip the NOT( NOT( * ) ) step
		lambda value : re.match(r'NOT\(NOT\((.)\) AND NOT\((.)\)\)', value)
	),
	(
		# NOT(A AND NOT(B)) -> NOT(A) OR B
		r'NOT\((.) AND NOT\((.)\)\)',
		lambda values : f'NOT({values[0]}) OR {values[1]}',
		lambda value : re.match( r'NOT\([A-Za-z]\sAND\sNOT\([A-Za-z]\)\)', value )
	),
	(
		# NOT(NOT(A) AND B) -> A OR NOT(B)
		r'NOT\(NOT\((.)\) AND (.)\)',
		lambda values : f'{values[0]} OR NOT({values[1]})',
		lambda value : re.match( r'NOT\(NOT\([A-Za-z]\)\sAND\s[A-Za-z]\)', value )
	),
	(
		# NOT(NOT(A) AND NOT(B) AND NOT(C) AND NOT(D) AND NOT(E)) -> (A OR B OR C OR D OR E)
		r'(?<=NOT\(NOT\()[A-E](?=\))',
		lambda values : ' OR '.join(values),
		lambda value : re.match(r'NOT\(NOT\([A-Z]\)(?:\sAND\sNOT\([A-Z]\))+\)', value)
	),
]

def simplify_boolean_operation( boolean_op : str ) -> str:
	# keep repeating until no simplifications can occur
	# print(boolean_op)
	hasSimplified = True
	while hasSimplified == True:
		hasSimplified = False
		for regex, transform, blacklist in SIMPLIFY_REGEX_TUPLES:
			# print(regex)
			if blacklist != None and blacklist(boolean_op) == True:
				continue # ignore
			# print( boolean_op )
			matches : list[re.Match] = [ v for v in re.finditer( regex, boolean_op ) ]
			if len(matches) == 0:
				continue # no matches
			# print(matches)
			# print(regex, matches)
			if len(matches) > 1:
				value : list[str] = [ value.group(0) for value in matches ]
			else:
				value : list[str] = matches[0].groups()
			hasSimplified = True
			output : str = transform( value )
			print(value, '->', output)
			start : int = matches[0].pos
			finish : int = matches[-1].endpos
			boolean_op = boolean_op[:start] + output + boolean_op[finish:]
	return boolean_op

def simplify_truth_table( values : list[str] ) -> list[str]:
	return [ simplify_boolean_operation(value) for value in values ]

def simplify_multi_dim_truth_table( value : list[list[str]] ) -> list[list[str]]:
	output = simplify_truth_table( np.array(value).flatten().tolist() )
	output = np.array(output)
	output = output.reshape( np.shape(value) ).tolist()
	return output

def calculate_operations( value : str ) -> int:
	OPS = ['AND', 'NOT', 'OR', 'NAND', 'XOR', 'XNOR', 'NOR']
	total : int = 0
	for item in OPS:
		total += value.count(item)
	return total

if __name__ == '__main__':
	value1 = 'NOT(A) AND NOT(B) AND NOT(C) AND NOT(D)'
	print( value1, '>>', simplify_boolean_operation( value1 )  )
	value2 = 'NOT(A) AND NOT(B)'
	print( value2, '>>', simplify_boolean_operation( value2 )  )
	value3 = 'NOT(NOT(A OR B))'
	print( value3, '>>', simplify_boolean_operation( value3 )  )
	value4 = 'NOT(NOT(A) AND NOT(B))'
	print( value4, '>>', simplify_boolean_operation( value4 )  )
	value5 = 'NOT(A AND NOT(B))'
	print( value5, '>>', simplify_boolean_operation( value5 )  )
	value6 : str = 'NOT(NOT(A) AND NOT(B) AND NOT(C))'
	print( value6, '>>', simplify_boolean_operation( value6 )  )

	# test = truth_table_multi_output(['00', '01', '10', '11'], ['0100', '1001', '0010'])
	# print( 'BEFORE SIMPLIFY: ', json.dumps(test, indent=4) )
	# print( calculate_operations( str(test) ) )
	# test = simplify_multi_dim_truth_table( test )
	# print( 'AFTER SIMPLIFY: ', json.dumps(test, indent=4) )
	# print( calculate_operations( str(test) ) )

	# test2 = truth_table_multi_output(['000', '001', '010', '011', '100', '101', '110', '111'], ['00100111'])
	# print( 'BEFORE SIMPLIFY: ', json.dumps(test2, indent=4) )
	# print( calculate_operations( str(test2) ) )
	# test2 = simplify_multi_dim_truth_table( test2 )
	# print( 'AFTER SIMPLIFY: ', json.dumps(test2, indent=4) )
	# print( calculate_operations( str(test2) ) )

	pass

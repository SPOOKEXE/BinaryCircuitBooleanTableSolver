
# use chat-gpt for REGEX PATTERNS
# https://chat.openai.com/c/41e7b086-9f66-4af0-9029-49d6e8d8b660

# also add a better method of testing (such as calculating the actual outputs then assertions/warns)

import numpy as np
import json
import re

from string import ascii_uppercase
from typing import Callable
from dataclasses import dataclass

def bin_to_bool_expression( binary_in : str ) -> str:
	items : list[str] = [ ascii_uppercase[i] if c == '1' else f'NOT({ascii_uppercase[i]})' for i, c in enumerate(binary_in) ]
	value : str = ' AND '.join(items)
	return binary_in == '1111' and value or f'{value}'

def truth_table_single_output( truth_table_rows : list[str], output : str ) -> list[str]:
	'''
	A | B | C | D | Z
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

def truth_table_multi_output( truth_table_rows : list[str], outputs : list[str] ) -> tuple[ list[list[str]], dict[str, str] ]:
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
	return completed, cache

PARENTHESIS_VALUE_REGEX = r'\(([^)]+)'

@dataclass
class BoolRegexSimplifier:
	regex : str
	transform : Callable[ [list[str]], str ]
	blacklist : Callable[ [str], bool ] | None = None

SIMPLIFY_REGEX_TUPLES : list[ BoolRegexSimplifier ] = [
	# NOT(NOT(*)) -> (*)
	BoolRegexSimplifier(
		regex = r'NOT\(NOT\((\w+)\)\)',
		transform = lambda values : ''.join(values),
		blacklist = lambda value : re.match(r'(?<=NOT\()NOT\(([A-Z])\)(?=\))', value) == None
	),
	# NOT(NOT(A) AND NOT(B) AND ...)
	BoolRegexSimplifier(
		regex = 	r'(?<=NOT\()[A-Z](?=\))',
		transform = lambda values : ' OR '.join(values),
		blacklist = lambda value : re.match(r'NOT\(NOT\([A-Z]\) AND NOT\([A-Z]\)(?: AND NOT\([A-Z]\))*\)', value) == None
	),
	# NOT(A) AND NOT(B) AND NOT(C) -> NOT(A OR B OR C)
	BoolRegexSimplifier(
		regex = r'(?<=NOT\()\w(?=\))',
		transform = lambda values : 'NOT(' + (' OR '.join(values)) + ')',
		blacklist = lambda value : re.match(r'NOT\([A-Z]\)(?:\s+AND\s+NOT\([A-Z]\))*', value) == None,
	),
	# NOT(A AND NOT(B)) -> NOT(A) OR B
	BoolRegexSimplifier(
		regex = r'NOT\((\w+) AND NOT\((\w+)\)\)',
		transform = lambda values : f'NOT({values[0]}) OR {values[1]}',
		blacklist = lambda value : re.match( r'NOT\((\w+) AND NOT\((\w+)\)\)', value ) == None,
	),
	# NOT(NOT(A) AND B) -> A OR NOT(B)
	BoolRegexSimplifier(
		regex = r'NOT\(NOT\((\w+)\) AND (\w+)\)',
		transform = lambda values : f'{values[0]} OR NOT({values[1]})',
		blacklist = lambda value : re.match( r'NOT\(NOT\((\w+)\) AND (\w+)\)', value ) == None,
	)
]

def simplify_boolean_operation( boolean_op : str ) -> str:
	hasSimplified = True
	while hasSimplified == True:
		hasSimplified = False
		for regexSimplifier in SIMPLIFY_REGEX_TUPLES:
			if regexSimplifier.blacklist != None and regexSimplifier.blacklist(boolean_op) == True: continue
			matches : list[re.Match] = [ v for v in re.finditer( regexSimplifier.regex, boolean_op ) ]
			if len(matches) == 0: continue
			if len(matches) > 1:
				value : list[str] = [ value.group(0) for value in matches ]
			else:
				value : list[str] = matches[0].groups()
				if len(value) == 0: return matches[0].string
			hasSimplified = True
			boolean_op = boolean_op[:matches[0].pos] + regexSimplifier.transform( value ) + boolean_op[matches[-1].endpos:]
	return boolean_op

def simplify_truth_table( values : list[str] ) -> list[str]:
	return [ simplify_boolean_operation(value) for value in values ]

def simplify_multi_dim_truth_table( value : list[list[str]] ) -> list[list[str]]:
	print( np.shape(value) )
	output : list[ str ] = simplify_truth_table( np.array(value).flatten().tolist() )
	#output : list[str] = [ v.replace('NOT', 'NAND') for v in output ]
	output = np.reshape( output, np.shape(value) ).tolist()
	return output

def calculate_operations( value : str ) -> int:
	OPS = ['AND', 'OR', 'NOT', 'XOR', 'XNOR', 'NOR']
	# for operation in OPS:
	# 	print( operation, value.count(operation), value )
	total : int = 0
	for item in OPS:
		index : int = str.find(value, item)
		while index != -1:
			total += 1
			index : int = value.find(item, index + len(item))
	return total

def run_test() -> None:
	TEST_BRANCHES : dict[str, str] = {
		'NOT(A) AND NOT(B) AND NOT(C) AND NOT(D)' : 'NOT(A OR B OR C OR D)',
		'NOT(A) AND NOT(B)' : 'NOT(A OR B)',
		'NOT(NOT(A OR B))' : 'NOT(NOT(A OR B))',
		'NOT(NOT(A) AND NOT(B))' : 'A OR B',
		'NOT(A AND NOT(B))' : 'NOT(A) OR B',
		'NOT(NOT(A) AND NOT(B) AND NOT(C))' : 'A OR B OR C',
		'NOT(NOT(A) AND B)' : 'A OR NOT(B)'
	}
	for inp, exp in TEST_BRANCHES.items():
		try: out : str = simplify_boolean_operation( inp )
		except: out : str = 'failed'
		if exp==out:
			print('Condition Passed: ', inp, '->', out)
		else:
			print('Condition Failed:', inp, 'GOT', out, 'EXPECTING', exp )
	for bulk, simple in TEST_BRANCHES.items():
		print('OPS:', calculate_operations( bulk ), '->', calculate_operations( simple ))
	print('TOTAL OPS:', calculate_operations( ' '.join(list(TEST_BRANCHES.keys())) ), '->', calculate_operations( ' '.join(list(TEST_BRANCHES.values())) ) )

if __name__ == '__main__':
	run_test()

	test = truth_table_multi_output(['00', '01', '10', '11'], ['0100', '1001', '0010'])
	print( 'BEFORE SIMPLIFY: ', json.dumps(test, indent=4) )
	print( calculate_operations( str(test) ) )
	test = simplify_multi_dim_truth_table( test )
	print( 'AFTER SIMPLIFY: ', json.dumps(test, indent=4) )
	print( calculate_operations( str(test) ) )

	# test1, mapped1 = truth_table_multi_output(['000', '001', '010', '011', '100', '101', '110', '111'], ['00100111'])
	# print( json.dumps(mapped1, indent=4) )
	# print( 'BEFORE SIMPLIFY: ', json.dumps(test1, indent=4) )
	# print( calculate_operations( str(test1) ) )
	# test2 = simplify_multi_dim_truth_table( test1 )
	# print( 'AFTER SIMPLIFY: ', json.dumps(test2, indent=4) )
	# print( calculate_operations( str(test2) ) )

	pass

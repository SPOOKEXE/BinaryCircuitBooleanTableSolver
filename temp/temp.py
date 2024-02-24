
# class BooleanLaws:

# 	@staticmethod
# 	def simplify_double_negations(expr : str) -> str:
# 		'''Removes ~(~ and ~~ expressions as they cancel out.'''
# 		expr = expr.replace("~(~", "")
# 		expr = expr.replace("~~", "")
# 		return expr

# 	@staticmethod
# 	def apply_absorption_laws_negation(expr : str) -> str:
# 		'''Simplfy "A | (~B & A)" and "A | (A & ~B)" expressions to the left-most character.'''
# 		# B | (~A & B) >> B
# 		regex_pattern = r'[A-Za-z]\s*\|\s*\(~[A-Za-z]\s*&\s*[A-Za-z]\)'
# 		if re.match(regex_pattern, expr) != None:
# 			return expr.split('|')[0].strip()
# 		# B | (B & ~A) >> B
# 		pattern = r'(\w)\s*\|\s*\(\1\s*&\s*~\w\)'
# 		simplified_expression = re.sub(pattern, r'\1', expr)
# 		return simplified_expression

# 	@staticmethod
# 	def apply_identity_laws(expr : str) -> str:
# 		'''Identity Law:
# 		1. A | 0 = A
# 		2. A & 1 = A
# 		'''
# 		return expr.replace("|0", "").replace("&1", "")

# 	@staticmethod
# 	def apply_domination_laws(expr : str) -> str:
# 		'''Domination Law:
# 		1. A | 1 = 1
# 		2. A & 0 = 0
# 		'''
# 		return expr.replace("|1", "1").replace("&0", "0")

# 	@staticmethod
# 	def apply_expansion(expr : str) -> str:
# 		'''Apply parenthesis expansion:
# 		(~A|B) & (A|B) >> (B|B) & (A|B) & (A|~A) & (B|~A)
# 		'''
# 		pattern : str = '\((.+)[|](.+)\)&\((.+)[|](.+)\)'
# 		try:
# 			items : list[str] = list(re.findall(pattern, expr)[0]) # can raise
# 			return re.sub( pattern, lambda _ : f'({ items[1] }&{ items[1] }) | ({ items[2] }&{ items[1] }) | ({items[2] }&{ items[0] }) | ({ items[1] }&{ items[0] })', expr )
# 		except:
# 			return expr

# 	@staticmethod
# 	def simplify_idempotent(expr : str) -> str:
# 		'''Idempotent Law:
# 		1. X | X = X
# 		2. X & X = X
# 		'''
# 		idempotent_pattern : str = r'([A-Za-z])\s*([&|])\s*\1'
# 		simplified_expression : str = re.sub(idempotent_pattern, r'\1', expr)
# 		return simplified_expression

# 	@staticmethod
# 	def apply_complement_law(expr : str) -> str:
# 		'''Complement Law:
# 		1. X + ~X = 1
# 		2. X & ~X = 0
# 		'''
# 		idempotent_pattern : str = r'^([A-Za-z])\s*[|&]\~\1|\1$'
# 		return re.sub(idempotent_pattern, r'\1', expr)

# 	@staticmethod
# 	def remove_single_parentheses(expr : str) -> str:
# 		'''Removes parenthesis around single character expressions.'''
# 		pattern : str = r'\((\w)\)'
# 		return re.sub(pattern, r'\1', expr)

# 	@staticmethod
# 	def apply_absorption_laws_normal(expr : str) -> str:
# 		'''
# 		Absorption Law:
# 		1. A|(A&B) >> A
# 		2. A|(B&A) >> A
# 		3. B|(B&A) >> B
# 		4. B|(A&B) >> B
# 		'''
# 		pattern : str = r'(\w)\s*\|\s*\((?:\1&(\w)|(\w)&\1)\)'
# 		return re.sub(pattern, r'\1', expr)

# 	@staticmethod
# 	def apply_unknown_combining_theorom(expr : str) -> str: # TODO
# 		'''SOMETHING LAW:
# 		1. A
# 		2. B
# 		'''
# 		filter_pattern : str = r'~\([A-Za-z&~()]+\)'
# 		if not re.fullmatch( filter_pattern, expr ): return expr
# 		regex_pattern = r'~?[A-Za-z]'
# 		try:
# 			matches = re.findall(regex_pattern, expr)
# 			return '&'.join([f'(~{v})' for v in matches])
# 		except: return expr

# class BooleanSimplifier:

# 	@staticmethod
# 	def simplify_boolean_expression(expr : str) -> str:
# 		expr = expr.replace(" ", "")
# 		expr = BooleanLaws.apply_expansion(expr)
# 		prev_expr : str = None
# 		while prev_expr != expr:
# 			prev_expr : str = expr
# 			expr = BooleanLaws.simplify_idempotent(expr)
# 			expr = BooleanLaws.simplify_double_negations(expr)
# 			expr = BooleanLaws.apply_absorption_laws_negation(expr)
# 			expr = BooleanLaws.apply_absorption_laws_normal(expr)
# 			expr = BooleanLaws.apply_identity_laws(expr)
# 			expr = BooleanLaws.apply_domination_laws(expr)
# 			expr = BooleanLaws.apply_complement_law(expr)
# 			expr = BooleanLaws.simplify_idempotent(expr)
# 			expr = BooleanLaws.remove_single_parentheses(expr)
# 			expr = BooleanLaws.apply_unknown_combining_theorom(expr)
# 			expr = expr.replace(' ', '') # remove un-needed spaces
# 		return expr

# def run_test() -> None:
# 	TEST_BRANCHES : dict[str, str] = {
# 		'(~A)&(~B)&(~C)&(~D)' : '~(A|B|C|D)', # TODO
# 		'~A & ~B' : '~(A | B)', # TODO
# 		'~(~(A | B))' : '~(~(A | B))', # TODO FIX THIS (leaves parenthesis on the right)
# 		'~(~(A) & ~(B))' : 'A | B',  # TODO FIX THIS (leaves parenthesis on the right)
# 		'~(A & ~(B))' : '~(A) | B',
# 		'~(~(A) & ~(B) & ~(C))' : 'A | B | C', # TODO SHOULD BE "A&~B&~C" BUT GIVES "A&~B&~C)""
# 		'~(~A & B)' : 'A | ~(B)' # TODO SHOULD BE "A|~B" BUT GIVES "A&B)"
# 	}
# 	for inp, exp in TEST_BRANCHES.items():
# 		try:
# 			out : str = simplify_boolean_expression( inp )
# 		except:
# 			out : str = 'failed'
# 		print(inp, '->', out)
# 		# if exp==out:
# 		# 	print('Condition Passed: ', inp, '->', out)
# 		# else:
# 		# 	print('Condition Failed:', inp, 'GOT', out, 'EXPECTING', exp )

# if __name__ == '__main__':
# 	run_test()
# 	pass

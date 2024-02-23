
import re

def simplify_boolean_expression(expression):
	# Remove white spaces for ease of processing
	expression = expression.replace(" ", "")

	# Helper function to apply De Morgan's laws
	def apply_demorgans_laws(expr):
		expr = expr.replace("~(~", "")
		expr = expr.replace("~~", "")
		return expr

	# Helper function to simplify double negations
	def simplify_double_negations(expr):
		return expr.replace("~~", "")

	# Helper function to apply absorption law
	def apply_absorption_laws(expr):
		# B | (~A & B) >> B
		regex_pattern = r'[A-Za-z]\s*\|\s*\(~[A-Za-z]\s*&\s*[A-Za-z]\)'
		if re.match(regex_pattern, expression) != None:
			return expression.split('|')[0].strip()
		# B | (B & ~A) >> B
		pattern = r'(\w)\s*\|\s*\(\1\s*&\s*~\w\)'
		simplified_expression = re.sub(pattern, r'\1', expression)
		return simplified_expression

	# Helper function to apply identity law
	def apply_identity_laws(expr):
		# Identity law: A | 0 = A
		expr = expr.replace("|0", "")
		# Identity law: A & 1 = A
		expr = expr.replace("&1", "")
		return expr

	# Helper function to apply domination law
	def apply_domination_laws(expr):
		# Domination law: A | 1 = 1
		expr = expr.replace("|1", "1")
		# Domination law: A & 0 = 0
		expr = expr.replace("&0", "0")
		return expr

	# Helper function to expand expression
	def apply_expansion(expr):
		# (~A|B)&(A|B) >> ['~A', 'B', 'A', 'B']
		# BECOMES (B|B) & (A|B) & (A|~A) & (B|~A)
		pattern = '\((.+)[|](.+)\)&\((.+)[|](.+)\)'
		try:
			items : list[str] = list(re.findall(pattern, expr)[0])
			return re.sub( pattern, lambda _ : f'({ items[1] }&{ items[1] }) | ({ items[2] }&{ items[1] }) | ({items[2] }&{ items[0] }) | ({ items[1] }&{ items[0] })', expr )
		except:
			return expr

	def simplify_idempotent(expression):
		# Define regex pattern for idempotent simplification
		idempotent_pattern = r'([A-Za-z])\s*([&|])\s*\1'
		# Apply the regex pattern to simplify the expression
		simplified_expression = re.sub(idempotent_pattern, r'\1', expression)
		return simplified_expression

	def apply_complement_law(expression):
		# Define regex pattern for complement law
		complement_pattern = r'\(([A-Za-z])&~\1\)'
		# Apply the regex pattern to remove complementary pairs
		simplified_expression = re.sub(complement_pattern, '0', expression)
		return simplified_expression

	def remove_parentheses(expression):
		# Define regex pattern to remove parentheses around single character expressions
		pattern = r'\((\w)\)'
		# Replace matches with the single character expression
		simplified_expression = re.sub(pattern, r'\1', expression)
		return simplified_expression

	def simplify_expression(expression):
		# Define regex pattern to find and simplify the expression
		pattern = r'(\w)\s*\|\s*\((?:\1&(\w)|(\w)&\1)\)'
		# Replace matches with the character found on the far left
		simplified_expression = re.sub(pattern, r'\1', expression)
		return simplified_expression

	def apply_morgans_theorom(expression):
		if not re.fullmatch( r'~\([A-Za-z&~()]+\)', expression ):
			return expression
		regex_pattern = r'~?[A-Za-z]'
		# Find all matches
		try:
			matches = re.findall(regex_pattern, expression)
			return '&'.join([f'(~{v})' for v in matches])
		except:
			return expression

	# Apply simplification rules iteratively until the expression stops changing
	print(expression)
	expression = apply_expansion(expression)
	print(expression)

	prev_expr = None
	while prev_expr != expression:
		prev_expr = expression
		expression = simplify_idempotent(expression)
		expression = apply_demorgans_laws(expression)
		expression = simplify_double_negations(expression)
		expression = apply_absorption_laws(expression)
		expression = apply_identity_laws(expression)
		expression = apply_domination_laws(expression)
		expression = apply_complement_law(expression)
		expression = simplify_expression(expression)
		expression = remove_parentheses(expression)
		expression = apply_morgans_theorom(expression)
		expression = expression.replace(' ', '')
		print(expression)
	return expression

# Example usage:
expression = "~(A & B & ~(C) & ~(D) & E)"
simplified_expression = simplify_boolean_expression(expression)
print("Original expression:", expression)
print("Simplified expression:", simplified_expression)

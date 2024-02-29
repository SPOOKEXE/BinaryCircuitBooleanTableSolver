from pyeda.inter import expr, expr2truthtable, expr


# Define the boolean expression
expression = expr("(A & B) | (A & C) | (B & C)").simplify()
print(expression)

print( expr2truthtable(expression) )

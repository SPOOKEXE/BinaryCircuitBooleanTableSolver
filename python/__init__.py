
from components import ANDComponent, ORComponent, NORComponent, XORComponent, NANDComponent, XNORComponent
from bool_logic import BooleanConverter

test : str = ANDComponent(5)
print(test.truth_table)

bool_expr : dict[str, str] = BooleanConverter.truth_table_to_boolean(test.truth_table)
print( bool_expr )


import json

from components import ANDComponent, ORComponent, NORComponent, XORComponent, NANDComponent, XNORComponent

n = ANDComponent(5)
print( json.dumps(n.truth_table, indent=4) )

# test, mapped = truth_table_multi_output(list(n.truth_table.keys()), [ ''.join(n.truth_table.values()) ])
# print( json.dumps(test, indent=4) )

# test2 = simplify_multi_dim_truth_table( test )
# print( json.dumps(test2, indent=4) )

# print( calculate_operations(str(test)), '->', calculate_operations(str(test2)) )

# test = truth_table_multi_output(['00', '01', '10', '11'], ['0100', '1001', '0010'])


from components import ANDComponent, ORComponent, NORComponent, XORComponent, NANDComponent, XNORComponent
from truth_table import sum_of_products

n = XNORComponent(5)

print( sum_of_products( n.truth_table ) )

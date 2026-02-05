
from fix import quicksort
result = quicksort([3, 6, 8, 10, 1, 2, 1])
expected = [1, 1, 2, 3, 6, 8, 10]
assert result == expected, f"Got {result}"
print('QUICKSORT PASSED')

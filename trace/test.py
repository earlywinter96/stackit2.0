def ArrayChallenge(arr):
    if len(arr) < 2:
        return -1  # Not enough elements to determine a pattern

    is_arithmetic = True
    is_geometric = True

    diff = arr[1] - arr[0]
    ratio = arr[1] / arr[0] if arr[0] != 0 else None

    for i in range(1, len(arr)):
        if arr[i] - arr[i-1] != diff:
            is_arithmetic = False
        if arr[i-1] == 0 or arr[i] / arr[i-1] != ratio:
            is_geometric = False

    if is_arithmetic:
        return "Arithmetic"
    elif is_geometric:
        return "Geometric"
    else:
        return -1


# Test cases
print(ArrayChallenge([2, 4, 6, 8]))         # Arithmetic
print(ArrayChallenge([2, 6, 18, 54]))       # Geometric
print(ArrayChallenge([1, 2, 4, 8, 16]))     # Geometric
print(ArrayChallenge([3, 6, 9, 12]))        # Arithmetic
print(ArrayChallenge([1, 2, 4, 7]))         # -1
print(ArrayChallenge([-2, -4, -6, -8]))     # Arithmetic
print(ArrayChallenge([-2, 6, -18, 54]))     # Geometric
print(ArrayChallenge([5]))                 # -1 (not enough elements)
print(ArrayChallenge([2, 4, 8, 16, 33]))    # -1

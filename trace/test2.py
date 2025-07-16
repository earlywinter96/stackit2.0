def FirstFactorial(num):
    # __define-ocg__ Recursive approach to calculate factorial
    if num == 1:
        return 1
    else:
        return num * FirstFactorial(num - 1)

# Test cases
print(FirstFactorial(input))   # Output: 24
#print(FirstFactorial(8))   # Output: 40320

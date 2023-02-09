def isPerfectNumber(value):
  result = True
  for x in range(value):
    divider = x + 1
    if (divider > 1 and divider < value and value % divider == 0):
      result = False
  return result

def isPalindrom(value):
  result = True
  length = len(value)
  for x in range(length):
    if not (value[x] == value[length - x - 1]):
      result = False
    if (x > length / 2): # optimization to only go through half of the string
      break
  return result
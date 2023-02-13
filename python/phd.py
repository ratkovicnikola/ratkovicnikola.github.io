import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from operator import itemgetter
import sys

# xInput = [0.06,0.08,0.1,0.12,0.14,0.16,0.18,0.2,0.24,0.28,0.32,0.36,0.4,0.44,0.48,0.52,0.56,0.6,0.64,0.68,0.72,0.76,0.8,0.82,0.84,0.86,0.88,0.9,0.92]
# yInput = [0.9452,0.7306,0.6237,0.4570,0.3858,0.2874,0.2044,0.1393,0.0187,-0.1101,-0.2288,-0.2921,-0.3609,-0.3840,-0.3970,-0.3901,-0.3613,-0.3328,-0.2796,-0.2031,-0.0835,0.1281,0.3096,0.3788,0.4540,0.5625,0.6848,0.8332,0.9311]

def getPolynomialValue(x, coefficients, power):
  result = 0
  for i in range(power + 1):
    result += pow(x, power - i) * coefficients[i]
  return result

def getPolynomialText(coefficients, power):
  result = ''
  for i in range(power + 1):
    coeff = str(round(coefficients[i], 4)) if coefficients[i] < 0 else '+' + str(round(coefficients[i], 4))
    if (i == power):
      result += coeff
    else:
      result += coeff + 'x^' + str(power - i)

  result = result[1:] if result[0] == '+' else result
  result = result.replace('^1', '')
  result = result.replace('^2', '\u00b2')
  result = result.replace('^3', '\u00b3')
  return result

def getCoefficientText(power, value):
  valueString = str(round(value, 4))
  if (power == 1):
    return 'R=' + valueString
  elif (power == 2):
    return 'R\u00b2=' + valueString
  elif (power == 3):
    return 'R\u00b3=' + valueString
  else:
    return ''

def calculateYAxis(xArray, yArray, power):
  coefficients = np.polyfit(xArray, yArray, power)
  for i in range(power + 1):
    print(coefficients[i], i)
  result = []
  for i in range(len(xArray)):
    value = xArray[i]
    if (power > 0):
      result.append(getPolynomialValue(value, coefficients, power))
    else:
      result = None
  d = dict()
  d['coeff'] = coefficients
  d['yResult'] = result
  return d

if (len(sys.argv) != 3):
  print('Please input x and y values as command arguments')
else:
  args1 = sys.argv[1].split(',')
  args2 = sys.argv[2].split(',')

  try:
    xInput = list(map(float, args1))
    yInput = list(map(float, args2))

    if (len(xInput) == len(yInput)):
      power = 2
      calcResult = calculateYAxis(xInput, yInput, power)
      yResult, coeff = itemgetter('yResult', 'coeff')(calcResult)

      yInputCor = pd.Series(yInput)
      yResultCor = pd.Series(yResult)
      correlation = yInputCor.corr(yResultCor)
      print('coeff=', pow(correlation, power))

      polynomial = np.poly1d(coeff)
      x_axis = np.linspace(0, 2, 1)
      y_axis = polynomial(x_axis)

      text = getPolynomialText(coeff, power) + '\n' + getCoefficientText(power, correlation)

      plt.title('y = ' + text)
      plt.plot(x_axis, y_axis)
      plt.plot( xInput, yInput, 'go', label='Input values' )
      plt.plot( xInput, yResult, label='Function values' )
      plt.legend(loc='upper center')
      plt.grid(True)
      plt.show()
    else:
      print('X and Y values are not the same length')
  except Exception as err:
    print(err)
    print('Please input only numbers')
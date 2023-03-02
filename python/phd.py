import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import math

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
    coefficient = str(round(coefficients[i], 4)) if coefficients[i] < 0 else '+' + str(round(coefficients[i], 4))
    if (i == power):
      result += coefficient
    else:
      result += coefficient + 'x^' + str(power - i)

  result = result[1:] if result[0] == '+' else result
  result = result.replace('^1', '')
  result = result.replace('^2', '\u00b2')
  result = result.replace('^3', '\u00b3')
  return 'y = ' + result

def getCorrelationText(value):
  valueString = str(round(value, 4))
  return 'R\u00b2=' + valueString

def calculateY(xInput, power, polynomialCoefficients):
  result = []
  for i in range(len(xInput)):
    value = xInput[i]
    if (power > 0):
      result.append(getPolynomialValue(value, polynomialCoefficients, power))
    else:
      result = None
  return result

def showPlot(title, xInput, yInput, yResult):
  plt.title(title)
  plt.plot(xInput, yInput, 'go', label='Input values' )
  plt.plot(xInput, yResult, label='Function values' )
  plt.legend(loc='upper center')
  plt.grid(True)
  plt.show()

def showSubplots(title1, title2, xInput1, yInput1, yResult1, xInput2, yInput2, yResult2, isPartialWinner, rightModel):
  fig, axs = plt.subplots(1, 2, constrained_layout=True)
  suptitlePrefix = 'Right ' if rightModel else 'Left '
  fig.suptitle(suptitlePrefix + 'partial and adsorption model')
  axs[0].plot(xInput1, yInput1, 'go', label='Input values' )
  axs[0].plot(xInput1, yResult1, label='Function values' )
  axs[0].set_title(title1 + ' (winner)' if isPartialWinner else title1)
  axs[1].plot(xInput2, yInput2, 'go', label='Input values' )
  axs[1].plot(xInput2, yResult2, label='Function values' )
  axs[1].set_title(title2 if isPartialWinner else title2 + ' (winner)')
  plt.show()

def calculateDualModel(xInput, yInput):
  power = 2
  polynomialCoefficients = np.polyfit(xInput, yInput, power)
  yResult = calculateY(xInput, power, polynomialCoefficients)
  correlationCoefficient = pd.Series(yInput).corr(pd.Series(yResult)) * pd.Series(yInput).corr(pd.Series(yResult)) # R^2
  title = getPolynomialText(polynomialCoefficients, power) + '\n' + getCorrelationText(correlationCoefficient)
  showPlot(title, xInput, yInput, yResult)

def getSlicedModelXInput(xInput, resultLength, isPartial):
  if (isPartial):
    return xInput[0:resultLength]
  else:
    result = []
    for i in range(len(xInput)):
      if (i < resultLength):
        result.append(math.log10(xInput[i]))
    return result

def calculateSlicedModel(xInput, yInput, resultLength, isPartial):
  xInputNew = getSlicedModelXInput(xInput, resultLength, isPartial)
  power = 1
  yInputNew = yInput[0:resultLength]
  polynomialCoefficients = np.polyfit(xInputNew, yInputNew, power)
  yResult = calculateY(xInputNew, power, polynomialCoefficients)
  correlationCoefficient = pd.Series(yInputNew).corr(pd.Series(yResult)) * pd.Series(yInputNew).corr(pd.Series(yResult)) # R^2

  d = dict()
  d['correlationCoefficient'] = correlationCoefficient
  d['xInputNew'] = xInputNew
  d['yInputNew'] = yInputNew
  d['yResult'] = yResult
  d['title'] = getPolynomialText(polynomialCoefficients, power) + '\n' + getCorrelationText(correlationCoefficient)
  return d
  
def getSlicedModelValues(xInput, yInput, rangeStart, rangeEnd, isPartial):
  modelCoefficient = 0
  modelIndex = 0
  coefficientSum = 0
  for i in range(rangeStart, rangeEnd):
    result = calculateSlicedModel(xInput, yInput, i, isPartial)['correlationCoefficient']
    if (result > modelCoefficient):
      modelIndex = i
      modelCoefficient = result
    coefficientSum += result

  d = dict()
  d['modelCoefficient'] = modelCoefficient
  d['modelIndex'] = modelIndex
  d['coefficientSum'] = coefficientSum
  return d
  
def getBestSlicedModel(xInput, yInput, rightModel):
  rangeStart = 5
  rangeEnd = 8
  if (rightModel):
    xInput = list(reversed(xInput[-rangeEnd:]))
    yInput = list(reversed(yInput[-rangeEnd:]))

  partialModelValues = getSlicedModelValues(xInput, yInput, rangeStart, rangeEnd, True)
  adsorptionModelValues = getSlicedModelValues(xInput, yInput, rangeStart, rangeEnd, False)

  if (partialModelValues['coefficientSum'] > adsorptionModelValues['coefficientSum']):
    result1 = calculateSlicedModel(xInput, yInput, partialModelValues['modelIndex'], True)
    result2 = calculateSlicedModel(xInput, yInput, partialModelValues['modelIndex'], False)
    showSubplots(result1['title'], result2['title'], result1['xInputNew'], result1['yInputNew'], result1['yResult'],
      result2['xInputNew'], result2['yInputNew'], result2['yResult'], True, rightModel)
  else:
    result1 = calculateSlicedModel(xInput, yInput, adsorptionModelValues['modelIndex'], True)
    result2 = calculateSlicedModel(xInput, yInput, adsorptionModelValues['modelIndex'], False)
    showSubplots(result1['title'], result2['title'], result1['xInputNew'], result1['yInputNew'], result1['yResult'],
      result2['xInputNew'], result2['yInputNew'], result2['yResult'], False, rightModel)

if (len(sys.argv) != 3):
  print('Please input x and y values as command arguments')
else:
  args1 = sys.argv[1].split(',')
  args2 = sys.argv[2].split(',')

  try:
    xInput = list(map(float, args1))
    yInput = list(map(float, args2))

    if (len(xInput) == len(yInput)):
      calculateDualModel(xInput, yInput)
      getBestSlicedModel(xInput, yInput, False)
      getBestSlicedModel(xInput, yInput, True)
    else:
      print('X and Y values are not the same length')
  except Exception as err:
    print(err) # TODO: remove this error later
    print('Please input only numbers')
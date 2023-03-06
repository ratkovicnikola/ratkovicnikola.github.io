import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import sys
import math
import csv

decimals = 4

def getPolynomialValue(x, coefficients, power):
  result = 0
  for i in range(power + 1):
    result += pow(x, power - i) * coefficients[i]
  return round(result, decimals)

def getPolynomialText(coefficients, power):
  result = ''
  for i in range(power + 1):
    coefficient = str(round(coefficients[i], decimals)) if coefficients[i] < 0 else '+' + str(round(coefficients[i], decimals))
    if (i == power):
      result += coefficient
    else:
      result += coefficient + 'x^' + str(power - i)

  result = result[1:] if result[0] == '+' else result
  result = result.replace('^1', '')
  result = result.replace('^2', '\u00b2')
  result = result.replace('^3', '\u00b3')
  return 'y=' + result

def getCorrelationText(value):
  valueString = str(round(value, decimals))
  return 'R\u00b2=' + valueString

def getMinValuesText(coefficients):
  fiMin = -coefficients[1] / (2 * coefficients[0])
  xMin = ((decimals * coefficients[0] * coefficients[2]) - math.pow(coefficients[1], 2)) / (decimals * coefficients[0])
  xMinAntilog = math.pow(10, xMin)
  return ', \u03A6min=' + str(round(fiMin, decimals)) + ', Xmin=' + str(round(xMin, decimals)) + ', k\'=' + str(round(xMinAntilog, decimals))

def calculateY(xInput, power, polynomialCoefficients):
  result = []
  for i in range(len(xInput)):
    value = xInput[i]
    if (power > 0):
      result.append(getPolynomialValue(value, polynomialCoefficients, power))
    else:
      result = None
  return result

def showPlotAndWriteToCSV(title, xInput, yInput, yResult):
  plt.title(title)
  plt.plot(xInput, yInput, 'go', label='Input values' )
  plt.plot(xInput, yResult, label='Function values' )
  plt.legend(loc='upper center')
  plt.grid(True)
  plt.show()
  with open('./output1.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['xInput', 'yInput', 'yResult', title])
    for i in range(len(xInput)):
      writer.writerow([xInput[i], yInput[i], yResult[i]])

def showSubplotsAndWriteToCSV(title1, title2, xInput1, yInput1, yResult1, xInput2, yInput2, yResult2, isPartialWinner, rightModel):
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
  fileSuffix = '3' if rightModel else '2'
  with open('./output' + fileSuffix + '.csv', 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['xInput1', 'yInput1', 'yResult1', 'xInput2', 'yInput2', 'yResult2', title1, title2])
    for i in range(len(xInput1)):
      writer.writerow([xInput1[i], yInput1[i], yResult1[i], xInput2[i], yInput2[i], yResult2[i]])

def calculateDualModel(xInput, yInput):
  power = 2
  polynomialCoefficients = np.polyfit(xInput, yInput, power)
  yResult = calculateY(xInput, power, polynomialCoefficients)
  correlationCoefficient = pd.Series(yInput).corr(pd.Series(yResult)) * pd.Series(yInput).corr(pd.Series(yResult)) # R^2
  title = getPolynomialText(polynomialCoefficients, power) + '\n' + getCorrelationText(correlationCoefficient) + getMinValuesText(polynomialCoefficients)
  showPlotAndWriteToCSV(title, xInput, yInput, yResult)

def getSlicedModelXInput(xInput, resultLength, isPartial):
  if (isPartial):
    return xInput[0:resultLength]
  else:
    result = []
    for i in range(len(xInput)):
      if (i < resultLength):
        result.append(round(math.log10(xInput[i]), decimals))
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
  # adjust these two values below if needed
  rangeStart = 5
  rangeEnd = 8
  if (rightModel):
    xInput = list(reversed(xInput[-rangeEnd:]))
    yInput = list(reversed(yInput[-rangeEnd:]))

  partialModelValues = getSlicedModelValues(xInput, yInput, rangeStart, rangeEnd, True)
  adsorptionModelValues = getSlicedModelValues(xInput, yInput, rangeStart, rangeEnd, False)

  isPartialWinner = partialModelValues['coefficientSum'] > adsorptionModelValues['coefficientSum']
  winnerIndex = partialModelValues['modelIndex'] if isPartialWinner else adsorptionModelValues['modelIndex']
  result1 = calculateSlicedModel(xInput, yInput, winnerIndex, True)
  result2 = calculateSlicedModel(xInput, yInput, winnerIndex, False)
  showSubplotsAndWriteToCSV(result1['title'], result2['title'], result1['xInputNew'], result1['yInputNew'], result1['yResult'],
    result2['xInputNew'], result2['yInputNew'], result2['yResult'], isPartialWinner, rightModel)

def getInputValues():
  d = dict()
  try:
    input = pd.read_csv('./input.csv')
    inputColumns = pd.DataFrame(input, columns=['xInput', 'yInput'])
    d['xInput'] = inputColumns.get('xInput')
    d['yInput'] = inputColumns.get('yInput')
  except Exception as err:
    if (len(sys.argv) != 3):
      print('Please input valid X and Y values from CSV or command line arguments')
      d = None
    else:
      d['xInput'] = sys.argv[1].split(',')
      d['yInput'] = sys.argv[2].split(',')
  return d

try:
  input = getInputValues()
  if (input):
    xInput = list(map(float, input['xInput']))
    yInput = list(map(float, input['yInput']))

    if (len(xInput) == len(yInput)):
      calculateDualModel(xInput, yInput)
      getBestSlicedModel(xInput, yInput, False)
      getBestSlicedModel(xInput, yInput, True)
    else:
      print('X and Y values are not the same length')
except Exception as err:
  print(err)
  print('Error occurred, please try with different input values')
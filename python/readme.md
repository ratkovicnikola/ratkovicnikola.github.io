# How to use retention mechanism script (rm.py)

## Install Python version 3 for your operating system

Download Python installer from this link and install it on your machine (if not installed previously)
https://www.python.org/downloads/ \
This script can work on Python 2, but it is recommended to use it with Python 3.

## Install Python packages that are used in the script

### Run these commands:

>pip install numpy\
>pip install matplotlib.pyplot\
>pip install pandas

## Run the script (without input)

>python3 rm.py

## Pass input values to the script

In order to pass input values to the script, use eithier CSV file with name **input.csv** or send the values via
command line using comma separator.

### Example using CSV file (input.csv):

>xInput,yInput\
>0.06,0.1\
>0.08,0.2\
>0.1,0.3\
>0.12,0.4

### Example with sending the values via command line arguments

python3 rm.py 0.06,0.08,0.1,0.12 0.1,0.2,0.3,0.4

### Results and errors

If input values are sent correctly, script will show 3 plots that will show **Dual**, **HILIC** and **RP-HPLC** model respectively.\
Winers for **HILIC** and **RP-HPLC** models will be shown in the plots.\
Calculated values will also be stored in files **output1.csv**, **output2.csv** and **output3.csv** files.

If there is an error during script run, it will be written in console (command line or terminal).

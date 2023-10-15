import serial
import csv
import numpy as np
ser = serial.Serial('COM6', 19200, timeout=1)

ser.write(("DATA:FORM CURR,VOLT,POW"+"\n").encode())
ser.write(("DATA:FORM?"+"\n").encode())
line = ser.readline()
print(line.decode('utf-8'))

ser.write(("DATA:R?"+"\n").encode())
line = ser.readline()
result = line.decode('utf-8').strip().split(',')

result_float = np.array(list(map(float, result))).reshape(-1, 3)

with open('fcload.csv', 'a', newline='') as f:
    csv.writer(f).writerows(result_float)

print(result_float)

ser.close()

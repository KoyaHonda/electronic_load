from serial import Serial
import csv
from datetime import datetime, timedelta

def measure():
    ser = Serial(port='COM4', baudrate=38400, timeout=1)
    ser.close()
    ser.open()
    ser.write(f'MEAS? Urms1\r\n'.encode())
    res_volt = float(ser.readline().decode())
    ser.write(f'MEAS? Irms1\r\n'.encode())
    res_curr = float(ser.readline().decode())
    ser.write(f'MEAS? P1\r\n'.encode())
    res_pow = float(ser.readline().decode())

    print(res_volt, res_curr, res_pow)
    with open('fcpower.csv', 'a', newline='') as f:
        csv.writer(f).writerow([res_volt, res_curr, res_pow])


def main(period):
    assert isinstance(period, timedelta)
    period = period#timedelta(seconds=220)
    interval = timedelta(seconds=1)

    now = datetime.now()
    end = now+period
    next = now+interval

    while now < end:
        while now < next:
            now = datetime.now()
        next = now+interval
        measure()
        print(now)


if __name__ == '__main__':
    
    main(timedelta(seconds=220))
    input('enter to restart')
    main(timedelta(seconds=180))

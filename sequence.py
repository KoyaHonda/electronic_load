import serial
import pandas as pd


#### モード選択 ####
mode = "test"
# mode = "load"
###################


# pandasでexel読み込み
df = pd.read_excel("C:/Users/honko/Box/Honda_Koya/研究/データ/自転車電力需要シュミレーション.xlsx", header=None)
df.columns = df.iloc[1]
df = df.drop(df.index[0:2], axis=0)
df = df.drop(df.columns[-1], axis=1)


class MySerial:
    def open_port(self):
        if mode == "test":
            print("Port is opened.")
        else:
            # COMポートを開く (COMポート名称,ビットレート[bps],タイムアウト[s])
            self.ser = serial.Serial('COM6', 19200, timeout=1)

    def query(self, command):
        if mode == "test":
            print(command)
        else:
            self.ser.write((command+"\n").encode())
            line = self.ser.readline()
            print(line.decode('utf-8'))

    def send(self, command):
        if mode == "test":
            print(command)
        else:
            self.ser.write((command+"\n").encode()) # 改行しつつb" "形式に変換する。
    
    def close_port(self):
        if mode == "test":
            print("Port is closed.")
        else:
            # COMポートを閉じる
            self.ser.close()

my_serial = MySerial()
time_s = 210 #合計秒数


my_serial.open_port()

my_serial.query("*IDN?")
my_serial.send(":FUNC CC")
my_serial.query("FUNC?")
my_serial.send(":PROG:CRE '/flat road'")
my_serial.send(":PROG '/flat road'")
my_serial.send(":PROG:LOOP 1") #プログラムのループ数
my_serial.send(":PROG:STEPS:COUN" + " " + str(time_s)) #プログラムのステップ数

for i in range(1, time_s + 1):
    my_serial.send(":PROG:STEP" + str(i) + ":LEV"+ " " + str(df.iloc[i - 1, 1]) + "A") #ステップの設定値
    my_serial.send(":PROG:STEP" + str(i) + ":DWEL 1s") #ステップの実行時間 
    my_serial.send(":PROG:STEP" + str(i) + ":INP ON") #ステップのロード(ON, OFF)
    my_serial.send(":PROG:STEP" + str(i) + ":TRAN RAMP") #ステップの遷移(Ramp, Immediate)

my_serial.send(":PROG:STEP" + str(time_s) + ":TRIG:GEN TRIGOUT") #トリガ出力をTrigger outに設定


my_serial.close_port()
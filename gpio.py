#!/usr/bin/env python
# -*- coding: utf-8 -*-

import smbus                #I2C通信するためのモジュールsmbusをインポートする
import time                 #sleepするためにtimeモジュールをインポートする
import logging

global bus
global adress
bus = smbus.SMBus(1)    ##I2C通信するためのモジュールsmbusのインスタンスを作成
adress = 0x04           #arduinoのサンプルプログラムで設定したI2Cチャンネル


def get_alp():
    try:
        for i in range(100):#Arduinoからのメッセージを取得し表示する、chrはアスキーコードを文字へ変換
            msg = chr(bus.read_byte(adress))
            logging.debug(msg)
            #0.5sスリープする
            time.sleep(0.1)
            if msg != None:break
        return msg

    except KeyboardInterrupt  :         #Ctl+Cが押されたらループを終了
        logging.debug("\nCtl+C")
    except Exception as e:
        logging.debug(str(e))
    finally:
        logging.debug("\nexit program")
        
def comu_alp(alp):

    try:
        #Arduinoへ文字『alp』を送る、ordはアスキーコードを取得
        bus.write_byte(adress, ord(alp))

        get_alp()

    except KeyboardInterrupt  :         #Ctl+Cが押されたらループを終了
        print("\nCtl+C")
    except Exception as e:
        print(str(e))
    finally:
        print("\nSENDED")


        
"""メイン関数"""
if __name__ == '__main__':
    while True:
        word = input()
        print(comu_alp(word))
        print(get_alp())


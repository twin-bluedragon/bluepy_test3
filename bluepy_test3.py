# -*- coding: utf-8 -*-
#https://www.ipride.co.jp/blog/2510
#デバイスに接続するサンプル
#コンストラクタで直接指定するパターン
from bluepy import btle
import asyncio

SERVER_NAME = 'M5Stack' #サーバー名は'M5Stack'固定
#SERVICE_UUID = '4fafc201-1fb5-459e-8fcc-c5c9c331914b' #固定値　サービスUUIDは変更する必要あり
SERVICE_UUID = 'c8cb525e-dcda-4897-a92e-6980768e9854' #固定値　https://www.uuidgenerator.net/version4　で生成

MacAddresses = [] #BLE DeviceのMACアドレスのリスト
peripherals = [] #BLE Deviceのconnect済のハンドルのリスト

#CHARACTERISTIC_UUID = 'beb5483e-36e1-4688-b7f5-ea07361b26a8' #固定値　キャラクタリスティックUUIDも変更する必要あり
CHARACTERISTIC_UUID = 'dc530ce2-4cf5-4a76-a28c-6c711474c8b2' #固定値　https://www.uuidgenerator.net/version4　で生成
Handles=[] #各デバイスのキャラクタリスティックのハンドルのリスト

#デバイスをスキャンし、接続したいデバイスのMACアドレスを取得する
def scanDevices():
    scanner=btle.Scanner(0)
    devices=scanner.scan(3.0) #3秒間スキャン
    for device in devices:
        serverOK = False
        serviceOK = False
        #アドバタイジングデータを取得する
        for (adTypeCode, description, valueText) in device.getScanData():
            if(description=='Complete Local Name'):
                if(valueText==SERVER_NAME): #サーバー名がSERVER_NAMEと等しいかの検査
                    serverOK=True
            elif(description=='Complete 128b Services'): #サービスUUIDが目的のものと等しいか検査
                if(valueText==SERVICE_UUID):
                    serviceOK=True
        if(serverOK and serviceOK): #サーバー名とサービスUUIDの両方が目的のものと合っていれば、MACアドレスのリストを登録
            MacAddresses.append(device.addr)
            print("scan detect ",device.addr)

#MACアドレスのリストのデバイスと接続し、目的のキャラクタリスティックUUIDのハンドルを取得してリストに追加する
def connectDevices():
    #MacAddressesのデバイス全部と接続して、ハンドルのオブジェクトのリストを作る
    for macAddress in MacAddresses:
        peripherals.append(btle.Peripheral(macAddress))
        print("connect to ",macAddress)
    #それぞれのデバイスのキャラクタリスティックUUIDをスキャンしてのハンドルを取得してリストに追加する
    for peripheral in peripherals:
        for service in peripheral.getServices():
            for characteristic in service.getCharacteristics():
                if(characteristic.uuid==CHARACTERISTIC_UUID):
                    Handles.append(characteristic.getHandle())

#各デバイスからデータをリードする
def readDevices(devNo):
    data = peripherals[devNo].readCharacteristic(Handles[devNo])
    print(len(data)," ",data)

#各デバイスを切断する
def disconnectDevices():
    for peripheral in peripherals:
        peripheral.disconnect()

def main():
    scanDevices()
    connectDevices()
    
    for i in range(100):
        for devNo in range(len(peripherals)):
            readDevices(devNo)

    disconnectDevices()    

if __name__=="__main__":
    main()
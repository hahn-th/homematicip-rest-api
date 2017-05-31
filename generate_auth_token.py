import homematicip
import time

while True:
    access_point = input("Please enter the accesspoint id (SGTIN): ").replace('-', '').upper()
    if len(access_point) != 24:
        print("Invalid access_point id")
        continue
    break
pin = input("Please enter the PIN (leave Blank if there is none): ")

devicename = input("Please enter the client/devicename (leave blank to use default):")

homematicip.init(access_point)
auth = homematicip.Auth()

if pin != '':
    auth.pin=pin

if devicename != '':
    auth.connectionRequest(access_point,devicename)
else:
    auth.connectionRequest(access_point)

print("Please press the blue button on the access point")
while not auth.isRequestAcknowledged():
    print("Please press the blue button on the access point")
    time.sleep(2)

auth_token = auth.requestAuthToken()
clientId = auth.confirmAuthToken(auth_token)

print("Token successfully registered: ", auth_token)
print("Client ID is ", clientId)

import homematicip
import time

while True:
    access_point = raw_input("Please enter the accesspoint id (SGTIN): ").replace('-', ' ')
    if len(access_point) != 24:
        print "Invalid access_point id"
        continue
    break

homematicip.init(access_point)
auth = homematicip.Auth()

auth.connectionRequest(access_point)
print "Please press the blue button on the access point"
while not auth.isRequestAcknowledged():
    print "Please press the blue button on the access point"
    time.sleep(2)

auth_token = auth.requestAuthToken()
clientId = auth.confirmAuthToken(auth_token)

print "Token successfully registered: ", auth_token
print "Client ID is ", clientId

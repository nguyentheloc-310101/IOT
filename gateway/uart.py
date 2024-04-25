import serial.tools.list_ports


def getPort():
    ports = serial.tools.list_ports.comports()
    N = len(ports)
    commPort = "None"
    for i in range(0, N):
        port = ports[i]
        strPort = str(port)
        if "USB Serial Device" in strPort:
            splitPort = strPort.split(" ")
            commPort = splitPort[0]
    # return commPort
    return "COM8"


if getPort() != "None":
    ser = serial.Serial(port=getPort(), baudrate=115200)
    print(ser)


def processData(client, data):
    data = data.replace("!", "")
    data = data.replace("#", "")
    splitData = data.split(":")
    print("data wite:",data)
    if splitData[0] == "T":
        client.publishMessage("theloc3101/feeds/temperature_history", splitData[1])
    elif splitData[0] == "H":
        client.publishMessage("theloc3101/feeds/humid_history", splitData[1])
    elif splitData[0] == "L":
        client.publishMessage("theloc3101/feeds/light_history", splitData[1])


mess = ""


# def readSerial(client):
#     bytesToRead = ser.inWaiting()
#     if bytesToRead > 0:
#         global mess
#         mess = mess + ser.read(bytesToRead).decode("UTF-8")
#         print(mess)
#         while ("#" in mess) and ("!" in mess):
#             start = mess.find("!")
#             end = mess.find("#")
#             processData(client, mess[start : end + 1])
#             if end == len(mess):
#                 mess = ""
#             else:
#                 mess = mess[end + 1 :]
def readSerial(client):
    bytesToRead = ser.inWaiting()
    if bytesToRead > 0:
        global mess
        data = ser.read(bytesToRead)
        if data:
            try:
                decoded_data = data.decode("ascii")
                mess = mess + decoded_data
                print("mess from serial read: ", mess)
                while "#" in mess and "!" in mess:
                    start = mess.find("!")
                    end = mess.find("#")
                    if start != -1 and end != -1:  # Check if both delimiters are found
                        message = mess[start + 1:end]  # Extract the message between delimiters
                        processData(client, message)
                        mess = mess[end + 1:]  # Remove processed data from the buffer
                    else:
                        # Incomplete message, wait for more data
                        break
            except UnicodeDecodeError as e:
                print(f"UnicodeDecodeError: {e}")

                # Handle the error gracefully, such as logging it or trying different encodings




def writeSerial(data):
    ser.write(str(data).encode())

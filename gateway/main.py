from mqtt import MQTTClient
import os
from dotenv import load_dotenv

load_dotenv()
MQTT_SERVER = os.getenv("MQTT_SERVER")
MQTT_PORT = os.getenv("MQTT_PORT")
print(MQTT_PORT)

MQTT_USERNAME = os.getenv("MQTT_USERNAME")
MQTT_PASSWORD = os.getenv("MQTT_PASSWORD")
TOPICS = ["kd77/feeds/device"]


def test(payload):
    print("test: " + payload)


mqttClient = MQTTClient(MQTT_SERVER, MQTT_PORT, TOPICS, MQTT_USERNAME, MQTT_PASSWORD)
mqttClient.setRecvCallBack(test)
mqttClient.connect()


while True:
    pass

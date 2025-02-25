import machine
import dht
import time
import network
import ubinascii
from umqtt.simple import MQTTClient

# Konfigurasi WiFi
SSID = "LAB 2"
PASSWORD = "bersahaja"

# Konfigurasi Ubidots
TOKEN = "BBUS-fpMEeomIYnNQvzrhyIxwjfF7VA76jX"
DEVICE_ID = "67bbe70d50c03890b30a688d"
LABEL = "safeteamhsc193lolos"
BROKER = "industrial.api.ubidots.com"
TOPIC = f"/v1.6/devices/{LABEL}"

# Koneksi ke WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
    print("WiFi Connected!", wlan.ifconfig())

# Koneksi ke MQTT Ubidots
def connect_mqtt():
    client_id = ubinascii.hexlify(machine.unique_id()).decode()
    client = MQTTClient(client_id, BROKER, user=TOKEN, password="", port=1883, keepalive=60)
    client.connect()
    print("Connected to Ubidots MQTT Broker")
    return client

# Inisialisasi sensor DHT11 di pin D5
sensor = dht.DHT11(machine.Pin(15))

connect_wifi()
client = connect_mqtt()

while True:
    try:
        sensor.measure()
        suhu = sensor.temperature()
        kelembaban = sensor.humidity()

        print(f"Suhu: {suhu}°C | Kelembaban: {kelembaban}%")
        
        payload = f'{{"temperature": {suhu}, "humidity": {kelembaban}}}'
        client.publish(TOPIC, payload)
        print("Data sent to Ubidots")
    
    except OSError as e:
        print("Gagal membaca sensor!", e)
    
    time.sleep(5)

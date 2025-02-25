import machine
import dht
import time
import network
import urequests  # Untuk HTTP request ke Flask

# Konfigurasi WiFi
SSID = "LAB 2"
PASSWORD = "bersahaja"

# Konfigurasi Flask API (Pastikan sesuai dengan IP Flask)
FLASK_URL = "http://192.168.0.100:6000/send_data"  # Ganti dengan IP Flask API kamu

# Koneksi ke WiFi
def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    wlan.connect(SSID, PASSWORD)
    while not wlan.isconnected():
        pass
    print("WiFi Connected!", wlan.ifconfig())

# Inisialisasi sensor DHT11 di pin D5
sensor = dht.DHT11(machine.Pin(15))

connect_wifi()

while True:
    try:
        sensor.measure()
        suhu = sensor.temperature()
        kelembaban = sensor.humidity()

        print(f"Suhu: {suhu}°C | Kelembaban: {kelembaban}%")

        # Buat data JSON
        payload = {"temperature": suhu, "humidity": kelembaban}

        # Kirim data ke Flask API
        response = urequests.post(FLASK_URL, json=payload)
        print("Response:", response.text)
        response.close()

    except OSError as e:
        print("Gagal membaca sensor!", e)

    time.sleep(5)

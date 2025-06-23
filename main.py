from machine import Pin, I2C
import time
from bmp280 import BMP280
from sending_adafruit import sending_data_temperature, sending_data_pressure

i2c = I2C(scl=Pin(5), sda=Pin(4))
sensor = BMP280(i2c=i2c)

print("📡 Iniciando leitura e envio de dados a cada 15 segundos...\n")

while True:
    try:
        temperature, pressure = sensor.read_compensated_data()
        sending_data_temperature(temperature)
        sending_data_pressure(pressure)

    except Exception as error:
        print(f"❌ Erro na leitura do sensor ou envio: {error}")

    time.sleep(10)

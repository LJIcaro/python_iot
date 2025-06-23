import urequests as requests
import ujson

# === Configurações ===
ADAFRUIT_IO_USERNAME = "ljicaro"
ADAFRUIT_IO_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"
GROUP_NAME = "Device01-ljicaro"
GROUP_KEY = GROUP_NAME.lower()


# === Envio de dados separados ===
def sending_data_temperature(temperature):
    headers = {"X-AIO-Key": ADAFRUIT_IO_KEY, "Content-Type": "application/json"}
    url_temp = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}/feeds/{GROUP_KEY}.temperature/data"
    temp_payload = {"value": str(round(temperature, 2))}
    try:
        res_temp = requests.post(
            url_temp, headers=headers, data=ujson.dumps(temp_payload)
        )
        print(
            f"📤 Enviado temperature = {temp_payload['value']} °C | Status: {res_temp.status_code}"
        )
        res_temp.close()
    except Exception as e:
        print(f"❌ Erro ao enviar temperatura: {e}")


def sending_data_pressure(pressure):
    headers = {"X-AIO-Key": ADAFRUIT_IO_KEY, "Content-Type": "application/json"}
    url_press = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}/feeds/{GROUP_KEY}.pressure/data"
    pressure = pressure / 100.0
    press_payload = {"value": str(round(pressure, 2))}
    try:
        res_press = requests.post(
            url_press, headers=headers, data=ujson.dumps(press_payload)
        )
        print(
            f"📤 Enviado pressure = {press_payload['value']} hPa | Status: {res_press.status_code}"
        )
        res_press.close()
    except Exception as e:
        print(f"❌ Erro ao enviar pressão: {e}")

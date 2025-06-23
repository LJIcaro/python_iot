import requests
import json

ADAFRUIT_IO_USERNAME = "ljicaro"
ADAFRUIT_IO_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXX"
NAME_GROUP_FEEDS = "Device01-ljicaro"
GROUP_KEY = NAME_GROUP_FEEDS.lower()
FEEDS = ['temperature', 'pressure']

HEADERS = {
    "X-AIO-Key": ADAFRUIT_IO_KEY,
    "Content-Type": "application/json"
}

BASE_URL = f"https://io.adafruit.com/api/v2/{ADAFRUIT_IO_USERNAME}"
GROUPS_URL = f"{BASE_URL}/groups"
FEEDS_URL = f"{GROUPS_URL}/{GROUP_KEY}/feeds"


def list_groups():
    print("\n🔍 Listando grupos existentes...")
    res = requests.get(GROUPS_URL, headers=HEADERS)
    res.raise_for_status()
    grupos = res.json()
    print("📦 Grupos disponíveis:\n", json.dumps(grupos, indent=2))
    res.close()


def create_group():
    print(f"\n📁 Tentando criar grupo: '{NAME_GROUP_FEEDS}'")
    payload = {"name": NAME_GROUP_FEEDS}
    res = requests.post(GROUPS_URL, headers=HEADERS, data=json.dumps(payload))
    response = res.json()

    if "error" in response:
        if "name" in response["error"] and "has already been taken" in response["error"]["name"]:
            print(f"⚠️ Grupo '{NAME_GROUP_FEEDS}' já existe.")
        else:
            print(f"❌ Erro ao criar grupo: {response['error']}")
    else:
        print(f"✅ Grupo '{NAME_GROUP_FEEDS}' criado com sucesso!")

    res.close()


def create_feeds():
    print(f"\n🧪 Tentando criar feeds em: '{NAME_GROUP_FEEDS}'")
    for nome in FEEDS:
        payload = {"name": nome}
        res = requests.post(FEEDS_URL, headers=HEADERS, data=json.dumps(payload))
        response = res.json()

        if "error" in response:
            if "name" in response["error"] and "has already been taken" in response["error"]["name"]:
                print(f"⚠️ Feed '{nome}' já existe.")
            else:
                print(f"❌ Erro ao criar feed '{nome}': {response['error']}")
        else:
            print(f"✅ Feed '{nome}' criado com sucesso!")

        res.close()


if __name__ == "__main__":
    list_groups()
    create_group()
    create_feeds()

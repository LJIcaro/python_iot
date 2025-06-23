# python_iot

# Relatório do Projeto: Monitoramento de Temperatura e Pressão com ESP32 e Adafruit IO

---

## Dados do Projeto

- **Disciplina: *Aplicação de Cloud, IOT e Indústria 4.0 em Python*  
- **Integrantes: *Ícaro Lima, Eduardo Miguel, Ruan Müller, Alan Goes, Breno Chaves e Rafael Canella*  
- **Instituição: *CENTRO UNIVERSITÁRIO RUY BARBOSA - CAMPUS IMBUÍ/PARALELA*  
- **Professor(a): *VITOR EMMANUEL ANDRADE*  

---

## 1. Introdução

Este projeto tem como objetivo realizar a leitura de temperatura e pressão atmosférica utilizando um sensor BMP280 conectado a um microcontrolador ESP32. Os dados coletados são enviados periodicamente para a plataforma Adafruit IO, permitindo o monitoramento remoto em tempo real via dashboard web.

---

## 2. O que é o Adafruit IO?

O **Adafruit IO** é uma plataforma de Internet das Coisas (IoT) baseada em nuvem, desenvolvida pela Adafruit, que permite o armazenamento, visualização e automação de dados de sensores e dispositivos conectados.  
Com o Adafruit IO, é possível criar dashboards personalizados, visualizar gráficos, receber alertas e integrar diferentes dispositivos de forma simples e segura, utilizando APIs REST.

---

## 3. Funcionamento do Algoritmo

O algoritmo desenvolvido realiza as seguintes etapas:

1. **Inicialização do Hardware:**  
   - Configura o barramento I2C do ESP32 para comunicação com o sensor BMP280.
   - Inicializa o sensor para leitura dos dados ambientais.

2. **Leitura dos Dados:**  
   - A cada ciclo, o ESP32 lê a temperatura (em °C) e a pressão atmosférica (em Pa) do BMP280.

3. **Conversão de Unidades:**  
   - A pressão é convertida de Pascal (Pa) para hectopascal (hPa), unidade padrão em meteorologia, dividindo o valor por 100.

4. **Envio dos Dados para o Adafruit IO:**  
   - Os dados são enviados separadamente para dois feeds distintos (`temperature` e `pressure`) criados previamente na plataforma.
   - O envio é feito via requisições HTTP POST, utilizando a biblioteca `urequests` e o formato JSON.
   - O campo `"value"` do payload deve ser sempre uma string representando o valor numérico.

5. **Intervalo entre Envios:**  
   - O envio de temperatura e pressão ocorre de forma alternada, com um intervalo de 10 segundos entre cada envio, evitando sobrecarga e respeitando limites da API.

6. **Dashboard:**  
   - Os dados enviados podem ser visualizados em tempo real no dashboard do Adafruit IO, utilizando blocos de texto, gráficos ou gauges.

---

## 4. Principais Pontos Discutidos e Soluções

- **Conversão de Unidades:**  
  O sensor retorna a pressão em Pa, mas o Adafruit IO e a maioria dos dashboards utilizam hPa. Por isso, é necessário dividir o valor por 100 antes do envio.

- **Formato do Payload:**  
  O campo `"value"` deve ser enviado como string, mesmo que o valor seja numérico, para evitar erros de parsing na API do Adafruit IO.

- **URLs de Envio:**  
  Para feeds dentro de grupos, a URL correta é:  
  `https://io.adafruit.com/api/v2/{usuario}/feeds/{grupo}.{feed}/data`

- **Erros Comuns:**  
  - Erro 400 geralmente indica problema no valor enviado (tipo, formato ou valor fora do esperado) ou no endpoint.
  - Erro ao enviar dois valores juntos no mesmo payload: cada feed deve receber apenas um valor por vez.

- **Visualização no Dashboard:**  
  Se os dados forem enviados juntos em um único feed como JSON, o Adafruit IO exibirá apenas a string. Para gráficos e gauges separados, é necessário enviar cada dado para um feed distinto.

---

## 5. Exemplo de Código Principal

```python
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
        time.sleep(10)
        sending_data_pressure(pressure)
    except Exception as error:
        print(f"❌ Erro na leitura do sensor ou envio: {error}")

    time.sleep(10)
```

---

## 6. Considerações Finais

O projeto demonstra a integração entre hardware embarcado (ESP32), sensores ambientais e plataformas IoT na nuvem. O uso do Adafruit IO facilita o armazenamento, visualização e análise dos dados, além de permitir a expansão futura para automações e alertas.

Durante o desenvolvimento, foram enfrentados desafios comuns em projetos IoT, como conversão de unidades, formatação de payloads e tratamento de erros de API, todos solucionados com boas práticas de programação.

---

**Temos consciência que há dados sensíveis expostos como chave de api e nome da conta de usuário da plataforma Adafruit IO. Sendo a funcionalidade para fins didáticos, posteriormente ao prazo desse projeto os dados sensíveis serão trocados/invalidos. Caso o projeto fosse para a produção de alguma forma, o ideal seria o controle desses dados atráves de variáveis de ambiente e um arquivo de configurações.**

---

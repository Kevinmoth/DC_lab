import requests
import json
import time
import random
import string

#GENERADOR DE NITRO - By  MATECITOS
#Solo funciona hasta el 07/06/24
#Podes ejecutarlo desde replit.com/@jeta0021/Generador-Nitro#main.py


def generar_cadena_aleatoria(longitud):
    caracteres = string.ascii_letters + string.digits
    return ''.join(random.choices(caracteres, k=longitud))

if __name__ == "__main__":
    url = 'https://api.discord.gx.games/v1/direct-fulfillment'
    encabezados = {
        'authority': 'api.discord.gx.games',
        'accept': '*/*',
        'accept-language': 'es-ES,es;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.opera.com',
        'referer': 'https://www.opera.com/',
        'sec-ch-ua': '"Opera GX";v="105", "Chromium";v="119", "Not?A_Brand";v="24"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'cross-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36 OPR/105.0.0.0'
    }

    datos = {
        'partnerUserId': generar_cadena_aleatoria(64)
    }

    sesion = requests.Session()

    try:
        while True:
            respuesta = sesion.post(url, headers=encabezados, json=datos)

            if respuesta.status_code == 200:
                token = respuesta.json()['token']
                with open('Matecitos.txt', 'a') as archivo:
                    archivo.write(f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}\n")
                print("Codigo de NITRO generado, caduca en exactamente 30 dias, guardado en el archivo Matecitos.txt.\n\n")
                print(f"https://discord.com/billing/partner-promotions/1180231712274387115/{token}\n")
            else:
                print(f"La solicitud falló con el código de estado {respuesta.status_code}.")
                print(f"Mensaje de error: {respuesta.text}")

            time.sleep(1)

    except Exception as e:
        print(f"Se produjo un error: {str(e)}")

    finally:
        sesion.close()

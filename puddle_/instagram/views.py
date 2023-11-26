import os
import requests
from dotenv import load_dotenv

load_dotenv()

instagram_access_token = os.environ.get('INSTAGRAM_ACCESS_TOKEN')

def get_instagram_feed():
    access_token = instagram_access_token
    user_id = '6019732041456856'
    url = f'https://graph.instagram.com/{user_id}/media?fields=id,media_type,media_url,timestamp&access_token={access_token}'

    try:
        response = requests.get(url)

        # Verificar si la respuesta es exitosa y no está vacía
        if response.status_code == 200 and response.text:
            data = response.json()
            image_urls = [item['media_url'] for item in data.get('data', []) if item.get('media_type') == 'IMAGE']
            return image_urls[:5]
        else:
            print(f"Error en la solicitud: Estado {response.status_code}, Respuesta: {response.text}")
            return []

    except requests.RequestException as e:
        print(f"Error en la solicitud HTTP: {e}")
        return []
    except json.JSONDecodeError as e:
        print(f"Error al decodificar JSON: {e}")
        return []

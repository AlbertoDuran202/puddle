import os
import requests
from dotenv import load_dotenv

load_dotenv()

instagram_access_token = os.environ.get('INSTAGRAM_ACCESS_TOKEN')

def get_instagram_feed():
    access_token = instagram_access_token  # Utiliza el token que obtuviste de las variables de entorno
    user_id = '6019732041456856'
    url = f'https://graph.instagram.com/{user_id}/media?fields=id,media_type,media_url,timestamp&access_token={access_token}'
    response = requests.get(url)
    data = response.json()
    image_urls = [item['media_url'] for item in data['data'] if item['media_type'] == 'IMAGE']
    image_urls = image_urls[:5]
    return image_urls



import requests

def get_instagram_feed():
    access_token = 'IGQVJWUkZAxOHUxVEhrNGs4ZAG1COG5Ybnh1ZA0F6VGR4ZA0daU2ZAnZAlhJNlhBMHhDN09JQ3RyRTdtMVF0cV9DR3JvU1RNT3drSFJwT1ZATbVZACblNTTUtmeFJkeXFOOHNCOTlRZAWtQa1E3VDJCWWdjWWtZAVgZDZD'
    user_id = '6019732041456856'
    url = f'https://graph.instagram.com/{user_id}/media?fields=id,media_type,media_url,timestamp&access_token={access_token}'
    response = requests.get(url)
    data = response.json()
    image_urls = [item['media_url'] for item in data['data'] if item['media_type'] == 'IMAGE']
    image_urls = image_urls[:5]
    return image_urls




import requests

client_secret = '8f222a15efb508f630eae3697a719736'
short_lived_access_token = 'IGQVJYZAGt0R1NVZAGRHc09wWGRaRXJkMHUzMUp1ZAm5HSlMwQUtXTXBtcG5IRWktQkFKaWtod3lCWTlwZAjVOZAmRLVHk5SWEtQksxQms4dmlUM3RkczVrMzR4R0Q1NjQzVlYxMzhMbWN1ckdzZAktGNlZAkNgZDZD'

def exchange_short_lived_token(client_secret, short_lived_access_token):
    url = f"https://graph.instagram.com/access_token?grant_type=ig_exchange_token&client_secret={client_secret}&access_token={short_lived_access_token}"
    
    response = requests.get(url)
    data = response.json()
    
    if 'access_token' in data:
        long_lived_access_token = data['access_token']
        expires_in = data['expires_in']
        print(f"Long-lived access token: {long_lived_access_token}")
        print(f"Expires in: {expires_in} seconds")
    else:
        print(f"Error exchanging short-lived access token: {data}")


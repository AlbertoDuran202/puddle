import requests

access_token = 'IGQVJXbWNlVGo1V21DcDBiYTlvQUZAQWmJBcTlEUmdzdk1temFMRWVCaW5iNXZAYQ3hucllGWEFmTU9vWlhtNm02Q1pnZAE9icDRmdFVfU05BRGJ6V1RNSXY4YnlFam9JWTg2dWFIbXV0VEdmS0RGaTdQQwZDZD'
url = f'https://graph.instagram.com/me?fields=id,username&access_token={access_token}'

response = requests.get(url)
data = response.json()
user_id = data['id']
print(f"User ID: {user_id}")
import requests

headers = {}
token = requests.post('http://127.0.0.1:8000/api/token/', {'username':'itstime', 'password':'behappy'})
token=token.text
print(token)

token = token.split('access')[1].split(':')[1].replace('"','').replace('}','')
print(token)
headers['Authorization'] = f"Bearer {token}"
r = requests.get('http://127.0.0.1:8000/restapi/ticker/', headers = headers)

print(r.text)


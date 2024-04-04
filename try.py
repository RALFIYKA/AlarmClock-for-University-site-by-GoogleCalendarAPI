import requests

titulsite = (requests.get(url='https://eners.kgeu.ru/').text)
print(titulsite)    
import json
import requests

dado = requests.get("http://developers.agenciaideias.com.br/tempo/json/sao paulo - SP")
dado = json.loads(dado.text)

for num, key in enumerate(dado['previsoes']):
	if num <= 3:
		print(num, key['data'])
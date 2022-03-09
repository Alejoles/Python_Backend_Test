import requests

"""
    Obtenga el nombre del idioma que habla el pais y encriptelo con SHA1
"""

def alert_country(function):
    def wrapper(pais):
        response = requests.get(f"https://restcountries.com/v3.1/name/{pais}")
        if(not response.ok):
            return function('')
        return response.json()[0]
    return wrapper 

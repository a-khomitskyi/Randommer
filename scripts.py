from datetime import datetime
import requests
from random import choice, choices, randint

URL = 'https://randomuser.me/api/'
S_LETTER = 'qazxswedcvfrtgbnhyujmkiolp'
B_LETTER = 'QAZXSWEDCVFRTGBNHYUJMKIOLP'
SYMBOL = '!@#$%^&*()_-+={}[].,'


def person_gen(url):
	responce = \
	requests.get(url, params={'inc': 'name,login,dob,phone,location,picture,photo&noinfo'}).json()['results'][0]
	result = {}
	result['first'] = responce['name']['first']
	result['last'] = responce['name']['last']
	result['street'] = f"{responce['location']['street']['name']}, {responce['location']['street']['number']}"
	result['city'] = responce['location']['city']
	result['state'] = responce['location']['state']
	result['country'] = responce['location']['country']
	result['postcode'] = responce['location']['postcode']
	result['username'] = responce['login']['username']
	result['password'] = responce['login']['password'] + responce['login']['salt']
	result['born'] = '.'.join(
		str(datetime.fromisoformat(responce['dob']['date'][:-1]).date()).split('-')[::-1])
	result['phone'] = responce['phone']
	result['photo'] = responce['picture']['large']

	return result


def passgen(n: int = None) -> str:
	if n:
		return ''.join(choices(S_LETTER + B_LETTER + SYMBOL, k=n))
	return ''.join(choices(S_LETTER + B_LETTER + SYMBOL, k=randint(12, 19)))


def login_gen(n: int = None) -> str:
	if n:
		return ''.join(choices(S_LETTER, k=n))
	return ''.join(choices(S_LETTER, k=randint(8, 16)))


def quick_registration() -> dict:
	login = login_gen()
	passwd = passgen()
	return {'login': login, 'passwd': passwd}


def get_avatar(url: str) -> str:
	return f"{url}portraits/{choice(['men', 'women'])}/{randint(0, 100)}.jpg"


if __name__ == '__main__':
	# print(person_gen(URL))
	print(passgen())
	# print(login_gen())
	# print(quick_registration())
	# print(get_avatar(URL))

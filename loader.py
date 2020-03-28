import vk_api
import json
import getpass
import datetime
import os

DIRNAME = 'posts'
GROUPS = [
	'oldlentach', 'true_lentach', 'eshkin_krot',
	'mbkhmedia', 'satyrabezsortyra', 'meduzaproject',
	'currenttime', 'svobodaradio', 'novgaz',
	'lentaru', 'echomsk', 'takiedela_ru', 'tj',
	'tvrain', 'orangeeast',
]

if not os.path.exists(DIRNAME):
	os.mkdir(DIRNAME)

# authorize
print('login:', end=' ')
login = str(input())
password = str(getpass.getpass())

# Start session and get API object
print('Authorisation in process')
vk_session = vk_api.VkApi(login, password)
vk_session.auth()
vk = vk_session.get_api()

def get_year(unixtime):
	return datetime.datetime.utcfromtimestamp(unixtime).year

def get_posts(group):
	offset = 0
	posts = []
	path = os.path.join(DIRNAME, f'file{group}.jsonl')
	file = open(path, mode='w', encoding='utf-8')
	while True:
		new_posts = vk.wall.get(domain=group, offset=offset,
								count=100)['items']

		if len(new_posts) == 0:
			break

		offset += 100
		if offset % 5000 == 0:
			print('\toffset', offset, 'year', get_year(new_posts[0]['date']))

		for post in new_posts:
			post['group'] = group
			file.write(json.dumps(post) + '\n')

	file.close()


for group in GROUPS:
	try:
		print('Getting posts from', group)
		get_posts(group)
	except vk_api.exceptions.ApiError:
		print('Rate limit reached, last group is', group)
		break




import vk_api
import json
import getpass
import datetime
import os


def get_year(unixtime):
	return datetime.datetime.utcfromtimestamp(unixtime).year

def get_posts(group, vk, dirname):
	offset = 0
	today = str(datetime.date.today())
	path = os.path.join(dirname, f'file_{group}_{today}.jsonl')
	with open(path, mode='w', encoding='utf-8') as file:
		while True:
			new_posts = vk.wall.get(domain=group, offset=offset,
									count=100)['items']
			if len(new_posts) == 0:
				return

			offset += 100
			if offset % 5000 == 0:
				year = get_year(new_posts[0]['date'])
				print('\toffset', offset, 'year', year)

			for post in new_posts:
				post['group'] = group
				file.write(json.dumps(post) + '\n')


def load_files(groups, dirname='posts'):
	# authorize
	print('login:', end=' ')
	login = str(input())
	password = str(getpass.getpass())

	# Start session and get API object
	print('Authorisation...')
	vk_session = vk_api.VkApi(login, password)
	vk_session.auth()
	vk = vk_session.get_api()

	if not os.path.exists(dirname):
		os.mkdir(dirname)

	for group in groups:
		try:
			print('Getting posts from', group)
			get_posts(group, vk, dirname)
		except vk_api.exceptions.ApiError:
			print('Rate limit reached, last group is', group)
			break

if __name__ == '__main__':
	with open('groups.json', 'r') as file:
		groups = json.load(file)
	load_files(groups)



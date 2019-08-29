import vk_api
import json
import getpass
import datetime

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
    return datetime.datetime.utcfromtimestamp(
        unixtime).year

def get_posts(group):
    print('Getting posts from', group)
    offset = 0
    posts = []
    while True:
        try:
            new_posts = vk.wall.get(
                domain=group, offset=offset,
                count=100,
            )['items']
        except vk_api.exceptions.ApiError:
            print('Rate limit reached, last group is', group)
            break

        if len(new_posts) == 0:
            break

        new_posts = [
            {
                'text': post['text'],
                'date': post['date'],
                'likes': post['likes']['count'],
                'reposts': post['reposts']['count'],
                'public': group,
            } for post in new_posts
        ]
        offset += 100
        if offset % 1000 == 0:
            print('     offset', offset,
                'year', get_year(new_posts[0]['date']))
        
        posts.extend(new_posts)
    return posts

groups = [
    'oldlentach', 'true_lentach', 'eshkin_krot',
    'mbkhmedia', 'satyrabezsortyra', 'meduzaproject',
    'currenttime', 'svobodaradio', 'novgaz',
    'lentaru', 'echomsk', 'takiedela_ru', 'tj',
    'tvrain', 'orangeeast',
]
posts = []
for group in groups:
    posts.extend(get_posts(group))

with open('posts.json', mode='w', encoding='utf-8') as file:
    json.dump(posts, file)


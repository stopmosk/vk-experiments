import matplotlib.pyplot as plt

from api_vk_functions import *


# Токен нужно получать ежедневно
with open('token.txt') as f:
    token = f.readline().strip()


# Получаем id всех своих друзей
friends_ids = get_friends_ids(token)


# Зависимость количества друзей от id
data = []
for i in range(0, 10000000, 100000):
    cnt = 0
    for el in friends_ids:
        if i <= el < i + 100000:
            cnt += 1
    data.append(cnt)

plt.plot(range(0, 100), data)
plt.ylim(0, 100)
# plt.show()


# Получаем ФИО всех друзей по их id
persons = get_friends_names(token, friends_ids)


# Посчитаем статистику имён
names = {}
for person in persons:
    if person['first_name'] not in names:
        names[person['first_name']] = 1
    else:
        names[person['first_name']] += 1

print('\n10 самых популярных имён среди друзей:')
print(sorted(names.items(), key=lambda item: item[1], reverse=True)[:10])


# Посчитаем статистику фамилий
l_names = {}
for person in persons:
    if person['last_name'] not in l_names:
        l_names[person['last_name']] = 1
    else:
        l_names[person['last_name']] += 1

print('\n10 самых популярных фамилий:')
print(sorted(l_names.items(), key=lambda item: item[1], reverse=True)[:10])


# Получаем айдишники всех групп всех друзей
friends_groups = get_friends_groups_ids(token, friends_ids)


# Удаляем все повторы
unique_groups_ids = set()
for friend in friends_groups:
    unique_groups_ids.update(friend)


# Узнаём названия всех групп по айдишникам
group_names = get_groups_names(token, sorted(list(unique_groups_ids)))
# print(group_names)


# Посмотрим, в каких группах состоит больше всего друзей
groups_counts = {}
for friend in friends_groups:
    for group_id in friend:
        if group_id not in groups_counts:
            groups_counts[group_id] = 1
        else:
            groups_counts[group_id] += 1


# Получим список айдишников моих групп
my_groups_ids = get_groups_ids(token)

# Выкинем группы, в которых я сам состою
not_my_groups = {}
for group in my_groups_ids:
    # print(group)
    if group in groups_counts:
        del groups_counts[group]

# Вывод на экран 50 самых популярных групп среди друзей, где я не состою
print('\n\n50 самых популярных групп среди друзей, где я не состою:')
outputs = True
if outputs:
    s = sorted(groups_counts.items(), key=lambda item: item[1], reverse=True)
    for e in s[:50]:
        print(group_names[str(e[0])], e[1])

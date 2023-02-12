import vk_api
import io
from create_png.image import *
import const
import pandas as pd

vk = vk_api.VkApi(token = const.token) #Авторизоваться как сообщество
upload = vk_api.VkUpload(vk)

#vk.method('messages.send', {'user_id':161556052,'message':'Бот запущен', 'random_id': 0})
blockedUsers = []

def start_bot(url):
	for i in const.admin:
		vk.method('messages.send', {'user_id':i,'message':f'Бот запущен\nURL для подключения {url}', 'random_id': 0})
		
def finish_bot():
	#запись в файл заблокированных пользователей
	with open("./logs/log.csv", "a", encoding="UTF-16") as file: 
		file.write(str(blockedUsers)+'\n')
	pd.read_csv("./logs/log.csv", sep=",", encoding="UTF-16").to_excel("./logs/result.xlsx", index=None)	
	for i in const.admin:
		vk.method('messages.send', {'user_id':i,'message':'Бот остановлен', 'random_id': 0})

def get_id_by_userName(idsAndTags, name_case = 'dat'):
	# получает на вход короткие ссылки и ID пользователей, возвращает user_id и имена в заданном падеже
	# idsAndTags: string (короткие ссылки и ID - слова разделены запятыми)
	# name_case: string (падеж имени - одно из значений: И.п - "nom", Р.п - "gen", Д.п - "dat", В.п - "acc", Т.п - "ins", П.п - "abl")
	# 
	# return:  - список с объектами со свойствами, где прописаны Имена в нужном падеже и ID
	users = vk.method('users.get',{'user_ids': str(idsAndTags), 'name_case': name_case})
	usersList = []

	for user in users:
		usersList.append({
			"user_id" : user["id"],
			"name" : user['first_name'] + ' ' + user['last_name']
		})
	return usersList


def send_valentinka(sender_id, usersList, text_valintinka):
	global blockedUsers
	if sender_id in blockedUsers:
		vk.method("messages.send", {"user_id": sender_id, "message": "Вы заблокированы","random_id": 0})
		return
	if len(usersList) == 0:
		vk.method("messages.send", {
			"user_id": sender_id, 
			"message": 'Упс, я не нашёл в ВК ни одного пользователя с таким ID или коротким именем. Проверьте, пожалуйста, правлиьность написания',
			"random_id": 0
		})
		return

	#
	#	ТУТ ОБРАБОТКА КАРТИНКИ
	#
	img = new_valentinka(text_valintinka)

	img_byte_arr = io.BytesIO()
	img.save(img_byte_arr, format='PNG')
	img_byte_arr.seek(0)
	# 
	# ЗАГРУЗКА ФОТО
	# 

	upload = vk_api.VkUpload(vk)
	photo = upload.photo_messages(img_byte_arr)
	owner_id = photo[0]['owner_id']
	photo_id = photo[0]['id']
	attachment = "photo{}_{}".format(owner_id, photo_id)

	successful_send_names = []	#имена людей, которым дошли валентинки
	fail_send_names = []		#имена людей, которым не дошли валентинки
	
	# 
	# ОТПРАВКА ФОТО
	# 
	for user in usersList:
		try:
			vk.method("messages.send", {"user_id": user['user_id'], "message": "💌 Вам пришла анонимная валентинка!", "attachment": attachment, "random_id": 0})
			successful_send_names.append(user['name'])
		except vk_api.exceptions.ApiError as error:
			if error.code == 901:
				fail_send_names.append(user['name'])

	# 
	# ОТПРАВКА ОТЧЁТА ОТПРАВИТЕЛЮ ВАЛЕНТИНОК
	# 
	text = ''
	if len(successful_send_names) != 0:
		text = text + 'Успешно отправлено '
		for i in range(len(successful_send_names)):
			text += successful_send_names[i]
			if i != len(successful_send_names) - 1:
				text += ', '
		text += '\n\n'
	if len(fail_send_names) != 0:
		text = text + 'Возникла ошибка при отправке валентинок '
		for i in range(len(fail_send_names)):
			text += fail_send_names[i]
			if i != len(fail_send_names) - 1:
				text += ', '
		text += '\n' 
		text += 'Эти' if len(fail_send_names) > 1 else 'Этот'
		text += ' пользовател' + ('и' if len(fail_send_names) > 1 else 'ь')
		text += ' запретил' + ('и' if len(fail_send_names) > 1 else '')
		text += ' отправку сообщений от сообщества Профкома студентов ПсковГУ или ещё ни разу не писал' + ('и' if len(fail_send_names) > 1 else '')
		text += ' сюда.'
	vk.method("messages.send", {"user_id": sender_id, "message": text,"random_id": 0})
		
def blockUser (sender_id, user_ids):
	global blockedUsers
	for user in get_id_by_userName(user_ids, "nom"):
		blockedUsers.append(user["user_id"])

		vk.method('messages.send', {'user_id':user["user_id"],'message':'Вы заблокированы. Н', 'random_id': 0})

		vk.method('messages.send', {'user_id':161556052,'message':f'Пользователь @id{user["user_id"]} ({user["name"]}) заблокирован', 'random_id': 0})
		if sender_id != 161556052:
			vk.method('messages.send', {'user_id':sender_id,'message':f'Пользователь @id{user["user_id"]} ({user["name"]}) заблокирован', 'random_id': 0})



#blockUser(161556052, 161556052)
#send_valentinka(161556052, get_id_by_userName('vladi6008', 'dat'), 'Текст')
# для установки всех ПАКЕТОВ для работы pip install -r requirements.txt
import json
import sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.error import HTTPError
import datetime
from const import ip, port
from vk_bot import get_id_by_userName, send_valentinka, blockUser, finish_bot, start_bot

url = "starting server: http://"+ ip+ ":"+str(port)
start_bot(url)

class RequestHandler(BaseHTTPRequestHandler):

    def do_POST(self):
        try: 
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            self.send_response(200)
            self.end_headers()

            # Сохранение запроса.json в list 
            end_data = json.loads(body)
            end_data['type'] = int(end_data['type'])
            if "sender_id" in end_data:
                end_data["sender_id"] = int(end_data['sender_id'])

              
            print('GET-DATA: ', end_data)
            #создание объекта класса POST для отправки валентинок
            valentinka = PostHandler(end_data)
            valentinka.get_Post()
            
            

            response = {'status': 'success'}
            self.wfile.write(json.dumps(response).encode())
            

        except HTTPError as e:
            print("error POST requests: ", e)
        
    
    def do_GET(self):
   
        # send response status code
        self.send_response(200)

        # send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # write message to client 
        message = "<H3>You are so beutiful ^^ ♡♡♡♡</H3>"
        
        self.wfile.write(bytes(message, "utf16")) 

#обрабатывает входящий POST запрос        
class PostHandler:
    save_log = {} # для записи логов в .csv
    
    def __init__(self, Data_js):
        self.data_js = Data_js
        ids = ''
        id_name = ''
        try:
            for user in get_id_by_userName(self.data_js['user_ids']):
                ids += str(user['user_id'])+'; '
            for user in get_id_by_userName(self.data_js['user_ids']):
                id_name += str(user['name'])+'; '
            self.save_log = {
                'userName': id_name, 
                'id_sender': self.data_js['sender_id'], 
                'text': self.data_js['text'], 
                'id_get':ids 
                }
        except:
            print('Error writing log file')    

    def __str__(self):
        print('json информация: ', self.data_js)

    #__ это private методы доступные только в классе
    def __sendPicture(self):
        date_now = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
        send_valentinka(
            self.data_js['sender_id'], # айди отправителя
            get_id_by_userName(self.data_js['user_ids'], 'dat'), #передача user_list для отправки
            self.data_js['text']
            )
        with open("./logs/log.csv", "a", encoding="UTF-16") as file:
            file.write(f"{date_now}, {self.save_log['userName']}, {self.save_log['id_sender']}, {self.save_log['text'].replace(',', '`')}, {self.save_log['id_get']}\n")

    def __finishBot(self):
        finish_bot()
        sys.exit("Programm finish !!")
    def __userBlock(self):
        blockUser(self.data_js['sender_id'], self.data_js['user_ids'])
        #сохранение инфы о блокированных пользователях
        with open("./logs/block_user.csv", "a", encoding="UTF-16") as file:
            file.write(f"{self.data_js['sender_id']}, {self.data_js['user_ids']}")

    
    #действия в завивисимости от type из запроса
    def get_Post(self):
        #доделат чтобы выбирало type
        if (self.data_js['type'] == 0):
            self.__sendPicture()
        elif(self.data_js['type'] == 1):
            self.__finishBot()
        elif(self.data_js['type'] == 2):
            self.__userBlock()
        elif(self.data_js['type'] == 3):#отправка уникальной валентинки админом 
            print('type 3')
        else:
            print('not found type')

    

    


if __name__ == '__main__':         
    httpd = HTTPServer((ip, port), RequestHandler)
    print(url) #ссылка чтобы вставить вк бота для отправки json запросов
    
    httpd.serve_forever()
    

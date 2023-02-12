import requests

url = 'http://192.168.0.104:8080/'    
data = ({
	"type" : 1,
	"sender_id" : 161556052, #int - ID отправителя
	"user_ids" : "hello_id",  #string - строка с ID и Тегами получателей
	"text" : "ахуенно" #string - текст валентинки 
    }  
    )
    
res = requests.post(url, json=data)
print("Запрос отправлен: ", res)
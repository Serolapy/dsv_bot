from PIL import Image, ImageDraw, ImageFont
import textwrap

def splitText(text, max_width):
	#разбиение на строки, если были переносы
	rows = text.split("\n")
	#разбиение на слова
	for k in range(len(rows)):
		rows[k] = "\n".join(textwrap.wrap(rows[k], width=max_width))
	return "\n".join(rows)


def new_valentinka(text):
	kolvo_simv = len(text)
	textSize = 0

	#выбираем размер шрифта
	if kolvo_simv <= 60:
		# только тут надо, чтобы все слова были <= 10 символов
		max10simv = True
		for word in text.split():
			if len(word) > 10:
				max10simv = False
				break
		if max10simv and len(splitText(text, 10).split('\n')) <= 6:
			textSize = 79
			text = splitText(text, 10)
	if textSize == 0 and kolvo_simv <= 126:
		if len(splitText(text, 15).split('\n')) <= 9:
			textSize = 55
			text = splitText(text, 15)

	if textSize == 0:
		textSize = 35
		text = splitText(text, 23)

	img = Image.open("valentinka.png") 
	draw = ImageDraw.Draw(img)
	font = ImageFont.truetype("Old-Soviet.otf", textSize) 
	color = (227, 47, 43)  
	position = (425, 353 - textSize * len(text.split('\n')) / 2) 
	align = "center"  
	draw.multiline_text(position, text, fill=color, font=font, align=align)  
	return img
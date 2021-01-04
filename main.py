import sys
from sys import argv
# Импортируем наш интерфейс
from form import *
from PyQt5 import QtCore, QtGui, QtWidgets
import random
import requests
import telebot
import time
# проверка на простое число

#основный класс программы
class MyWin(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        try:
            with open('config.txt','r',encoding="utf-8") as config:
                nast=config.read().split('\n')
                self.ui.textEdit.setText(nast[0])
                self.ui.textEdit_2.setText(nast[3])
                self.ui.textEdit_3.setText(nast[2])
                self.ui.textEdit_4.setText(nast[1])
        except:
            pass
            #print(nast)
        self.ui.pushButton.clicked.connect(self.post)


    def post(self):
        with open('config.txt','w',encoding="utf-8") as config:
            tokenT=self.ui.textEdit_4.toPlainText()
            tokenVK =self.ui.textEdit.toPlainText()
            self.chat_id=self.ui.textEdit_3.toPlainText()
            domain = self.ui.textEdit_2.toPlainText().split()
            config.write(tokenVK+'\n')
            config.write(tokenT+'\n')
            config.write(self.chat_id+'\n')
            config.write(" ".join(domain))
        self.globdate=0
        self.First=True
        self.bot = telebot.TeleBot(tokenT)
        try:
            for i in domain:
                self.get_text_messages(i,tokenVK)
        except:
            em = QtWidgets.QErrorMessage(self)
            em.showMessage("Не те данные")
            em.setStyleSheet("color: rgb(55, 177, 244);")

    def get_text_messages(self,domains,tokenVK):
            ver = 5.103
            sait = 'https://api.vk.com/method/wall.get'
            count=self.ui.spinBox.value()
            response = requests.get(sait,
                                    params={'access_token': tokenVK, 'v': ver, 'domain': domains, 'count': count})
            data = response.json()['response']['items']
            with open("bd1.txt",'r+') as bd:
                date=int(bd.read())
                if self.First:
                    self.globdate=date
                    First=False
                if data[1]['date']>date or data[0]['date']>date :
                    bd.seek(0)
                    bd.truncate()
                    bd.write(str(max(data[1]['date'],data[0]['date'])))
            data=data[::-1]
            for i in data:
                if i['date']>self.globdate:
                    time.sleep(5)
                    self.obra(i,-1)
                else:
                    pass

    def obra(self,i,imsize):
        try:
            dano=[]
            dlina = len(i['attachments'])
            if dlina==1 and i['attachments'][0]["type"]=='photo':
                if self.ui.checkBox.isChecked():
                    self.bot.send_photo(self.chat_id, i['attachments'][0]['photo']['sizes'][imsize]['url'],caption=i['text'].split('#')[0])
                else:
                    self.bot.send_photo(self.chat_id, i['attachments'][0]['photo']['sizes'][imsize]['url'])
                return
            for j in range(dlina):
                if i['attachments'][j]["type"]!='photo':
                    continue
                if j==0 and self.ui.checkBox.isChecked():
                    dano.append(telebot.types.InputMediaPhoto(i['attachments'][j]['photo']['sizes'][imsize]['url'],caption=i['text'].split('#')[0]))
                else:
                    dano.append(telebot.types.InputMediaPhoto(i['attachments'][j]['photo']['sizes'][imsize]['url']))
            print(dano)
            self.bot.send_media_group(self.chat_id,dano)
        except:
            return




#Инициализация программы
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())

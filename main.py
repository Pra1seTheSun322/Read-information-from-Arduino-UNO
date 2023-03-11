from threading import Thread

from kivy.app import App
from kivy.lang.builder import Builder
from kivy.graphics.svg import Window
from kivy.uix.floatlayout import FloatLayout

import serial
from serial import Serial
from serial.tools import list_ports

#Внешний вид приложения
KV = '''
box:    
    orientation:'horizontal'
    canvas:
        Color:
            rgba:1,1,1,1
        Rectangle:
            pos:self.pos
            size:self.size  
    id:MainWidget
    Label:
        id:lb
        color:0,0,0,1
        text:'Info from port Arduino UNO'   
        size_hint:None, None
        size:200,200
        pos_hint: {'center': (.5, .8)} 
    Button:
        size_hint:None, None
        size:200,44
        pos_hint: {'center': (.5, .2)}
        text:'Get Text from arduino'
        on_release:MainWidget.ReadFromArduino()     
    Spinner:
        id:sp
        size_hint: None, None
        size: 100, 44
        pos_hint: {'center': (.5, .5)}
        text: 'Ports'
        values: ' '
        on_press:MainWidget.threaded_func()

'''
#Уставка размера окна
Window.size = (600, 400)


class box(FloatLayout):
    def threaded_func(self): #Сканирование портов подключенных к ПК
        ports = list_ports.comports()
        for p in ports:
            i = 0
            d = p.device
            self.ids['sp'].values[i] = p.device
            i = i + 1


    def ReadFromArduino(self): #Запуска потока с функцией "Status"
        t = Thread(target=self.status, daemon=True)
        t.start()


    def status(self): #Функция для считывания информации с порта Arduino
        try:
            Arduino = Serial(self.ids['sp'].text, 9600)
            data = (Arduino.readline().decode('ascii'))
            self.ids['lb'].text = data
        except serial.serialutil.SerialException:
            self.ids['lb'].text = 'No found'



class MainApp(App): #Вызов всей оболочки
    def build(self):
        return Builder.load_string(KV)


MainApp().run() #Запуск приложения

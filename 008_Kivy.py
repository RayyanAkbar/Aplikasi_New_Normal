import kivy
from kivy.app import App
from kivy.uix.label import Label
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.uix.popup import Popup
import csv
import pandas as pd
import smtplib
import pymongo
from pymongo import MongoClient

# Window.clearcolor = (1,1,1,1)

class Login(Screen):
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    def masuk(self):
        cluster = MongoClient(
            "mongodb+srv://Rayyan:tidung@cluster0.0xv8i.mongodb.net/Project3?retryWrites=true&w=majority")
        db = cluster["Project3"]
        collection = db["Akun"]
        email = self.email.text
        password = self.password.text
        cari = collection.find_one({"Email":email})
        pasw = cari["Password"]
        if self.password.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            if password == pasw:
                sm.current = "utama"
            else:
                invalidLogin()
        else:
            invalidForm()



class Buat(Screen):
    namee = ObjectProperty(None)
    email = ObjectProperty(None)
    password = ObjectProperty(None)
    def buat(self):
        cluster = MongoClient(
            "mongodb+srv://Rayyan:tidung@cluster0.0xv8i.mongodb.net/Project3?retryWrites=true&w=majority")
        db = cluster["Project3"]
        collection = db["Akun"]
        if self.namee.text != "" and self.email.text != "" and self.email.text.count(
                "@") == 1 and self.email.text.count(".") > 0:
            name = self.namee.text
            emaill = self.email.text
            pasw = self.password.text
            post = {"Username":name,"Email": emaill, "Password": pasw}
            collection.insert_one(post)
            self.reset()
            sm.current ="konfir"

        else:
            invalidForm()
    def reset(self):
        self.namee.text = ""
        self.email.text = ""
        self.password.text = ""

class Konfirmasi(Screen):
    pass
class Konfirmasi1(Screen):
    pass

class WindowUtama(Screen):
    provinsi = ObjectProperty(None)
    kabupaten = ObjectProperty(None)

    def tempat(self):
        cek = pd.read_csv("DataPB.csv")
        prov = cek["Provinsi"]
        kab = cek["Kabupaten"]
        provinsi = self.provinsi.text
        kabupaten = self.kabupaten.text
        if self.provinsi.text != "" and self.kabupaten.text != "":
            for i in prov:
                if i == provinsi:
                    for k in kab:
                        if k == kabupaten:
                            sm.current = "ketiga"
                        else:
                            invalidKab()
                else:
                    invalidKab()
        else:
            invalidKab()

class Menu(Screen):
    pass

class WindowKedua(Screen):
    pass

class WindowKetiga(Screen):
    email = ObjectProperty(None)
    tempat = ObjectProperty(None)
    def pesan(self):
        cluster = MongoClient(
            "mongodb+srv://Rayyan:tidung@cluster0.0xv8i.mongodb.net/Project3?retryWrites=true&w=majority")
        db = cluster["Project3"]
        collection = db["DataBase"]
        nama = self.tempat.text
        a = collection.find_one({"Nama":nama})
        c = a["jumlah"]
        if c <= 100:
            pesan = '''[INFORMASI PUSAT PERBELANJAAN A]
            Protokol Kesehatan :
            1. Memakai masker bagi pengunjung
            2. Menerapkan physical / sosial distancing antar pengunjug
            3. Tidak berdesakan
            4. Selalu patuhi arahan petugas
            5. Menyiapkan pembayaran non-tunai
            Saat ini jumlah pengunjung di Mall A berada pada rentang 0 - 100 orang yang terkategorikan Hijau'''
        if c > 100 and c <= 160:
            pesan = '''[INFORMASI PUSAT PERBELANJAAN A]
            Protokol Kesehatan :
            1. Memakai masker bagi pengunjung
            2. Menerapkan physical / sosial distancing antar pengunjug
            3. Tidak berdesakan
            4. Selalu patuhi arahan petugas
            5. Menyiapkan pembayaran non-tunai
               Saat ini jumlah pengunjung di Mall A berada pada rentang 100 - 160 orang yang terkategorikan Kuning'''
        if c > 160:
            pesan = '''[INFORMASI PUSAT PERBELANJAAN A]
            Protokol Kesehatan :
            1. Memakai masker bagi pengunjung
            2. Menerapkan physical / sosial distancing antar pengunjug
            3. Tidak berdesakan
            4. Selalu patuhi arahan petugas
            5. Menyiapkan pembayaran non-tunai
            Saat ini jumlah pengunjung di Mall A berada pada rentang > 160 orang yang terkategorikan Merah'''
        sender = "rayyanakbari5@gmail.com"
        ke = self.email.text
        pas = "tidung54321"
        server = smtplib.SMTP("smtp.gmail.com", 587)
        server.starttls()
        server.login(sender, pas)
        server.sendmail(sender, ke, pesan)
        print("pengiriman sukses")

class WindowManager(ScreenManager):
    pass

def invalidForm():
    pop = Popup(title='Data Tidak Valid',
                  content=Label(text='Tolong Masukkan Data yang Benar.'),
                  size_hint=(None, None), size=(300, 400))
    pop.open()

def invalidLogin():
    pop = Popup(title='Akun Error',
                  content=Label(text='Email dan Password Salah.'),
                  size_hint=(None, None), size=(300, 400))
    pop.open()

def invalidKab():
    pop = Popup(title='Provinsi / Kabupaten Tidak di Temukan',
                  content=Label(text='Tolong Masukkan Provinsi / Kabupaten yang Benar.'),
                  size_hint=(None, None), size=(500, 300))
    pop.open()

kv  = Builder.load_file('ku.kv')
sm = WindowManager()
screens = [Login(name="login"),Buat(name="buat"),Konfirmasi(name="konfir"),Konfirmasi1(name="konfir1"),Menu(name="menu"),WindowUtama(name="utama"),WindowKedua(name="kedua"),WindowKetiga(name="ketiga")]
for screen in screens:
    sm.add_widget(screen)
sm.current = "login"

class KuApp(App):
    def build(self):
        return sm


if __name__== "__main__":
    KuApp().run()


#     nama = ObjectProperty(None)
#     email = ObjectProperty(None)
#
#     def button(self):
#         print("Nama Pengguna:", self.nama.text,"Email:", self.email.text)
#         self.nama.text = ""
#         self.email.text = ""
    #
    #
    # # def __init__(self, **kwargs):
    # #     super(MyGrid,self).__init__(**kwargs)
    # #
    # #     self.cols = 1
    # #
    # #     self.inside = GridLayout ()
    # #     self.inside.cols = 2
    # #
    # #     self.inside.add_widget(Label(text="Nama Pengguna :"))
    # #     self.nama = TextInput(multiline=False)
    # #     self.inside.add_widget(self.nama)
    # #
    # #     self.inside.add_widget(Label(text="Alamat Email :"))
    # #     self.email = TextInput(multiline=False)
    # #     self.inside.add_widget(self.email)
    # #
    # #     self.add_widget(self.inside)
    # #
    # #
    # #     self.submit = Button(text='Cari', font_size=40)
    # #     self.submit.bind(on_press=self.pressed)
    # #     self.add_widget(self.submit)
    # #
    # # def pressed(self, instance):
    # #     nama = self.nama.text
    # #     email = self.email.text
    # #
    # #     print("Nama:", nama, "Email:", email)
    # #
    # #     self.nama.text = ""
    # #     self.email.text = ""


# class MyApp(App):
#     def build(self):
#         return


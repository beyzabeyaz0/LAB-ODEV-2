# -*- coding: ISO-8859-9 -*-
# Yukar�daki sat�r SyntaxError: Non-UTF-8 code starting with '\xf6' in file b�yle bir hata sebebiyle eklendi.

#AYB�KE T�R�D� 220502005 EL�F BEYZA BEYAZ 220502033
# B�LG�SAYAR PROGRAMLAMA LAB-2 �DEV-2

import csv

class Tir:
    def __init__(self,gelis_zamani,tir_plakasi, ulke, ton_20_adet, ton_30_adet, yuk_miktari,maliyet):  # olaylar.csv parametreleri
        self.gelis_zamani = gelis_zamani
        self.tir_plakasi = tir_plakasi[-3:]
        self.ulke = ulke
        self.ton_20_adet = int(ton_20_adet)
        self.ton_30_adet = int(ton_30_adet)
        self.yuk_miktari = int(yuk_miktari)
        self.maliyet = maliyet
class Gemi:
    def __init__(self, gelis_zamani, gemi_adi, kapasite,gidecek_ulke):  # gemiler.csv parametreleri
        self.gelis_zamani = gelis_zamani
        self.gemi_adi = gemi_adi
        self.yuk_durumu = 0  # Kapasite dolumunu kontrol etmek amac�yla ba�lang�� de�eri belirledik.
        self.kapasite = int(kapasite)
        self.gidecek_ulke = gidecek_ulke

class LimanOtomasyonu:
    def __init__(self, tir, gemi):
        self.tirlar = self.tir_degerleri(tir)
        self.gemiler = self.gemi_degerleri(gemi)
        self.yukle()

    def tir_degerleri(self, dosya):
        tirlar = []
        with open(dosya, 'r', newline='', encoding='ISO-8859-9') as file:
            reader = csv.reader(file)
            next(reader)  # ilk sat�rda verilerin isimleri yazd��� i�in buray� atlamak ama�l�
            for row in reader:
                tirlar.append(Tir(row[0], row[1], row[2],row[3],row[4],row[5],row[6]))
        return sorted(tirlar, key=lambda x: x.tir_plakasi)

    def gemi_degerleri(self, dosya):
        gemiler = []
        with open(dosya, 'r', newline='', encoding='ISO-8859-9') as file:
            reader = csv.reader(file)
            next(reader)  # ilk sat�rda verilerin isimleri yazd��� i�in buray� atlamak ama�l�
            for row in reader:
                gemiler.append(Gemi(row[0], row[1],row[2],row[3]))
        return sorted(gemiler, key=lambda x: x.gemi_adi)

    def yukle(self):  # Y�KLEME-�ND�RME ��LEMLER� FONKS�YONU

                            # TIRLARDAK� TON ADET SAYILARINA G�RE �ST�F ALANLARINA Y�K BIRAKMA DURUMU
        istif_alani1 = []
        istif_alani2 = []
        istif_kapasitesi = 750
        for tir in self.tirlar:
            if tir.ton_20_adet == 1:  # Ton adetinin 1 ve 0 olma durumuna g�re ka� ton y�k y�klenece�ini �eken ko�ulland�rmalar
                if sum(istif_alani1) + 20 <= istif_kapasitesi:
                    istif_alani1.append(20)
                elif sum(istif_alani2) + 20 <= istif_kapasitesi:
                    istif_alani2.append(20)
                else:
                    print("�stif alanlar� dolmu�tur!")
                    break
            if tir.ton_30_adet == 1:
                if sum(istif_alani1) + 30 <= istif_kapasitesi:
                    istif_alani1.append(30)
                elif sum(istif_alani2) + 30 <= istif_kapasitesi:
                    istif_alani2.append(30)
                else:
                    print("�stif alanlar� dolmu�tur!")
                    break

                                            # TIRLARDAN GEM�LERE Y�KLEME DURUMU
        for tir in self.tirlar:
            for gemi in self.gemiler:
                if tir.ulke == gemi.gidecek_ulke:  # �lkeleri e�le�en t�r ve gemiler y�klenir
                    print(f"T�r {tir.tir_plakasi} y�k indiriyor...")
                    if gemi.yuk_durumu + tir.yuk_miktari > 0.95 * gemi.kapasite:  # Y�k geminin kapasitesini a�ma durumu
                        dolma_durumu = int(0.95 * gemi.kapasite) - gemi.yuk_durumu  # 95'ini hesaplar
                        if dolma_durumu > 0:  # Miktar y�zde 95'inden fazla ise gemi ayr�l�r.
                            tir.yuk_miktari = tir.yuk_miktari - dolma_durumu
                            gemi.yuk_durumu = gemi.yuk_durumu + dolma_durumu
                            print(f"{gemi.gemi_adi}.s�ra numaral� gemi kapasitesini doldurdu.Limandan ayr�l�yor. Y�k durumu: {gemi.yuk_durumu}")
                    else:
                        gemi.yuk_durumu += tir.yuk_miktari  # T�rda kalan y�klerin aktar�lma durumu
                        print(f"{gemi.gemi_adi}.s�ra numaral� gemi y�k durumu: {gemi.yuk_durumu}")
                        break  # e�er t�rda y�k bittiyse break ile y�k alma bitirilir.

                        # HER GEM� VE TIR ���N S�ZL�K DE��KEN� OLU�TURMA VE VER�LERE ULA�MA �RNEKLER�
        tir_sozluk = {tir.tir_plakasi: {"Geli� zaman�":tir.gelis_zamani,"�lke": tir.ulke,"Y�k miktar�": tir.yuk_miktari,"20 tonluk konteyn�r adeti": tir.ton_20_adet,"30 tonluk konteyn�r adeti": tir.ton_30_adet, "Maliyet":tir.maliyet} for tir in self.tirlar}
        gemi_sozluk = {gemi.gemi_adi: {"Geli� zaman�":gemi.gelis_zamani,"Gidece�i �lke": gemi.gidecek_ulke,"Y�k durumu": gemi.yuk_durumu,"Kapasite": gemi.kapasite} for gemi in self.gemiler}
        # Kullan�m
        bilgi = input("Hangi arac�n bilgisine eri�mek istersiniz? (TIR,GEMI)")
        if bilgi == "TIR":
            plaka = input("T�r plakas� giriniz:")
            if plaka in tir_sozluk:
                print(f"T�r Bilgileri: {tir_sozluk[plaka]}")
            else:
                print(f"{plaka} plakal� t�r bulunamad�.")
        elif bilgi == "GEMI":
            gemi_adi = input("Geminin ad�n� giriniz:")
            if gemi_adi in gemi_sozluk:
                print(f"Gemi Bilgileri: {gemi_sozluk[gemi_adi]}")
            else:
                print(f"{gemi_adi} s�ral� gemi bulunamad�.")
        else:
            print("D�zg�n bir ifade girin.")


tir_dosya = 'olaylar.csv'
gemi_dosya = 'gemiler.csv'
calistirici = LimanOtomasyonu(tir_dosya, gemi_dosya)


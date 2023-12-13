# -*- coding: ISO-8859-9 -*-
# Yukarıdaki satır SyntaxError: Non-UTF-8 code starting with '\xf6' in file böyle bir hata sebebiyle eklendi.

#AYBÜKE TÜRİDİ 220502005 ELİF BEYZA BEYAZ 220502033
# BİLGİSAYAR PROGRAMLAMA LAB-2 ÖDEV-2

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
        self.yuk_durumu = 0  # Kapasite dolumunu kontrol etmek amacıyla başlangıç değeri belirledik.
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
            next(reader)  # ilk satırda verilerin isimleri yazdığı için burayı atlamak amaçlı
            for row in reader:
                tirlar.append(Tir(row[0], row[1], row[2],row[3],row[4],row[5],row[6]))
        return sorted(tirlar, key=lambda x: x.tir_plakasi)

    def gemi_degerleri(self, dosya):
        gemiler = []
        with open(dosya, 'r', newline='', encoding='ISO-8859-9') as file:
            reader = csv.reader(file)
            next(reader)  # ilk satırda verilerin isimleri yazdığı için burayı atlamak amaçlı
            for row in reader:
                gemiler.append(Gemi(row[0], row[1],row[2],row[3]))
        return sorted(gemiler, key=lambda x: x.gemi_adi)

    def yukle(self):  # YÜKLEME-İNDİRME İŞLEMLERİ FONKSİYONU

                            # TIRLARDAKİ TON ADET SAYILARINA GÖRE İSTİF ALANLARINA YÜK BIRAKMA DURUMU
        istif_alani1 = []
        istif_alani2 = []
        istif_kapasitesi = 750
        for tir in self.tirlar:
            if tir.ton_20_adet == 1:  # Ton adetinin 1 ve 0 olma durumuna göre kaç ton yük yükleneceğini çeken koşullandırmalar
                if sum(istif_alani1) + 20 <= istif_kapasitesi:
                    istif_alani1.append(20)
                elif sum(istif_alani2) + 20 <= istif_kapasitesi:
                    istif_alani2.append(20)
                else:
                    print("İstif alanları dolmuştur!")
                    break
            if tir.ton_30_adet == 1:
                if sum(istif_alani1) + 30 <= istif_kapasitesi:
                    istif_alani1.append(30)
                elif sum(istif_alani2) + 30 <= istif_kapasitesi:
                    istif_alani2.append(30)
                else:
                    print("İstif alanları dolmuştur!")
                    break

                                            # TIRLARDAN GEMİLERE YÜKLEME DURUMU
        for tir in self.tirlar:
            for gemi in self.gemiler:
                if tir.ulke == gemi.gidecek_ulke:  # Ülkeleri eşleşen tır ve gemiler yüklenir
                    print(f"Tır {tir.tir_plakasi} yük indiriyor...")
                    if gemi.yuk_durumu + tir.yuk_miktari > 0.95 * gemi.kapasite:  # Yük geminin kapasitesini aşma durumu
                        dolma_durumu = int(0.95 * gemi.kapasite) - gemi.yuk_durumu  # 95'ini hesaplar
                        if dolma_durumu > 0:  # Miktar yüzde 95'inden fazla ise gemi ayrılır.
                            tir.yuk_miktari = tir.yuk_miktari - dolma_durumu
                            gemi.yuk_durumu = gemi.yuk_durumu + dolma_durumu
                            print(f"{gemi.gemi_adi}.sıra numaralı gemi kapasitesini doldurdu.Limandan ayrılıyor. Yük durumu: {gemi.yuk_durumu}")
                    else:
                        gemi.yuk_durumu += tir.yuk_miktari  # Tırda kalan yüklerin aktarılma durumu
                        print(f"{gemi.gemi_adi}.sıra numaralı gemi yük durumu: {gemi.yuk_durumu}")
                        break  # eğer tırda yük bittiyse break ile yük alma bitirilir.

                        # HER GEMİ VE TIR İÇİN SÖZLÜK DEĞİKENİ OLUŞTURMA VE VERİLERE ULAŞMA ÖRNEKLERİ
        tir_sozluk = {tir.tir_plakasi: {"Geliş zamanı":tir.gelis_zamani,"Ülke": tir.ulke,"Yük miktarı": tir.yuk_miktari,"20 tonluk konteynır adeti": tir.ton_20_adet,"30 tonluk konteynır adeti": tir.ton_30_adet, "Maliyet":tir.maliyet} for tir in self.tirlar}
        gemi_sozluk = {gemi.gemi_adi: {"Geliş zamanı":gemi.gelis_zamani,"Gideceği ülke": gemi.gidecek_ulke,"Yük durumu": gemi.yuk_durumu,"Kapasite": gemi.kapasite} for gemi in self.gemiler}
        # Kullanım
        bilgi = input("Hangi aracın bilgisine erişmek istersiniz? (TIR,GEMI)")
        if bilgi == "TIR":
            plaka = input("Tır plakası giriniz:")
            if plaka in tir_sozluk:
                print(f"Tır Bilgileri: {tir_sozluk[plaka]}")
            else:
                print(f"{plaka} plakalı tır bulunamadı.")
        elif bilgi == "GEMI":
            gemi_adi = input("Geminin adını giriniz:")
            if gemi_adi in gemi_sozluk:
                print(f"Gemi Bilgileri: {gemi_sozluk[gemi_adi]}")
            else:
                print(f"{gemi_adi} sıralı gemi bulunamadı.")
        else:
            print("Düzgün bir ifade girin.")


tir_dosya = 'olaylar.csv'
gemi_dosya = 'gemiler.csv'
calistirici = LimanOtomasyonu(tir_dosya, gemi_dosya)


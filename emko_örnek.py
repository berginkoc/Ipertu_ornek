from pyModbusTCP.client import ModbusClient

ayrac1 = "=========="
ayrac2 = "----------"
# Konfigürasyon:
# Port: 3501 - Device ID 1: SGN4P1-00-00-00-00_1 - Ethernet Gateway
# Port: 3501 - Device ID 2: SMR1P1-01-00-00-00   - Input Modülü
# Port: 3501 - Device ID 3: SMR1P1-00-00-01-00_1 - Output Modülü

# Port: 3502 - Device ID 1: RS485 1. Port

# Modbus -1 adresli

def emko_uzak_io_ornek_program():
    # Modbus bağlantı hattının tanımlanması:
    c = ModbusClient(host="192.168.0.64", auto_open=True, auto_close=False)
    d = 0
    while True:
        try:
            print(ayrac1)
            print("Döngü Başı")

            # Modbus port ve Device ID(Unit ID) ayarlarının atanması:
            c.port = 3501

            # Modbus device id ayarlarının yapılması - Output modülü
            c.unit_id = 2

            # https://www.emkoelektronik.com.tr/tr/urunler/16-xdijital-girisli-genisleme-modulu
            # Datasheet syf:27 - 40011 R Dijital Girişler Dijital girişlerin durumunu bitsel olarak gösterir.
            # 40011 hedef adres Modbus -1 adresli olduğu için adres bilgisi:10, uzunluk 1
            # Input modülünden verinin okunması
            a = c.read_holding_registers(10, 1)

            # Okunan verilerin binary formatında gösterimi
            snc = bin(a[0])
            print("Read register Sonuç: ", snc, len(snc), c.port)
            sifir_uzn = "0" * (10 - len(snc))
            snc = "0b" + sifir_uzn + snc[-(len(snc) - 2):]
            print("Binary gösterimi:", snc)
            # 0. Input tetiklendiğinde değişkeni arttır.
            if snc[-1] == "1":
                d = d + 1
            # 1. input tetiklendiğinde değişkeni düşür.
            if snc[-2] == "1":
                d = d - 1
            print(ayrac2)

            # Modbus device id ayarlarının yapılması - Output modülü
            c.unit_id = 3

            # Değişken değeri 0'dan büyük ise yazdır.
            if d >= 0:
                # https://www.emkoelektronik.com.tr/tr/urunler/15-xtransistor-cikisli-genisleme-modulu
                # Datasheet syf:30 - 40011 R/W Dijital Çıkışlar Dijital çıkışlarının durumunu bitsel olarak gösterir.
                # 40011 hedef adres Modbus -1 adresli olduğu için adres bilgisi:10, uzunluk 1
                # Output modülüne veri aktarılması
                c.write_single_register(10, d)
                print("Output modülüne yazılan değer:", d)
            else:
                d = 0
            print(ayrac2)
            # Modbus RTU 1. port'a bağlı cihaz içerisinden veri almak için port ve device id ayarı:
            c.port = 3502
            c.unit_id = 1

            # Modbus RTU 1. port üzerine bağlı ürün içerisinden verinin çekilmesi.
            # Bu programda 7. adres üzerinden veri çekildi.
            okunan_veri = c.read_holding_registers(6, 1)
            print("oku:", okunan_veri)
            print(ayrac1)

        except Exception as e:
            print(e)


if __name__ == "__main__":
    emko_uzak_io_ornek_program()

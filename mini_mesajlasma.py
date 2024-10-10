from tkinter import *
import socket
import threading

host = "172.27.46.67"
port1 = 50006
port2 = 50007

client_socket = None

def gonder():
    global client_socket, entry1
    message = entry1.get()
    if message:  # Mesajın boş olmadığını kontrol et
        try:
            client_socket.send(message.encode())  # Mesajı sunucuya gönder
            entry1.delete(0, END)  # Mesaj gönderildikten sonra giriş alanını temizle
        except BrokenPipeError:
            print("Bağlantı kapandı, mesaj gönderilemedi.")
        except Exception as e:
            print(f"Bir hata oluştu: {e}")

def baglanti():
    global client_socket
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port1))  # Sunucuya bağlan
        print("Bağlantı kuruldu.")
    except Exception as e:
        print(f"Bağlantı hatası: {e}")

def dinle():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind((host, port2))
    server_socket.listen()

    conn, addr = server_socket.accept()
    print("Bağlanan:", str(addr))

    while True:
        try:
            data = conn.recv(1024).decode()  # Mesajı al
            if not data:
                print("Bağlantı kesildi.")
                break
            print("Alınan:", data)
            response_data = "Mesaj alındı"
            conn.send(response_data.encode())  # Yanıt gönder
            # Gelen mesajları liste kutusunda göster
            list.insert(END, "Gelen mesaj: " + data)
        except Exception as e:
            print(f"Dinleme hatası: {e}")
            break

def baslat():
    baglanti()  # Önce bağlantıyı başlat
    # GUI elemanları: Giriş kutusu ve gönderme butonu
    global entry1
    label1 = Label(pencere1, text="Mesajını buraya yaz:")
    label1.place(x=100, y=100)
    label1.config(bg="grey")
    entry1 = Entry(pencere1)
    entry1.place(x=100, y=150)
    buton1 = Button(pencere1, text="Göndermek için tıkla", bg="grey", command=gonder)
    buton1.place(x=100, y=200)

    # Mesaj dinleme iş parçacığını başlat
    t2 = threading.Thread(target=dinle)
    t2.daemon = True  # Ana program kapanınca iş parçacığını da kapat
    t2.start()

# Tkinter pencere ayarları
pencere1 = Tk()
pencere1.geometry("1500x600")
pencere1.title("Mini Mesajlaşma Uygulaması")
frame1 = Frame(pencere1, bg="grey", width=750, height=600)
frame1.place(x=0, y=0)

# Gelen mesajları göstermek için liste kutusu
label2 = Label(pencere1, text="Mesajlarını burdan gör:")
label2.place(x=850, y=100)
list = Listbox(pencere1, width=50, height=20)
list.place(x=850, y=200)

# Bağlanma butonu
buton1 = Button(pencere1, text="Bağlanmak için tıkla", command=baslat)
buton1.pack()

pencere1.mainloop()
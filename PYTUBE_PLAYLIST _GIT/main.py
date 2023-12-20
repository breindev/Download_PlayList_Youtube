from ctypes import windll
from BlurWindow.blurWindow import GlobalBlur # pip instalar BlurWindow
# from tkinter.ttk import*
from tkinter import ttk
from tkinter import*
from pytube import * #pip install pytube
import threading
from time import sleep
main = Tk()
main.title("BRELoad")
main.config(bg="green")
main.resizable(0,0)
main.attributes("-transparent","green")
main.update()
hWnd = windll.user32.GetForegroundWindow()
GlobalBlur(hWnd)

estado = StringVar() # ESTADO DE LA DESCARGA
FRAME_MAIN = Frame(main,bg="green");FRAME_MAIN.pack(ipadx=10,pady=10)
MENSAJE = Label(FRAME_MAIN,bg="green",fg="white",font=("arial",12,"bold"))
MENSAJE.pack()

Label(FRAME_MAIN,text="▶ YouTube",fg="white",bg="red",
                font=("arial",12,"bold")).pack(ipadx=10,ipady=10)
Label(FRAME_MAIN,text="PEGA EL LINK DEL PLAYLIST:",bg="green",font=("arial",12,"bold"),fg="white").pack(pady=(20,0))
LINK = Entry(FRAME_MAIN,width=50,relief=SOLID,
                        highlightthickness=2,highlightcolor="white")
LINK.pack(ipady=5)
LINK.focus_set()
Lista_Saved= ttk.Treeview(columns=("a","b"),selectmode="none",show="headings")
Lista_Saved.heading('#1', text='TÍTULO', anchor='center')
Lista_Saved.heading('#2', text='DURACIÓN', anchor='center')
Lista_Saved.column('a', anchor='left', width=300)
Lista_Saved.column('b', anchor='center', width=80)
Lista_Saved.pack()
def mensaje():
    LINK.config(state=DISABLED);DOWNLOAD.config(state=DISABLED)
    sms = "Descargando"
    pivot = True
    while len(estado.get()) == 0:
        if pivot:
            sms+=" ."
            if len(sms) == 17: pivot = False
        else:
            sms = sms[:-2]
            if len(sms) == 11: pivot = True
        MENSAJE.config(text=sms)
        sleep(1/2)
    LINK.config(state=NORMAL);DOWNLOAD.config(state=NORMAL)
    LINK.delete(0,"end")
    
def hilo(link):
    h1 = threading.Thread(target=mensaje)
    h1.start()
    def descarga(link):
        def datos_de_video(yt):
            nombre = yt.title # TITULO DEL VIDEO
            duracion = yt.length #SEGUNDOS
            return nombre,duracion
        if len(link) != 0:
            p = Playlist(link)
            links = p.video_urls
            for url in links:
                try: 
                    DATOS = datos_de_video(YouTube(url))
                    nombre_limpio = DATOS[0]
                    yt = YouTube(url).streams.get_highest_resolution()
                    yt.download(filename=f"{nombre_limpio}.mp4")
                    for i in '\/:*?"<>|~,': #ELIMINA CARACTERES NO PERMITIDOS POR WINDOWS
                        nombre_limpio = nombre_limpio.replace(i,"")
                    Lista_Saved.insert("",'end',iid=url,values=(DATOS[0],f"{DATOS[1]}s"))
                except(Exception):
                    Lista_Saved.insert("",'end',open=True,values=("VIDEO CON RESTRICCION DE EDAD","+18"))
            MENSAJE.config(text="Video descargado !")
            estado.set("¡ PLAYLIST DESCARGADO CON ÉXITO !")
        else:
            MENSAJE.config(text="Se produjo un error al descargar!")
            estado.set("¡ ERROR !")
    estado.set("")
    h2 = threading.Thread(target=descarga,args=(link,))
    h2.start()
DOWNLOAD = Button(FRAME_MAIN,text="DESCARGAR ▼",
                bg="lightgreen",cursor="hand2",command=lambda:hilo(LINK.get()))
DOWNLOAD.pack(pady=(20,0))
main.mainloop()

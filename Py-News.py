from bs4 import BeautifulSoup
from tkinter import *
import urllib.parse
from PIL import Image, ImageTk
import io
import re
from tkinter import ttk
import threading
import requests

root = Tk()
root.config(bg="white")
root.title("Py-News--Rohit")
root.geometry('950x600')
root.wm_iconbitmap('icone.ico')
#--to style Button--------------------------

style = ttk.Style()
style.map("C.TButton",
    foreground=[('pressed', 'red'), ('active', 'blue')],
    background=[('pressed', '!disabled', 'black'), ('active', 'white')]
    )
style.configure('TButton', font = 
               ('calibri',20, 'bold'), 
                    borderwidth = '1')
#----------------------------------------
#------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------

def display(frame):
    try:
        source=requests.get("https://inshorts.com/en/read").text
        soup=BeautifulSoup(source,'lxml')
        match=soup.find('div',class_="card-stack")
        match=match.find_all('div')
        new=''
        row=0
        image_no=0
        rowi=0
        for i in match:
           news=i.find('div',itemprop="articleBody")
           title=i.find('span',itemprop="headline")
           if news==None:
              continue
           if new!=news.text and title!=None:
              new=news.text    
              t=news.text
              Label(frame, text="%s" % row, width=3, borderwidth="1",relief="solid").grid(row=row, column=0)
              globals()['a'+str(row)]=Text(frame,width=50,height=8,bg='white',foreground='#258528',font=('Comic Sans MS', 15))
              eval('a'+str(row)).grid(row=row, column=2)
              eval('a'+str(row)).insert(END,news.text)

              globals()['im'+str(image_no)] = Image.open('abc.png')
              globals()['im'+str(image_no)] = eval('im'+str(image_no)).resize((250, 200), Image.ANTIALIAS)
              globals()['image'+str(image_no)] = ImageTk.PhotoImage(eval('im'+str(image_no)))
              globals()['label'+str(image_no)] = Label(frame, image=eval('image'+str(image_no)))
              eval('label'+str(image_no)).grid(row=rowi,column=1)
              row+=1
              rowi+=1
              image_no=image_no+1

        image_no=0
        rowi=0
        for i in match:
            url=i.find('div',class_="news-card-image")
            if url==None:
                pass
            else:
                url=str(url).strip()
                new=str(new).strip()
                if url!=new:
                   url=str(url)
                   link=re.findall('url(.*)',url)[0][2:-4]
                   new=url
                   cover=link
                   globals()['raw_data'+str(image_no)] = urllib.request.urlopen(cover).read()
                   globals()['im'+str(image_no)] = Image.open(io.BytesIO(eval('raw_data'+str(image_no))))
                   globals()['im'+str(image_no)] = eval('im'+str(image_no)).resize((250, 200), Image.ANTIALIAS)

                   globals()['image'+str(image_no)] = ImageTk.PhotoImage(eval('im'+str(image_no)))
                   globals()['label'+str(image_no)] = Label(frame, image=eval('image'+str(image_no)))
                   eval('label'+str(image_no)).grid(row=rowi,column=1)
                   rowi+=1
                   image_no=image_no+1
    except:
        print("No internet connection")





#----------------------------------------------------------------------------------

canvas02=Canvas(root,width=96,height=96,bg="white")
canvas02.place(x=200,y=0)
photoi2=PhotoImage(file='3.png')
canvas02.create_image(0,0,anchor=NW,image=photoi2)

#----------------------------------------------------------------------------------

def onFrameConfigure(canvas):
    canvas.configure(scrollregion=canvas.bbox("all"))

canvas = Canvas(root, borderwidth=0, background="white",width=900,height=400)
frame = Frame(canvas, background="#ffffff")

vsb = Scrollbar(root, orient="vertical", command=canvas.yview)
canvas.configure(yscrollcommand=vsb.set)
vsb.pack(side="right", fill="y")
canvas.place(x=10,y=100)
photoi1=PhotoImage(file='stay.png')
canvas.create_image(0,0,anchor=NW,image=photoi1)

canvas.create_window((4,4), window=frame, anchor="nw")

frame.bind("<Configure>", lambda event, canvas=canvas: onFrameConfigure(canvas))

title=Label(root,text="Py-News",bg="white",font=('Comic Sans MS', 45),fg='#d76737')
title.place(x=350,y=10)

show=ttk.Button(root,text="show news",command=lambda:threading.Thread(target=display,args=(frame,)).start())
show.place(x=650,y=40)



root.mainloop()

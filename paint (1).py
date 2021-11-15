from tkinter import *
from tkinter.filedialog import asksaveasfilename as saveAs
import PIL
from PIL import Image, ImageDraw, ImageTk
from keras.models import load_model
from tkinter.colorchooser import askcolor
from matplotlib import pyplot as plt
import numpy as np
import pickle


class paint(object):
    def __init__(self):
        win = Tk()
        win.title("Paint")
        self.app_width = 900
        self.app_height = 550

        self.screen_width = win.winfo_screenwidth()
        self.screen_height = win.winfo_screenheight()

        self.xh = (self.screen_width / 2) - (self.app_width / 2)
        self.yh = (self.screen_height / 2 ) - (self.app_height / 2)

        win.geometry(f'{self.app_width}x{self.app_height}+{int(self.xh)}+{int(self.yh)}')
        win.resizable(0,0)
        #win.iconbitmap('Paint.ico') # Delete this line if you don't have file "Paint.ico" in this folder
        lastx, lasty = None, None
        topframe = Frame(win, bg='#90CCF4', padx=15, pady=5)
        topframe.pack(side=TOP, expand='no', fill='x')
        save_ = Button(topframe, text="PREDICT", command=self.save, bg='green', fg='white', font='Arial 12 bold', cursor='hand2',width=10)
        save_.pack(side=LEFT)

        global color_icon
        color_icon = ImageTk.PhotoImage(file='D:\\SOFTWARES\\Jupyter\\colors.png')

        color_button = Button(topframe, image=color_icon, bg='#ECECEC', fg='black', font='Arial 12 bold', 
            cursor='hand2',width=32,height=28, command=self.choose_color)
        color_button.pack(side=LEFT)

        reset=Button(topframe, text='Clear', bg='#ECECEC', fg='black', font='Arial 12 bold', cursor='hand2',width=10,command=self.clear)
        reset.pack(side=RIGHT)

        _exit=Button(topframe, text='Exit',command=self.exitt, bg='red', fg='white', font='Arial 12 bold', cursor='hand2',width=10)
        _exit.pack(side=RIGHT)

        self.pw = PanedWindow(win, borderwidth=2)
        self.pw.pack(fill=BOTH, expand=True)
        
        self.pw2 = PanedWindow(win, borderwidth=2)
        self.pw.add(self.pw2)
        self.leftframe = Frame(self.pw, width = 50)
        self.pw.add(self.leftframe)
        self.pw.paneconfig(self.leftframe, minsize = 250)
        self.rightframe = Frame(self.pw2 )
        self.pw2.add(self.rightframe)
        self.pw2.paneconfig(self.rightframe)

        self.cv = Canvas(self.rightframe, width=640, height=480, bg='black')

        self.image1 = PIL.Image.new('RGB', (640, 480), 'black')
        self.draw = ImageDraw.Draw(self.image1)

        self.cv.bind('<1>', self.activate_paint)
        self.cv.pack(expand=YES, fill=BOTH)


        self.heading = Label(self.leftframe, text='OUTPUT', font='Arial 12 bold')
        self.heading.pack()
        self.output=Text(self.leftframe, font='Arial 14')
        self.output.pack()


        self.eraser_on = True
        self.color = 'yellow'
        self.count=0

        win.mainloop()

    def choose_color(self):
        self.eraser_on = False
        self.color = askcolor(color=self.color)[1]

    def save(self):
        cnn = load_model('cnn.h5')

        print(type(self.image1))

        #filename=saveAs(title="Save image as...",filetype=(("PNG images","*.png"),("JPEG images","*.jpg"),("GIF images","*.gif")))
        filename = 'cnn'+str(self.count)+'.png'
        self.image1.save(filename)
        self.count+=1
        
        randomImg = self.image1.convert('L')        
        randomImg = randomImg.resize((32,32))
        randomImg= np.array(randomImg)
        randomImg= np.resize(randomImg,(32,32))
        randomImg = randomImg.astype('float32')
        randomImg /= 255

        ip=np.resize(randomImg,(1,32,32,1))

        #plt.figure()
        #plt.subplot(111)
        #plt.imshow(ip[0])
        #predicting the class
        prediction = cnn.predict(ip)

        with open("StrToNum.txt", "rb") as myFile:
            StrToNum = pickle.load(myFile)
        with open("NumToStr.txt", "rb") as myFile:
            NumToStr = pickle.load(myFile)

        pred,percent = [NumToStr[np.argmax(prediction[0])] , round(max(prediction[0])*100,2)]
        self.output.delete(1.0,END)
        self.output.insert(END,'Character:\n'+str(pred) + '\n\nProbability:\n' + str(percent) + '\n\nFilename:\n' + filename)
        #self.output.insert(END,str(pred) + '\n' + str(percent) + '\n' + filename)


    def activate_paint(self,e):
        global lastx, lasty
        self.cv.bind('<B1-Motion>', self.paint)
        lastx, lasty = e.x, e.y

    def paint(self,e):
        #self.line_width = self.choose_size_button.get()
        paint_color = 'white' if self.eraser_on else self.color
        global lastx, lasty
        x, y = e.x, e.y
        self.cv.create_line(lastx, lasty, x, y,width=50, fill=paint_color,capstyle=ROUND, smooth=TRUE, splinesteps=36)

        self.draw.line((lastx, lasty, x, y), fill=paint_color, width=50)
        lastx, lasty = x, y
    def clear(self):
        self.cv.delete('all')
        self.output.delete(1.0,END)
        self.image1 = PIL.Image.new('RGB', (640, 480), 'black')
        self.draw = ImageDraw.Draw(self.image1)
        
    def exitt(self):
        exit()


if __name__ == '__main__':
    paint()

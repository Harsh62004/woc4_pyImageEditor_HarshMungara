from tkinter import *
import os
from turtle import bgcolor
from PIL import Image
from tkinter.filedialog import askopenfilename, asksaveasfilename
from PIL import ImageTk
from PIL import ImageOps
from tkinter import messagebox
import imghdr
from PIL import ImageDraw
from collections import*
import ctypes
from tkinter import colorchooser

#--------------------------------------------------------------DARK MODE---------------------------------------------------------------
#--------------------------------------------------------------DARK MODE---------------------------------------------------------------
#--------------------------------------------------------------DARK MODE---------------------------------------------------------------
#--------------------------------------------------------------DARK MODE---------------------------------------------------------------
#--------------------------------------------------------------DARK MODE---------------------------------------------------------------
#--------------------------------------------------------------DARK MODE---------------------------------------------------------------

def dark(root):
    root.destroy()

    def drawOnImage(canvas):
        canvas.data.colourPopToHappen=False
        canvas.data.cropPopToHappen=False
        canvas.data.drawOn=True
        my_color= colorchooser.askcolor()[1]
        colourChosen(canvas,my_color)


    def colourChosen(canvas, colour):
        if canvas.data.image!=None:
            canvas.data.drawColour=colour
            canvas.data.mainWindow.bind("<B1-Motion>",\
                                        lambda event: drawDraw(event, canvas))
        
        

    def drawDraw(event, canvas):
        if canvas.data.drawOn==True:
            x=int(round((event.x-canvas.data.imageTopX)*canvas.data.imageScale))
            y=int(round((event.y-canvas.data.imageTopY)*canvas.data.imageScale))
            draw = ImageDraw.Draw(canvas.data.image)
            draw.ellipse((x-3, y-3, x+ 3, y+3), fill=canvas.data.drawColour,\
                        outline=None)
            save(canvas)
            canvas.data.undoQueue.append(canvas.data.image.copy())
            canvas.data.imageForTk=resize_func(canvas)
            drawImage(canvas)



    def crop(canvas):
        
        canvas.data.cropaction=True
        messagebox.showinfo(title="Crop", message="Draw cropping rectangle and press Enter" , parent=canvas.data.mainWindow)
        if canvas.data.image!=None:
            canvas.data.mainWindow.bind("<ButtonPress-1>", lambda event: startCrop(event, canvas))
            canvas.data.mainWindow.bind("<B1-Motion>", lambda event: drawCrop(event, canvas))
            canvas.data.mainWindow.bind("<ButtonRelease-1>", lambda event: endCrop(event, canvas))

    def startCrop(event, canvas):
        
        if canvas.data.endCrop==False and canvas.data.cropaction==True:
            canvas.data.startCropX=event.x
            canvas.data.startCropY=event.y

    def drawCrop(event,canvas):
        if canvas.data.endCrop==False and canvas.data.cropaction==True:
            canvas.data.tempCropX=event.x
            canvas.data.tempCropY=event.y
            canvas.create_rectangle(canvas.data.startCropX,canvas.data.startCropY,canvas.data.tempCropX,canvas.data.tempCropY, fill="gray", stipple="gray12", width=0)

    def endCrop(event, canvas):

        if canvas.data.cropaction==True:
            canvas.data.endCrop=True
            canvas.data.endCropX=event.x
            canvas.data.endCropY=event.y
            canvas.create_rectangle(canvas.data.startCropX,canvas.data.startCropY,canvas.data.endCropX, canvas.data.endCropY, fill="gray", stipple="gray12", width=0 )
            canvas.data.mainWindow.bind("<Return>", lambda event: performCrop(event, canvas))

    def performCrop(event,canvas):
        canvas.data.image=\
        canvas.data.image.crop(\
        (int(round((canvas.data.startCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
        int(round((canvas.data.startCropY-canvas.data.imageTopY)*canvas.data.imageScale)),
        int(round((canvas.data.endCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
        int(round((canvas.data.endCropY-canvas.data.imageTopY)*canvas.data.imageScale))))
        canvas.data.endCrop=False
        canvas.data.cropaction=False
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=resize_func(canvas)
        drawImage(canvas)
        
    def rotate_right(canvas):
        ig=canvas.data.image
        newimg= ig.rotate(-90)

        canvas.data.image=newimg
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=resize_func(canvas)
        drawImage(canvas)

    def rotate_left(canvas):
        ig=canvas.data.image
        newimg= ig.rotate(90)
        canvas.data.image=newimg
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=resize_func(canvas)
        drawImage(canvas)

    def reset(canvas):
        canvas.data.cropaction=False
        
        if canvas.data.image!=None:
            canvas.data.image=canvas.data.originalImage.copy()
            save(canvas)
            canvas.data.undoQueue.append(canvas.data.image.copy())
            canvas.data.imageForTk=resize_func(canvas)
            drawImage(canvas)


    def mirror(canvas):
        
        canvas.data.cropaction=False
        
        if canvas.data.image!=None:
            canvas.data.image=ImageOps.mirror(canvas.data.image)
            save(canvas)
            canvas.data.undoQueue.append(canvas.data.image.copy())
            canvas.data.imageForTk=resize_func(canvas)
            drawImage(canvas)

    def flip(canvas):
        
        canvas.data.cropaction=False
        
        if canvas.data.image!=None:
            canvas.data.image=ImageOps.flip(canvas.data.image)
            save(canvas)
            canvas.data.undoQueue.append(canvas.data.image.copy())
            canvas.data.imageForTk=resize_func(canvas)
            drawImage(canvas)


    def closeBrightnessWindow(canvas):
        if canvas.data.image!=None:
            save(canvas)
            canvas.data.undoQueue.append(canvas.data.image.copy())
            canvas.data.brightnessWindowClose=True

    def changeBrightness(canvas, brightnessWindow, brightnessSlider, \
                        previousVal):
        if canvas.data.brightnessWindowClose==True:
            brightnessWindow.destroy()
            canvas.data.brightnessWindowClose=False
            
        else:
            if canvas.data.image!=None and brightnessWindow.winfo_exists():
                sliderVal=brightnessSlider.get()
                scale=(sliderVal-previousVal)/100.0
                canvas.data.image=canvas.data.image.point(\
                    lambda i: i+ int(round(i*scale)))  
                canvas.data.imageForTk=resize_func(canvas)
                drawImage(canvas)
                canvas.after(50, \
                lambda: changeBrightness(canvas, brightnessWindow, \
                                        brightnessSlider, sliderVal))

        
    def brightness(canvas):
        canvas.data.colourPopToHappen=False
        canvas.data.cropPopToHappen=False
        canvas.data.drawOn=False
        brightnessWindow=Toplevel(canvas.data.mainWindow)
        brightnessWindow.title("Brightness")
        brightnessSlider=Scale(brightnessWindow, from_=-100, to=100,\
                            orient=HORIZONTAL)
        brightnessSlider.pack()
        OkBrightnessFrame=Frame(brightnessWindow)
        OkBrightnessButton=Button(OkBrightnessFrame, text="OK", \
                                command=lambda: closeBrightnessWindow(canvas))
        OkBrightnessButton.grid(row=0,column=0)
        OkBrightnessFrame.pack(side=BOTTOM)
        changeBrightness(canvas, brightnessWindow, brightnessSlider,0)
        brightnessSlider.set(0)


    def keyPressed(canvas, event):
        if event.keysym=="z":
            undo(canvas)
        elif event.keysym=="y":
            redo(canvas)
            
    def undo(canvas):
        if len(canvas.data.undoQueue)>0:
            lastImage=canvas.data.undoQueue.pop()
            canvas.data.redoQueue.appendleft(lastImage)
        if len(canvas.data.undoQueue)>0:
            canvas.data.image=canvas.data.undoQueue[-1]
        save(canvas)
        canvas.data.imageForTk=resize_func(canvas)
        drawImage(canvas)

    def redo(canvas):
        if len(canvas.data.redoQueue)>0:
            canvas.data.image=canvas.data.redoQueue[0]
        save(canvas)
        if len(canvas.data.redoQueue)>0:
            
            lastImage=canvas.data.redoQueue.popleft()
            canvas.data.undoQueue.append(lastImage)
        canvas.data.imageForTk=resize_func(canvas)
        drawImage(canvas)


    def saveAs(canvas):
        if canvas.data.image!=None:
            filename=asksaveasfilename(defaultextension=".jpg")
            im=canvas.data.image
            im.save(filename)

    def save(canvas):
        if canvas.data.image!=None:
            im=canvas.data.image
            im.save(canvas.data.imageLocation)

    def insert_image(canvas):
        imageName=askopenfilename()
        filetype=""

        try: filetype=imghdr.what(imageName)
        except:
            messagebox.showinfo(title="Image File",\
            message="Choose an Image File!" , parent=canvas.data.mainWindow)
        
        if filetype in ['jpeg', 'bmp', 'png', 'tiff']:
            canvas.data.imageLocation=imageName
            im= Image.open(imageName)
            canvas.data.image=im
            canvas.data.originalImage=im.copy()
            canvas.data.undoQueue.append(im.copy())
            canvas.data.imageSize=im.size 
            canvas.data.imageForTk=resize_func(canvas)
            drawImage(canvas)
        else:
            messagebox.showinfo(title="Image File",\
            message="Choose an Image File!" , parent=canvas.data.mainWindow)


    def resize_func(canvas):
        im=canvas.data.image
        if canvas.data.image!=None:
        
            imageWidth=canvas.data.image.size[0] 
            imageHeight=canvas.data.image.size[1]
        
            if imageWidth>imageHeight:
                resizedImage=im.resize((canvas.data.width,\
                    int(round(float(imageHeight)*canvas.data.width/imageWidth))))
            
                canvas.data.imageScale=float(imageWidth)/canvas.data.width
            else:
                resizedImage=im.resize((int(round(float(imageWidth)*canvas.data.height/imageHeight)),\
                                        canvas.data.height))
                canvas.data.imageScale=float(imageHeight)/canvas.data.height
            
            canvas.data.resizedIm=resizedImage
            return ImageTk.PhotoImage(resizedImage)
    
    def drawImage(canvas):
        if canvas.data.image!=None:
            
            canvas.create_image(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0,
                            canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0,
                                anchor=NW, image=canvas.data.imageForTk)
            canvas.data.imageTopX=int(round(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0))
            canvas.data.imageTopY=int(round(canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0))


    def initial_func(root, canvas):
        Button_func(root, canvas)
        menu_func(root, canvas)
        canvas.data.image=None
        canvas.data.cropaction=False
        canvas.data.endCrop=False
        canvas.data.brightnessWindowClose=False
        canvas.data.brightnessLevel=None
        
        canvas.data.undoQueue=deque([], 10)
        canvas.data.redoQueue=deque([], 10)
        canvas.pack()


    def Button_func(root, canvas):
        backgroundColour="white"
        buttonWidth=14
        buttonHeight=2
        toolKitFrame=Frame(root)
        cropButton=Button(toolKitFrame, text="Crop",\
                        background=backgroundColour ,\
                        width=buttonWidth, height=buttonHeight, \
                        activeforeground="BLACK",activebackground="WHITE", bg="BLACK",fg='BLUE', \
                        command=lambda:crop(canvas))
        cropButton.grid(row=0,column=0)
        
        mirrorButton=Button(toolKitFrame, text="Mirror",\
                            background=backgroundColour, \
                            width=buttonWidth,height=buttonHeight, \
                            activeforeground="BLACK",activebackground="WHITE", bg="BLACK",fg='BLUE',\
                            command=lambda: mirror(canvas))
        mirrorButton.grid(row=0,column=2)
        flipButton=Button(toolKitFrame, text="Flip",\
                        background=backgroundColour ,\
                        width=buttonWidth,height=buttonHeight, \
                        activeforeground="BLACK",activebackground="WHITE", bg="BLACK",fg='BLUE', \
                        command=lambda: flip(canvas))
        flipButton.grid(row=0,column=3)
        drawButton=Button(toolKitFrame, text="Draw",\
                        background=backgroundColour ,width=buttonWidth,\
                        activeforeground="BLACK",activebackground="WHITE", bg="BLACK",fg='BLUE',\
                        height=buttonHeight,command=lambda: drawOnImage(canvas))
        drawButton.grid(row=0,column=4)
        brightnessButton=Button(toolKitFrame, text="Brightness",\
                                background=backgroundColour ,\
                                width=buttonWidth, height=buttonHeight,\
                                activeforeground="BLACK",activebackground="WHITE", bg="BLACK",fg='BLUE', \
                                command=lambda: brightness(canvas))
        brightnessButton.grid(row=0,column=5)
        resetButton=Button(toolKitFrame, text="Reset",\
                        background=backgroundColour ,width=buttonWidth,\
                        activeforeground="BLACK",activebackground="WHITE", bg="BLACK",fg='BLUE', \
                        height=buttonHeight, command=lambda: reset(canvas))
        resetButton.grid(row=0,column=6)
        
        toolKitFrame.pack(side=TOP)


    def menu_func(root, canvas):
        
        menubar=Menu(root)
        filemenu=Menu(menubar,tearoff=0)
        filemenu.add_command(label="New", command=lambda:insert_image(canvas))
        filemenu.add_command(label="Save", command=lambda:save(canvas))
        filemenu.add_command(label="Save As", command=lambda:saveAs(canvas))
        menubar.add_cascade(label="File", menu=filemenu)
        filemenu.config(bg="BLACK",fg="BLUE")
        root.config(menu=menubar)
        editmenu = Menu(menubar, tearoff=0)
        editmenu.add_command(label="Rotate right", command=lambda:rotate_right(canvas))
        editmenu.add_command(label="Rotate right", command=lambda:rotate_right(canvas))
        editmenu.config(bg="BLACK",fg="BLUE")
        mymenu=Menu(editmenu)
        mymenu.add_command(label="Rotate right", command=lambda:rotate_right(canvas))
        mymenu.add_command(label="Rotate right", command=lambda:rotate_left(canvas))
        menubar.add_cascade(label="Edit", menu=editmenu)
        mymenu.config(bg="BLACK",fg="BLUE")
        root.config(menu=menubar)
        menubar.add_command(label="Undo-Z", command=lambda:undo(canvas))
        menubar.add_command(label="Redo-Y", command=lambda:redo(canvas))
        menubar.add_command(label="Light Mode", command=lambda:light(root))
        menubar.config(bg="BLACK",fg="BLUE")
        root.config(menu=menubar)


    def light(root):
        root.destroy()
        run()


    def run1():
        root = Tk()
        root.title("Python Photo Editor")
        root.configure(bg='black')
        canvasWidth=500
        canvasHeight=500
        canvas = Canvas(root, width=canvasWidth, height=canvasHeight, highlightthickness=2, highlightbackground="red", \
                        background="Black")
        class Struct: pass
        canvas.data = Struct()
        canvas.data.width=canvasWidth
        canvas.data.height=canvasHeight
        canvas.data.mainWindow=root
        initial_func(root, canvas)
        root.bind("<Key>", lambda event:keyPressed(canvas, event))
    
        root.mainloop()  


    run1()
#--------------------------------------------------------------DARK MODE---------------------------------------------------------------
#--------------------------------------------------------------DARK MODE---------------------------------------------------------------
#--------------------------------------------------------------DARK MODE---------------------------------------------------------------
#--------------------------------------------------------------DARK MODE---------------------------------------------------------------
#--------------------------------------------------------------DARK MODE---------------------------------------------------------------
#--------------------------------------------------------------DARK MODE---------------------------------------------------------------

def drawOnImage(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=True
    my_color= colorchooser.askcolor()[1]
    colourChosen(canvas,my_color)


def colourChosen(canvas, colour):
    if canvas.data.image!=None:
        canvas.data.drawColour=colour
        canvas.data.mainWindow.bind("<B1-Motion>",\
                                    lambda event: drawDraw(event, canvas))
    
    

def drawDraw(event, canvas):
    if canvas.data.drawOn==True:
        x=int(round((event.x-canvas.data.imageTopX)*canvas.data.imageScale))
        y=int(round((event.y-canvas.data.imageTopY)*canvas.data.imageScale))
        draw = ImageDraw.Draw(canvas.data.image)
        draw.ellipse((x-3, y-3, x+ 3, y+3), fill=canvas.data.drawColour,\
                     outline=None)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=resize_func(canvas)
        drawImage(canvas)



def crop(canvas):
    
    canvas.data.cropaction=True
    messagebox.showinfo(title="Crop", message="Draw cropping rectangle and press Enter" , parent=canvas.data.mainWindow)
    if canvas.data.image!=None:
        canvas.data.mainWindow.bind("<ButtonPress-1>", lambda event: startCrop(event, canvas))
        canvas.data.mainWindow.bind("<B1-Motion>", lambda event: drawCrop(event, canvas))
        canvas.data.mainWindow.bind("<ButtonRelease-1>", lambda event: endCrop(event, canvas))

def startCrop(event, canvas):
    
    if canvas.data.endCrop==False and canvas.data.cropaction==True:
        canvas.data.startCropX=event.x
        canvas.data.startCropY=event.y

def drawCrop(event,canvas):
    if canvas.data.endCrop==False and canvas.data.cropaction==True:
        canvas.data.tempCropX=event.x
        canvas.data.tempCropY=event.y
        canvas.create_rectangle(canvas.data.startCropX,canvas.data.startCropY,canvas.data.tempCropX,canvas.data.tempCropY, fill="gray", stipple="gray12", width=0)

def endCrop(event, canvas):

    if canvas.data.cropaction==True:
        canvas.data.endCrop=True
        canvas.data.endCropX=event.x
        canvas.data.endCropY=event.y
        canvas.create_rectangle(canvas.data.startCropX,canvas.data.startCropY,canvas.data.endCropX, canvas.data.endCropY, fill="gray", stipple="gray12", width=0 )
        canvas.data.mainWindow.bind("<Return>", lambda event: performCrop(event, canvas))

def performCrop(event,canvas):
    canvas.data.image=\
    canvas.data.image.crop(\
    (int(round((canvas.data.startCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
    int(round((canvas.data.startCropY-canvas.data.imageTopY)*canvas.data.imageScale)),
    int(round((canvas.data.endCropX-canvas.data.imageTopX)*canvas.data.imageScale)),
    int(round((canvas.data.endCropY-canvas.data.imageTopY)*canvas.data.imageScale))))
    canvas.data.endCrop=False
    canvas.data.cropaction=False
    save(canvas)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=resize_func(canvas)
    drawImage(canvas)
    
def rotate_right(canvas):
    ig=canvas.data.image
    newimg= ig.rotate(-90)

    canvas.data.image=newimg
    save(canvas)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=resize_func(canvas)
    drawImage(canvas)

def rotate_left(canvas):
    ig=canvas.data.image
    newimg= ig.rotate(90)
    canvas.data.image=newimg
    save(canvas)
    canvas.data.undoQueue.append(canvas.data.image.copy())
    canvas.data.imageForTk=resize_func(canvas)
    drawImage(canvas)

def reset(canvas):
    canvas.data.cropaction=False
    
    if canvas.data.image!=None:
        canvas.data.image=canvas.data.originalImage.copy()
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=resize_func(canvas)
        drawImage(canvas)


def mirror(canvas):
    
    canvas.data.cropaction=False
    
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.mirror(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=resize_func(canvas)
        drawImage(canvas)

def flip(canvas):
    
    canvas.data.cropaction=False
    
    if canvas.data.image!=None:
        canvas.data.image=ImageOps.flip(canvas.data.image)
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.imageForTk=resize_func(canvas)
        drawImage(canvas)


def closeBrightnessWindow(canvas):
    if canvas.data.image!=None:
        save(canvas)
        canvas.data.undoQueue.append(canvas.data.image.copy())
        canvas.data.brightnessWindowClose=True

def changeBrightness(canvas, brightnessWindow, brightnessSlider, \
                     previousVal):
    if canvas.data.brightnessWindowClose==True:
        brightnessWindow.destroy()
        canvas.data.brightnessWindowClose=False
        
    else:
        if canvas.data.image!=None and brightnessWindow.winfo_exists():
            sliderVal=brightnessSlider.get()
            scale=(sliderVal-previousVal)/100.0
            canvas.data.image=canvas.data.image.point(\
                lambda i: i+ int(round(i*scale)))  
            canvas.data.imageForTk=resize_func(canvas)
            drawImage(canvas)
            canvas.after(50, \
            lambda: changeBrightness(canvas, brightnessWindow, \
                                     brightnessSlider, sliderVal))

       
def brightness(canvas):
    canvas.data.colourPopToHappen=False
    canvas.data.cropPopToHappen=False
    canvas.data.drawOn=False
    brightnessWindow=Toplevel(canvas.data.mainWindow)
    brightnessWindow.title("Brightness")
    brightnessSlider=Scale(brightnessWindow, from_=-100, to=100,\
                           orient=HORIZONTAL)
    brightnessSlider.pack()
    OkBrightnessFrame=Frame(brightnessWindow)
    OkBrightnessButton=Button(OkBrightnessFrame, text="OK", \
                              command=lambda: closeBrightnessWindow(canvas))
    OkBrightnessButton.grid(row=0,column=0)
    OkBrightnessFrame.pack(side=BOTTOM)
    changeBrightness(canvas, brightnessWindow, brightnessSlider,0)
    brightnessSlider.set(0)


def keyPressed(canvas, event):
    if event.keysym=="z":
        undo(canvas)
    elif event.keysym=="y":
        redo(canvas)
        
def undo(canvas):
    if len(canvas.data.undoQueue)>0:
        lastImage=canvas.data.undoQueue.pop()
        canvas.data.redoQueue.appendleft(lastImage)
    if len(canvas.data.undoQueue)>0:
        canvas.data.image=canvas.data.undoQueue[-1]
    save(canvas)
    canvas.data.imageForTk=resize_func(canvas)
    drawImage(canvas)

def redo(canvas):
    if len(canvas.data.redoQueue)>0:
        canvas.data.image=canvas.data.redoQueue[0]
    save(canvas)
    if len(canvas.data.redoQueue)>0:
        
        lastImage=canvas.data.redoQueue.popleft()
        canvas.data.undoQueue.append(lastImage)
    canvas.data.imageForTk=resize_func(canvas)
    drawImage(canvas)


def saveAs(canvas):
    if canvas.data.image!=None:
        filename=asksaveasfilename(defaultextension=".jpg")
        im=canvas.data.image
        im.save(filename)

def save(canvas):
    if canvas.data.image!=None:
        im=canvas.data.image
        im.save(canvas.data.imageLocation)

def insert_image(canvas):
    imageName=askopenfilename()
    filetype=""

    try: filetype=imghdr.what(imageName)
    except:
        messagebox.showinfo(title="Image File",\
        message="Choose an Image File!" , parent=canvas.data.mainWindow)
    
    if filetype in ['jpeg', 'bmp', 'png', 'tiff']:
        canvas.data.imageLocation=imageName
        im= Image.open(imageName)
        canvas.data.image=im
        canvas.data.originalImage=im.copy()
        canvas.data.undoQueue.append(im.copy())
        canvas.data.imageSize=im.size 
        canvas.data.imageForTk=resize_func(canvas)
        drawImage(canvas)
    else:
        messagebox.showinfo(title="Image File",\
        message="Choose an Image File!" , parent=canvas.data.mainWindow)


def resize_func(canvas):
    im=canvas.data.image
    if canvas.data.image!=None:
       
        imageWidth=canvas.data.image.size[0] 
        imageHeight=canvas.data.image.size[1]
       
        if imageWidth>imageHeight:
            resizedImage=im.resize((canvas.data.width,\
                int(round(float(imageHeight)*canvas.data.width/imageWidth))))
           
            canvas.data.imageScale=float(imageWidth)/canvas.data.width
        else:
            resizedImage=im.resize((int(round(float(imageWidth)*canvas.data.height/imageHeight)),\
                                    canvas.data.height))
            canvas.data.imageScale=float(imageHeight)/canvas.data.height
        
        canvas.data.resizedIm=resizedImage
        return ImageTk.PhotoImage(resizedImage)
 
def drawImage(canvas):
    if canvas.data.image!=None:
        
        canvas.create_image(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0,
                        canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0,
                            anchor=NW, image=canvas.data.imageForTk)
        canvas.data.imageTopX=int(round(canvas.data.width/2.0-canvas.data.resizedIm.size[0]/2.0))
        canvas.data.imageTopY=int(round(canvas.data.height/2.0-canvas.data.resizedIm.size[1]/2.0))


def initial_func(root, canvas):
    Button_func(root, canvas)
    menu_func(root, canvas)
    canvas.data.image=None
    canvas.data.cropaction=False
    canvas.data.endCrop=False
    canvas.data.brightnessWindowClose=False
    canvas.data.brightnessLevel=None
    canvas.data.undoQueue=deque([], 10)
    canvas.data.redoQueue=deque([], 10)
    canvas.pack()

def Button_func(root, canvas):
    backgroundColour="white"
    buttonWidth=14
    buttonHeight=2
    toolKitFrame=Frame(root)
    cropButton=Button(toolKitFrame, text="Crop",\
                      background=backgroundColour ,\
                      width=buttonWidth, height=buttonHeight, \
                      activeforeground="WHITE",activebackground="BLACK", bg="WHITE",fg='RED', \
                      command=lambda:crop(canvas))
    cropButton.grid(row=0,column=0)
    
    mirrorButton=Button(toolKitFrame, text="Mirror",\
                        background=backgroundColour, \
                        width=buttonWidth,height=buttonHeight, \
                        activeforeground="WHITE",activebackground="BLACK", bg="WHITE",fg='RED',\
                        command=lambda: mirror(canvas))
    mirrorButton.grid(row=0,column=2)
    flipButton=Button(toolKitFrame, text="Flip",\
                      background=backgroundColour ,\
                      width=buttonWidth,height=buttonHeight, \
                      activeforeground="WHITE",activebackground="BLACK", bg="WHITE",fg='RED', \
                      command=lambda: flip(canvas))
    flipButton.grid(row=0,column=3)
    drawButton=Button(toolKitFrame, text="Draw",\
                      background=backgroundColour ,width=buttonWidth,\
                      activeforeground="WHITE",activebackground="BLACK", bg="WHITE",fg='RED',\
                      height=buttonHeight,command=lambda: drawOnImage(canvas))
    drawButton.grid(row=0,column=4)
    brightnessButton=Button(toolKitFrame, text="Brightness",\
                            background=backgroundColour ,\
                            width=buttonWidth, height=buttonHeight,\
                            activeforeground="WHITE",activebackground="BLACK", bg="WHITE",fg='RED', \
                            command=lambda: brightness(canvas))
    brightnessButton.grid(row=0,column=5)
    resetButton=Button(toolKitFrame, text="Reset",\
                       background=backgroundColour ,width=buttonWidth,\
                       activeforeground="WHITE",activebackground="BLACK", bg="WHITE",fg='RED', \
                       height=buttonHeight, command=lambda: reset(canvas))
    resetButton.grid(row=0,column=6)
    
    toolKitFrame.pack(side=TOP)

def menu_func(root, canvas):
    
    menubar=Menu(root)
    filemenu=Menu(menubar,tearoff=0)
    filemenu.add_command(label="New", command=lambda:insert_image(canvas))
    filemenu.add_command(label="Save", command=lambda:save(canvas))
    filemenu.add_command(label="Save As", command=lambda:saveAs(canvas))
    menubar.add_cascade(label="File", menu=filemenu)
    root.config(menu=menubar)
    editmenu = Menu(menubar, tearoff=0)
    editmenu.add_command(label="Rotate right", command=lambda:rotate_right(canvas))
    editmenu.add_command(label="Rotate left", command=lambda:rotate_left(canvas))

    menubar.add_cascade(label="Edit", menu=editmenu)
    root.config(menu=menubar)
    menubar.add_command(label="Undo-Z", command=lambda:undo(canvas))
    menubar.add_command(label="Redo-Y", command=lambda:redo(canvas))
    menubar.add_command(label="Dark Mode", command=lambda:dark(root))
    root.config(menu=menubar)


def run():
    root = Tk()
    root.title("Python Photo Editor")
    canvasWidth=500
    canvasHeight=500
    canvas = Canvas(root, width=canvasWidth, height=canvasHeight, \
                    background="GHOST WHITE")
    class Struct: pass
    canvas.data = Struct()
    canvas.data.width=canvasWidth
    canvas.data.height=canvasHeight
    canvas.data.mainWindow=root
    initial_func(root, canvas)
    root.bind("<Key>", lambda event:keyPressed(canvas, event))
   
    root.mainloop()  


run()



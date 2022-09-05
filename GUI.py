#importing modules
import tkinter as tk
from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askopenfilename
from PIL import Image, ImageTk
import numpy as np
from keras.models import load_model

#loading the model
Model = load_model("Age_and_gender_detector_checkpoint.h5")

#initializing the GUI
top = tk.Tk()
top.geometry('800x600')
top.title('Age and Gender Detector')
top.configure(background = '#CDCDCD')
heading = Label(top, text = 'Age and Gender Detector', pady = 20, font = ('arial', 20, 'bold'))
heading.configure(background = '#CDCDCD', foreground = '#364156')
heading.pack()

#labels for Age and Gender
age_label = Label(top, background = '#CDCDCD', font = ('arial',15,'bold'))
gender_label = Label(top, background = '#CDCDCD', font = ('arial',15,'bold'))
age_label.pack(side = 'bottom', expand = True)
gender_label.pack(side = 'bottom', expand = True)
sign_image = Label(top)
sign_image.pack(side = 'bottom', expand = True)

#Detection funcion for age and gender
def Detect(file_path):
    global Label_packed
    img = Image.open(file_path)
    img = img.resize((48,48))
    img = np.expand_dims(img, axis = 0)
    img = np.array(img)
    img = np.delete(img, 0 ,1)
    img = np.resize(img, (48,48,3))
    print(img.shape)
    genders = ['Male', 'Female']
    img = np.array([img])/255
    prediction = Model.predict(img)
    age = int(np.round(prediction[1][0]))
    gender = int(np.round(prediction[0][0]))
    print("Predicted Age:", age)
    print("Predicted Gender:", genders[gender])
    age_label.configure(foreground = "#011638", text = age)
    gender_label.configure(foreground = "#011638", text = genders[gender])

#Defining  Detection Button function
def Detect_button(file_path):
    Detection_button = Button(top, text = "Detect Image", command = lambda: Detect(file_path), padx = 10, pady = 5)
    Detection_button.configure(background = '#364156', foreground = 'white', font = ('arial', 10, 'bold'))
    Detection_button.place(relx = 0.79, rely = 0.46)

#Defining Upload Image function
def Upload_image():
    try:
        file_path = askopenfilename()
        uploaded = Image.open(file_path)
        uploaded.thumbnail(((top.winfo_width()/2.25),(top.winfo_height()/2.25)))
        imge = ImageTk.PhotoImage(uploaded)
        sign_image.configure(image = imge)
        sign_image.image = imge
        age_label.configure(text = '')
        gender_label.configure(text = '')
        Detect_button(file_path)
        print("passed")
    except:
        pass

upload = Button(top, text = "Upload an Image", command = Upload_image, padx = 10, pady = 5)
upload.configure(background = '#364156', foreground = 'white', font = ('arial', 10, 'bold'))
upload.pack(side = 'bottom', pady = 50)

top.mainloop()
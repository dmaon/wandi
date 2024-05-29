from tkinter import *
from tkinter import ttk
from tkinter import PhotoImage, filedialog
from tkinter import messagebox
from PIL import ImageTk, Image
from setuptools import Command
import cv2
from wandi import *

class Application(Tk):



    def __init__(self,parent):
        Tk.__init__(self,parent)
        self.parent = parent

        # Variables
        self.img = self.canvasImage = None
        self.canvasWidth = self.canvasHeight = 0
        self.x = self.y = 0
        self.cv2image = None # base image of canvas
        self.lastImage = None # last modification on image
        self.anySelection = False

        # Instances
        self.wand = Wandi()

        self.createWidgets()



    def createWidgets(self):

        # Init

        # Main frame with padding
        self.form = ttk.Frame(self)
        self.form.grid(row=0, column=0, sticky=(N,E,S,W), padx=(5,3), pady=5)

        # Widgets of left side frame
        self.leftFrame = ttk.Frame(self.form)
        self.leftFrame.grid(row=0, column=0, sticky=(N,E,S,W))
        self.canvasBox = Canvas(self.leftFrame, bg="snow", relief=SUNKEN)
        self.canvasBox.bind('<Button-1>', self.getPosition)
        self.canvasBox.bind('<Button-3>', self.clearSelection)
        self.canvasBox.grid(row=0, column=0, sticky=(N,E,S,W))
        self.canvasImage = self.canvasBox.create_image(0, 0, anchor='nw')

        # Widgets of right side frame
        self.rightFrame = ttk.Frame(self.form, width=200)
        self.rightFrame.grid(row=0, column=1, sticky=(N,E,S,W), padx=(6,4))

        # Load image frame
        self.loadImageFrame = ttk.LabelFrame(self.rightFrame, text="Selecting image:", padding=(10))
        self.loadImageFrame.grid(row=0, column=0, sticky=(N,E,S,W))

        self.imagePath = StringVar()
        self.imageAdressEntry = ttk.Entry(self.loadImageFrame, textvariable=self.imagePath)
        self.imageAdressEntry.grid(row=0, column=0, sticky=(W,E))
        
        self.loadImageBtn = ttk.Button(self.loadImageFrame, text="Load Image")
        self.loadImageBtn.bind('<Button-1>', self.selectImage)
        self.loadImageBtn.grid(row=1, column=0, sticky=(W,E), pady=(5,0))

        # Setting frame
        self.settings = ttk.LabelFrame(self.rightFrame, text="Settings:", padding=(10))
        self.settings.grid(row=1, column=0, sticky=(W,E))

        self.grayImageStatusValues = {"off":"image-color", "on":"image-gray"}
        self.grayImageStatusVar = StringVar(value=self.grayImageStatusValues["off"])
        self.grayImageStatus = ttk.Checkbutton(self.settings, text="Gray image", onvalue=self.grayImageStatusValues["on"], offvalue=self.grayImageStatusValues["off"], variable=self.grayImageStatusVar, command=self.changeColorMode)
        self.grayImageStatus.grid(row=0, column=0 ,sticky=(W,E))

        self.blurImageStatusValues = {"off":"no-blur", "on":"has-blur"}
        self.blurImageStatusVar = StringVar(value=self.blurImageStatusValues["off"])
        self.blurImageStatus = ttk.Checkbutton(self.settings, text="Blurry image", onvalue=self.blurImageStatusValues["on"], offvalue=self.blurImageStatusValues["off"], variable=self.blurImageStatusVar, command=self.changeBlurMode)
        self.blurImageStatus.grid(row=1, column=0 ,sticky=(W,E))
        # self.imageBluryState = StringVar(value="blur-none")
        # self.imageBluryState.set(1)
        # languages = [
        #     ("No blur image", "blur-none"),
   	    #     ("Blur one", "blur-one"),
        #     ("Blur two", "blur-two"),
        #     ("Blur three", "blur-three"),
        # ]
        # i = 1
        # for language, val in languages:
        #     ttk.Radiobutton(self.settings, text=language, variable=self.imageBluryState, value=val, command=self.changeBlurMode).grid(row=i, column=0, sticky=(W,E))
        #     i += 1


        blurTypes = ('Simple blur', 'Gaussian blur', 'Median blur')
        self.blurImageType = StringVar()
        self.blurImageTypeComboLabel = ttk.Label(self.settings, text="Blur type")
        self.blurImageTypeCombo = ttk.Combobox(self.settings, textvariable = self.blurImageType)
        # self.blurImageTypeCombo.bind('<<ComboboxSelected>>', self.changeBlurMode)
        self.blurImageTypeCombo.bind('<<ComboboxSelected>>', lambda event: self.changeBlurMode())
        self.blurImageTypeCombo['values'] = blurTypes
        self.blurImageTypeComboLabel.grid(row=2, column=0, sticky=(W,E))
        self.blurImageTypeCombo.grid(row=3, column=0 ,sticky=(W,E))
        self.blurImageTypeCombo.current(0)

        # self.blurIntensity = IntVar(value=1)
        # self.blurIntensitySpinboxLabel = ttk.Label(self.settings, text="Blur intensity")
        # self.blurIntensitySpinbox = ttk.Spinbox(self.settings, from_=1, to=20, textvariable=self.blurIntensity)
        # self.blurIntensitySpinboxLabel.grid(row=4, column=0, sticky=(W,E))
        # self.blurIntensitySpinbox.grid(row=5, column=0, sticky=(W,E))

        self.kernelSize = IntVar(value=3)
        self.kernelSizeSpinboxLabel = ttk.Label(self.settings, text="Kernel size")
        self.kernelSizeSpinbox = ttk.Spinbox(self.settings, from_=3, to=21, increment=2, textvariable=self.kernelSize, command=self.changeBlurMode)
        self.kernelSizeSpinboxLabel.grid(row=6, column=0, sticky=(W,E))
        self.kernelSizeSpinbox.grid(row=7, column=0, sticky=(W,E))

        self.minThr = IntVar(value=30)
        self.minThrSpinboxLabel = ttk.Label(self.settings, text="Minimum threshold")
        self.minThrSpinbox = ttk.Spinbox(self.settings, from_=10, to=70, textvariable=self.minThr)
        self.minThrSpinboxLabel.grid(row=8, column=0, sticky=(W,E))
        self.minThrSpinbox.grid(row=9, column=0, sticky=(W,E))

        self.maxThr = IntVar(value=30)
        self.maxThrSpinboxLabel = ttk.Label(self.settings, text="Maximum threshold")
        self.maxThrSpinbox = ttk.Spinbox(self.settings, from_=10, to=70, textvariable=self.maxThr)
        self.maxThrSpinboxLabel.grid(row=10, column=0, sticky=(W,E))
        self.maxThrSpinbox.grid(row=11, column=0, sticky=(W,E))


        # Exit button
        self.exitBtn = ttk.Button(self.rightFrame, text="Exit", command=self.quit)
        self.exitBtn.grid(row=2, column=0, sticky=(W,E), pady=(5,0))



        self.grid_columnconfigure(0,weight=1)
        self.grid_rowconfigure(0,weight=1)

        self.form.grid_columnconfigure(0,weight=1)
        # self.form.grid_columnconfigure(1,weight=1) # This line for static width of frame should be comment 
        self.form.grid_rowconfigure(0,weight=1)
        
        self.leftFrame.grid_columnconfigure(0,weight=1)
        self.leftFrame.grid_rowconfigure(0,weight=1)

        self.rightFrame.grid_columnconfigure(0,weight=1)

        self.loadImageFrame.grid_columnconfigure(0,weight=1)
    

    def getCanvasSize(self):
        # Get canvas width and height
        self.canvasWidth = self.canvasBox.winfo_width()
        self.canvasHeight = self.canvasBox.winfo_height()


    def checkFileIsValid(self, filePath):
        if(len(filePath) > 0):
            fileExtension = filePath.split('.')[-1]
            if (fileExtension == "png"):
                return True
        return False


    # Show openfiledialog for choosing a file
    def selectImage(self, event):
        filePath = filedialog.askopenfilename(
            # initialdir='/',
            title='Open a sample',
            filetypes=[
                ("PNG Files", ".png"),
                ])

        if (self.checkFileIsValid(filePath)):
           # Set image path entry
            self.imagePath.set(filePath)
            self.canvasChangeImage()


    def canvasChangeImage(self):
        self.changeColorMode()


    def changeColorMode(self):
        self.getCanvasSize()
        imagePath = self.imageAdressEntry.get()

        if (self.checkFileIsValid(imagePath) == False):
            return False

        image = cv2.imread(imagePath)
        height, width = image.shape[:2]
        max_height =  self.canvasHeight
        max_width = self.canvasWidth

        if (self.grayImageStatusVar.get() == self.grayImageStatusValues["off"]):
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # only shrink if image is bigger than required
        if (max_height < height or max_width < width):
            image = cv2.resize(image, (max_width, max_height), interpolation=cv2.INTER_AREA)


        self.cv2image = image.copy()
        self.lastImage = image.copy()
        
        self.img = ImageTk.PhotoImage(image=Image.fromarray(image))
        self.canvasBox.itemconfig(self.canvasImage, image = self.img)

        if (self.blurImageStatusVar.get() == self.blurImageStatusValues["on"]):
            self.changeBlurMode()
        # else:
        #     self.selectWithWand()


    def changeBlurMode(self):
        if (self.cv2image is None):
            return False


        if (self.blurImageStatusVar.get() == self.blurImageStatusValues["off"]):
            self.changeColorMode()
        else:
            blurType = self.blurImageType.get()
            kernelSize = self.kernelSize.get()
            self.img = self.cv2image.copy()

            if (blurType == "Simple blur"):
                self.img = cv2.blur(self.img, (kernelSize,kernelSize))
            elif (blurType == "Gaussian blur"):
                self.img = cv2.GaussianBlur(self.img, (kernelSize,kernelSize), 0)
            elif (blurType == "Median blur"):
                self.img = cv2.medianBlur(self.img, kernelSize)
                
            self.lastImage = self.img.copy()

            self.img = ImageTk.PhotoImage(image=Image.fromarray(self.img))
            self.canvasBox.itemconfig(self.canvasImage, image = self.img)

            # if (self.anySelection):
            #     self.selectWithWand()


    def getPosition(self, event):
        self.x, self.y
        self.x = event.x
        self.y = event.y
        self.selectWithWand()     


    def selectWithWand(self):
        if (self.lastImage is None):
            return False

        # opencv coordinate => [row][col]
        # system coordinate => [x][y]
        self.wand.row = self.y # row = y
        self.wand.col = self.x # col = x
        self.wand.image = self.lastImage.copy()
        nrow, ncol = self.wand.image.shape[:2]
        imageColorMode = (self.grayImageStatusVar.get() == self.grayImageStatusValues["on"])

        if (self.x < ncol and self.y < nrow):
            sample = self.wand.image[self.wand.row][self.wand.col]
            self.img = self.wand.wandi(self.wand.image, (self.wand.row, self.wand.col), min=sample, max=sample, dynamicThr=True, isGray=imageColorMode,ds=[sample, 1])
            self.img = ImageTk.PhotoImage(image=Image.fromarray(self.img))
            self.canvasBox.itemconfig(self.canvasImage, image = self.img)
            self.anySelection = True


    def clearSelection(self, event):
        if (self.anySelection == False and self.lastImage is None):
            return False

        self.img = ImageTk.PhotoImage(image=Image.fromarray(self.lastImage))
        self.canvasBox.itemconfig(self.canvasImage, image = self.img)

        self.anySelection = False



if __name__ == "__main__":

    window_height = 600
    window_width = 1000

    app = Application(None)
    app.title("Sample application")
    app.minsize(window_width, window_height)
    app.attributes('-zoomed', True)    

    # Center position
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    app.mainloop()
    


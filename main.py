from gui import *

if __name__ == "__main__":

    window_height = 600
    window_width = 1000

    app = Application(None)
    app.title("Wandi")
    app.minsize(window_width, window_height)
    app.attributes('-zoomed', True)    

    # Center position
    screen_width = app.winfo_screenwidth()
    screen_height = app.winfo_screenheight()
    x_cordinate = int((screen_width/2) - (window_width/2))
    y_cordinate = int((screen_height/2) - (window_height/2))
    app.geometry("{}x{}+{}+{}".format(window_width, window_height, x_cordinate, y_cordinate))

    app.mainloop()
import tkinter as tk
from PIL import ImageTk, Image

class Home(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("800x600")
        
        self._frame = None
        self.switch_frame(StartPage)

    def switch_frame(self, frame_class):
        new_frame = frame_class(self)
        if self._frame is not None:
            self._frame.destroy()
        self._frame = new_frame
        self._frame.pack()

class StartPage(tk.Frame):
    def __init__(self, master):
        
        tk.Frame.__init__(self, master)
        master.title("♬")
        tk.Label(self, text="Music Application", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        tk.Label(self).pack(side="top", fill="x", pady=5)
        tk.Button(self, text="Play music ▶",
                  command=lambda: master.switch_frame(PlayWindow)).pack()
        tk.Button(self, text="Download music ⇩",
                  command=lambda: master.switch_frame(DownloadWindow)).pack()

class PlayWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("♬")
        
        # tk.Frame.configure(self,bg='blue')
        # tk.Label(self, text="Page one", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        
        tk.Label(self, text= "Play Music").pack()
        tk.Label(self).pack()

        frame_control = tk.Frame(self)
        frame_search = tk.Frame(self)

        tk.Button(frame_control, text="Delete").grid(row=0, column=3)
        tk.Button(frame_control, text="Play").grid(row=0, column=0)
        tk.Button(frame_control, text="Pause/Unpause").grid(row=0, column=1)
        tk.Button(frame_control, text="Stop").grid(row=0, column=2)

        frame_control.pack()

        tk.Label(frame_search, width='40').grid(row=0,column=0)
        tk.Entry(frame_search, width='44').grid(row=0,column=1)
        tk.Button(frame_search, text='Search').grid(row=0,column=2)

        frame_search.pack()

        listSongs = tk.Listbox(self, width= '100', height='30', selectmode= 'SINGLE')

        listSongs.insert(1, "Hay trao cho anh - SON TUNG MTP")
        listSongs.insert(1, "SO FAR AWAY")
        listSongs.pack()

        tk.Button(self, text="Back", command=lambda: master.switch_frame(StartPage)).pack()
class DownloadWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # tk.Frame.configure(self,bg='red')
        # tk.Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        
        tk.Label(self, text= "Download Music").pack()
        tk.Label(self).pack()

        frame_search = tk.Frame(self)

        tk.Entry(frame_search, width='44').pack(side='left')
        tk.Button(frame_search, text='Search').pack(side='left')

        frame_search.pack()
        tk.Label(self).pack()

        listSongs = tk.Listbox(self, width= '100', height='20', selectmode= 'SINGLE')
        listSongs.pack()

        tk.Button(self, text='Download').pack()

        tk.Label(self).pack()
        tk.Button(self, text="Back", command=lambda: master.switch_frame(StartPage)).pack()

if __name__ == "__main__":
    app = Home()
    app.mainloop()
import tkinter as tk
from PIL import ImageTk, Image
from youtube_dl import YoutubeDL
import json



class Home(tk.Tk):
    def __init__(self):
        tk.Tk.__init__(self)
        self.geometry("800x600")
        self.config(bg='silver')
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
        tk.Label(self, text="Music Application",bd=2, font=('Consolas', 18, "bold",'underline')).pack(side="top", fill="x", pady=5)
        tk.Label(self,heigh=5).pack(side="top", fill="x", pady=5)
        tk.Button(self,height=5,bd=2,bg='gray', text="Play music ▶",width=30, font='Consolas 12',
                  command=lambda: master.switch_frame(PlayWindow)).pack()
        tk.Label(self,heigh=5).pack(side="top", fill="x", pady=5)
        tk.Button(self, height=5,bd=2,bg='gray', text="Download music ⇩",width=30, font='Consolas 12',
                  command=lambda: master.switch_frame(DownloadWindow)).pack()

        tk.Label(self, text='Enjoy each melody ☊', font='Consolas 14', height=100).pack()
class PlayWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        master.title("♬")
        
        tk.Label(self, text= "Play Music",font='Consolas 14').pack()
        tk.Label(self).pack()

        frame_control = tk.Frame(self)
        frame_search = tk.Frame(self)
        frame_volume = tk.Frame(self)

        tk.Button(frame_control,bg='gray',width=5,bd=2, text="✘",font='Consolas 10', command=self.delete).grid(row=0, column=3)
        tk.Button(frame_control, bg='gray',text="▶",bd=2,font='Consolas 10',width=5, command= self.play).grid(row=0, column=0)
        self.option = False
        self.pauseBtn = tk.Button(frame_control,bg='gray',bd=2,font='Consolas 10',width=5, text="▶/||", command=self.pause)
        self.pauseBtn.grid(row=0, column=1)
        tk.Button(frame_control, text="▮",width=5,bg='gray',bd=2,font='Consolas 10',command=self.stop).grid(row=0, column=2)
        
        frame_control.pack()
        
        self.value=tk.IntVar()
        self.volume = tk.Scale(frame_volume, variable=self.value,from_=0, to=100, bd=2, orient='horizontal',command=self.set_Volume)
        self.volume.grid(row=0, column=1)
        self.down = tk.PhotoImage(file='down.png')
        tk.Label(frame_volume, image=self.down).grid(row=0, column=0)
        self.up = tk.PhotoImage(file='up.png')
        tk.Label(frame_volume, image=self.up).grid(row=0, column=2)
        tk.Label(frame_volume,width=60).grid(row= 0, column=3)
        frame_volume.pack()

        tk.Label(frame_search, width='40').grid(row=0,column=0)
        self.search_entry = tk.Entry(frame_search,bd=2, width='44',font='Consolas 10')
        self.search_entry.grid(row=0,column=1)
        self.search_btn = tk.Button(frame_search, bg='gray',bd=2,text='Search',font='Consolas 10',command=self.search)
        self.search_btn.grid(row=0,column=2)

        frame_search.pack()

        self.listSongs = tk.Listbox(self, width= '100',bd=2,font='Consolas 10', height='26', selectmode= 'SINGLE')
        self.loadMusic()
        self.listSongs.pack()

        tk.Button(self, text="Back",bd=2,font='Consolas 10', bg='gray',command=lambda: master.switch_frame(StartPage)).pack()
    
    def set_Volume(self,val):
        from pygame import mixer
        import pygame
        # print(float(val)*0.01)
        mixer.init()
        pygame.mixer.music.set_volume(float(val)*0.01)

    def play(self):
        # print(self.listSongs.curselection())
        
        with open('data.json', 'r') as file_json:
            data = json.load(file_json)

        position = self.listSongs.curselection()[0]
        id = data[position]['ID']

        import os
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        # Chạy nhạc
        from pygame import mixer
        mixer.init()
        # 'C:\\Users\\h\\Desktop\\SS1 Final Project\\songs'+'/%(id)s'
        mixer.music.load('.\\songs\\{}.mp3'.format(id))
        mixer.music.play()

    def pause(self):
        import pygame
        
        if self.option == False:
            pygame.mixer.music.pause()
            self.option = True
        else:
            pygame.mixer.music.unpause()
            self.option = False

    def stop(self):
        import pygame
        pygame.mixer.music.stop()

    def delete(self):
        lst = []
        with open('data.json', 'r') as file_json:
            data = json.load(file_json)

        lst = data
        
        position = self.listSongs.curselection()[0]
        id=lst[position]['ID']

        del lst[position]

        with open('data.json', 'w') as outfile:
            json.dump(lst, outfile)
        
        import os
        os.remove('.\\songs\\{}.mp3'.format(id))

        # message delete successfully
        self.messagess = tk.messagebox.showinfo('♬','Success!')
        self.loadMusic()

    def loadMusic(self):
        with open('data.json', 'r') as file_json:
            data = json.load(file_json)

        if self.listSongs.size() != 0:
            self.listSongs.delete(0,self.listSongs.size() - 1)

        listBox = self.listSongs
        for i in range(len(data)):
            listBox.insert('end',data[i]['Title'])

    def search(self):
        
        keySearch = self.search_entry.get()

        if keySearch != '':
            with open('data.json', 'r') as file_json:
                data = json.load(file_json)
            # print(data[0]['tag'])
            if len(data) != 0:
                for i in range(len(data)):
                    if str(keySearch).upper() in data[i]['tag'] or str(keySearch).lower() in data[i]['tag']:
                        self.listSongs.delete(0,self.listSongs.size() - 1)
                        self.listSongs.insert(1,data[i]['Title'])
        else:
            self.loadMusic()

class DownloadWindow(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        # tk.Frame.configure(self,bg='red')
        # tk.Label(self, text="Page two", font=('Helvetica', 18, "bold")).pack(side="top", fill="x", pady=5)
        
        tk.Label(self, text= "Download Music",font='Consolas 14').pack()
        tk.Label(self).pack()

        frame_search = tk.Frame(self)

        self.input = tk.Entry(frame_search,bd=2,font='Consolas 10', width='44')
        self.input.pack(side='left')
        self.btnDownload = tk.Button(frame_search,bd=2,bg='gray',font='Consolas 10', text='Search',command=self.search)
        self.btnDownload.pack(side='left')
        frame_search.pack()
        tk.Label(self).pack()

        self.litsBox = tk.Listbox(self,bd=2, width= '100',font='Consolas 10', height='26', selectmode= 'SINGLE')
        self.litsBox.pack()

        tk.Button(self, text='Download',bd=2,bg='gray',font='Consolas 10',command=self.download).pack()
        
        tk.Label(self).pack()
        tk.Button(self, text="Back",bd=2,bg='gray',font='Consolas 10', command=lambda: master.switch_frame(StartPage)).pack()

    def saveData(self, obj):
        lst = []
        with open('data.json', 'r') as file_json:
            data = json.load(file_json)

        lst = data
        lst.append(obj)
        # sort by title
        for i in range(len(lst)):
            for j in range(len(lst)):
                if lst[j]['Title'][0] > lst[i]['Title'][0]:
                    temp = lst[i]
                    lst[i] = lst[j]
                    lst[j] = temp

        with open('data.json', 'w') as outfile:
            json.dump(lst, outfile)

    def download(self):
        from tkinter import messagebox
        self.messages = tk.messagebox.showinfo('♬','Download...\nWait a minute!')
        index = self.litsBox.curselection()
        # print(index[0])
        # print(self.litsBox.get(index))

        with open('search.json') as json_file:
            data = json.load(json_file)
        
        id = data['entries'][index[0]]['id']

        options = {
            # lấy tên file down về là id của video, lấy id làm tên file để tiện quản lí
            'outtmpl': '.\\songs'+'/%(id)s',
            'postprocessors': [{
                'key': 'FFmpegExtractAudio',  # Tách lấy audio
                'preferredcodec': 'mp3',  # Format ưu tiên là mp3
                'preferredquality': '192',  # Chất lượng bitrate

            }]
        }

        ydl = YoutubeDL(options)
        # download() có thể truyền vào 1 str hoặc 1 list
        ydl.download(["https://www.youtube.com/watch?v={}".format(id)])

        obj = {
            'ID': data['entries'][index[0]]['id'],
            'Title': data['entries'][index[0]]['title'],
            'Creator': data['entries'][index[0]]['creator'],
            'Duration': data['entries'][index[0]]['duration'],
            'tag' : data['entries'][index[0]]['tags']
        }   

        self.saveData(obj)

        from tkinter import messagebox
        self.mess = tk.messagebox.showinfo('♬','Success!')
    
    def search(self):
        from tkinter import messagebox
        self.message = tk.messagebox.showinfo('♬','Searching...\nWait a minute!')

        key = self.input.get()
        
        options = {
            'default_search': 'ytsearch10',
            'quiet': True
        }

        ydl = YoutubeDL(options)
        search_result = ydl.extract_info(key, download=False)

        with open('search.json', 'w', encoding="utf8") as json_file:
            json.dump(search_result, json_file)
        
        songs = search_result["entries"]

        listSongs = self.litsBox

        if listSongs.size() != 0:
            listSongs.delete(0,listSongs.size() - 1)
        
        for i in range(len(songs)):
            listSongs.insert((i+1),songs[i]['title'])

if __name__ == "__main__":
    app = Home()
    app.mainloop()
import json
import pygame
from youtube_dl import YoutubeDL


def showMenu():
    print('Hello this is TK music app')
    print('Pick one of a option:')
    print('1. Show ALL songs')
    print('2. Show detail of a song')
    print('3. Play a song')
    print('4. Search and download the song')
    print('5. Exit')

def showAllSongs():
    with open('data.json', 'r') as json_file:
        songs = json.load(json_file)

    if len(songs) != 0:
        for i in range(len(songs)):
            print(str(i+1) + '.' + songs[i]['Title'])
            # print('   Title: ' + songs[i]['Title'])
            # print('   Creator: ' + songs[i]['Creator'])
            # print('   Duration: ' + str(songs[i]['Duration']))
    else:
        print('Song list is empty')

def showDetailOfSong():
    showAllSongs()

    with open('data.json', 'r') as json_file:
        songs = json.load(json_file)

    if len(songs) != 0:
        try:
            position = int(input("Enter song number: "))
            if position in range(len(songs) + 1):
                print(str(position) + '.' + ' Title: ' +
                      songs[position-1]['Title'])
                print("   Id: "+ songs[position-1]['ID'])
                if songs[position-1]['Creator'] != None:
                    print('   Creator: ' + songs[position-1]['Creator'])
                print('   Duration: ' + str(songs[position-1]['Duration']))
        except Exception as err:
            print(err)
    else:
        print('Song list is empty')


def downloadSong(id):
    options = {
        # lấy tên file down về là id của video, lấy id làm tên file để tiện quản lí
        'outtmpl': '%(id)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',  # Tách lấy audio
            'preferredcodec': 'mp3',  # Format ưu tiên là mp3
            'preferredquality': '192',  # Chất lượng bitrate

        }]
    }

    ydl = YoutubeDL(options)
    # download() có thể truyền vào 1 str hoặc 1 list
    ydl.download(["https://www.youtube.com/watch?v={}".format(id)])


def saveData(obj):
    lst = []
    with open('data.json', 'r') as file_json:
        data = json.load(file_json)

    lst = data

    lst.append(obj)

    with open('data.json', 'w') as outfile:
        json.dump(lst, outfile)


def searchAndDownload():
    print('Enter the song you want to search')
    key = input('>>> ')

    print('Searching for songs, please wait ...')

    options = {
        'default_search': 'ytsearch5',
        'quiet': True
    }

    ydl = YoutubeDL(options)
    search_result = ydl.extract_info(key, download=False)

    with open('search.json', 'w', encoding="utf8") as json_file:
        json.dump(search_result, json_file)

    songs = search_result["entries"]

    for i in range(len(songs)):
        print(str(i+1) + '. ' + str(songs[i]['title']))

    print('Enter the song position you want to download')
    print("Enter (0) if you don't want download anything")
    posDownload = int(input('>>> '))
    #print(videos[posDownload -1]['id'])

    if posDownload == 0:
        pass
    elif int(posDownload) in [1, 2, 3, 4, 5]:
        downloadSong(songs[posDownload - 1]['id'])

        obj = {
            'ID': songs[posDownload - 1]['id'],
            'Title': songs[posDownload - 1]['title'],
            'Creator': songs[posDownload - 1]['creator'],
            'Duration': songs[posDownload - 1]['duration']
        }

        saveData(obj)

    else:
        print('Wrong input!')


def playMusic():
    showAllSongs()

    with open('data.json', 'r') as json_file:
        songs = json.load(json_file)

    try:
        pos = int(input('Enter song number to play: '))
        id = songs[pos-1]['ID']

        import os
        os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
        # Chạy nhạc
        from pygame import mixer
        mixer.init()
        mixer.music.load('{}.mp3'.format(id))
        mixer.music.play()

        while True:
            controller = input('Enter playback option(unpause, pause, stop): ')

            if controller == 'pause':
                pygame.mixer.music.pause()
            elif controller == 'stop':
                pygame.mixer.music.stop()
                break
            elif controller == 'unpause':
                pygame.mixer.music.unpause()

    except Exception as err:
        print(err)


condition = True
while condition:
    showMenu()
    try:
        n = int(input('>>> '))

        if n == 1:
            showAllSongs()
            input('Press any key to continue ...')
        elif n == 2:
            showDetailOfSong()
            input('Press any key to continue ...')
        elif n == 3:
            playMusic()
            input('Press any key to continue ...')
        elif n == 4:
            searchAndDownload()
            input('Press any key to continue ...')
        elif n == 5:
            condition = False
            print('Goodbye!')
        else:
            print('Wrong option! Please pick again!')
            input('Press any key to continue ...')
    except Exception as err:
        print(err)

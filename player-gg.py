import os.path
import tkinter as tk
from pygame import mixer
from ttkthemes import themed_tk as t_tk
from tkinter import ttk, filedialog
import mutagen
from mutagen.mp3 import MP3
from PIL import Image, ImageTk
import time


# noinspection PyShadowingNames
class MediaPlayer:
    def __init__(self, window):
        style = ttk.Style()
        style.theme_use("breeze")

        background = "gray"

        style.configure("Tscale", background=background)
        self.root = window
        self.root.configure(bg="black")
        # ----------------------------------------------------------------------------------------------------------------------
        # Button Icons

        self.play_icon = Image.open('Music Player/play.png')
        self.play_icon = self.play_icon.resize((40, 40), Image.Resampling.LANCZOS)
        self.play_icon = ImageTk.PhotoImage(self.play_icon)

        self.pause_icon = Image.open('Music Player/pause.png')
        self.pause_icon = self.pause_icon.resize((40, 40), Image.Resampling.LANCZOS)
        self.pause_icon = ImageTk.PhotoImage(self.pause_icon)

        self.rewind_icon = Image.open('Music Player/previous.png')
        self.rewind_icon = self.rewind_icon.resize((40, 40), Image.Resampling.LANCZOS)
        self.rewind_icon = ImageTk.PhotoImage(self.rewind_icon)

        self.next_icon = Image.open('Music Player/next.png')
        self.next_icon = self.next_icon.resize((40, 40), Image.Resampling.LANCZOS)
        self.next_icon = ImageTk.PhotoImage(self.next_icon)

        self.speaker_icon = Image.open('Music Player/speaker.png')
        self.speaker_icon = self.speaker_icon.resize((30, 30), Image.Resampling.LANCZOS)
        self.speaker_icon = ImageTk.PhotoImage(self.speaker_icon)

        self.delete_icon = Image.open("Music Player/delete.png")
        self.delete_icon = self.delete_icon.resize((30, 30), Image.Resampling.LANCZOS)
        self.delete_icon = ImageTk.PhotoImage(self.delete_icon)

        self.delete_all_icon = Image.open("Music Player/delete2.png")
        self.delete_all_icon = self.delete_all_icon.resize((30, 30), Image.Resampling.LANCZOS)
        self.delete_all_icon = ImageTk.PhotoImage(self.delete_all_icon)

        self.add_icon = Image.open("Music Player/song.png")
        self.add_icon = self.add_icon.resize((30, 30), Image.Resampling.LANCZOS)
        self.add_icon = ImageTk.PhotoImage(self.add_icon)

        self.shuffle_icon = Image.open("Music Player/shuffle.png")
        self.shuffle_icon = self.shuffle_icon.resize((30, 30), Image.Resampling.LANCZOS)
        self.shuffle_icon = ImageTk.PhotoImage(self.shuffle_icon)

        self.repeat_icon = Image.open("Music Player/repeat.png")
        self.repeat_icon = self.repeat_icon.resize((30, 30), Image.Resampling.LANCZOS)
        self.repeat_icon = ImageTk.PhotoImage(self.repeat_icon)

        self.auto_play_icon = Image.open("Music Player/auto_play.png")
        self.auto_play_icon = self.auto_play_icon.resize((30, 30), Image.Resampling.LANCZOS)
        self.auto_play_icon = ImageTk.PhotoImage(self.auto_play_icon)

        self.stop_icon = Image.open("Music Player/stop.png")
        self.stop_icon = self.stop_icon.resize((40, 40), Image.Resampling.LANCZOS)
        self.stop_icon = ImageTk.PhotoImage(self.stop_icon)

        self.add_multiple_icon = Image.open("Music Player/song2.png")
        self.add_multiple_icon = self.add_multiple_icon.resize((40, 40), Image.Resampling.LANCZOS)
        self.add_multiple_icon = ImageTk.PhotoImage(self.add_multiple_icon)

        self.home_icon = Image.open("Music Player/logohome.png")
        self.home_icon = ImageTk.PhotoImage(self.home_icon)

        # ----------------------------------------------------------------------------------------------------------------------
        # SCREEN PLACEMENT

        tk.Label(self.root, text="", background=background, height=8, width=120).place(x=5, y=400)

        self.play_list = tk.Listbox(self.root, width=30, height=18, bg="black", fg="blue")
        self.play_list.place(x=300, y=60)

        self.time_elapsed_label = tk.Label(self.root, text="00:00:00", fg="blue", background=background, padx=5,
                                           activebackground=background)
        self.time_elapsed_label.place(x=8, y=400)

        self.music_duration_label = tk.Label(self.root, text="00:00:00", fg="blue", background=background, padx=5,
                                             activebackground=background)
        self.music_duration_label.place(x=480, y=400)

        self.progress_scale = ttk.Scale(self.root, orient="horizontal", from_=0, length=410,
                                        command=self.progress_scale_moved,
                                        cursor="hand2")
        self.progress_scale.place(x=70, y=400)

        self.play_button = tk.Button(self.root, image=self.play_icon, command=self.play_pause_checker, cursor="hand2",
                                     bd=0,
                                     background=background, activebackground=background)
        self.play_button.place(x=210, y=450)

        self.next_button = tk.Button(self.root, image=self.next_icon, command=self.next_song, cursor="hand2", bd=0,
                                     background=background, activebackground=background)
        self.next_button.place(x=330, y=450)

        self.rewind_button = tk.Button(self.root, image=self.rewind_icon, command=self.previous_song, cursor="hand2",
                                       bd=0,
                                       background=background, activebackground=background)
        self.rewind_button.place(x=150, y=450)

        self.speaker_button = tk.Button(self.root, image=self.speaker_icon, command="command", cursor="hand2", bd=0,
                                        background=background, activebackground=background)
        self.speaker_button.place(x=185, y=500)

        self.shuffle_button = tk.Button(self.root, image=self.shuffle_icon, command="command", cursor="hand2",
                                        bd=0, background=background, activebackground=background)
        self.shuffle_button.place(x=105, y=455)

        self.repeat_button = tk.Button(self.root, image=self.repeat_icon, command=self.repeat_song, cursor="hand2",
                                       bd=0, background=background, activebackground=background)
        self.repeat_button.place(x=385, y=455)

        self.volume_scale = ttk.Scale(self.root, from_=0, to=100, orient="horizontal", command="simple",
                                      cursor="hand2")
        self.volume_scale.place(x=210, y=506)

        self.auto_play_button = tk.Button(self.root, image=self.auto_play_icon, command="command", cursor="hand2",
                                          bd=0, background=background, activebackground=background)
        self.auto_play_button.place(x=330, y=500)

        self.stop_button = tk.Button(self.root, image=self.stop_icon, command="command", cursor="hand2",
                                     bd=0, background=background, activebackground=background)
        self.stop_button.place(x=270, y=450)

        self.home_label = tk.Label(self.root, image=self.home_icon)
        self.home_label.place(x=60, y=60)

        self.song_name_show = tk.Listbox(self.root, background=background)
        self.song_name_show.place(x=60, y=280, width=200, height=100)

        # --------------------------------------------------------------------------------------------------------------

        self.status = tk.Label(self.root, text="Playing-------- Song: 0 of 0", fg="black", anchor="w",
                               background=background, font="Lucia 9 bold", bd=5, relief="ridge", width=500)
        self.status.place(x=5, y=540, relwidth=1)

        self.menu = tk.Menu(self.root)
        self.root.configure(menu=self.menu)

        m1 = tk.Menu(self.menu, background="grey", tearoff=False, bd=0, activebackground="black")
        self.menu.add_cascade(label="Actions", menu=m1)

        m1.add_command(label="Add Song", command=self.add_songs, image=self.add_icon, compound="left")

        m2 = tk.Menu(self.menu, background="grey", tearoff=False, bd=0, activebackground="black")
        self.menu.add_cascade(label="Delete", menu=m2)

        m2.add_command(label="Delete Song", command="command", image=self.delete_icon, compound="left")
        m2.add_command(label="Delete All Songs", command="command", image=self.delete_all_icon, compound="left")

        # ----------------------------------------------------------------------------------------------------------------------

        self.directory_list = []
        self.songs_to_play = []
        self.repeat_condition = False
        self.pause = False

    # ----------------------------------------------------------------------------------------------------------------------
    # BACK-END FUNCTIONS
    def add_songs(self):
        songs = filedialog.askopenfilenames(title="Select Music Folder", filetypes=(("mp3 files", '*.mp3'),
                                                                                    ("webm files", "*.webm")))
        for song in songs:
            song_name = os.path.basename(song)
            directory_path = song.replace(song_name, "")
            self.directory_list.append({'path': directory_path, 'song': song_name})
            self.play_list.insert('end', song_name)

        self.play_list.select_set('0')

    def play_pause_checker(self):
        try:
            self.songs_to_play.append(self.play_list.get('active'))
            length = len(self.songs_to_play)

            if len(self.songs_to_play) == 1:
                self.play_song()

            if self.songs_to_play[length - 1] != self.songs_to_play[length - 2]:
                self.root.after_cancel(self.updater)
                self.play_song()

            else:
                self.pause_unpause()
        except AttributeError:
            print("ATTRIBUTE ERROR")

    def pause_unpause(self):
        if not self.pause:
            self.root.after_cancel(self.updater)
            self.play_button.config(image=self.play_icon)
            self.pause = True

            self.status.config(text=f"Paused: {self.play_list.get('active')}===>{self.play_list.index('active')+1} "
                               f"of {self.play_list.size()}")
            mixer.music.pause()
        else:
            self.pause=False
            self.play_button.config(image=self.pause_icon)
            self.status.config(text=f"Playing: {self.play_list.get('active')}===>{self.play_list.index('active') + 1} "
                               f"of {self.play_list.size()}")
            mixer.music.unpause()
            self.scaler_update()

    def play_song(self):
        try:
            self.progress_scale['value'] = 0
            self.time_elapsed_label['text'] = "00:00:00"

            song_name = self.play_list.get('active')
            self.status.config(text=f"Playing: {song_name} Song: {self.play_list.index('active')} of "
                                    f"{self.play_list.size()}")

            directory_path = None
            for dictio in self.directory_list:
                if dictio['song'] == song_name:
                    directory_path = dictio['path']

            song_with_path = f"{directory_path}/{song_name}"
            music_data = MP3(song_with_path)
            self.music_length = int(music_data.info.length)
            self.music_duration_label['text'] = time.strftime('%H:%M:%S', time.gmtime(self.music_length))

            self.progress_scale['to'] = self.music_length
            self.play_button.config(image=self.pause_icon)
            mixer.music.load(song_with_path)
            mixer.music.play()
            self.scaler_update()
        except (FileNotFoundError, mutagen.MutagenError):
            print("INVALID!!")

    def progress_scale_moved(self, x):
        self.root.after_cancel(self.updater)

        scale_at = self.progress_scale.get()
        song_name = self.play_list.get('active')
        directory_path = None

        for dictio in self.directory_list:
            if dictio['song'] == song_name:
                directory_path = dictio['path']

        mixer.music.load(f"{directory_path}/{song_name}")
        mixer.music.play(0, scale_at)
        self.scaler_update()

    def scaler_update(self):
        if self.progress_scale['value'] < self.music_length:
            self.progress_scale['value'] += 1

            self.time_elapsed_label['text'] = time.strftime('%H:%M:%S', time.gmtime(self.progress_scale.get()))

            self.updater = self.root.after(1000, self.scaler_update)
        elif self.repeat_condition:
            self.play_song()
        else:
            self.progress_scale['value'] = 0
            self.time_elapsed_label['text'] = "00:00:00"

    def repeat_song(self):
        if not self.repeat_condition:
            self.repeat_condition = True
            self.repeat_button.config(image=self.repeat_button)
        else:
            self.repeat_condition = False
            self.repeat_button.config(image=self.repeat_icon)

    def next_song(self):
        self.root.after_cancel(self.updater)
        song_index = self.play_list.index('active')
        self.play_list.select_clear('active')

        list_length = self.play_list.size()

        if list_length - 1 == song_index:
            self.play_list.select_set(0)
            self.play_list.activate(0)
            self.play_pause_checker()
        else:
            self.play_list.select_set(song_index)
            self.play_list.activate(song_index + 1)
            self.play_pause_checker()

    def previous_song(self):
        self.root.after_cancel(self.updater)
        song_index = self.play_list.index('active')
        self.play_list.select_clear('active')

        list_length = self.play_list.size()

        if song_index == 0:
            self.play_list.select_set(list_length - 1)
            self.play_list.activate(list_length - 1)
            self.play_pause_checker()
        else:
            self.play_list.select_set(song_index - 1)
            self.play_list.activate(song_index - 1)
            self.play_pause_checker()


# ----------------------------------------------------------------------------------------------------------------------


if __name__ == "__main__":
    window = t_tk.ThemedTk()
    mixer.init()
    window.title("NOT-MUSIC-PLAYER")
    window.wm_iconbitmap('Music Player/music.ico')
    window.minsize(width=540, height=590)
    window.resizable(False, False)

    x = MediaPlayer(window)
    window.mainloop()

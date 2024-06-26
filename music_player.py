import os
import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import pygame
from mutagen.mp3 import MP3

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
        self.current = None

    def add_song(self, song):
        new_node = Node(song)
        if not self.head:
            self.head = new_node
            self.tail = new_node
            self.current = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def delete_song(self, song_name):
        current = self.head
        while current:
            if os.path.basename(current.data) == song_name:
                if current.prev:
                    current.prev.next = current.next
                if current.next:
                    current.next.prev = current.prev
                if current == self.head:
                    self.head = current.next
                if current == self.tail:
                    self.tail = current.prev
                if current == self.current:
                    self.current = current.next if current.next else current.prev
                return
            current = current.next

class MusicPlayer:
    def __init__(self, root):
        self.root = root
        self.root.title("Mp3 Player")
        self.root.geometry("875x450")
        self.root.configure(bg="#09ABA6") 

        self.song_list = DoublyLinkedList()
        self.paused = False

        self.init_player()
        self.init_ui()

    def init_ui(self):
        self.song_label = tk.Label(self.root, text="Now Playing: ", font=("Arial", 12), bg="#09ABA6")
        self.song_label.pack(pady=(10, 0))

        self.song_listbox = tk.Listbox(self.root, width=80, height=15, font=("Arial", 10), bg="white")
        self.song_listbox.pack(pady=20)
        self.song_listbox.bind('<<ListboxSelect>>', self.on_select_song)

        self.progress_bar_frame = tk.Frame(self.root, bg="#09ABA6")
        self.progress_bar_frame.pack(pady=20)

        self.elapsed_time_label = tk.Label(self.progress_bar_frame, text="0:00", font=("Arial", 10), bg="#09ABA6")
        self.elapsed_time_label.grid(row=0, column=0)
        
        self.style = ttk.Style()
        self.style.theme_use('default')
        self.style.configure("TProgressbar", background='blue') 

        self.progress_scale = ttk.Scale(self.progress_bar_frame, from_=0, to=1000, orient=tk.HORIZONTAL, length=800)
        self.progress_scale.grid(row=0, column=1)

        self.remaining_time_label = tk.Label(self.progress_bar_frame, text="0:00", font=("Arial", 10), bg="#09ABA6")
        self.remaining_time_label.grid(row=0, column=2)

        button_bg = "#378DF0" 
        button_fg = "white"

        self.volume_label = tk.Label(self.root, text="Volume: ", font=("Arial", 10), bg="#09ABA6")
        self.volume_label.pack(side=tk.LEFT, padx=10, pady=(10, 0))

        self.volume_slider = ttk.Scale(self.root, from_=0, to=1, orient=tk.HORIZONTAL, length=200, command=self.set_volume)
        self.volume_slider.set(0.5)
        self.volume_slider.pack(side=tk.LEFT, padx=10, pady=(10, 0))

        self.play_button = tk.Button(self.root, text="▶ Play", command=self.play_music, font=("Arial", 12), bg=button_bg, fg=button_fg)
        self.play_button.pack(side=tk.LEFT, padx=(50, 5), pady=5)

        self.pause_button = tk.Button(self.root, text="|| Pause", command=self.pause_music, font=("Arial", 12), bg=button_bg, fg=button_fg)
        self.pause_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.prev_button = tk.Button(self.root, text="⏮ Previous", command=self.play_previous, font=("Arial", 12), bg=button_bg, fg=button_fg)
        self.prev_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.next_button = tk.Button(self.root, text="Next ⏭", command=self.play_next, font=("Arial", 12), bg=button_bg, fg=button_fg)
        self.next_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_button = tk.Button(self.root, text="Add Song", command=self.add_song, font=("Arial", 12), bg=button_bg, fg=button_fg)
        self.add_button.pack(side=tk.RIGHT, padx=5, pady=5)

        self.delete_button = tk.Button(self.root, text="Delete Song", command=self.delete_song, font=("Arial", 12), bg=button_bg, fg=button_fg)
        self.delete_button.pack(side=tk.RIGHT, padx=5, pady=5)

    def init_player(self):
        pygame.init()
        pygame.mixer.init()
        self.root.after(1000, self.update_progress)  

    def set_volume(self, val):
        pygame.mixer.music.set_volume(float(val))

    def add_song(self):
        song = filedialog.askopenfilename(filetypes=[("Audio Files", "*.mp3;*.wav")])
        if song:
            self.song_list.add_song(song)
            song_name = os.path.basename(song)
            self.song_listbox.insert(tk.END, song_name)
            self.song_listbox.itemconfig(tk.END, {'fg': 'green'})  
            messagebox.showinfo("Song Added", f"Added: {song_name}")

    def delete_song(self):
      selected_song_index = self.song_listbox.curselection()
      if selected_song_index:
        selected_song_index = int(selected_song_index[0])
        song_name = self.song_listbox.get(selected_song_index)
        self.song_list.delete_song(song_name)
        self.song_listbox.delete(selected_song_index)
        messagebox.showinfo("Song Deleted", f"Deleted: {song_name}")
        self.update_playlist()


    def play_music(self):
        if self.song_list.current:
            if self.paused:
                pygame.mixer.music.unpause()
                self.paused = False
            else:
                pygame.mixer.music.load(self.song_list.current.data)
                pygame.mixer.music.play()
                self.update_progress()
                current_song = os.path.basename(self.song_list.current.data)
                self.song_label.config(text="Now Playing: " + current_song)

    def pause_music(self):
        if pygame.mixer.music.get_busy():
            pygame.mixer.music.pause()
            self.paused = True

    def play_next(self):
        if self.song_list.current and self.song_list.current.next:
            self.song_list.current = self.song_list.current.next
            self.play_music()
        else:
                messagebox.showinfo("No Next Song", "There is no next song available")    

    def play_previous(self):
        if self.song_list.current and self.song_list.current.prev:
            self.song_list.current = self.song_list.current.prev
            self.play_music()
        else:
                messagebox.showinfo("No Previous Song", "There is no previous song available")
    

    def update_playlist(self):
        self.song_listbox.delete(0, tk.END)
        current = self.song_list.head
        while current:
            song_name = os.path.basename(current.data)
            self.song_listbox.insert(tk.END, song_name)
            current = current.next

    def on_select_song(self, event):
        selected_song_index = self.song_listbox.curselection()
        if selected_song_index:
            selected_song_index = int(selected_song_index[0])
            current = self.song_list.head
            for _ in range(selected_song_index):
                current = current.next
            self.song_list.current = current
            self.play_music()

    def update_progress(self):
     if pygame.mixer.music.get_busy() and not self.paused:
        current_time = pygame.mixer.music.get_pos() / 1000
        if self.song_list.current:
            song = MP3(self.song_list.current.data)
            total_length = song.info.length
            progress = (current_time / total_length) * 1000
            self.progress_scale.set(progress)
            self.elapsed_time_label.config(text=self.format_time(current_time))
            remaining_time = total_length - current_time
            self.remaining_time_label.config(text='-' + self.format_time(remaining_time))
            if current_time >= total_length:  # Check if the current song has finished
                self.play_next()  # If finished, automatically play the next song
     self.root.after(100, self.update_progress)
  

    def format_time(self, time_sec):
       mins = time_sec // 60
       secs = time_sec % 60
       return f"{mins:01}" if mins >= 0 else "0:00"



        

if __name__ == "__main__":
    root = tk.Tk()
    music_player = MusicPlayer(root)
    root.mainloop()

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

    
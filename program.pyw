import tkinter
from tkinter import messagebox
import time
import random
import webbrowser
import threading
import pygame
pygame.init()

streamer_name = "" # change this to whatever your name is

KeyDown = 2
KeyUp = 3

JoyHatMotion = 9
JoyButtonDown = 10
JoyButtonUp = 11

down_strum = (0, -1)
up_strum = (0, 1)

watching_types = [
    pygame.QUIT,
    KeyDown,
    KeyUp,
    JoyHatMotion,
    JoyButtonDown,
    JoyButtonUp
]

right_paw_pos = (-20, 130)

class Program:
    def exit(self):
        pygame.quit()
        exit()

    def random_events(self):
        while (True):
            if (self.use_random):
                self.strum = True
                time.sleep(self.auto_bongo_delay)
                self.strum = False
                self.frets = [0]
                time.sleep(self.auto_bongo_delay)
                self.frets = []
            time.sleep(0.01)
            
    def console(self):
        while (True):
            user_input = input()
            exec(user_input)

    def open_options(self):
        def set_name(a, b, c):
            self.streamer_name = update_name.get()
            self.update_streamer_name()

        def auto_bongo_toggle():
            if (self.use_random):
                self.use_random = False

            else:
                self.use_random = True

            auto_bongo_button["text"] = "Disable auto-bongo" if self.use_random else "Enable auto-bongo"

        def show_streamer_toggle():
            if (self.display_streamer_name):
                self.display_streamer_name = False

            else:
                self.display_streamer_name = True

            show_streamer_button["text"] = "Show streamer name" if self.display_streamer_name else "Hide streamer name"
            
        def set_auto_bongo_speed():
            temp = float(bongo_speed_box.get())
            if (temp < 0.1):
                temp = 0.1
            self.auto_bongo_delay = temp

        def exit_window():
            window.destroy()

        def show_info():
            def open_url(url):
                webbrowser.open_new(url)
                
            info_window = tkinter.Tk()
            info_window.title("Info")
            info_window.resizable(False, False)
            
            info_label1 = tkinter.Label(info_window, text="Please report any bugs at:")
            info_label1.pack()
            
            issues_link = tkinter.Label(info_window, text="https://github.com/expliked/Guitar-Hero-Bongo-Cat/issues", fg="blue", cursor="hand2")
            issues_link.pack()
            issues_link.bind("<Button-1>", lambda e: open_url("https://github.com/expliked/Guitar-Hero-Bongo-Cat/issues"))
            
            info_label2 = tkinter.Label(info_window, text="Program created by expliked")
            info_label2.pack()

            info_label3 = tkinter.Label(info_window, text="Thanks for downloading!")
            info_label3.pack()

            info_window.geometry("350x250")
            info_window.mainloop()
            
        window = tkinter.Tk()
        window.title("Options")
        window.resizable(False, False)

        update_name = tkinter.StringVar()
        update_name.trace_add("write", set_name)
        streamer_name_label = tkinter.Label(window, text="Set streamer name")
        streamer_name_label.pack(padx=10, pady=(10, 0))
        
        streamer_name_box = tkinter.Entry(window, textvariable=update_name, width=20)
        streamer_name_box.pack(padx=10, pady=(5, 0))

        bongo_speed_label = tkinter.Label(window, text="Set auto-bongo speed interval")
        bongo_speed_label.pack(padx=10, pady=(10, 0))
        
        default_bongo_speed = tkinter.StringVar(value=str(self.auto_bongo_delay))
        bongo_speed_box = tkinter.Spinbox(window, from_=0.1, to=100, increment=0.1, textvariable=default_bongo_speed, width=10, command=set_auto_bongo_speed)
        bongo_speed_box.pack(padx=10, pady=(5, 0))

        auto_bongo_text = "Disable auto-bongo" if self.use_random else "Enable auto-bongo"
        auto_bongo_button = tkinter.Button(window, text=auto_bongo_text, command=auto_bongo_toggle)
        auto_bongo_button.pack(padx=10, pady=(0, 10))

        show_streamer_name_text = "Hide streamer name" if self.display_streamer_name else "Show streamer name"
        show_streamer_button = tkinter.Button(window, text=show_streamer_name_text, command=show_streamer_toggle)
        show_streamer_button.pack(padx=10, pady=(0, 10))
        
        confirm_button = tkinter.Button(window, text="Done", command=exit_window)
        confirm_button.pack(padx=10, pady=(20, 0))

        info_button = tkinter.Button(window, text="Info", command=show_info)
        info_button.pack(padx=10, pady=(10, 0))
        
        window.geometry("300x300")
        window.mainloop()



    def update_streamer_name(self):
        self.streamer_font = pygame.font.SysFont("Impact", 40)
        self.text_surface = self.streamer_font.render(self.streamer_name, False, (0, 0, 0))
        self.text_rectangle = self.text_surface.get_rect(center=(self.window_size[0] / 2, (self.window_size[1] / 2) + 225))
        
    def execute(self, window_name, window_size, use_random, use_delay, streamer_name):
        self.window_name = window_name
        self.window_size = window_size

        self.display_streamer_name = True
        self.streamer_name = streamer_name
        self.auto_bongo_delay = use_delay
        
        self.use_random = use_random
        
        pygame.display.set_caption(self.window_name)
        self.game_display = pygame.display.set_mode(self.window_size)
        self.game_clock = pygame.time.Clock()
        
        self.game_display.fill((255, 255, 255))
        pygame.display.update()

        bongo_not_strumming = pygame.image.load("assets/cat-0.png")
        bongo_strumming = pygame.image.load("assets/cat-1.png")

        bongo_not_fretting = pygame.image.load("assets/paw-right-0.png")
        
        bongo_fretting = [
            pygame.image.load("assets/paw-right-1.png"),
            pygame.image.load("assets/paw-right-2.png"),
            pygame.image.load("assets/paw-right-3.png"),
            pygame.image.load("assets/paw-right-5.png"),
            pygame.image.load("assets/paw-right-5.png")
        ]
        
        fretting_img = random.choice(bongo_fretting)
        
        try:
            self.controller = pygame.joystick.Joystick(0)
            
        except pygame.error:
            tkinter.Tk().withdraw()
            messagebox.showerror("Error", "Controller not detected or unplugged")
            self.exit()

        self.controller.init()

        self.update_streamer_name()
        
        self.frets = []
        previous_frets = []
        self.strum = False
        
        random_thread = threading.Thread(target=self.random_events)
        random_thread.start()
            
        while (True):
            for event in pygame.event.get():
                print(event)
                if (event.type not in watching_types):
                    continue

                if (event.type == pygame.QUIT):
                    self.exit()

                if (event.type == KeyDown):
                    if (event.key == 32): # space
                        options_thread = threading.Thread(target=self.open_options)
                        options_thread.start()
                        
                if not (self.use_random):
                    
                    if (hasattr(event, "button")):
                        if (event.button in [6, 7]):
                            if (event.type == 10):
                                self.strum = True
                                continue

                            if (event.type == 11):
                                self.strum = False
                                continue
                            
                        if (event.button not in [0, 1, 2, 3, 4]):
                            continue
                        if (event.type == JoyButtonDown):
                            
                            self.previous_frets = self.frets
                            self.frets.append(event.button)
                            fretting_img = random.choice(bongo_fretting)
                                
                            continue
                        
                        if (event.type == JoyButtonUp):
                            self.frets.remove(event.button)
                            continue
                        
                    if (hasattr(event, "hat")):
                        if (event.value == down_strum or event.value == up_strum):
                            self.strum = True
                            continue
                        
                        if (event.value == (0, 0)):
                            self.strum = False
                            continue
                    
            self.game_display.fill((255, 255, 255))
            
            if (self.strum):
                self.game_display.blit(bongo_strumming, (0, 0))
                
            else:
                self.game_display.blit(bongo_not_strumming, (0, 0))

            if (self.frets != previous_frets):
                self.game_display.blit(fretting_img, right_paw_pos)

            else:
                self.game_display.blit(bongo_not_fretting, right_paw_pos)

            if (self.display_streamer_name):
                self.game_display.blit(self.text_surface, self.text_rectangle)
                
            pygame.display.update()
            self.game_clock.tick(60)
            time.sleep(0.001)
            
if (__name__ == "__main__"):
    program = Program()
    program.execute("Guitar Hero Bongo Cat (press space for options)", (500, 500), False, 0.1, streamer_name)

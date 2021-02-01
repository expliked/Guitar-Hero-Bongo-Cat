import tkinter
from tkinter import messagebox
import time
import webbrowser
import threading
import pygame
pygame.init()

streamer_name = "expliked" # change this to whatever your name is

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
        def set_name():
            self.streamer_name = streamer_name_box.get()
            self.update_streamer_name()
            #window.destroy()

        def auto_bongo_toggle():
            if (self.use_random):
                self.use_random = False

            else:
                self.use_random = True

            auto_bongo_button["text"] = "Disable auto-bongo" if self.use_random else "Enable auto-bongo"

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
        
        streamer_name_box = tkinter.Entry(window, textvariable=tkinter.StringVar(window, value=self.streamer_name), width=20)
        streamer_name_box.pack(padx=10, pady=(10, 0))

        streamer_name_button = tkinter.Button(window, text="Set streamer name", command=set_name)
        streamer_name_button.pack(padx=10, pady=(5, 0))

        default_bongo_speed = tkinter.StringVar(value=str(self.auto_bongo_delay))
        bongo_speed_box = tkinter.Spinbox(window, from_=0.1, to=100, increment=0.1, textvariable=default_bongo_speed, width=10)
        bongo_speed_box.pack(padx=10, pady=(10, 0))

        bongo_speed_button = tkinter.Button(window, text="Set auto-bongo speed", command=set_auto_bongo_speed)
        bongo_speed_button.pack(padx=10, pady=(5, 10))
        
        auto_bongo_text = "Disable auto-bongo" if self.use_random else "Enable auto-bongo"
        auto_bongo_button = tkinter.Button(window, text=auto_bongo_text, command=auto_bongo_toggle)
        auto_bongo_button.pack(padx=10, pady=(0, 10))

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

        self.streamer_name = streamer_name
        self.auto_bongo_delay = use_delay
        
        self.use_random = use_random
        #console_thread = threading.Thread(target=self.console)
        #console_thread.start()
        
        pygame.display.set_caption(self.window_name)
        self.game_display = pygame.display.set_mode(self.window_size)
        self.game_clock = pygame.time.Clock()
        
        self.game_display.fill((255, 255, 255))
        pygame.display.update()
        
        bongo_none = pygame.image.load("assets/bongo_none.png")
        bongo_strumming = pygame.image.load("assets/bongo_strumming.png")
        bongo_fretting = pygame.image.load("assets/bongo_fretting.png")
        bongo_both = pygame.image.load("assets/bongo_both.png")
        
        try:
            self.controller = pygame.joystick.Joystick(0)
            
        except pygame.error:
            tkinter.Tk().withdraw()
            messagebox.showerror("Error", "Controller not detected or unplugged")
            self.exit()

        self.controller.init()

        self.update_streamer_name()
        
        self.frets = []
        self.previous_frets = []
        self.strum = False
        
        random_thread = threading.Thread(target=self.random_events)
        random_thread.start()
            
        while (True):
            for event in pygame.event.get():
                if (event.type not in watching_types):
                    continue

                print(event)
                #"""
                if (event.type == pygame.QUIT):
                    self.exit()

                if (event.type == KeyDown):
                    if (event.key == 32): # space
                        self.open_options()
                        
                if not (use_random):
                    if (hasattr(event, "button")):
                        if (event.type == JoyButtonDown):
                            self.frets.append(event.button)

                        if (event.type == JoyButtonUp):
                            self.frets.remove(event.button)

                    if (hasattr(event, "hat")):
                        if (event.value == down_strum or event.value == up_strum):
                            self.strum = True

                        if (event.value == (0, 0)):
                            self.strum = False
                #"""
            self.game_display.fill((255, 255, 255))
            
            if (self.frets and self.strum):
                self.game_display.blit(bongo_both, (0, 0))
                
            if (self.frets and not self.strum):
                self.game_display.blit(bongo_fretting, (0, 0))

            if (self.strum and not self.frets):
                self.game_display.blit(bongo_strumming, (0, 0))

            if (not self.strum and not self.frets):
                self.game_display.blit(bongo_none, (0, 0))

            self.game_display.blit(self.text_surface, self.text_rectangle)
            pygame.display.update()
            self.game_clock.tick(60)
            time.sleep(0.001)
            
if (__name__ == "__main__"):
    program = Program()
    program.execute("Guitar Hero Bongo Cat (press space for options)", (500, 500), False, 0.1, streamer_name)

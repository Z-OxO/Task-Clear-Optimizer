import psutil
from time import sleep
from tkinter import *
from customtkinter import *
import configparser
from threading import Thread
from functools import partial
import sys
import os


class ProcessKill:
    def __init__(self):
        # CONSTANT
        self.PROCESS_LIST_KILL = [
            "opera.exe",
            "OneDrive.exe",
            "Skype.exe",
            "Spotify.exe",
            "Discord.exe",
            "wuauclt.exe",
            "CCXProcess.exe",
            "steam.exe",
            "steamwebhelper.exe",
            "XboxPcAppFT.exe",
            "Voicemod.exe",
            "eSound Music.exe",
            "chrome.exe",
            "firefox.exe",
            "msedge.exe",
            "Safari.exe",
            "brave.exe",
            "iexplore.exe",
        ]

        # Variables

        self.theme_color = ["dark-blue", "green", "blue"]
        self.mode = ["dark", "light"]

        # Main window
        self.window = CTk()
        self.window.geometry("650x650")
        self.window.resizable(False, False)
        self.window.title("Z_OxO Optimizer Process Program")

    def load_config(self):
        self.config = configparser.ConfigParser()
        try:
            if getattr(sys, "frozen", False):
                # Check if pyinstaller froze .exe
                executable_dir = sys._MEIPASS
            else:
                executable_dir = os.path.dirname(os.path.abspath(__file__))

            self.config_path = os.path.join(executable_dir, "config.ini")

            self.config.read(self.config_path)
            theme_color = self.config.get("Settings", "theme_color")
            mode = self.config.get("Settings", "mode")
            self.fortnite_path = self.config.get("paths", "fortnite")
            # Make theme and mode the first element in OptionButton in Settings
            self.theme_color.remove(theme_color)
            self.theme_color.insert(0, theme_color)
            self.mode.remove(mode)
            self.mode.insert(0, mode)
            set_default_color_theme(theme_color)
            set_appearance_mode(mode)
        except Exception as e:
            print("Error loading configuration:", e)

    def save_config(self, option, value):
        self.config = configparser.ConfigParser()

        try:
            if getattr(sys, "frozen", False):
                # Check if pyinstaller froze .exe
                executable_dir = sys._MEIPASS
            else:
                executable_dir = os.path.dirname(os.path.abspath(__file__))

            self.config_path = os.path.join(executable_dir, "config.ini")

            self.config.read(self.config_path)
            self.config.set("Settings", option, value)
            with open(self.config_path, "w") as config_file:
                self.config.write(config_file)
        except Exception as e:
            print("Error saving configuration:", e)

    def clean_widgets(self, win):
        for widget in win.winfo_children():
            widget.destroy()
        win.update()

    def game_menu(self):
        self.clean_widgets(self.window)

        def get_games_path():
            if chk_ftn == True:
                self.config.read(self.config_path)
                fortnite_path = self.config.get("paths", "fortnite")
                if fortnite_path == "None":
                    if not os.path.exists("C:\Program Files\Epic Games\Fortnite"):
                        fortnite_path = filedialog.askdirectory("C:\\")
                        self.config.set("paths", "fortnite", fortnite_path)
                        with open(self.config_path, "w") as config_file:
                            self.config.write(config_file)

        game_menu_frame = CTkFrame(self.window, height=650, width=650)

        game_menu_frame.pack()
        chk_ftn = BooleanVar(value=False)
        CTkCheckBox(
            game_menu_frame,
            text="Fortnite",
            variable=chk_ftn,
            onvalue=True,
            offvalue=False,
            command=get_games_path,
        ).grid(column=0, row=0)

    # Build the Setting Menu
    def setting_menu(self):
        def update_mode(mode):
            set_appearance_mode(mode)
            self.window.update()
            self.save_config("mode", mode)

        def update_theme(theme_color):
            set_default_color_theme(theme_color)
            self.clean_widgets(self.window)
            self.setting_menu()
            self.save_config("theme_color", theme_color)

        self.clean_widgets(self.window)
        CTkOptionMenu(
            self.window,
            width=500,
            height=100,
            values=self.mode,
            command=update_mode,
            font=("", 50),
        ).pack(anchor="center", side="top", padx=20, pady=100)
        CTkOptionMenu(
            self.window,
            width=500,
            height=100,
            values=self.theme_color,
            command=update_theme,
            font=("", 50),
        ).pack(anchor="center", side="top", padx=20, pady=20)
        CTkButton(
            self.window,
            height=40,
            width=100,
            text="Main Menu",
            font=("", 15),
            command=self.widgets_build_main,
        ).pack(side="bottom", anchor="sw", padx=20, pady=20)

    # Build the Main Menu widgets
    def widgets_build_main(self):
        self.clean_widgets(self.window)
        main_frame = CTkFrame(self.window, height=650, width=650)
        main_frame.pack()
        CTkLabel(
            main_frame,
            text="Kill task and free memory and CPU usage for your pc",
            font=("", 25),
        ).grid(row=0, column=0, padx=20, pady=20, columnspan=2)

        CTkButton(
            main_frame,
            height=40,
            width=100,
            text="Settings",
            font=("", 15),
            command=lambda: self.setting_menu(),
        ).grid(row=1, column=0, sticky="nw", padx=20, pady=20)

        CTkButton(
            main_frame,
            height=40,
            width=100,
            text="Manually stop process",
            font=("", 15),
            command=self.manually_process,
        ).grid(row=1, column=1, sticky="n", padx=20, pady=20)

        CTkButton(
            main_frame,
            height=40,
            width=100,
            text="Game Menu",
            font=("", 15),
            command=lambda: self.game_menu(),
        ).grid(row=1, column=1, sticky="ne", padx=20, pady=20)

        self.scrollableBar = CTkScrollableFrame(
            main_frame,
            width=450,
            label_text="Process console : ",
            label_font=("", 15, "bold", "underline"),
        )
        self.scrollableBar.grid(row=2, column=0, columnspan=2, padx=20, pady=50)

        CTkButton(
            main_frame,
            height=50,
            width=500,
            text="Click to optimize process",
            font=("", 20),
            command=lambda: self.process_kill(),
        ).grid(row=3, column=0, columnspan=2, padx=0, pady=20)

        self.window.mainloop()

    def process_kill(self):
        self.clean_widgets(self.scrollableBar)
        cpt_process = 0
        # Iter in the process list
        for proc in psutil.process_iter():
            # Check if the process name is in the Process list
            if proc.name() in self.PROCESS_LIST_KILL:
                try:
                    proc.terminate()
                    cpt_process += 1
                    CTkLabel(
                        master=self.scrollableBar,
                        text=f"Process {proc.name()} successively kill.",
                        fg_color="green",
                        bg_color="green",
                    ).pack(anchor="w")
                    sleep(0.2)
                    self.window.update()
                except (
                    psutil.NoSuchProcess,
                    psutil.AccessDenied,
                    psutil.ZombieProcess,
                ):
                    CTkLabel(
                        master=self.scrollableBar,
                        text=f"Unable to complete process {proc.name()}.",
                        fg_color="red",
                        bg_color="red",
                    ).pack(anchor="w")
                    self.window.update()
                    sleep(0.2)
        CTkLabel(
            master=self.scrollableBar,
            text=f"FINISH WITH : {cpt_process} PROCESS TERMINATE.",
            fg_color="green",
            bg_color="green",
        ).pack(anchor="w")
        self.window.update()
        sleep(0.2)

    # Build the "Manually kill process" Menu
    def manually_process(self):
        # Scrollbar Button pressed function
        def kill_process(process, process_button):
            try:
                process.terminate()
                Success_label = CTkLabel(
                    self.window,
                    text=f"Succesfully terminated",
                    text_color="green",
                    font=("", 25),
                )
                Success_label.grid(row=1, column=1, sticky="s", padx=10, pady=10)
                try:
                    process_button.destroy()
                except Exception as e:
                    print(e)
                print("destroy")
                self.scrollableBar.update()
                sleep(0.5)
                Success_label.destroy()
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
                psutil.ZombieProcess,
            ) as e:
                failed_label = CTkLabel(
                    self.window,
                    text=f"Failed to terminate: {e}",
                    text_color="red",
                    font=("", 10),
                )
                failed_label.grid(row=1, column=1, sticky="s", padx=10, pady=10)
                self.scrollableBar.update()
                sleep(0.5)
                failed_label.destroy()

        self.clean_widgets(self.window)

        # Main frame of manually kill menu
        frame = CTkFrame(self.window, height=650, width=650)
        frame.columnconfigure(2)
        frame.rowconfigure(2)
        frame.pack()

        self.scrollableBar = CTkScrollableFrame(
            frame,
            width=600,
            height=400,
            label_text="Process list",
            label_font=("", 20, "bold", "underline"),
        )
        self.scrollableBar.grid(column=1, row=1, pady=20, padx=20)

        processes_info = []

        # Collect and filter process
        for proc in psutil.process_iter(["pid", "name", "memory_info"]):
            if proc.info["name"] == "svchost.exe":
                pass
            else:
                processes_info.append(
                    {
                        "process": proc,
                        "text": (
                            proc.name()
                            + "  "
                            + str(proc.cpu_percent())
                            + "  "
                            + str(
                                round(proc.info["memory_info"].rss / (1024 * 1024), 1)
                            )
                            + " MB RAM USAGE"
                        ),
                    }
                )

        # Sort by ram usage
        sorted_processes = sorted(
            processes_info,
            key=lambda x: x["process"].info["memory_info"].rss,
            reverse=True,
        )

        # Add process buttons in the scrollbar
        for process_info in sorted_processes:
            text = process_info["text"]
            process = process_info["process"]

            process_button = CTkButton(
                self.scrollableBar,
                text=text,
                width=500,
                height=10,
            )
            # Pass the kill process function to all the buttons
            process_button.configure(
                command=lambda process=process, process_button=process_button: kill_process(
                    process, process_button
                )
            )
            process_button.pack(pady=3)

        CTkButton(
            frame,
            height=40,
            width=10,
            text="RESET LIST",
            font=("", 15),
            command=self.manually_process,
        ).grid(row=0, column=1, sticky="n", padx=10, pady=10)

        CTkButton(
            frame,
            height=40,
            width=10,
            text="Main Menu",
            font=("", 15),
            command=self.widgets_build_main,
        ).grid(row=2, column=1, sticky="sw", padx=10, pady=10)


if __name__ == "__main__":
    App = ProcessKill()
    App.load_config()
    App.widgets_build_main()

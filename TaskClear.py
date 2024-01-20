import psutil
from time import sleep
from tkinter import *
from customtkinter import *
import configparser
from threading import Thread
from functools import partial


class ProcessKill:
    def __init__(self):
        # CONSTANT
        self.PROCESS_LIST_KILL = [
            "OneDrive.exe",
            "Skype.exe",
            "Spotify.exe",
            "Discord.exe",
            "spoolsv.exe",
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
        self.window.geometry("650x600")
        self.window.resizable(False, False)
        self.window.title("Z_OxO Optimizer Process Program")

    def load_config(self):
        config = configparser.ConfigParser()
        try:
            config.read("config.ini")
            theme_color = config.get("Settings", "theme_color")
            mode = config.get("Settings", "mode")
            set_default_color_theme(theme_color)
            set_appearance_mode(mode)
        except Exception as e:
            print("Error loading configuration:", e)

    def save_config(self, option, value):
        config = configparser.ConfigParser()
        config.read("config.ini")
        config.set("Settings", option, value)
        with open("config.ini", "w") as config_file:
            config.write(config_file)

    def clean_widgets(self, win):
        for widget in win.winfo_children():
            widget.destroy()
        win.update()

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

    def widgets_build_main(self):
        self.clean_widgets(self.window)
        CTkLabel(
            self.window,
            text="Kill task and free memory and CPU usage for your pc",
            font=("", 25),
        ).grid(row=0, column=0, padx=20, pady=20, columnspan=2)

        CTkButton(
            self.window,
            height=40,
            width=100,
            text="Settings",
            font=("", 15),
            command=lambda: self.setting_menu(),
        ).grid(row=1, column=0, sticky="sw", padx=20, pady=20)

        CTkButton(
            self.window,
            height=40,
            width=100,
            text="Manually stop process",
            font=("", 15),
            command=self.manually_process,
        ).grid(row=1, column=1, sticky="se", padx=20, pady=20)

        self.scrollableBar = CTkScrollableFrame(
            self.window,
            width=450,
            label_text="Process console : ",
            label_font=("", 15, "bold", "underline"),
        )
        self.scrollableBar.grid(row=2, column=0, columnspan=2, padx=20, pady=50)

        CTkButton(
            self.window,
            height=50,
            width=500,
            text="Click to optimize process",
            font=("", 20),
            command=lambda: self.process_kill(),
        ).grid(row=3, column=0, columnspan=2, padx=0, pady=20)

        self.window.mainloop()

    def process_kill(self):
        self.clean_widgets(self.scrollableBar)
        for proc in psutil.process_iter():
            if proc.name() in self.PROCESS_LIST_KILL:
                try:
                    proc.terminate()
                    CTkLabel(
                        master=self.scrollableBar,
                        text=f"Process {proc.name()} successively kill.",
                        fg_color="green",
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
                    ).pack(anchor="w")
                    self.window.update()
                    sleep(0.2)

    def manually_process(self):
        def kill_process(process, process_button):
            print("called")
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
        self.scrollableBar = CTkScrollableFrame(
            self.window,
            width=600,
            height=400,
            label_text="Process list",
            label_font=("", 20, "bold", "underline"),
        )
        self.scrollableBar.grid(column=1, row=0, pady=20, padx=20)

        processes_info = []

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

        for process_info in sorted_processes:
            text = process_info["text"]
            process = process_info["process"]

            process_button = CTkButton(
                self.scrollableBar,
                text=text,
                width=500,
                height=10,
            )
            process_button.configure(
                command=lambda process=process, process_button=process_button: kill_process(
                    process, process_button
                )
            )
            process_button.pack(pady=3)

        CTkButton(
            self.window,
            height=40,
            width=10,
            text="Main Menu",
            font=("", 15),
            command=self.widgets_build_main,
        ).grid(row=1, column=1, sticky="sw", padx=10, pady=10)


if __name__ == "__main__":
    App = ProcessKill()
    App.load_config()
    App.widgets_build_main()

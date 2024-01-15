import psutil
from time import sleep
from tkinter import *
from customtkinter import *


class ProcessKill:
    def __init__(self):
        self.process_names_to_kill = [
            "opera.exe",
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
        set_appearance_mode("dark")
        set_default_color_theme("dark-blue")
        self.window = CTk()
        self.window.geometry("650x500")
        self.window.resizable(False, False)
        self.window.title("Z_OxO Optimizer Process Program")

    def widgets_build(self):
        CTkLabel(
            self.window,
            text="Kill task and free memory and CPU usage for your pc",
            font=("", 25),
        ).pack(side="top", padx=20, pady=20)

        # Utilisez un attribut pour stocker la barre de défilement
        self.scrollableBar = CTkScrollableFrame(
            self.window,
            width=450,
            label_text="This is process console : ",
            label_font=("", 15, "bold", "underline"),
        )
        self.scrollableBar.pack(side="bottom", padx=20, pady=50)

        CTkButton(
            self.window,
            height=50,
            width=500,
            text="Click to optimize process",
            font=("", 20),
            command=lambda: self.process_kill(),
        ).pack(side="top", padx=0, pady=20)

        self.window.mainloop()

    def process_kill(self):
        for widget in self.scrollableBar.winfo_children():
            widget.destroy()

        for proc in psutil.process_iter():
            if proc.name() in self.process_names_to_kill:
                try:
                    proc.terminate()
                    CTkLabel(
                        master=self.scrollableBar,
                        text=f"Process {proc.name()} successively kill.",
                        fg_color="green",
                    ).pack(anchor="w")
                    sleep(0.2)
                    self.window.update
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


ProcessKill().widgets_build()

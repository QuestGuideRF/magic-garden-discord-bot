import sys
import os
import tkinter as tk
from src .core .config import Config
from src .gui .main_window import HarvestBotGUI
def main ():
    Config .load ()
    root =tk .Tk ()
    app =HarvestBotGUI (root )
    root .mainloop ()
if __name__ =="__main__":
    main ()
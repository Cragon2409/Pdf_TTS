import shutil

import tkinter as tk
from tkinter import filedialog
import os

root = tk.Tk()
root.withdraw()

SAVES_FOLDER = "saves/"

def new_save(path, folder_name):
    new_folder = SAVES_FOLDER + '/' + folder_name
    if os.path.exists(new_folder):
        raise ValueError("Save Name Already Taken")
    
    os.makedirs(new_folder)
    os.makedirs(new_folder + '/images')

    shutil.copyfile(path, new_folder + '/raw.pdf')



if __name__ == "__main__":
    file_path = filedialog.askopenfilename()

    save_name = input("Save name: ")
    new_save(file_path, save_name)
# -*- coding: utf-8 -*-

from tkinter import *
from tkinter import messagebox
from tkinter import ttk
from tkinter import tix
import winsound

from libs.numbersToLetters import NumberToLetter
from i18n.transliterationData_HU import dataTable


class MEDIATURMIXGUI:

    def __init__(self, root):
        self.root = root
        self.root.protocol("WM_DELETE_WINDOW", self.__destroyWindow)
        self.root.title('Mediaturmix - v1.0')
        self.root.config(width=400, height=200)
        self.__center(self.root)

        self.entryVar = None
        self.entrydata = None
        
        self.folderRoot = r'..\Umbrella\recording_20160928\numbers'
        
        self.__createMainFrame()

        self.N2L = NumberToLetter(dataTable)

        self.root.mainloop()

    def __destroyWindow(self):
        if messagebox.askokcancel("Quit", "Do you really wish to quit?"):
            self.root.destroy()

    def __center(self, win):
        win.update_idletasks()
        width = win.winfo_width()
        frm_width = win.winfo_rootx() - win.winfo_x()
        win_width = width + 2 * frm_width
        height = win.winfo_height()
        titlebar_height = win.winfo_rooty() - win.winfo_y()
        win_height = height + titlebar_height + frm_width
        x = win.winfo_screenwidth() // 2 - win_width // 2
        y = win.winfo_screenheight() // 2 - win_height // 2
        win.geometry('{}x{}+{}+{}'.format(width, height, x, y))
        win.deiconify()

    def __createMainFrame(self):
        self.label = Label(self.root, text="Enter a number:")
        self.label.pack()

        self.entryVar = StringVar()
        e = Entry(self.root, textvariable=self.entryVar)
        e.pack()

        self.greet_button = Button(
            self.root, text="Transliterate...", command=self.__process)
        self.greet_button.pack()

        self.text = Text(self.root)
        self.text.pack()

    def __process(self):
        self.entrydata = self.entryVar.get()
        if self.entrydata:
            self.text.delete(1.0, END)
            self.text.insert(INSERT, "number: {:>15}\n".format(self.entrydata))
            self.N2L.set_number(str(self.entrydata), 'cardinal')
            transliteration = self.N2L.get_transliterations(join=True)
            self.text.insert(INSERT, "transliteration: {:>10}\n".format(transliteration))
            filenames = self.N2L.get_filenames()
            self.text.insert(INSERT, "file names: {:>19}\n".format(" ".join(filenames)))
            fileNameContents = self.N2L.get_fileNameContents()
            self.text.insert(INSERT, "file name contents: {:>8}\n".format(" ".join(fileNameContents)))
            self.__playFiles(*filenames)

    def __playFiles(self, *args):
        for f in args:
            winsound.PlaySound(r'{}\{}'.format(self.folderRoot, f), winsound.SND_FILENAME)

    def __playTestAudioFile(self):
        # 100 and 10 meters
        winsound.PlaySound(r'audios\100.wav', winsound.SND_FILENAME)
        winsound.PlaySound(r'audios\and.wav', winsound.SND_FILENAME)
        winsound.PlaySound(r'audios\10.wav', winsound.SND_FILENAME)
        winsound.PlaySound(r'audios\meters.wav', winsound.SND_FILENAME)

if __name__ == '__main__':
    try:
        MEDIATURMIXGUI(tix.Tk())
    except:
        print("...mi a fészkes foton...\n")

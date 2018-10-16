#!/bin/bash
import uuid
import json
import time
from thread import start_new_thread, allocate_lock
import os


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

def cls():
    os.system('cls' if os.name=='nt' else 'clear')



class pypet:
    uuid = ""
    name = ""
    age = 0 #months
    hunger = 0 #prozent
    happines = 0
    hygiene = 0
    health = 0
    rested = 0
    alive_since = 0
    update_lock = allocate_lock()
    dead = False
    def __init__(self,_name, _load_config):
        self.uuid = str(uuid.uuid4())
        self.name = _name
        self.alive_since = int(time.time())
        self.age = 0 #days
        self.hunger = 40 #prozent 0= gut
        self.happines = 100#prozent
        self.hygiene = 100#prozent
        self.health = 100#prozent
        self.rested = 10#prozent
        self.dead = False # if true program terminates

        self.update_lock = allocate_lock()
        if _load_config == False:
            print("#################")
            print(bcolors.HEADER +"A new pet was born, its name is " + self.name + bcolors.ENDC)
            print("#################")
    
    def gen_json_stats(self):
        data = {}
        data['uuid'] = self.uuid
        data['name'] = self.name
        data['age'] = self.age
        data['alive_since'] = self.alive_since
        json_data = json.dumps(data)
        return json_data
    

    def print_bars(self,_perc,_inv, _name):
        bars_max = 5
        bard_draw = int((_perc*0.01) * bars_max)
        counter = 0
        out = ""
        for x in range(int(bars_max)):
            if counter < bard_draw:
                if _inv == True:
                    out = out + " "
                else:
                    out = out + "#"
            else:
                if _inv == True:
                    out = out + "#"
                else:
                    out = out + " "
            counter = counter +1

        col_perc = _perc
        if _inv:
            col_perc = 100-_perc
        
        col_pre = ""

        col_post = bcolors.ENDC

        if col_perc >= 80:
            col_pre = bcolors.OKGREEN
        elif col_perc < 20:
            col_pre = bcolors.FAIL
        else:
            col_pre = bcolors.WARNING

        print(col_pre+_name + ": " + out + " ("+str(_perc)+"%)" +col_post)


    def show_pet(self):
        pass

    def save_pet(self, _cfg_string):
        pass

    def load_pet(self, _cfg_string):
        pass
    def print_stats(self):
        print(bcolors.HEADER +"#    -STATS-    #" + bcolors.ENDC)
        print("NAME: " + self.name)
        print("AGE IN DAYS:" + str(self.age))
        self.print_bars(self.hunger,True, "Hunger")
        self.print_bars(self.happines,False, "Happines")
        self.print_bars(self.hygiene,False, "Hygiene")
        self.print_bars(self.health,False, "Health")
        self.print_bars(self.rested,False, "Reseted")
        print(bcolors.HEADER +"#---------------#" + bcolors.ENDC)

    #UPDATE FUNC FROM THREAD
    def update(self):
        self.update_lock.acquire()
        if self.dead:
            pass
            #TODO EVENT SYSTEM
        #update age with alvice since
        #update all other stuff according to age and so on
        #TODO CHECK LIVE STATE 
        self.update_lock.release()



       

    def input_cmd(self, cmd):
        self.update_lock.acquire()
        
        if cmd == "status":
            self.print_stats()
        else:
            print(bcolors.FAIL +"this cmd is invalid"+ bcolors.ENDC)

        show_pet()
        self.update_lock.release()




_ri = raw_input("Do you want to load a pet? (y/n)> ")
if _ri == "y":
    pet = pypet(_ri, True)
    pet.load_pet()
else:
    _ri = raw_input("What's your new pets name?> ")
    pet = pypet(_ri, False)
    pet.print_stats()





def update_thread_func(threadName, delay):
   # print(threadName)
    while 1:  
        time.sleep(delay)
        pet.update()
start_new_thread( update_thread_func, ("Thread-1", 5, ))



while 1:
    if pet.dead:
        pass

   #MAIN THREAD DO INPUT STUFF
    s = raw_input("> ")
    cls()
    if s == "help":
        print("-> help for this page")
        print("-> status for pet states")
    elif s == "":
        pass
    else:
        pet.input_cmd(s)

        


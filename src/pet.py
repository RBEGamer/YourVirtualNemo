#!/bin/bash
import uuid
import json
import time
from thread import start_new_thread, allocate_lock
import os
import random
import re #regex


#THIS ARE COLOR CODES FOR THE TERMINAL, SO ITS POSSIBLE TO COLOR TEXT
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m' #DISABLE COLOR
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# CLEARS THE USERS TERMINAL
def cls():
    if os.name=='nt':
        os.system('cls')
    else:
        os.system('clear')



class pypet:

    #PHRASES THE PET CAN SAY FOR SPECIFIC ACTIONS
    phrase_hunger = ["Im hungry", "Give me food!!!!"]
    hunger_phrase_spoken = False

    phrase_saved = ["I saved my DNA to a mystery file maybe the file is called: %file"]
    #STAT VARIABLES FOR YOUR PET
    uuid = ""
    name = ""
    age = 0 #months
    hunger = 0 #prozent
    happines = 0
    hygiene = 0
    health = 0
    rested = 0
    alive_since = 0


    dead = False
    update_lock = allocate_lock()
    save_file_base_dir = "."#CURRENT DIR
    save_file_path = "./pet.json" #DEFUALT PATH


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
        self.save_file_path = self.save_file_base_dir+"/pet_" + str(self.uuid).replace("-", "") + ".json"


        if _load_config == False:
            print("#################")
            print(bcolors.HEADER +"A new pet was born, its name is " + self.name + bcolors.ENDC)
            print("#################")
    

        
    
    #PRINTS OUT A COLORED BAR
    def print_bars(self,_perc,_inv, _name):
        bars_max = 10
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
        #TODO PET ANIMATioN
        pass

    def save_pet(self):
        data = {}
        data['uuid'] = self.uuid
        data['name'] = self.name
        data['age'] = self.age
        data['alive_since'] = self.alive_since

        #SAVE USER DATA TODO DICT
        data['hunger'] = self.hunger
        data['happines'] = self.happines
        data['hygiene'] = self.hygiene
        data['health'] = self.health
        data['rested'] = self.rested
        #FINALLY SAVE FILE TO DISK
        json_data = json.dumps(data)
        try:
            with open(self.save_file_path,'w+') as f:
            #convert to string:
                data = f.read()
                f.seek(0)
                f.write(json_data)
                f.truncate()
                f.close()
            print(bcolors.OKGREEN + str(random.choice(self.phrase_saved)).replace("%file",self.save_file_path) + bcolors.ENDC)
        except:
            print(bcolors.FAIL +"./pet.json can not be written."+ bcolors.ENDC)
        


    def load_pet(self):
        files_in_dir = os.listdir(self.save_file_base_dir)#READ ALL FILES IN BASE_DIR_FOLDER
        matched_files = []
        for tf in files_in_dir: #FOR EACH FILE THAT MATCH THE NAME PATTERN WRITE TO OTHER LIST
            if re.match("pet_[a-z0-9]*.json",tf):
                matched_files.append(tf) 
        if not matched_files:#If no files found show message
            print("NO SAVEFILES FOUND! Please use the save command to save a pet")
            return
        print("-------- SAVE FILES ------")
        counter = 0
        #TODO SHOW PET NAME
        for mf in matched_files:#SHOW LIST WITH ALL SAVE FILES
            print "[" + str(counter) + "] " +str(mf)
            counter = counter+1
        print("--------------")
        print("Please choose a pet by typing the letter in the letters")
        s = raw_input("> ")#ASK USER TO ENTER NUMBER
        if not s:
            print(bcolors.FAIL +"the given load index is invalid, please try again"+ bcolors.ENDC)
            return
        if not matched_files[int(s)]:
            print(bcolors.FAIL +"the given load index is invalid, please try again"+ bcolors.ENDC)
            return
        print "try loading file:" + matched_files[int(s)]
        try:#TRY OPEN AND LOADING FILE AND RESTORE ALL USER VARIABLES
             with open(matched_files[int(s)]) as f:
                data = json.load(f)
                #TODO DICT
                self.uuid = data['uuid']
                self.name = data['name']
                self.age = data['age']
                self.alive_since = data['alive_since']
                self.hunger = data['hunger']
                self.happines = data['happines']
                self.hygiene = data['hygiene']
                self.health = data['health']
                self.rested = data['rested']
                print(bcolors.OKGREEN +"YEAH! Your pet:"+ self.name + " was loaded"+ bcolors.ENDC)
        except:
            print(bcolors.FAIL +matched_files[int(s)]+" can not be loaded."+ bcolors.ENDC)
       








    def print_stats(self):
        print(bcolors.HEADER +"#    -STATS-    #" + bcolors.ENDC) #WRITE HEADER
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


    def show_pet_help(self):
        print("h -> this help page")
        print("status -> get health/hunger bars")
        print("save -> save your pet as a file")
        print("load -> load a file to load a pet")

        
       

    def input_cmd(self, cmd):
        self.update_lock.acquire()
        
        if cmd == "status":
            self.print_stats()
        elif cmd == "save":
            self.save_pet()
        elif cmd == "load":
            self.load_pet()
        elif cmd == "help":
            self.show_pet_help()
        else:
            print(bcolors.FAIL +"this cmd is invalid"+ bcolors.ENDC)
        self.show_pet()
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


   #MAIN THREAD DO INPUT STUFF
    s = raw_input("> ")
    cls()

    if s == "":
        pass
    else:
        pet.input_cmd(s)

        


from fusion_solar_py.client import FusionSolarClient
import re 
import time
import pywhatkit
import datetime
import os
from colorama import Fore, Style
import pyautogui
import webbrowser
#import toshiba_ac 

avg = []
production_avg = 0 
daily_prod = []




last_exe = None

def cooldown():
    if hour >= 22:
        print(Fore.CYAN + "Enter Night Mode, restarting at 0500" + Style.RESET_ALL)
        time.sleep(28800) # from 22 to 6 
    
    time.sleep(340) # 5 minutes and a bit so new data is guarented 340s
    check_time()
    get_data()
    

def check_time():    
    global date
    date = datetime.datetime.now()
 

    return date.day, date.hour 



day, hour = check_time()
print(f"Date:{day} Time {hour}")


def wash_message(day):
    get_data()
    date_send = date.day, date.month , date.year
    last_exe = day
    
    message = f"Enough electricity is produced for:{date_send} " # THE MESSAGE YOU WANT TO SEND

    
    if soc >= 10 and production_avg >= 0.5: # ADJUST TO YOUR NEEDS 
        print(Fore.YELLOW + "Notification will be sent now ! " + Style.RESET_ALL)
        webbrowser.open("") # ENTER YOUR WHATSAPP CHANNEL/NUMBER
        time.sleep(20)
        os.system(f'xdotool type "{message}"')
        time.sleep(1)
        os.system('xdotool key enter')
        time.sleep(2)
        os.system('xdotool key ctrl+w') # close tab again
        os.system('xdotool key alt+tab')
    elif soc >= 15: # ADJUST TO YOUR NEEDS 
        print(Fore.YELLOW + "Notification will be sent now ! " + Style.RESET_ALL)
        webbrowser.open("") # ENTER YOUR WHATSAPP CHANNEL/NUMBER
        time.sleep(20)
        os.system(f'xdotool type "{message}"')
        time.sleep(10)
        os.system('xdotool key Return')
        time.sleep(5)
        os.system('xdotool key ctrl+w') # close tab again
        time.sleep(5)
        os.system('xdotool key alt+Tab')
        
    return last_exe 
    
    

    
   

def get_data():
    global production_avg
    client = FusionSolarClient("user", "password", huawei_subdomain="uni003eu5", # enter your credentials, check domain may delete/change it
                                )

    os.system("clear")
    print(Fore.BLUE + r"""  
                                                                                                                                                                                              
                                                                                                                                                                                          
FFFFFFFFFFFFFFFFFFFFFF                                     iiii                                             SSSSSSSSSSSSSSS                  lllllll                                      
F::::::::::::::::::::F                                    i::::i                                          SS:::::::::::::::S                 l:::::l                                      
F::::::::::::::::::::F                                     iiii                                          S:::::SSSSSS::::::S                 l:::::l                                      
FF::::::FFFFFFFFF::::F                                                                                   S:::::S     SSSSSSS                 l:::::l                                      
  F:::::F       FFFFFFuuuuuu    uuuuuu      ssssssssss   iiiiiii    ooooooooooo   nnnn  nnnnnnnn         S:::::S               ooooooooooo    l::::l   aaaaaaaaaaaaa  rrrrr   rrrrrrrrr   
  F:::::F             u::::u    u::::u    ss::::::::::s  i:::::i  oo:::::::::::oo n:::nn::::::::nn       S:::::S             oo:::::::::::oo  l::::l   a::::::::::::a r::::rrr:::::::::r  
  F::::::FFFFFFFFFF   u::::u    u::::u  ss:::::::::::::s  i::::i o:::::::::::::::on::::::::::::::nn       S::::SSSS         o:::::::::::::::o l::::l   aaaaaaaaa:::::ar:::::::::::::::::r 
  F:::::::::::::::F   u::::u    u::::u  s::::::ssss:::::s i::::i o:::::ooooo:::::onn:::::::::::::::n       SS::::::SSSSS    o:::::ooooo:::::o l::::l            a::::arr::::::rrrrr::::::r
  F:::::::::::::::F   u::::u    u::::u   s:::::s  ssssss  i::::i o::::o     o::::o  n:::::nnnn:::::n         SSS::::::::SS  o::::o     o::::o l::::l     aaaaaaa:::::a r:::::r     r:::::r
  F::::::FFFFFFFFFF   u::::u    u::::u     s::::::s       i::::i o::::o     o::::o  n::::n    n::::n            SSSSSS::::S o::::o     o::::o l::::l   aa::::::::::::a r:::::r     rrrrrrr
  F:::::F             u::::u    u::::u        s::::::s    i::::i o::::o     o::::o  n::::n    n::::n                 S:::::So::::o     o::::o l::::l  a::::aaaa::::::a r:::::r            
  F:::::F             u:::::uuuu:::::u  ssssss   s:::::s  i::::i o::::o     o::::o  n::::n    n::::n                 S:::::So::::o     o::::o l::::l a::::a    a:::::a r:::::r            
FF:::::::FF           u:::::::::::::::uus:::::ssss::::::si::::::io:::::ooooo:::::o  n::::n    n::::n     SSSSSSS     S:::::So:::::ooooo:::::ol::::::la::::a    a:::::a r:::::r            
F::::::::FF            u:::::::::::::::us::::::::::::::s i::::::io:::::::::::::::o  n::::n    n::::n     S::::::SSSSSS:::::So:::::::::::::::ol::::::la:::::aaaa::::::a r:::::r            
F::::::::FF             uu::::::::uu:::u s:::::::::::ss  i::::::i oo:::::::::::oo   n::::n    n::::n     S:::::::::::::::SS  oo:::::::::::oo l::::::l a::::::::::aa:::ar:::::r            
FFFFFFFFFFF               uuuuuuuu  uuuu  sssssssssss    iiiiiiii   ooooooooooo     nnnnnn    nnnnnn      SSSSSSSSSSSSSSS      ooooooooooo   llllllll  aaaaaaaaaa  aaaarrrrrrr   """ + Style.RESET_ALL)
        
    # IF YOU HAVE MULTIPLE PLANTS THEN (ALL OF) THIS NEEDS TO BE CHANGED
    stats = client.get_power_status()
    plant_overview = client.get_station_list()

    # get the current power of your first plant
    print(Fore.GREEN + f"Current power production: { plant_overview[0]['currentPower'] }" + Style.RESET_ALL )
    global production
    production = plant_overview[0]["currentPower"]
    # get the plant ids
    plant_ids = client.get_plant_ids()

    # get battery id
    battery_ids = client.get_battery_ids(plant_ids)
    battery_data = client.get_battery_basic_stats(battery_ids)
    battery_data = str(battery_data)
    
    
    print("#"*100)
    
    get_soc = re.search(r'state_of_charge=([\d.]+)', battery_data) # searches for soc followed by number optional with decimal point 
    global soc
    soc = float(get_soc.group(1)) # gives out the found value 
    print(Fore.RED + f"State of Charge: {soc}%" + Style.RESET_ALL)
    avg.append(production)
    daily_prod.append(production + str(datetime.datetime.minute))
    if len(avg) == 5: # if 5 elements in the list the average will be calculated, first (oldest) element will be deleted again, so avrage over last 30min
        for i in range(0,len(avg)):
            
            production_avg += round(float(avg[i]),2)
            #print(production_avg,i)
        production_avg = production_avg / 5
        production_avg= round(production_avg,2)
        remove_elemt = avg[0]
        avg.remove(remove_elemt)
        
    print(f"current average production: {production_avg}")
    
    
    client.log_out()
   
def check_ac():
    print("jfgj")
    # should start the ac unit automatically when it gets to hot / to much electricity


   



while True:
    day, hour = check_time()
    cooldown() 
    x = []
    y = []
    file_name = f"{str(datetime.datetime.date)}"
    if hour >= 21:
    elif hour >= 8 and day != last_exe:
        last_exe = wash_message(day)

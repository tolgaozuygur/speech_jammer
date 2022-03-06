from distutils.errors import PreprocessError
import time
import subprocess
import random

#Variables.
delay_min = 180000
delay_max = 220000

is_sevice_enabled = 0

def program_handler():
    #Variables.
    global delay_max, delay_min
    global is_sevice_enabled
    global alsa_process

    #Get seed.
    random.seed()

    while True: 
        try:
            #Wait until the user makes an input.
            if is_sevice_enabled == 0:
                user_input = input("Input 'p' to enable the DAF service\n")
            if is_sevice_enabled == 1:
                user_input = input("Input 'p' to disable the DAF service\n")

            #If program wasn't running, run.
            if user_input == "p" and is_sevice_enabled == 0:  
                print("Program state changed to 'ENABLED'.")

                #Get a random delay value.
                random_delay = random.randint(delay_min, delay_max)
                print("Delay: ", random_delay)

                #Start loopback system.
                alsa_process = subprocess.Popen(["alsaloop","-C","default","-P","default","-t",str(random_delay)])

                #Reset the user input.
                user_input = ""

                #Set service to 'ENABLED'
                is_sevice_enabled = 1

            #If program was running, terminate.
            if user_input == "p" and is_sevice_enabled == 1:
                #Terminate the service.
                alsa_process.terminate()

                print("Program state changed to 'DISABLED'.")   

                #Reset the user input.
                user_input = ""

                #Set service to 'DISABLED'.
                is_sevice_enabled = 0
        except KeyboardInterrupt:
            #Terminate the service.
            alsa_process.terminate()

            #Say what is wrong.
            print("Program stopped via keyboard interrupt, terminating the service.")

            #Break the loop just in case.
            break

#Start the program.
program_handler()
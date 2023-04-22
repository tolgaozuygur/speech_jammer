#!/usr/bin/env python3

import sounddevice as sd
import random

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

def main():
    random.seed()
    print("Press Return to start/stop or 'q' for terminate:")
    
    while True:
        if  input() == 'q':
            print("Program terminated.")
            break
        print("Program started.")
        try:
            with sd.Stream(latency=random.randint(180, 200) / 1000, # random latency value between 180ms and 200ms
                           callback=callback):
                if  input() == 'q':
                    print("Program terminated.")
                    break
                print("Program stopped...")
        except sd.PortAudioError as e:
            print("Error:", e)
            if e.errno == -9987:
                print("Please make sure you have a microphone connected or its not muted.")
            break
        except KeyboardInterrupt:
            print("Program stopped via keyboard interrupt.")

if __name__ == "__main__":
    main()

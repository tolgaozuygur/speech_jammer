#!/usr/bin/env python3

import sounddevice as sd
import random

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)
    outdata[:] = indata

def main():
    random.seed()

    try:
        with sd.Stream(latency=random.randint(180, 200) / 1000, # random latency value between 180ms and 200ms
                       callback=callback):
            print('#' * 40)
            print('press Return to quit')
            print('#' * 40)
            input()
    except KeyboardInterrupt:
        print("Program stopped via keyboard interrupt.")

if __name__ == "__main__":
    main()

#import
import sys, os
import time
import threading

import WindowCall as wind

#====================Main(START)==================

if __name__ == "__main__":

    try:
        #INIT VALUES
        t = threading.Thread(
            target=wind.Show_Window,
            args=('debug')
        )
        
        t.start()
        t.join()
        
        print("START PROCESSING")
        
    except:
        print("END")
        
    finally:
        print("CLEAN")

#====================Main(END)==================
import time
import pyautogui
loop_on = False
sleep_after_press_delay = 1

def sleep_time(sleepy):
    print("waiting: ", sleepy)
    time.sleep(sleepy)

def sleep_after_press():
    # print("wait_standard: ", 5)
    #time.sleep(1.5)
    time.sleep(sleep_after_press_delay)

def load_track(deck):
    print("load_track: ", deck)
    if deck == 1:
        pyautogui.hotkey('shift', 'left')
    elif deck == 2:
        pyautogui.hotkey('shift', 'right')
    else:
        pyautogui.hotkey('shift', 'left')
        time.sleep(sleep_after_press_delay)
        pyautogui.hotkey('shift', 'right')
    sleep_after_press_delay

def play(deck):
    print("play: ", deck)
    if deck == 1:
        pyautogui.press('D')
    elif deck == 2:
        pyautogui.press('L')
    else:
        pyautogui.press('D')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('L')
    sleep_after_press_delay

def tab_tempo(deck):
    print("tab_tempo: ", deck)
    if deck == 1:
        pyautogui.hotkey('shift', '!')
    elif deck == 2:
        pyautogui.hotkey('shift', '^')
    else:
        pyautogui.hotkey('shift', '!')
        time.sleep(sleep_after_press_delay)
        pyautogui.hotkey('shift', '^')
    sleep_after_press_delay

def sync_tempo(deck):
    print("sync_tempo: ", deck)
    if deck == 1:
        pyautogui.press('1')
    elif deck == 2:
        pyautogui.press('6')
    else:
        pyautogui.press('1')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('6')
    sleep_after_press_delay
    
def auto_toggle():
    print("auto_toggle")
    pyautogui.hotkey('shift', 'f12')
    sleep_after_press_delay
    
def auto_next():
    print("auto_next")
    pyautogui.hotkey('shift', 'f11')
    sleep_after_press_delay

def loop_activate(deck, loop_status):
    if(loop_status):
        print("loop_OFF: ", deck)
        loop_status = False
    else:
        print("loop_ON: ", deck)
        pyautogui.press('q') # Set Loop In Point D1
        time.sleep(sleep_after_press_delay)
        pyautogui.press('u') # Set Loop In Point D2
        loop_status = True
        
    if deck == 1:
        pyautogui.press('q')
    elif deck == 2:
        pyautogui.press('u')
    else:
        pyautogui.press('q')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('u')
    sleep_after_press_delay
    return loop_status
    
def loop_onoff(deck, loop_status):
    if(loop_status):
        print("loop_OFF: ", deck)
        loop_status = False
    else:
        print("loop_ON: ", deck)
        pyautogui.press('4') # Set Loop In Point D1
        time.sleep(sleep_after_press_delay)
        pyautogui.press('9') # Set Loop In Point D2
        loop_status = True
        
    if deck == 1:
        pyautogui.press('4')
    elif deck == 2:
        pyautogui.press('9')
    else:
        pyautogui.press('4')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('9')
    sleep_after_press_delay
    return loop_status

def loop_in(deck):
    print("loop_out: ", deck)
    if deck == 1:
        pyautogui.press('2')
    elif deck == 2:
        pyautogui.press('7')
    else:
        pyautogui.press('2')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('7')
    sleep_after_press_delay
    
def loop_out(deck):
    print("loop_out: ", deck)
    if deck == 1:
        pyautogui.press('3')
    elif deck == 2:
        pyautogui.press('8')
    else:
        pyautogui.press('3')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('8')
    sleep_after_press_delay
    
def loop_halve(deck):
    print("loop_halve: ", deck)
    if deck == 1:
        pyautogui.press('w')
    elif deck == 2:
        pyautogui.press('i')
    else:
        pyautogui.press('w')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('i')
    sleep_after_press_delay

def loop_double(deck):
    print("loop_double: ", deck)
    if deck == 1:
        pyautogui.press('e')
    elif deck == 2:
        pyautogui.press('o')
    else:
        pyautogui.press('e')
        time.sleep(sleep_after_press_delay)
        pyautogui.press('o')
    sleep_after_press_delay
    
def scratch(deck, delay, loop_on):
    print("scratch: ", deck, " delay", delay)
    loop_on = loop_activate(deck, loop_on)

    loop_halve(deck) 
    sleep_time(delay*2)
    loop_halve(deck)
    loop_halve(deck)
    sleep_time(delay*0.5)
    loop_double(deck)
    sleep_time(delay*0.7)
    loop_double(deck)
    sleep_time(delay)
    loop_double(deck)
    
    loop_on = loop_onoff(deck, loop_on)

    sleep_after_press_delay
    return loop_on
    
sleep_time(5)
auto_toggle()

while True:
    sleep_time(2) 
    sync_tempo(3)    

    loop_on = scratch(3,3,loop_on)
    sleep_time(10)
    
    auto_next()
    
    sleep_time(10)
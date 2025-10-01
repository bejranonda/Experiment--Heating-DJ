import time
import pyautogui
loop_on = False

def sleep_time(sleepy):
    print("waiting: ", sleepy)
    time.sleep(sleepy)

def sleep_after_press():
    # print("wait_standard: ", 5)
    time.sleep(1.5)

def load_track(deck):
    print("load_track: ", deck)
    if deck == 1:
        pyautogui.hotkey('shift', 'left')
    elif deck == 2:
        pyautogui.hotkey('shift', 'right')
    else:
        pyautogui.hotkey('shift', 'left')
        pyautogui.hotkey('shift', 'right')
    sleep_after_press()

def play(deck):
    print("play: ", deck)
    if deck == 1:
        pyautogui.press('D')
    elif deck == 2:
        pyautogui.press('L')
    else:
        pyautogui.press('D')
        pyautogui.press('L')
    sleep_after_press()

def tab_tempo(deck):
    print("tab_tempo: ", deck)
    if deck == 1:
        pyautogui.hotkey('shift', '!')
    elif deck == 2:
        pyautogui.hotkey('shift', '^')
    else:
        pyautogui.hotkey('shift', '!')
        pyautogui.hotkey('shift', '^')
    sleep_after_press()

def sync_tempo(deck):
    print("sync_tempo: ", deck)
    if deck == 1:
        pyautogui.press('1')
    elif deck == 2:
        pyautogui.press('6')
    else:
        pyautogui.press('1')
        pyautogui.press('6')
    sleep_after_press()
    
def auto_toggle():
    print("auto_toggle")
    pyautogui.hotkey('shift', 'f12')
    sleep_after_press()
    
def auto_next():
    print("auto_next")
    pyautogui.hotkey('shift', 'f11')
    sleep_after_press()

def loop_activate(deck, loop_status):
    if(loop_status):
        print("loop_OFF: ", deck)
        loop_status = False
    else:
        print("loop_ON: ", deck)
        pyautogui.press('q') # Set Loop In Point D1
        pyautogui.press('u') # Set Loop In Point D2
        loop_status = True
        
    if deck == 1:
        pyautogui.press('q')
    elif deck == 2:
        pyautogui.press('u')
    else:
        pyautogui.press('q')
        pyautogui.press('u')
    sleep_after_press()
    return loop_status
    
def loop_onoff(deck, loop_status):
    if(loop_status):
        print("loop_OFF: ", deck)
        loop_status = False
    else:
        print("loop_ON: ", deck)
        pyautogui.press('4') # Set Loop In Point D1
        pyautogui.press('9') # Set Loop In Point D2
        loop_status = True
        
    if deck == 1:
        pyautogui.press('4')
    elif deck == 2:
        pyautogui.press('9')
    else:
        pyautogui.press('4')
        pyautogui.press('9')
    sleep_after_press()
    return loop_status

def loop_in(deck):
    print("loop_out: ", deck)
    if deck == 1:
        pyautogui.press('2')
    elif deck == 2:
        pyautogui.press('7')
    else:
        pyautogui.press('2')
        pyautogui.press('7')
    sleep_after_press()
    
def loop_out(deck):
    print("loop_out: ", deck)
    if deck == 1:
        pyautogui.press('3')
    elif deck == 2:
        pyautogui.press('8')
    else:
        pyautogui.press('3')
        pyautogui.press('8')
    sleep_after_press()
    
def loop_halve(deck):
    print("loop_halve: ", deck)
    if deck == 1:
        pyautogui.press('w')
    elif deck == 2:
        pyautogui.press('i')
    else:
        pyautogui.press('w')
        pyautogui.press('i')
    sleep_after_press()

def loop_double(deck):
    print("loop_double: ", deck)
    if deck == 1:
        pyautogui.press('e')
    elif deck == 2:
        pyautogui.press('o')
    else:
        pyautogui.press('e')
        pyautogui.press('o')
    sleep_after_press()
    
sleep_time(5)
auto_toggle()

while True:
    sleep_time(2) 
    sync_tempo(3)
    
    sleep_time(1)
    loop_on = loop_activate(3, loop_on)
    #loop_in(3)
    
    #sleep_time(5)
    #loop_out(3)
    
    sleep_time(5)
    loop_halve(3)
    
    sleep_time(3)
    loop_halve(3)
    
    loop_halve(3)
    
    loop_double(3)
    loop_double(3)
    
    loop_double(3)
    
    loop_on = loop_onoff(3, loop_on)
    sleep_time(10)
    auto_next()
    sleep_time(10)
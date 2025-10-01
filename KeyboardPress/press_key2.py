import time
import pyautogui
print("sleep 3 sec")
time.sleep(3) # Sleep for 3 seconds
print("a")
pyautogui.press('a')
print("sleep 1 sec")
time.sleep(1)
print("W")
pyautogui.press('W')
print("sleep 1 sec")
time.sleep(1)
print("ctrl s")
pyautogui.hotkey('ctrl', 's')
print("ctrl o")
pyautogui.hotkey('ctrl', 'o')
print("Esc")
pyautogui.press('esc')
aW
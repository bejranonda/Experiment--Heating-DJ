from pykeyboard import PyKeyboard
k = PyKeyboard()

# To Create an Alt+Tab combo
print("Alt")
k.press_key(k.alt_key)
print("Tab")
k.tap_key(k.tab_key)
print("Release")
k.release_key(k.alt_key)
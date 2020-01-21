import pyautogui
import shutil
import os
import time
from PIL import Image
import keyboard
from threading import Thread
import subprocess
import glob



#initializing screen size and checking if the screen file exists, if not creating one
try:
    with open("screen") as screen:
        string=screen.read()
        print(string)
except:
    os.system("echo 300,300 > screen")
    with open("screen") as screen:
        string=screen.read()
        print(string)
global screen_x, screen_y
screen_x, screen_y = string.split(",")

#random var
state = 0

#renaming png files and converting jpg files
def rename_def():
    while(True):
        try:
            for file in glob.glob("*.jpg"):
                time.sleep(0.1)
                im1 = Image.open(file)
                im1.save('test.png')
                os.remove(file)
            for file in glob.glob("*.png"):
                time.sleep(0.1)
                shutil.move(file, 'test.png')
        except:
            pass

# calling the other script
rename = Thread(target=rename_def)
rename.daemon=True
rename.start()


def main():
    try:
        global screen_x, screen_y
        screen_x, screen_y= int(screen_x), int(screen_y)

        #preparing and refactoring the image
        paused=False
        pyautogui.PAUSE = 0
        src="test.png"

        img = Image.open(src)
        img.convert("RGBA")
        pixels = img.load() # create the pixel map

        width, height = img.size
        new_height= height/width
        new_height=int(new_height*250)
        img = img.resize((250, new_height)) 

        for y in range(0, img.size[1], 2):    # for every col:
            for x in range(0, img.size[0], 2):    # For every row
                if keyboard.is_pressed('q'):  # if key 'q' is pressed 
                    paused=True
                
                if (paused):
                    break
                
                #get the pixels and prepare the var
                i = img.getpixel((x,y))
                try:
                    r,g,b,a=i
                    i=(r,g,b)
                except:
                    try:
                        r,g,b=i
                        a=255
                    except:
                        pass
                
                #drawing the image
                try:
                    if i < (220, 220, 220) and a > 0 and i >= (1,1,1):
                        pyautogui.moveTo(screen_x + x, screen_y + y) # Move the mouse to the x, y coordinates 100, 150.
                        pyautogui.click()
                except:
                    if i > 0:
                        pyautogui.moveTo(screen_x + x, screen_y + y) # Move the mouse to the x, y coordinates 100, 150.
                        pyautogui.click()
            if (paused):
                break
                
                
    except:
        pass
    os.remove("test.png")
    print("File Removed!")

print("press pos1 to set the draw space and press q to cancel the drawing\n")
while(True):
    try: 
        #refresh the screen position
        if keyboard.is_pressed('pos1'):  # if key 'q' is pressed 
            screen_x, screen_y = pyautogui.position()
            print(screen_x, screen_y, state)
            os.system("echo " + str(screen_x) +"," + str(screen_y) + "> screen")
        time.sleep(0.1)

        #calling the main function
        main()
    except:
        pass
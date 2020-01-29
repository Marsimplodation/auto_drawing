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
global config
config = []
try:
    with open("config") as screen:
        string=screen.read()
        config = string.split(";")
        print(string)
except:
    os.system("echo screen:300,300;ppp:0;resolution:300 > config")
    with open("config") as screen:
        string=screen.read()
        config = string.split(";")
        print(string)
global screen_x, screen_y, res_x, ppp

for i in config:
    print(i)
    if "screen" in str(i):
        i=(i.replace("screen:", ""))
        screen_x, screen_y = str(i).split(",")
    if "resolution:" in str(i):
        i=(i.replace("resolution:", ""))
        res_x = str(i)
    if "ppp:" in str(i):
        i = (i.replace("ppp:", ""))
        ppp = str(i)

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
        global screen_x, screen_y, res_x, ppp
        screen_x, screen_y, res_x, ppp= int(screen_x), int(screen_y), int(res_x), float(ppp)

        #preparing and refactoring the image
        paused=False
        pyautogui.PAUSE = 0
        src="test.png"

        img = Image.open(src)
        img.convert("RGBA")
        pixels = img.load() # create the pixel map

        width, height = img.size
        new_height= height/width
        new_height=int(new_height*res_x)
        img = img.resize((res_x, new_height))

        for y in range(0, img.size[1], 1):    # for every col:
            for x in range(0, img.size[0], 1):    # For every row
                time.sleep(ppp) #make it compatible with most drawing programms
                if keyboard.is_pressed('q'):  # cancels the drawing
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
                        pyautogui.moveTo(screen_x + x, screen_y + y) # Move the mouse to the pixel coordinate.
                        pyautogui.click()
                except:
                    if i > 0:
                        pyautogui.moveTo(screen_x + x, screen_y + y) # Move the mouse to the pixel coordinate.
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
        if keyboard.is_pressed('pos1'):
            screen_x, screen_y = pyautogui.position()
            print(screen_x, screen_y, state)
            os.system("echo screen:" + str(screen_x) +"," + str(screen_y) + ";ppp:"+str(ppp)+";resolution:"+str(res_x)+";" + "> config")
        time.sleep(0.1)

        #calling the main function
        main()
    except:
        pass
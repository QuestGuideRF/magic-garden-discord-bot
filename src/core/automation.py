import pyautogui
import time
import sys
import os
from pynput .keyboard import Controller ,Key
from .import state
from .config import Config
pyautogui .FAILSAFE =True
keyboard =Controller ()
try :
    import cv2
    CV2_AVAILABLE =True
except ImportError as e :
    CV2_AVAILABLE =False
    print (f"WARNING: OpenCV (cv2) not found: {e }")
    print ("Функции обнаружения изображений не будут работать должным образом.")
def resource_path (relative_path ):
    try :
        base_path =sys ._MEIPASS
    except AttributeError :
        base_path =os .path .abspath (".")
    return os .path .join (base_path ,relative_path )
def locate_image (image ,confidence ,bottom_half =False ,grayscale =True ):
    if not CV2_AVAILABLE :
        print ("ОШИБКА: OpenCV недоступен. Невозможно найти изображения.")
        return None
    try :
        image_path =resource_path (image )
        screen_width ,screen_height =pyautogui .size ()
        region =(0 ,0 ,screen_width ,screen_height )
        if bottom_half :
            region =(0 ,screen_height //2 ,screen_width ,screen_height //2 )
        return pyautogui .locateOnScreen (
        image_path ,
        confidence =confidence ,
        region =region ,
        grayscale =grayscale
        )
    except pyautogui .ImageNotFoundException :
        return None
    except Exception as e :
        state .stats ['errors']+=1
        print (f"Error locating image {image }: {e }")
        return None
def check_inventory_full ():
    state .stats ['inventory_checks']+=1
    image_path =os .path .join (Config .IMAGE_FOLDER ,"inventory_full.png")
    return locate_image (image_path ,confidence =Config .CONFIDENCE )is not None
def check_harvest_button ():
    image_path =os .path .join (Config .IMAGE_FOLDER ,"harvest_button.png")
    return locate_image (image_path ,confidence =Config .CONFIDENCE )is not None
def press_key (key ,hold =0.05 ):
    try :
        keyboard .press (key )
        time .sleep (hold )
        keyboard .release (key )
    except Exception as e :
        state .stats ['errors']+=1
        print (f"Error pressing key {key }: {e }")
def press_hotkey (key1 ,key2 ,delay =0.5 ):
    try :
        keyboard .press (key1 )
        keyboard .press (key2 )
        time .sleep (0.05 )
        keyboard .release (key2 )
        keyboard .release (key1 )
        time .sleep (delay )
    except Exception as e :
        state .stats ['errors']+=1
        print (f"Error pressing hotkey {key1 } + {key2 }: {e }")
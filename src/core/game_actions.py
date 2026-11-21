import time
from pynput .keyboard import Key
from .import state
from .import automation
from .config import Config
def sell_crops (logger =print ):
    state .stats ['total_sells']+=1
    state .stats ['last_sell_time']=time .time ()
    logger (f"📦 Inventory full at ({state .current_position ['row']}, {state .current_position ['col']}) - Selling...","warning")
    saved_position =state .current_position .copy ()
    automation .press_hotkey (Key .shift ,'3')
    time .sleep (0.3 )
    automation .press_key (Key .space )
    time .sleep (0.5 )
    automation .press_hotkey (Key .shift ,'2')
    time .sleep (Config .SELL_RETURN_DELAY )
    state .current_position .update (saved_position )
    logger ("✓ Урожай продан! Возобновляем сбор урожая...","success")
def move (direction ,steps =1 ,logger =print ):
    for _ in range (steps ):
        if not state .bot_running :
            return
        automation .press_key (direction )
        state .stats ['total_moves']+=1
        if direction =='w':
            state .current_position ['row']-=1
        elif direction =='s':
            state .current_position ['row']+=1
        elif direction =='a':
            state .current_position ['col']-=1
        elif direction =='d':
            state .current_position ['col']+=1
        time .sleep (Config .MOVE_DELAY )
        if automation .check_inventory_full ():
            sell_crops (logger )
def harvest (logger =print ):
    for _ in range (Config .HARVEST_COUNT ):
        if not state .bot_running :
            return
        if automation .check_inventory_full ():
            sell_crops (logger )
            automation .press_key (Key .space )
        automation .press_key (Key .space )
        time .sleep (Config .HARVEST_DELAY )
    state .stats ['total_harvests']+=1
def return_to_start (logger =print ):
    last_row_index =Config .GRID_SIZE -1
    if state .current_position ['row']>0 :
        move ('w',state .current_position ['row'],logger =logger )
    if state .current_position ['col']>0 :
        move ('a',state .current_position ['col'],logger =logger )
    state .current_position ['row']=0
    state .current_position ['col']=0
def harvest_loop (logger =print ):
    state .current_position ['row']=0
    state .current_position ['col']=0
    for row in range (Config .GRID_SIZE ):
        if not state .bot_running :return
        state .current_position ['row']=row
        if row %2 ==0 :
            for col in range (Config .GRID_SIZE ):
                if not state .bot_running :return
                state .current_position ['col']=col
                harvest (logger )
                if col <Config .GRID_SIZE -1 :
                    move ('d',logger =logger )
        else :
            for col in range (Config .GRID_SIZE -1 ,-1 ,-1 ):
                if not state .bot_running :return
                state .current_position ['col']=col
                harvest (logger )
                if col >0 :
                    move ('a',logger =logger )
        if row <Config .GRID_SIZE -1 :
            move ('s',logger =logger )
    if state .bot_running :
        logger ("✓ Сетка готова. Возвращаясь к началу...","info")
        return_to_start (logger )
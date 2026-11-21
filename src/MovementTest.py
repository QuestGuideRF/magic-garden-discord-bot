import time
from pynput .keyboard import Controller
GRID_SIZE =10
MOVE_DELAY =0.15
keyboard =Controller ()
def press_key (key ,hold =0.05 ):
    keyboard .press (key )
    time .sleep (hold )
    keyboard .release (key )
def move (direction ,steps =1 ):
    for _ in range (steps ):
        press_key (direction )
        time .sleep (MOVE_DELAY )
def movement_test ():
    print ("🚶 Начинаю тест на движение змеи...")
    for row in range (GRID_SIZE ):
        if row %2 ==0 :
            for col in range (GRID_SIZE -1 ):
                move ('d')
        else :
            for col in range (GRID_SIZE -1 ):
                move ('a')
        if row <GRID_SIZE -1 :
            move ('s')
    print ("🔄 Возвращаемся в исходное положение...")
    last_row =GRID_SIZE -1
    if last_row %2 ==0 :
        move ('a',GRID_SIZE -1 )
        move ('w',GRID_SIZE -1 )
    else :
        move ('w',GRID_SIZE -1 )
    print ("✅ Путь пройден и возвращен в исходное положение!")
print ("Тест начнется через 3 секунды... Переключитесь в окно игры!")
time .sleep (3 )
movement_test ()
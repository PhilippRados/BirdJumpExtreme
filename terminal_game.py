import curses
import random
import time
from threading import Thread

# initialize application
stdscr = curses.initscr()

curses.noecho()
stdscr.keypad(True)
curses.curs_set(0)

init_h,init_w = stdscr.getmaxyx()
min_width = 90
menu = ['PLAY', 'Choose Character','Scoreboard', 'Exit']
characters = ["Uwe","Charsten","Robert","Hans","Peter","Simon","Ursulla","Heike"]

curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)

def print_menu(row,inhalt):
    for i,text in enumerate(inhalt):
        h, w = stdscr.getmaxyx()
        x = w//2 - len(text)//2
        y = (h//2 - 2) + i
        if i == row:
            stdscr.addstr(y,x,text,curses.color_pair(1))
        else:
            stdscr.addstr(y,x,text)

def check_for_resize():
    too_large = True if init_w > min_width else False
    while too_large:
        stdscr.clear()
        resize_h, resize_w = stdscr.getmaxyx()
        question = f"The game is best played at a smaller window-size. Current size: {resize_w}"
        stdscr.addstr(resize_h//2,(resize_w//2)-len(question)//2, question) 
        too_large = False if resize_w < min_width else True
        stdscr.refresh() 

def create_env(h,w):
    number_of_platforms = (h // 1)-5
    platform_pos = [(0,0),(h-1, random.randint(1,w-5))]
    for _ in range(number_of_platforms):
        platform_pos.append((platform_pos[-1][0]-1, random.randint(1,w-6)))
    del platform_pos[0]
    return platform_pos


def print_env(env,counter):
    loop_env = env
    number_of_exceeded_platforms = 0
    for y,x in loop_env:
        y += counter
        stdscr.addstr(init_h-1,x,"    ")
        if y > 0 and y < init_h:
            stdscr.addstr(y,x,"=====")
            stdscr.addstr(y-1,x,"     ")
        elif y > init_h:
            number_of_exceeded_platforms += 1
            y += counter
            y_sorted_by_height = sorted(loop_env, key=lambda tup: tup[0])
            env.remove(y_sorted_by_height[-1])
            env.append(((3-counter) + number_of_exceeded_platforms, random.randint(1,init_w-6)))
        else:
           y += 1


def move_left(current_x, current_y):
    stdscr.addstr(current_y,current_x+1," ") 

def move_right(current_x, current_y):
    stdscr.addstr(current_y,current_x-1," ") 

def press_exit():
    stdscr.clear()
    prompt = "If you say so"
    stdscr.addstr(init_h//2,(init_w//2)-len(prompt)//2, prompt)
    stdscr.refresh()


def play(resize_w, resize_h, character="o/00\o"):
    playing = True
    current_x, current_y = 10, resize_h//2
    env = create_env(resize_h, resize_w)
    counter = 0
    plateau_height = [0,0]
    score = 0
    while playing:   
        if counter > score:
            score = counter
        stdscr.clear()
        print_env(env,counter)
        stdscr.addstr(0,0,f"Score: {score}")
        
        stdscr.refresh()
        if current_y < resize_h and current_y > 0:
            stdscr.addstr(current_y,current_x,"o/00\o")
        elif current_y > resize_h:
            playing = False

        #when platform hit
        if stdscr.instr(current_y+1, current_x,1) == b"=": #maybe use inwstr
            plateau_height[0] = plateau_height[1]
            plateau_height[1] = current_y

            #when new platform is higher
            if plateau_height[1] < plateau_height[0]:
                for _ in range(8):
                    time.sleep(0.01)
                    stdscr.clear()
                    counter += 1
                    if current_y < resize_h and current_y > 0:
                        stdscr.addstr(current_y,current_x,"o/00\o")
                    elif current_y > resize_h:
                        playing = False
                    print_env(env,counter)
                    stdscr.refresh()

            #if new platform isnt higher than before
            else:
                for _ in range(8):
                    stdscr.clear()
                    print_env(env,counter)
                    time.sleep(0.01)
                    counter += 1
                    if current_y < resize_h and current_y > 0:
                        stdscr.addstr(current_y,current_x,"o/00\o")
                    elif current_y > resize_h:
                        playing = False
                    stdscr.refresh()

        else:
            counter -= 1
        
        stdscr.timeout(70)
        inp = stdscr.getch()
        if inp == curses.KEY_LEFT and current_x > 1:
            current_x -= 3 
            move_left(current_x, current_y)
        elif inp == curses.KEY_RIGHT and current_x < (resize_w-6): 
            current_x += 3
            move_right(current_x, current_y)


    stdscr.clear()
    stdscr.addstr(resize_h//2,resize_w//2 - 10, f"Game over. Your score was {score}")
    stdscr.refresh()

def choose_character():
    current_idx = 0
    stdscr.clear()
    print_menu(current_idx, characters)
    stdscr.refresh()

    char_key = stdscr.getch()
    while char_key != 10:
        if char_key == curses.KEY_UP and current_idx > 0:
            current_idx -= 1
            print_menu(current_idx, characters)
        elif char_key == curses.KEY_DOWN and current_idx< 3:
            current_idx += 1
            print_menu(current_idx, characters)

    character_chosen = characters[current_idx]
    return character_chosen



def main(stdscr):
    current_row = 0
    game = True
    character = "o/00\o"

    while game:
        check_for_resize()
        stdscr.clear()
        stdscr.refresh()
        resize_h, resize_w = stdscr.getmaxyx()

        print_menu(current_row, menu) 
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
            print_menu(current_row, menu)
        elif key == curses.KEY_DOWN and current_row < 3:
            current_row += 1
            print_menu(current_row, menu)
    
        #EXIT Button
        if key == 10 and current_row == 3:
            press_exit()
            game = False
        
        #character choice
        if key == 10 and current_row == 1:
            character = choose_character()

        #PLAY Button
        elif key == 10 and current_row == 0:
            stdscr.clear()
            play(resize_w, resize_h, character)
            break

        #Scoreboard Button
        elif key == 10 and current_row == 2:
            stdscr.clear()
            question = "Work in progress..."
            stdscr.addstr(init_h//2,(init_w//2)-len(question)//2, question)
            stdscr.refresh()
            break
            
curses.wrapper(main)

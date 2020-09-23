import curses
import random
import time

# initialize application
stdscr = curses.initscr()

curses.noecho()
stdscr.keypad(True)
curses.curs_set(0)

init_h,init_w = stdscr.getmaxyx()
min_width = 90
menu = ['PLAY', 'Scoreboard', 'Exit']

curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)

def print_menu(row):
    for i,text in enumerate(menu):
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

def create_env(h,w, platform_anz=15):
    return [(random.randint(1,h-5), random.randint(1,w-5)) for i in range(platform_anz)]

def print_env(env,counter):
    for y,x in env:
        y += counter
        stdscr.addstr(init_h-1,x,"    ")
        if y > 0 and y < init_h:
            stdscr.addstr(y,x,"=====")
            stdscr.addstr(y-1,x,"    ")
        else:
            y += counter
            y_sorted_by_height = sorted(env, key=lambda tup: tup[0])
            env.remove(y_sorted_by_height[-1])
            env.append((1-counter, random.randint(1,init_w-5))) 


def move_left(current_x, current_y):
    stdscr.addstr(current_y,current_x+1," ") 

def move_right(current_x, current_y):
    stdscr.addstr(current_y,current_x-1," ") 

def press_exit():
    stdscr.clear()
    prompt = "If you say so"
    stdscr.addstr(init_h//2,(init_w//2)-len(prompt)//2, prompt)
    stdscr.refresh()


def play(resize_w, resize_h):
    playing = True
    current_x, current_y = 10, resize_h//2
    env = create_env(resize_h, resize_w)
    counter = 0
    while playing:   
        #counter += 1
        stdscr.clear()
        print_env(env,counter)
        
        stdscr.refresh()
        if current_y < resize_h:
            stdscr.addstr(current_y,current_x,"o/00\o")
        else:
            playing = False


        if stdscr.instr(current_y+1, current_x+2,1) == b"=":
            current_y -= 8
            # maybe put a timeout here so that the player goes down slower
            #counter += 4
            if stdscr.instr(current_y+1, current_x+2,1) == b"=":
                counter += 2            
        else:
            current_y += 1

        stdscr.timeout(100)
        inp = stdscr.getch()
        if inp == curses.KEY_LEFT and current_x > 0:
            current_x -= 4 
            move_left(current_x, current_y)
        elif inp == curses.KEY_RIGHT and current_x < (resize_w-6): 
            current_x += 4
            move_right(current_x, current_y)

    stdscr.clear()
    stdscr.addstr(resize_h//2,resize_w//2 - 5, "Game over")
    stdscr.refresh()
        

        

def main(stdscr):
    current_row = 0
    game = True

    while game:
        check_for_resize()
        stdscr.clear()
        stdscr.refresh()
        resize_h, resize_w = stdscr.getmaxyx()

        print_menu(current_row) 
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
            print_menu(current_row)
        elif key == curses.KEY_DOWN and current_row < 2:
            current_row += 1
            print_menu(current_row)
    
        #EXIT Button
        if key == 10 and current_row == 2:
            press_exit()
            game = False

        #PLAY Button
        elif key == 10 and current_row == 0:
            stdscr.clear()
            play(resize_w, resize_h)
            break
        
        elif key == 10 and current_row == 1:
            stdscr.clear()
            question = "Work in progress..."
            stdscr.addstr(init_h//2,(init_w//2)-len(question)//2, question)
            stdscr.refresh()
            break
            
curses.wrapper(main)
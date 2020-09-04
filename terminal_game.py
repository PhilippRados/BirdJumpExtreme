
import curses
import time
import random

# initialize application
stdscr = curses.initscr()

# tweak terminal settings
curses.noecho()
stdscr.keypad(True)
curses.curs_set(0)

h,w = stdscr.getmaxyx()

menu = ['PLAY', 'Scoreboard', 'Exit']

curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)

def print_menu(row):
    for i,text in enumerate(menu):
        x = w//2 - len(text)//2
        y = (h//2 - 2) + i
        if i == row:
            stdscr.addstr(y,x,text,curses.color_pair(1))
        else:
            stdscr.addstr(y,x,text)

def print_env():
    env_pos = [(random.randint(1,h-5), random.randint(10,w-10)) for i in range(10)]
    return env_pos

def press_exit():
    stdscr.clear()
    prompt = "If you say so"

    stdscr.addstr(h//2,(w//2)-len(prompt)//2, prompt)
    stdscr.refresh()


def play(difficulty):
    playing = True
    current_x, current_y = 10, h//2
    env = print_env()
    counter = 0
    while playing:     
        counter += 1
        for y,x in env:
            if y > 1 and y < (h-1):
                y += counter
                stdscr.addstr(y,x,"--")
                stdscr.addstr(y-1,x,"  ") 
            else:
                y += counter
                
        
        curses.halfdelay(difficulty)
        stdscr.addstr(current_y,current_x,"#")

        inp = stdscr.getch()
        stdscr.nodelay(True)
        if inp  == curses.KEY_LEFT:
            current_x -= 1 
            stdscr.addstr(current_y,current_x,"#")
            stdscr.addstr(current_y, current_x+1," ")
        elif inp == curses.KEY_RIGHT:
            current_x += 1
            stdscr.addstr(current_y,current_x,"#")
            stdscr.addstr(current_y, current_x-1," ")
        
        curses.halfdelay(difficulty)
        


def main(stdscr):
    current_row = 0
    print_menu(current_row)    
    game = True

    while game:
        too_large = curses.is_term_resized(50,40)
        while too_large:
            stdscr.clear()
            question = "The game is best played at a smaller window-size (y=50,x=40)"
            resize_h, resize_w = stdscr.getmaxyx()
            stdscr.addstr(resize_h//2,(resize_w//2)-len(question)//2, question) 
            stdscr.refresh()

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
            play(3)
            #stdscr.refresh()
            break
        
        elif key == 10 and current_row == 1:
            stdscr.clear()
            question = "Work in progress..."
            stdscr.addstr(h//2,(w//2)-len(question)//2, question)
            stdscr.refresh()
            break
            
curses.wrapper(main)
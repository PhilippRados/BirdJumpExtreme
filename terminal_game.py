
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
        h, w = stdscr.getmaxyx()
        x = w//2 - len(text)//2
        y = (h//2 - 2) + i
        if i == row:
            stdscr.addstr(y,x,text,curses.color_pair(1))
        else:
            stdscr.addstr(y,x,text)

def print_env(h,w):
    env_pos = [(random.randint(1,h-5), random.randint(1,w-5)) for i in range(15)]
    return env_pos

def press_exit():
    stdscr.clear()
    prompt = "If you say so"
    stdscr.addstr(h//2,(w//2)-len(prompt)//2, prompt)
    stdscr.refresh()


def play(difficulty, resize_w, resize_h):
    playing = True
    current_x, current_y = 10, h//2
    env = print_env(resize_h, resize_w)
    counter = 0
    while playing:   
        counter += 1
        stdscr.clear()
        curses.halfdelay(difficulty)
        #current_y += 1
        for y,x in env:
            y += counter
            stdscr.addstr(h-1,x,"    ")
            if y > 1 and y < h:
                stdscr.addstr(y,x,"====")
                stdscr.addstr(y-1,x,"    ")
            else:
                y += counter
                y_sorted_by_height = sorted(env, key=lambda tup: tup[0])
                env.remove(y_sorted_by_height[-1])
                env.append((1-counter, random.randint(1,w-5)))
        
        stdscr.refresh()
        stdscr.nodelay(True)
        stdscr.addstr(current_y,current_x,"#")
        inp = stdscr.getch()
        
        if inp  == curses.KEY_LEFT:
            current_x -= 1 
            # for characters look into 
            stdscr.addstr(current_y,current_x,"#")
            stdscr.addstr(current_y, current_x+1," ")
        elif inp == curses.KEY_RIGHT:
            current_x += 1
            stdscr.addstr(current_y,current_x,"#")
            stdscr.addstr(current_y, current_x-1," ")
        
        
        curses.halfdelay(difficulty)
        


def main(stdscr):
    current_row = 0
    game = True

    while game:
        too_large = True if w > 90 else False
        while too_large:
            stdscr.clear()
            resize_h, resize_w = stdscr.getmaxyx()
            question = f"The game is best played at a smaller window-size. Current size: {resize_w}"
            stdscr.addstr(resize_h//2,(resize_w//2)-len(question)//2, question) 
            too_large = False if resize_w < 90 else True
            stdscr.refresh()
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
            play(3, resize_w, resize_h)
            #stdscr.refresh()
            break
        
        elif key == 10 and current_row == 1:
            stdscr.clear()
            question = "Work in progress..."
            stdscr.addstr(h//2,(w//2)-len(question)//2, question)
            stdscr.refresh()
            break
            
curses.wrapper(main)
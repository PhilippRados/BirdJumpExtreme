import curses
import random
import time
from tabulate import tabulate
import pickle
from curses.textpad import Textbox, rectangle
from asciimatics.renderers import FigletText

# initialize application
stdscr = curses.initscr()

curses.noecho()
stdscr.keypad(True)
curses.curs_set(0)

init_h,init_w = stdscr.getmaxyx()
menu = ['PLAY', 'Choose Character','Scoreboard', 'Exit']
characters = [">o)\n(_>",' (@>\n{||\n ""'," ,_\n>' )\n( ( \ \n ''","  /\n,'`./\n`.,'\ \n  \ ",
        "  _\n /_|\n('_)<|\n \_|","   __\n _/__)\n(8|)_}}-\n `\__)"]

curses.start_color()
curses.init_pair(1, curses.COLOR_BLACK, curses.COLOR_YELLOW)

#initialize scoreboard
try:
    open("score_board.pickle","rb")
except:
    score = []
    pickle.dump(score, open("score_board.pickle","wb"))
    

def print_menu(row):
    for i,text in enumerate(menu):
        h, w = stdscr.getmaxyx()
        x = w//2 - len(text)//2
        y = (h//2 - 2) + i
        if i == row:
            stdscr.addstr(y,x,text,curses.color_pair(1))
        else:
            stdscr.addstr(y,x,text)

def print_character_menu(row):
    stdscr.clear()
    y_counter = 0        
    for i,text in enumerate(characters):
        h, w = stdscr.getmaxyx()
        character_height = 8
        x1 = w//2 - 9
        x2 = w//2 + 1

        if i % 2 == 0:
            y_counter += 1
            y = (h//6) + (y_counter * character_height)
            if i == row:
               print_player_highlighted(y,x1,text)
            else:
                print_player(y,x1,text) 
        else:
            y = (h//6) + (y_counter * character_height)
            if i == row:
               print_player_highlighted(y,x2,text)
            else:
                print_player(y,x2,text)  

def check_for_resize(w,h,max_width=90,min_height=36):
    wrong_size = True if w > max_width or h < min_height else False
    while wrong_size:
        stdscr.clear()
        resize_h, resize_w = stdscr.getmaxyx()
        text = f"The game is best played at a vertical-rectangle shape"
        text2 = f"Current size(x,y): {resize_w,resize_h}" 
        print_centered(resize_w,resize_h,text)
        print_centered(resize_w,resize_h+2,text2)
        wrong_size = False if resize_w < max_width and resize_h > min_height else True
        stdscr.refresh() 

def create_env(h,w):
    number_of_platforms = (h // 1)-6
    platform_pos = [(0,0),(h-1, random.randint(1,w-8))]
    for _ in range(number_of_platforms):
        platform_pos.append((platform_pos[-1][0]-1, random.randint(1,w-8)))
    del platform_pos[0]
    return platform_pos


def print_env(w,h,env,counter):
    loop_env = env
    number_of_exceeded_platforms = 0
    for y,x in loop_env:
        y += counter
        stdscr.addstr(h-1,x," " * 7)
        if y > 0 and y < h:
            stdscr.addstr(y,x,"=" * 7)
            stdscr.addstr(y-1,x," " * 7)
        elif y > h:
            number_of_exceeded_platforms += 1
            y += counter
            y_sorted_by_height = sorted(loop_env, key=lambda tup: tup[0])
            env.remove(y_sorted_by_height[-1])
            env.append(((3-counter) + number_of_exceeded_platforms, random.randint(1,w-8)))
        else:
           y += 1

def move(current_x, current_y,right):
    if right:
        stdscr.addstr(current_y,current_x-1," ") 
    else:
        stdscr.addstr(current_y,current_x+1," ")   

def press_exit():
    stdscr.clear()
    prompt = "If you say so"
    stdscr.addstr(init_h//2,(init_w//2)-len(prompt)//2, prompt)
    stdscr.refresh()

def slice_character_string(character):
    idx = 0
    sliced_list = []
    for pos,i in enumerate(character):
        if i == "\n":
            sliced_list.append(character[idx:pos])
            idx = pos + 1
    sliced_list.append(character[idx:pos+1])
    return sliced_list


def print_player(current_y, current_x,character):
    sliced_character = slice_character_string(character)
    for i in range(len(sliced_character)):
        stdscr.addstr(current_y - i,current_x - 1,sliced_character[-(i+1)])

def print_player_highlighted(current_y,current_x, character,width=8,height=4):
    sliced_character = slice_character_string(character)
    for i in range(height):
        if i >= len(sliced_character):
            stdscr.addstr(current_y - i,current_x -1," "*width,curses.color_pair(1))
        else:
            text = sliced_character[-(i+1)] + " " * (width - len(sliced_character[-(i+1)]))
            stdscr.addstr(current_y - i,current_x - 1,text,curses.color_pair(1))



def play(resize_w, resize_h, character=">o)\n(_>",name="Player1"):
    playing = True  
    current_x, current_y = 10, resize_h//2
    env = create_env(resize_h, resize_w)
    counter = 0
    score = 0
    timer_since_platform_hit = 0
    start_time = time.time()
    while playing:
        if timer_since_platform_hit > 3:
            playing = False
        if counter > score:
            score = counter

        stdscr.clear()
        print_env(resize_w,resize_h,env,counter)
        print_player(current_y, current_x,character)
        stdscr.addstr(0,0,f"Score: {score}")
        stdscr.refresh()
        
        #when platform hit
        if stdscr.instr(current_y+1, current_x,1) == b"=": #maybe use inwstr
            for i in range(10):
                time.sleep(0.01)
                stdscr.clear()
                counter += 1
                print_player(current_y, current_x, "_._O-")
                if i < 7:
                    stdscr.addstr(current_y + 1,current_x, "^  ^· ")
                    stdscr.addstr(current_y + 2,current_x, " ^^.. ")
                print_env(resize_w,resize_h,env,counter)
                stdscr.addstr(0,0,f"Score: {score}")
                stdscr.refresh()
            start_time = time.time()

        else:
            counter -= 1
        
        stdscr.timeout(100)
        inp = stdscr.getch()
        if inp == curses.KEY_LEFT and current_x > 1:
            current_x -= 4 
            move(current_x, current_y,False)
        elif inp == curses.KEY_RIGHT and current_x < (resize_w-6): 
            current_x += 4
            move(current_x, current_y,True)
        
        timer_since_platform_hit = time.time() - start_time
    save_score(name,score)
    return score

def save_score(name,score):
    scoreboard = pickle.load(open("score_board.pickle","rb"))

    if len(scoreboard) < 10:
        scoreboard.append([name,score])
        pickle.dump(sorted(scoreboard, key=lambda tup:tup[1],reverse=True),open("score_board.pickle","wb"))
    elif scoreboard[-1][1] <= score:
        del scoreboard[-1]
        scoreboard.append([name,score])
        pickle.dump(sorted(scoreboard, key=lambda tup:tup[1],reverse=True), open("score_board.pickle","wb"))


def choose_character(w,h):
    current_idx = 0
    stdscr.clear()
    print_character_menu(current_idx)
    stdscr.refresh()

    while True:
        print_centered(w,h,"Press 'm' to jump back to menu","bottom")
        print_centered(w,h,"To choose character press ENTER","top")

        char_key = stdscr.getch()
        if char_key == curses.KEY_UP and current_idx > 1:
            current_idx -= 2
            print_character_menu(current_idx)
        elif char_key == curses.KEY_DOWN and current_idx < len(characters) - 2:
            current_idx += 2
            print_character_menu(current_idx)
        elif char_key == curses.KEY_LEFT and current_idx % 2 != 0: 
            current_idx -= 1
            print_character_menu(current_idx)
        elif char_key == curses.KEY_RIGHT and current_idx % 2 == 0:
            current_idx += 1
            print_character_menu(current_idx)
        if char_key == ord("m"):
            current_idx = 0
            break
        if char_key == 10:
            break
    
    character_chosen = characters[current_idx]
    return character_chosen

def scoreboard_screen(score_list,w,h):
    stdscr.clear()
    x1 = w//2 - 10
    x2 = w//2 + 5
    y = h//4
    
    stdscr.addstr(y-1,x1,"NAME",curses.A_STANDOUT)
    stdscr.addstr(y-1,x2,"SCORE",curses.A_STANDOUT)
    stdscr.addstr(y,x1,"-" * 20)

    for name,score in score_list:
        y += 2
        stdscr.addstr(y,x1,name)
        stdscr.addstr(y,x2,str(score))
        
        stdscr.addstr(y+1,x1,"-" * 20)
    print_centered(w,h,"TOP 10","top")
    print_centered(w,h,"Press 'm' to jump back to menu","bottom")
    stdscr.refresh()
    return navigation_key_press()

def endscreen(score,w,h):
    stdscr.clear()
    print_centered(w,h,f"Game over. Your score was {score}","mid")
    print_centered(w,h,"Press 'm' to jump back to menu","bottom")
    return navigation_key_press()

def print_centered(w,h,text,pos="mid"):
    if pos == "mid":
        stdscr.addstr(h//2,w//2 - len(text)//2,text)
    elif pos == "bottom":
        stdscr.addstr(h-2,w//2 - len(text)//2,text)
    elif pos =="top":
        stdscr.addstr(2,w//2 - len(text)//2,text,curses.A_BOLD) 

def navigation_key_press():
    game = True
    stdscr.nodelay(False)
    while True:
        end_key = stdscr.getch()
        if end_key == ord('m'):
            pass
            break
        elif end_key == ord("q"):
            game = False
            break
    return game

def name_screen(w,h):
    print_centered(w,h,"Enter NAME: (hit ENTER to send)","top")

    editwin = curses.newwin(1,12, 5,(w//2)-6)
    rectangle(stdscr, 4,w//2-8,6,w//2+8)
    stdscr.refresh()

    box = Textbox(editwin)
    box.edit()
    return box.gather()

def main(stdscr):
    current_row = 0
    game = True
    character = ">o)\n(_>"

    while game:
        resize_h, resize_w = stdscr.getmaxyx()
        check_for_resize(resize_w,resize_h)
        stdscr.clear()
        stdscr.refresh()

        print_menu(current_row) 
        stdscr.timeout(70)
        key = stdscr.getch()
        if key == curses.KEY_UP and current_row > 0:
            current_row -= 1
            print_menu(current_row)
        elif key == curses.KEY_DOWN and current_row < 3:
            current_row += 1
            print_menu(current_row)
    
        #EXIT Button
        if key == 10 and current_row == 3:
            press_exit()
            game = False
        
        #character choice
        if key == 10 and current_row == 1:
            character = choose_character(resize_w,resize_h)

        #PLAY Button
        elif key == 10 and current_row == 0:
            stdscr.clear()
            name = name_screen(resize_w, resize_h)
            score = play(resize_w, resize_h, character, name)
            game = endscreen(score,resize_w, resize_h)

        #Scoreboard Button
        elif key == 10 and current_row == 2:
            scoreboard = pickle.load(open("score_board.pickle","rb"))
            game = scoreboard_screen(scoreboard,resize_w, resize_h)
            
curses.wrapper(main)
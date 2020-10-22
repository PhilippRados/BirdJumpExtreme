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
menu = ['PLAY', 'Choose Character','Scoreboard', 'Exit']
characters = [">o)\n(_>",' (@>\n{||\n ""'," ,_\n>' )\n( ( \ \n ''","  /\n,'`./\n`.,'\ \n  \ ",
        "  _\n /_|\n('_)<|\n \_|","   __\n _/__)\n(8|)_}}-\n `\__)"]

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
    platform_pos = [(0,0),(h-1, random.randint(1,w-8))]
    for _ in range(number_of_platforms):
        platform_pos.append((platform_pos[-1][0]-1, random.randint(1,w-8)))
    del platform_pos[0]
    return platform_pos


def print_env(env,counter):
    loop_env = env
    number_of_exceeded_platforms = 0
    for y,x in loop_env:
        y += counter
        stdscr.addstr(init_h-1,x,"       ")
        if y > 0 and y < init_h:
            stdscr.addstr(y,x,"=======")
            stdscr.addstr(y-1,x,"       ")
        elif y > init_h:
            number_of_exceeded_platforms += 1
            y += counter
            y_sorted_by_height = sorted(loop_env, key=lambda tup: tup[0])
            env.remove(y_sorted_by_height[-1])
            env.append(((3-counter) + number_of_exceeded_platforms, random.randint(1,init_w-8)))
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



def play(resize_w, resize_h, character=">o)\n(_>"):
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
        print_env(env,counter)
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
                    stdscr.addstr(current_y + 3,current_x, " .^^ ")
                    stdscr.addstr(current_y + 4,current_x, "^ ^.^")
                print_env(env,counter)
                stdscr.refresh()
            start_time = time.time()

        else:
            counter -= 1
        
        stdscr.timeout(70)
        inp = stdscr.getch()
        if inp == curses.KEY_LEFT and current_x > 1:
            current_x -= 4 
            move(current_x, current_y,False)
        elif inp == curses.KEY_RIGHT and current_x < (resize_w-6): 
            current_x += 4
            move(current_x, current_y,True)
        
        timer_since_platform_hit = time.time() - start_time
        
    stdscr.clear()
    stdscr.addstr(resize_h//2,resize_w//2 - 10, f"Game over. Your score was {score}")
    stdscr.refresh()

def choose_character():
    current_idx = 0
    stdscr.clear()
    print_character_menu(current_idx)
    stdscr.refresh()

    while True:
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
        if char_key == 10:
            break

    character_chosen = characters[current_idx]
    return character_chosen


def main(stdscr):
    current_row = 0
    game = True
    character = ">o)\n(_>"

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
        elif key == curses.KEY_DOWN and current_row < 3:
            current_row += 1
            print_menu(current_row)
    
        #EXIT Button
        if key == 10 and current_row == 3:
            press_exit()
            game = False
        
        #character choice
        if key == 10 and current_row == 1:
            character = choose_character()
            play(resize_w,resize_h,character)

        #PLAY Button
        elif key == 10 and current_row == 0:
            stdscr.clear()
            play(resize_w, resize_h, character)

        #Scoreboard Button
        elif key == 10 and current_row == 2:
            stdscr.clear()
            question = "Work in progress..."
            stdscr.addstr(init_h//2,(init_w//2)-len(question)//2, question)
            stdscr.refresh()
            break
            
curses.wrapper(main)

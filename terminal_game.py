import curses
import random
import time
import pickle
from curses.textpad import Textbox, rectangle
from art import text2art

# initialize application
stdscr = curses.initscr()

curses.noecho()
stdscr.keypad(True)
curses.curs_set(0)

init_h,init_w = stdscr.getmaxyx()
menu = ['PLAY', 'Choose Character','Scoreboard', 'Exit']
characters = [">o)\n(_>",' (@>\n{||\n ""'," ,_\n>' )\n( ( \ \n ''","  /\n,'`./\n`.,'\ \n  \ ",
        "  _\n /_|\n('_)<|\n \_|","   __\n _/__)\n(8|)_}}\n `\__)"]

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

def print_character_menu(row,locked_character,score=1):
    stdscr.clear()
    y_counter = 0

    for i,text in enumerate(characters):
        if score < locked_character[i]:
            text = u"   \U0001F512\n"+f"  {locked_character[i]}"

        h, w = stdscr.getmaxyx()
        character_height = 8
        x1 = w//2 - 9
        x2 = w//2 + 1

        if i % 2 == 0:
            y_counter += 1
            y = (h//6) + (y_counter * character_height)
            if i == row:
                print_multiple_lines_highlighted(y,x1,text)
            else:
                print_multiple_lines(y,x1,text)
        else:
            y = (h//6) + (y_counter * character_height)
            if i == row:
                print_multiple_lines_highlighted(y,x2,text)
            else:
                print_multiple_lines(y,x2,text)

def check_for_resize(max_width=90,min_width=66,min_height=46):
    h,w = stdscr.getmaxyx()
    wrong_size = True if w > max_width or h < min_height \
         or w < min_width else False
    while wrong_size:
        stdscr.clear()
        resize_h, resize_w = stdscr.getmaxyx()
        text = "Resize your window"
        text2 = "its either too small or too big"
        print_centered(resize_w,resize_h,text)
        print_centered(resize_w,resize_h+2,text2)
        wrong_size = False if resize_w < max_width and \
            resize_h > min_height and resize_w > min_width else True
        stdscr.refresh()

def create_env(h,w):
    number_of_platforms = h-6
    fake_platform_idx = random.sample(range(number_of_platforms),2)
    platform_pos = [(0,0),(h-1, random.randint(1,w-8),False)]
    for i in range(number_of_platforms):
        if i in fake_platform_idx:
            platform_pos.append((platform_pos[-1][0]-1, random.randint(1,w-8),True))
        else:
            platform_pos.append((platform_pos[-1][0]-1, random.randint(1,w-8),False))
    del platform_pos[0]
    return platform_pos

def check_threshhold_drop(loop_env,score,threshhold):
    dropped_platforms = idx_fake_platforms(loop_env,2)

    if len(threshhold) > 0 and score > threshhold[0] and len(dropped_platforms) > 1:
        for i in range(2):
            if len(loop_env) > dropped_platforms[i]: 
                del loop_env[dropped_platforms[i]]
        del threshhold[0]
    return threshhold

def print_env(w,h,env,counter,score,fake_platform_probs):
    loop_env = env
    number_of_exceeded_platforms = 0

    for y,x,fake in loop_env:
        y += counter
        stdscr.addstr(h-1,x," " * 7)
        if y > 0 and y < h and fake == False:
            stdscr.addstr(y,x,"=" * 7)
            stdscr.addstr(y-1,x," " * 7)
        elif y > 0 and y < h and fake == True:
            stdscr.addstr(y,x,"x" * 7,curses.color_pair(1))
            stdscr.addstr(y-1,x," " * 7)

        elif y > h:
            number_of_exceeded_platforms += 1
            y += counter
            y_sorted_by_height = sorted(loop_env, key=lambda tup: tup[0])
            env.remove(y_sorted_by_height[-1])
            if random.random() > fake_platform_probs:
                env.append(((3-counter) + number_of_exceeded_platforms, random.randint(1,w-8),False))
            else:
                env.append(((3-counter) + number_of_exceeded_platforms, random.randint(1,w-8),True))
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


def print_multiple_lines(current_y, current_x,character):
    sliced_character = slice_character_string(character)
    for i in range(len(sliced_character)):
        stdscr.addstr(current_y - i,current_x - 1,sliced_character[-(i+1)])

def print_multiple_lines_highlighted(current_y,current_x, character,width=8,height=4,locked=False):
    sliced_character = slice_character_string(character)
    for i in range(height):
        if i >= len(sliced_character):
            stdscr.addstr(current_y - i,current_x -1," "*width,curses.color_pair(1))
        else:
            first_part_of_string = sliced_character[-(i+1)]
            first_len = len(first_part_of_string)
            if u"\U0001F512" in first_part_of_string: #not extend highlight if lock
                first_len += 1
            text = first_part_of_string + " " * (width - first_len)
            stdscr.addstr(current_y - i,current_x - 1,text,curses.color_pair(1))

def pause_screen(w,h):
    stdscr.clear()
    text = text2art("Pause","small")
    print_multiple_lines((h//2)-3,w//2-12,text)

    print_centered(w,h,"press 'm' to resume")
    print_centered(w,h + 2,"press 'q' to go back to the menu")
    stdscr.refresh()
    return navigation_key_press()

def print_top_bar(resize_w, score):
    text = "'p' for pause"
    stdscr.addstr(0,resize_w - (len(text)+2),text)
    stdscr.addstr(0,0,f"Score: {score}")
    stdscr.addstr(1,0,"-"*resize_w)


def idx_fake_platforms(env,number_of_dropped_platforms):
    result = []
    neue = [i for i in env if i[2] == True]
    if len(neue) > 1:
        for i in range(number_of_dropped_platforms):
            random_drop = random.choice(neue)
            result.append(env.index(random_drop))
            neue.remove(random_drop)
    return result

def play(resize_w, resize_h, character=">o)\n(_>",name="Player1"):
    playing = True
    current_x, current_y = 10, resize_h//2
    env = create_env(resize_h, resize_w)
    counter = 0
    score = 0
    timer_since_platform_hit = 0
    start_time = time.time()
    score_threshholds = [100,200,300,500,600,750,1000]
    threshhold_len = len(score_threshholds)
    fake_platform_probs = 0.05

    while playing:
        check_for_resize()
        if timer_since_platform_hit > 3:
            playing = False

        if threshhold_len > len(score_threshholds):
            threshhold_len = len(score_threshholds)
            fake_platform_probs += 0.05

        if counter > score:
            score = counter

        stdscr.clear()
        print_env(resize_w,resize_h,env,counter,score,fake_platform_probs)
        score_threshholds = check_threshhold_drop(env,score,score_threshholds)

        print_multiple_lines(current_y, current_x,character)
        print_top_bar(resize_w, score)
        stdscr.refresh()

        #when platform hit
        if stdscr.instr(current_y+1, current_x,1) == b"=":
            for i in range(10):
                time.sleep(0.01)
                stdscr.clear()
                counter += 1
                print_multiple_lines(current_y, current_x, "_._O-")
                if i < 7:
                    stdscr.addstr(current_y + 1,current_x, "^  ^· ")
                    stdscr.addstr(current_y + 2,current_x, " ^^.. ")

                print_env(resize_w,resize_h,env,counter,score,fake_platform_probs)
                score_threshholds = check_threshhold_drop(env, score,score_threshholds)

                print_top_bar(resize_w, score)
                stdscr.refresh()
            start_time = time.time()
        else:
            counter -= 1

        stdscr.timeout(100)
        inp = stdscr.getch()
        if inp == curses.KEY_LEFT and current_x > 3:
            current_x -= 4
            move(current_x, current_y,False)
        elif inp == curses.KEY_RIGHT and current_x < (resize_w-6):
            current_x += 4
            move(current_x, current_y,True)
        if inp == ord("p"):
            playing = pause_screen(resize_w, resize_h)
            start_time = time.time()

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
    scoreboard = pickle.load(open("score_board.pickle","rb"))
    best_score = scoreboard[0][1] if len(scoreboard) > 0 else 1
    locked_character = [0,250,500,750,1000,1500]

    while True:
        check_for_resize()
        print_character_menu(current_idx,locked_character,best_score)
        print_centered(w,h,"Press 'm' to jump back to menu","bottom")
        print_centered(w,2,"To choose character press ENTER","top")
        print_centered(w,4,"You have to score more points to unlock new characters","top")
        stdscr.refresh()

        char_key = stdscr.getch()
        if char_key == curses.KEY_UP and current_idx > 1:
            current_idx -= 2
            print_character_menu(current_idx,locked_character,best_score)
        elif char_key == curses.KEY_DOWN and current_idx < len(characters) - 2:
            current_idx += 2
            print_character_menu(current_idx, locked_character, best_score)
        elif char_key == curses.KEY_LEFT and current_idx % 2 != 0:
            current_idx -= 1
            print_character_menu(current_idx, locked_character, best_score)
        elif char_key == curses.KEY_RIGHT and current_idx % 2 == 0:
            current_idx += 1
            print_character_menu(current_idx, locked_character, best_score)
        if char_key == ord("m"):
            current_idx = 0
            break
        locked = True if locked_character[current_idx] > best_score else False
        if char_key == 10 and locked == False:
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

    text = text2art("Top 10","small")
    print_multiple_lines(7,(w//2)-12,text)
    print_centered(w,h,"Press 'm' to jump back to menu","bottom")
    stdscr.refresh()
    return navigation_key_press()

def endscreen(score,w,h):
    stdscr.clear()
    text = text2art("Game Over","small")
    print_multiple_lines((h//2)-3,(w//2)-20,text)

    print_centered(w,h,f"Your score was {score}","mid")
    print_centered(w,h,"Press 'm' to jump back to menu","bottom")
    print_centered(w,h+2,"To replay press 'r'","mid")

    return navigation_key_press(True)

def print_centered(w,h,text,pos="mid"):
    if pos == "mid":
        stdscr.addstr(h//2,w//2 - len(text)//2,text)
    elif pos == "bottom":
        stdscr.addstr(h-2,w//2 - len(text)//2,text)
    elif pos =="top":
        stdscr.addstr(h,w//2 - len(text)//2,text,curses.A_BOLD)

def navigation_key_press(endscreen=False):
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
        elif endscreen and end_key == ord("r"):
            game = "r"
            break
    return game

def name_screen(w,h):
    print_centered(w,2,"Enter NAME: (hit ENTER to send)","top")
    print_centered(w,h,"To play the game use your arrow keys:","mid")
    print_centered(w,h+2,"<- left | right ->","mid")

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
        resize_h,resize_w = stdscr.getmaxyx()
        check_for_resize()
        stdscr.clear()

        top = text2art("Bird jump","small")
        bottom = text2art("extreme","small")

        print_multiple_lines(10,(resize_w//2)-20,top)
        print_multiple_lines(15,(resize_w//2)-15,bottom)
        stdscr.refresh()

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
            character = choose_character(resize_w,resize_h)

        #PLAY Button
        elif key == 10 and current_row == 0:
            stdscr.clear()
            name = name_screen(resize_w, resize_h)
            while True:
                score = play(resize_w, resize_h, character, name)
                game = endscreen(score,resize_w, resize_h)
                if game == "r":
                    continue
                else:
                    break

        #Scoreboard Button
        elif key == 10 and current_row == 2:
            scoreboard = pickle.load(open("score_board.pickle","rb"))
            game = scoreboard_screen(scoreboard,resize_w, resize_h)

curses.wrapper(main)

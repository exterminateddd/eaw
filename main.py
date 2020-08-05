from tkinter import *
from random import *
from time import *


root = Tk()
root.title('hello world!')
root.configure(background="black")
root.geometry('500x500')
root.resizable(False, False)

eaten_enemies = 0
speed = 10
enemy_respawns = 0

is_dead = False


enemy = Button(root)
enemy.configure(background="yellow")

square = Button(root)
square.configure(background="red")


def move_enemy(direction):
    try:
        dir_ = direction
        if dir_ == 'DOWN':
            if 400 > int(enemy.place_info()['y']) > 40:
                enemy.place(y=int(enemy.place_info()['y'])+randint(-8, 0), x=int(enemy.place_info()['x']) + randint(-4, 4))
            else:
                dir_ = 'UP'
        if dir_ == 'UP':
            if 400 > int(enemy.place_info()['y']) > 40:
                enemy.place(y=int(enemy.place_info()['y']) - randint(0, 8), x=int(enemy.place_info()['x']) + randint(-4, 4))
            else:
                enemy.place(y=int(enemy.place_info()['y'])+randint(-8, 0), x=int(enemy.place_info()['x']) + randint(-4, 4))

        if dir_ == 'RIGHT':
            if 400 > int(enemy.place_info()['x']) > 40:
                enemy.place(y=int(enemy.place_info()['y']) + randint(-4, 4), x=int(enemy.place_info()['x']) + randint(0, 8))
            else:
                dir_ = 'LEFT'
        if dir_ == 'LEFT':
            if 400 > int(enemy.place_info()['x']) > 40:
                enemy.place(y=int(enemy.place_info()['y']) + randint(-4, 4), x=int(enemy.place_info()['x']) + randint(0, 8))
            else:
                enemy.place(y=int(enemy.place_info()['y']) + randint(-4, 4), x=int(enemy.place_info()['x']) + randint(-8, 0))
    except TclError:
        pass


alert = Label(root)
alert.configure(text='Enemies eaten: '+str(eaten_enemies))
alert.pack(anchor='nw')

speed_alert = Label(root)
speed_alert.configure(text='Speed: '+str(speed)+'px / move')
speed_alert.place(x=390, y=0)

game_over = Label(root)
game_over.configure(foreground="red", font="Arial 48")


def spawn_enemy():
    enemy.place_forget()
    enemy.place(width=randint(12, 20), height=randint(12, 20), x=randint(30, 400), y=randint(40, 400))


def spawn_square():
    if choice(range(0, 3)) == 1:
        square.place(x=randint(40, 100), y=randint(40, 100), width=randint(100, 144), height=randint(96, 141))
    else:
        square.place(x=randint(250, 400), y=randint(250, 400), width=randint(100, 144), height=randint(96, 141))


def check_if_eaten(player_info, enemy_info):
    p_x = int(player_info['x'])
    p_y = int(player_info['y'])

    p_w = int(player_info['width'])
    p_h = int(player_info['height'])

    e_x = int(enemy_info['x'])
    e_y = int(enemy_info['y'])

    e_w = int(enemy_info['width'])
    e_h = int(enemy_info['height'])

    if p_y < e_y < p_y+p_h:
        if p_x+p_w > e_x > p_x:
            global eaten_enemies, speed, enemy_respawns
            eaten_enemies += 1
            if not eaten_enemies % 2:
                enemy_respawns += 1
            if speed < 30:
                speed += 1
            alert.pack_forget()
            alert.configure(text='Enemies eaten: '+str(eaten_enemies))
            alert.pack(anchor='nw')
            speed_alert.place_forget()
            speed_alert.configure(text='Speed: '+str(speed)+'px / move')
            speed_alert.place(x=390, y=0)
            enemy.place_forget()
            spawn_enemy()
            if enemy_respawns > 0:
                respawn_enemy.configure(text=f'Respawn Enemy (left {enemy_respawns})', command=lambda: spawn_enemy())
            else:
                respawn_enemy.configure(text=f'Respawn Enemy (left {enemy_respawns})')
            respawn_enemy.pack(side="bottom", anchor="w")


def check_if_killed_by_square(player_info, square_info):
    p_x = int(player_info['x'])
    p_y = int(player_info['y'])

    p_w = int(player_info['width'])
    p_h = int(player_info['height'])

    s_x = int(square_info['x'])
    s_y = int(square_info['y'])

    s_w = int(square_info['width'])
    s_h = int(square_info['height'])

    if s_y < p_y < s_y+s_h:
        if s_x+s_w > p_x > s_x:
            global eaten_enemies, speed, is_dead
            eaten_enemies = 0
            speed = 10
            game_over.place(width=320, height=60, x=90, y=200)
            game_over.configure(text='Game Over!')
            is_dead = True
            enemy.destroy()


WIDTH = 70
HEIGHT = 26


player = Button(root)
player.configure(background='gray', text='ZZZZ><><ZZZZ')
player.place(width=WIDTH, height=HEIGHT, x=220, y=220)


def move_up():
    if not is_dead:
        if int(player.place_info()['y']) > 40:
            if int(player.place_info()['width']) == WIDTH:
                player.place(x=int(player.place_info()['x'])-WIDTH//4)
                player.place(y=int(player.place_info()['y'])-WIDTH//1.75)
            player.place(width=HEIGHT, height=WIDTH)
            player.place(y=(int(player.place_info()['y'])) - speed)
            try:
                check_if_eaten(player.place_info(), enemy.place_info())
                check_if_killed_by_square(player.place_info(), square.place_info())
            except TclError:
                pass
            move_enemy('UP')


def move_down():
    if not is_dead:
        if int(player.place_info()['y']) < 400:
            if int(player.place_info()['width']) == WIDTH:
                player.place(x=int(player.place_info()['x'])+WIDTH//1.75)
            player.place(width=HEIGHT, height=WIDTH)
            player.place(y=(int(player.place_info()['y'])) + speed)
            try:
                check_if_eaten(player.place_info(), enemy.place_info())
                check_if_killed_by_square(player.place_info(), square.place_info())
            except TclError:
                pass
            move_enemy('DOWN')


def move_left():
    if not is_dead:
        if 20 < int(player.place_info()['x']):
            if int(player.place_info()['width']) == HEIGHT:
                player.place(y=int(player.place_info()['y'])+WIDTH//1.75)
            player.place(width=WIDTH, height=HEIGHT)
            player.place(x=(int(player.place_info()['x'])) - speed)
            try:
                check_if_eaten(player.place_info(), enemy.place_info())
                check_if_killed_by_square(player.place_info(), square.place_info())
            except TclError:
                pass
            move_enemy('LEFT')


def move_right():
    if not is_dead:
        if int(player.place_info()['x']) < 400:
            if int(player.place_info()['width']) == HEIGHT:
                player.place(y=int(player.place_info()['y'])+WIDTH//1.75)
            player.place(width=WIDTH, height=HEIGHT)
            player.place(x=(int(player.place_info()['x'])) + speed)
            try:
                check_if_eaten(player.place_info(), enemy.place_info())
                check_if_killed_by_square(player.place_info(), square.place_info())
            except TclError:
                pass
            move_enemy('RIGHT')


ctrl_up = Button(root, text='Up', command=move_up)
ctrl_down = Button(root, text='Down', command=move_down)
ctrl_left = Button(root, text='Left', command=move_left)
ctrl_right = Button(root, text='Right', command=move_right)


# ctrl_up.place(x=424, y=420, width=40)
# ctrl_down.place(x=424, y=478, width=40)
# ctrl_left.place(x=400, y=448, width=40)
# ctrl_right.place(x=444, y=448, width=40)

respawn_enemy = Button(root)
if enemy_respawns > 0:
    respawn_enemy.configure(text=f'Respawn Enemy (left {enemy_respawns})', command=lambda: spawn_enemy())
else:
    respawn_enemy.configure(text=f'Respawn Enemy (left {enemy_respawns})')
respawn_enemy.pack(side="bottom", anchor="w")


spawn_enemy()
spawn_square()

root.bind('<Left>', lambda x: move_left())
root.bind('<Right>', lambda x: move_right())
root.bind('<Up>', lambda x: move_up())
root.bind('<Down>', lambda x: move_down())

root.bind('<w>', lambda x: move_left())
root.bind('<a>', lambda x: move_right())
root.bind('<s>', lambda x: move_up())
root.bind('<d>', lambda x: move_down())

root.mainloop()

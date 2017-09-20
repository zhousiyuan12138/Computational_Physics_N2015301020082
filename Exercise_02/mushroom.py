import time
import os

# You can creat pixel art and get the pixel codes at
# https://jsfiddle.net/shinoring/nmygxhsy/
mushroom_1=('000000dddd00000000000dddddd000000000dddddddd0000000'
'dddddddddd00000d33dddddd33d000ddde3dddd3eddd00ddde333333eddd0dddd'
'e3edde3eddddddddeeeddeeedddddddddddddddddddd0ddddeeeeeedddd00000'
'eeeeeeee00000033eeeeeeee0000033333eeeee330000333333eee3330000033333ee3330000')

mushroom_2=('000000dddd00000000000dddddd000000000dddddddd0000000'
'dddddddddd00000d33dddddd33d000ddde3dddd3eddd00ddde333333eddd0dddd'
'e3edde3eddddddddeeeddeeedddddddddddddddddddd0ddddeeeeeedddd00000'
'eeeeeeee00000000eeeeeeee330000033eeeee333330000333eee33333300000333ee3333300')

color_dic={
'0':"\033[0m  ", # blank
'd':'\033[48;5;130m  ', # brown
'e':'\033[48;5;216m  ', # face
'3':'\033[48;5;0m  ', # black
}

# make the mushroom to step right
def move_right(frame):
    for i in range(0, 16):
        # insert 4 blank space in the beginning of every row
        frame = frame[:(16+4)*i] + "0"*4 + frame[(16+4)*i:]
    return(frame)

# animate frames
def action(frame,col = 16):
    i = 0
    # look up colors by the color codes in each frame and print color blocks.
    for pixel in frame:
        print(color_dic[pixel], end = "")
        i += 1
        # set the color to blank and move to the next row.
        if i % col == 0:
            print('\033[0m')
    time.sleep(0.5) # pause 0.5s between every two frames.
    os.system('clear') # clear the screen to show the next frame.

os.system('clear') # Clear screen before movie start

while True:
    action(mushroom_1)
    action(move_right(mushroom_2), col = 20)

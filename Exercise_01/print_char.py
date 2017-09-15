# This is a program for printing fullwidth characters in a 16x16 lattice.
# It took me quite a long time.
# And I'd like to express my special thanks to
# (@slipperstree)[https://github.com/slipperstree/raspled], without whose
# shared code for referrence, I wouldn't be able to get it through.
#
# Please use this with the HZK16.dat file.

import numpy

yourname = input("Please enter your name: ")

char_list = []
for i in yourname:
	char_list.append(i)

# importing HZK16 in binary mode
char_library = []
char_library = numpy.fromfile('HZK16.dat', dtype='b')

# Get the codes for character
def get_code(char):

    gbcode = char.encode('gb2312') #获取汉字国标码

    try:
        blocode = gbcode[0] - 160 # 获取汉字区码
        poscode = gbcode[1] - 160 # 获取汉字位码
    except:
        print('请输入全角字符！')
        exit()

    # get the offset value of character in HZK16
    offset = (94 * (blocode - 1) + (poscode - 1)) * 32

    # get pixel values for the character lattice in HZK16
    pixel_codes = []
    for i in range(offset, offset + 32):
        byte = char_library[i]
        pixel_codes.append(byte)
    return pixel_codes

# decides which pixel to draw black and which not, according
# to the pixel_codes given by get_code()
def disp_char(pixel_codes):
    for i in range(0, 32):
        # the 8-digit binary value for 8 pixels, e.g. 10100010
	# two values produce a line,
	# and a character is composed of 16 lines.
        pixel_8_unit = pixel_codes[i]
        for j in range(0, 8):
            if (pixel_8_unit & 0x80):
                print(style * 2, end = "")
            else:
                print("  ", end = "")
            pixel_8_unit <<= 1
        if (i % 2):
            print(newline)
    return

# arguments available for the program
import getopt
import sys
options, remainder = getopt.getopt(sys.argv[1:], 's:o:', ['os=', 'style='])

style = '@' # set default display style and newline style
os_newlines = {'win':'\r\n', 'mac':'\r', 'linux':'\n'}
newline = os_newlines['win']

for opt, arg in options:
    if opt in ('-s', '--style'):
        style = arg # choose the display style of characters
    elif opt in ('-o', '--os'):
        os = arg # choose the operating system
        newline = os_newlines[os]

# display characters on screen
for char in char_list:
    disp_char(get_code(char))
    print(newline)

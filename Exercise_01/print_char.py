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

    try:
        gbcode = char.encode('gb2312') #获取汉字国标码
        blocode = gbcode[0] - 160 # 获取汉字区码
        poscode = gbcode[1] - 160 # 获取汉字位码
    except:
        print('请输入全角国标字符！')
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
                print(symbol * 2, end = "")
            else:
                print("  ", end = "")
            pixel_8_unit <<= 1
        if (i % 2):
            print(newline)
    return

# pixel_lines is for storing 16 lines of pixel codes
pixel_lines = [[],[],[],[],[],[],[],[],[],[],[],[],[],[],[],[]]
# Please refer to the fuction 'disp_char' for what 'get_char_hori' does.
# They are different mainly in that 'get_char_hori' stores the pixel information
# for future printing, while 'disp_char' prints directly
def get_char_hori(pixel_codes):
    for i in range(0, 32):
        pixel_8_unit = pixel_codes[i]
        for j in range(0, 8):
            if (pixel_8_unit & 0x80):
                pixel_lines[i//2].append(symbol * 2)
            else:
                pixel_lines[i//2].append("  ")
            pixel_8_unit <<= 1
        if (i % 2):
            # make space at the end of every line for each character.
            pixel_lines[i//2].append("  ")
    return

# print charcters from the value of pixel_lines
def disp_char_hori(hori_lines):
    for line in hori_lines:
        for bit in line:
            print(bit, end = "")
        print(newline)
    return

# arguments available for the program
import getopt
import sys
options, remainder = getopt.getopt(sys.argv[1:], 's:o:h', ['os=', 'symbol=', 'horizontal'])

symbol = '@' # set default display style and newline style
os_newlines = {'win':'\r\n', 'mac':'\r', 'linux':'\n'}
newline = os_newlines['mac']
style = 'vertical'

for opt, arg in options:
    if opt in ('-s', '--symbol'):
        symbol = arg # choose the symbol to form the lattice
    elif opt in ('-o', '--os'):
        os = arg # choose the operating system
        newline = os_newlines[os]
    elif opt in ('-h', '--horizontal'):
        style = 'horizontal'

# display characters on screen
if style == 'vertical':
    for char in char_list:
        disp_char(get_code(char))
        print(newline) # make spaces between each character
else:
    for char in char_list:
        get_char_hori(get_code(char))
    # unindent to print only once
    disp_char_hori(pixel_lines)

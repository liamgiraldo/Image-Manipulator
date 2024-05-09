import os
import a5helper
import a5image
import a5pixel

"""
This file is the app for image editing.

Author:  msf257 lag288
Date: 07/28/22
"""
print('Before you run! All images must be in the same directory as this script. Thank you!')


#ask geisler if this is okay. This SINGLE line might be plagarism
#Got the ok, the source for this is: https://stackoverflow.com/questions/3207219/how-do-i-list-all-files-of-a-directory
folder_contents = os.listdir()
folder_bmp = []
for i in folder_contents:
    if ".bmp" in i:
        folder_bmp.append(i)

a5image_functions = ['add_pixel','red_shift','shift_brightness','make_monochrome','mirror_horizontal',
'mirror_vertical','add_noise','blur']

image_to_edit = str(input('What image would you like to edit? Type ls to view options: '))
while image_to_edit == 'ls':
    for i in folder_bmp:
        print(f'{i}\n')
    image_to_edit = str(input('What image would you like to edit? Type ls to view options: '))
while ".bmp" not in image_to_edit and image_to_edit != "ls":
    image_to_edit = str(input('Your file must contain .bmp !\nWhat image would you like to edit? Type ls to view options: '))

image_edited = a5helper.read_image(image_to_edit)
print(f'\nYour image selected is {image_to_edit}\n')
print(image_edited)

modifier = input('Select the number cooresponding to the modifier you wish to use.\nType ls to see options.')
while modifier == 'ls':
    for i in range(len(a5image_functions)):
        print(f'{i} {a5image_functions[i]}\n')
    modifier = str(input('Select the number cooresponding to the modifier you wish to use.\nType ls to see options.'))
while modifier not in ('0','1','2','3','4','5','6','7','8'):
    modifier = str(input('Invalid input! Select the number cooresponding to the modifier you wish to use.\nType ls to see options.'))

print(f'\nYour modifier selected is {modifier}\n')

#create another pixel if it is needed, modify accordingly
new_pixel = a5pixel.Pixel(0,0,0,255)
def clamp(x:int)->int:
    if x > 255:
        return 255
        print('An input was over 255. Clamping to 255')
    if x < 0:
        return 0
        print('An input was below 0. Clamping to 0')
    return x
def clampall(y : a5image.Image):
    for i in range(len(y._data)):
        for j in range(len(y._data[i])):
            clamp(y._data[i][j].r)
            clamp(y._data[i][j].g)
            clamp(y._data[i][j].b)
            clamp(y._data[i][j].a)
    return y

if modifier == '0':
    print(f'In order to use this modifier you must create your own pixel.')
    print(f'Input the red, green, blue values for your new pixel.')
    new_pixel.r = clamp(int(input('Input a Red from 0 to 255')))
    new_pixel.g = clamp(int(input('Input a Green from 0 to 255')))
    new_pixel.b = clamp(int(input('Input a Blue from 0 to 255')))
    new_pixel.a = clamp(int(input('Input an Alpha from 0 to 255')))
    image_edited.add_pixel(new_pixel)
    image_edited = clampall(image_edited)
    file_to_write = str(input('Input a file name to write to. Must contain .bmp '))
    a5helper.write_image(file_to_write,image_edited)
    print('Write successful. Program terminated.')
if modifier == '1':
    red_to_add = clamp(int(input('Input amount of red from 0 to 255. ')))
    image_edited.red_shift(red_to_add)
    image_edited = clampall(image_edited)
    file_to_write = str(input('Input a file name to write to. Must contain .bmp '))
    a5helper.write_image(file_to_write,image_edited)
    print('Write successful. Program terminated.')
if modifier == '2':
    brightness_shift = clamp(float(input('Input amount of brightness to increase by.')))
    image_edited.shift_brightness(brightness_shift)
    image_edited = clampall(image_edited)
    file_to_write = str(input('Input a file name to write to. Must contain .bmp '))
    a5helper.write_image(file_to_write,image_edited)
    print('Write successful. Program terminated.')
if modifier == '3':
    image_edited.make_monochrome()
    image_edited = clampall(image_edited)
    file_to_write = str(input('Input a file name to write to. Must contain .bmp '))
    a5helper.write_image(file_to_write,image_edited)
    print('Write successful. Program terminated.')
if modifier == '4':
    image_edited.mirror_horizontal()
    #not really a need to clamp but whatever
    image_edited = clampall(image_edited)
    file_to_write = str(input('Input a file name to write to. Must contain .bmp '))
    a5helper.write_image(file_to_write,image_edited)
    print('Write successful. Program terminated.')
if modifier == '5':
    image_edited.mirror_vertical()
    image_edited = clampall(image_edited)
    file_to_write = str(input('Input a file name to write to. Must contain .bmp '))
    a5helper.write_image(file_to_write,image_edited)
    print('Write successful. Program terminated.')
if modifier == '6':
    noise_amount = int(input(f'Input a range of noise. Goes from -input to input. '))
    image_edited.add_noise(noise_amount)
    image_edited = clampall(image_edited)
    file_to_write = str(input('Input a file name to write to. Must contain .bmp '))
    a5helper.write_image(file_to_write,image_edited)
    print('Write successful. Program terminated.')
if modifier == '7':
    image_edited.blur()
    image_edited = clampall(image_edited)
    file_to_write = str(input('Input a file name to write to. Must contain .bmp '))
    a5helper.write_image(file_to_write,image_edited)
    print('Write successful. Program terminated.')
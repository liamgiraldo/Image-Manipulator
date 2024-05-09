import a5pixel
import a5image

pix1 = a5pixel.Pixel(256,-1,5,6)
pix2 = a5pixel.Pixel(1,2,3,4)
pix3 = a5pixel.Pixel(2,3,4,5)
pix4 = a5pixel.Pixel(3,4,5,6)
pix5 = a5pixel.Pixel(4,5,6,7)
pix6 = a5pixel.Pixel(5,6,7,8)
pix7 = a5pixel.Pixel(6,7,8,9)
pix8 = a5pixel.Pixel(7,8,9,10)
pixlist1 = [pix1,pix2,pix3,pix4]
pixlist2 = [pix4,pix5,pix6,pix7]
grid = [pixlist1,pixlist2]

img1 = a5image.Image(grid,[5,5])
print(repr(img1))
print('after')
a5image.Image.mirror_vertical(img1)
print(repr(img1))
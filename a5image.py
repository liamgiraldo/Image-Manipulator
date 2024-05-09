# A funky import, but this allows us to 
#  type-annotate class methods properly
from __future__ import annotations
import random

from a5pixel import Pixel

"""
This file defines the Image class

Author:  msf257 lag288
Date: 07/28/22
"""

from typing import List
import a5pixel
import copy

def clamp(x : int) -> int:
  '''
  Ensures that a number is between 0 and 255
  This is easy to read code.
  '''
  if x > 255:
    return 255
  elif x < 0:
    return 0
  return x
class Image:
    """
    An Image object represents a complete image
    
    Specifically, an Image contains a rectangular matrix of pixels
      a resolution (with a width and height)
      along with a variety of methods for manipulating that matrix

    Attributes:
      _data : List[List[Pixel]]
        every row in _data must be the same length
        (note that the undescore '_' in front of data indicates 
          a "private" variable in Python.  While methods outside
          of this class can access / manipulate such a variable,
          this is stylistically discouraged)
      _resolution : List[int]
        the length of _resolution must be 2 ([width, height])
    """

    def __init__(self, image : List[List[a5pixel.Pixel]], resolution : List[int]):
        """
        Initializes this Image with the given matrix of Pixels
          and resolution (the latter is necessary for BMP metedata)

        Preconditions: image is a list of list of Pixels
          each row of the image must be of the same length
          neither the image nor any row may be of length 0

        resolution is a list of exactly two integers
        """
        assert type(image) == list
        assert type(resolution) == list
        assert len(resolution)==2
        for i in resolution:
          assert type(i) == int

        assert len(image) > 0
        for i in range(len(image)):
          assert type(image[i]) == list
          assert len(image[i]) > 0
          assert len(image[i]) == len(image[0])
          for j in range(len(image[i])):
            assert type(image[i][j]) == Pixel

        self._data = image
        self._resolution = resolution

    
    def __str__(self) -> str:
        """
        Returns a string representation of the dimensions 
          of the pixels matrix forming this Image
          

        Example:
          str(Image([[Pixel(1, 2, 3, 4)], [Pixel(4, 3, 2, 1)]], [1, 1]))
            -> "2x1 Image"
        """
        return f'{len(self._data)}x{len(self._data[0])} Image'



    def __repr__(self) -> str:
        """
        Returns the debugging representation of this Image
          (Hint: don't overthink this method, it should be simple)

        Example:
          repr(Image([[Pixel(1, 2, 3, 4)], [Pixel(4, 3, 2, 1)]], [2, 3]))
            -> "Image([[Pixel(1, 2, 3, 4)], [Pixel(4, 3, 2, 1)]], [2, 3])"
        """
        return f'Image({self._data}, {self._resolution})'
        

    def add_pixel(self, add_pixel : a5pixel.Pixel):
        """
        Adds the given Pixel amount to each Pixel in this Image 

        Precondition: pixel_shift is a Pixel
        """
        assert type(add_pixel)==a5pixel.Pixel
        for i in range(len(self._data)):
          for j in range(len(self._data[i])):
            #clamp is in a5pixel
            self._data[i][j] = self._data[i][j] + add_pixel
            

        
    def red_shift(self, amount : int):
        """
        Adds 'amount' to the red component of each Pixel in this Image

        Preconditions: amount is an int and is >= 0
        """
        assert type(amount) == int
        assert amount >= 0
        for i in range(len(self._data)):
          for j in range(len(self._data[i])):
            self._data[i][j].r = clamp(self._data[i][j].r + amount)

    
    def shift_brightness(self, amount : float):
        """
        Modified this image by shifting the brightness
          of each Pixel in this Image by the given amount

        If amount is greater than 1, the image is brightened
          while if the amount is between 0 and 1, the image is darkened

        Preconditions: amount is a float >= 0 
        """
        assert type(amount)==float
        assert amount >=0
        for i in range(len(self._data)):
          for j in range(len(self._data[0])):
            self._data[i][j]*=amount
              
            

    
    def make_monochrome(self):
        """
        Shifts the pixels in this Image to Monochrome
          
        This is done by averaging the non-alpha values in each Pixel

        For more details, see Pixel.monochrome
        """
        for i in range(len(self._data)):
          for j in range(len(self._data[i])):
            self._data[i][j] = self._data[i][j].monochrome()
        


    def mirror_horizontal(self):
        """
        Modifies this Image by mirroring it over the x-axis
        """
        self._data.reverse()

    
    def mirror_vertical(self):
        """
        Modifies this Image by mirroring it over the y-axis
        """
        for i in  range (len(self._data)):
          self._data[i].reverse()



    def add_noise(self, amount : int):
        """
        Modifies this Image by adding a random amount of "noise"
          to each Pixel of this Image

        Specifically, each Pixel in this image will have its
          red-green-blue components _separately_ increased
          by an amount randomly selected in the range [-amount, amount]
          Note that this amount is inclusive on both negative and positive
          Also note that each Pixel is modified independently
          Finally, the alpha value of each Pixel should be unmodified

        Hint: random.randint is very helpful for this method

        Preconditions: amount is an integer >= 0
        """
        assert type(amount) == int
        assert amount >= 0
        for i in range(len(self._data)):
          for j in range(len(self._data[i])):
            #unsure if I need to actually clamp them.
            self._data[i][j].r = clamp(self._data[i][j].r + random.randint(amount*-1,amount))
            self._data[i][j].g = clamp(self._data[i][j].g + random.randint(amount*-1,amount))
            self._data[i][j].b = clamp(self._data[i][j].b + random.randint(amount*-1,amount))

    def blur(self):
        """
        Modifies this Image by blurring each Pixel in the Image

        To blur a Pixel, average the red-green-blue components of 
          this Pixel and every adjacent Pixel

        Note that adjacency for blurring includes Pixels "diagonally" adjacent

        If the average value of a Pixel is not an integer, it should be rounded down

        Hint: consider building a new matrix of Pixels to avoid
          modifying the results of future Pixels when calculating a given Pixel

        Hint: be careful of "edge" cases (hehehe)

        Hint: this method is a bit of a pain
          -- consider doing the rest of the assignment first if you're struggling
        """
        #ill post errors here:
        '''
		Testing Image Blurring
assert_equals: expected [[Pixel(2, 5, 7, 0), Pixel(2, 5, 7, 0)], [Pixel(2, 5, 7, 0), Pixel(2, 5, 7, 0)]] 
but instead got [[Pixel(2, 5, 8, 0), Pixel(2, 5, 8, 0)], [Pixel(2, 5, 8, 0), Pixel(2, 5, 8, 0)]]
Line 196 of <ipython-input-1-7bb5f767c794>: testcase.assert_equals(expected._data, received._data)
Quitting with Error
        '''
        def returnEdge(x,y):
          temp=[]
          for i in range(-1,1):
            for j in range(-1,1):
              if not i>len(self._data)-1 and not i<0:
                if not j>len(self._data[0])-1 and not j<0:
                  temp.append(x+i)
                  temp.append(y+j)
          return temp
                                     
        temp=copy.deepcopy(self._data)
        if len(temp)!=1 and len(temp[0])!=1:
          for i in range(len(self._data)):
            for j in range(len(self._data[0])):
              pixel = a5pixel.Pixel(0,0,0,0)
              edges=returnEdge(i,j)
              for x in range(0,len(edges)-1,2):
                pixel = pixel +temp[x][x+1]
              avgr=pixel.r/(len(edges)/2)
              avgg=pixel.g/(len(edges)/2)
              avgb=pixel.b/(len(edges)/2)
              self._data[i][j]=a5pixel.Pixel(int(avgr),int(avgg),int(avgb),self._data[0][0].a)
'''
        def returnEdge(x, y):
          temparr = []
          for i in [-1, 0, 1]:
            for j in [-1, 0, 1]:
              if x+i<=len(self._data)-1 and x+i>=0:
                if y+j<=len(self._data[0])-1 and  y+j>=0:
                  temp.append(x+i)
                  temp.append(y+j)
          return temparr

        temp = copy.deepcopy(self._data)
        if len(temp) != 1 and len(temp[0])!=1:
          for i in range(len(self._data)):
            for j in range(len(self._data[0])):
              pixel = a5pixel.Pixel(0,0,0,0)
              edges = returnEdge(i, j)
              for x in range(0,len(edges)-1, 2):
                pixel = pixel + temp[edges[x]][edges[x+1]]
              avgr = pixel.r/(len(edges)/2)
              avgg = pixel.g/(len(edges)/2)
              avgb = pixel.b/(len(edges)/2)
              self._data[i][j] = a5pixel.Pixel(int(avgr), int(avgg), int(avgb), self._data[0][0].a)
              '''

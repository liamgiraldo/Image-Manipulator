# A funky import, but this allows us to type-annotate
#  class methods properly
from __future__ import annotations

"""
This file defines the Pixel class

Author:  msf257 lag288
Date: 07/28/22
"""

class Pixel:
    """
    A Pixel object represents a single pixel on screen
      per the bitmap standard, a pixel has four attributes
      r represents the red value of the pixel (higher is more red)
      g represents the green value of the pixel
      b represents the blue value of the pixel
      a represents the opacity of the pixel (higher means more opaque)

    Attributes:
      r [0 <= int <= 255]
      g [0 <= int <= 255]
      b [0 <= int <= 255]
      a [0 <= int <= 255]
    """

    def __init__(self, red : int, green : int, blue : int, alpha : int):
        """
        Instantiates a Pixel with the given attributes
        Note that if any attribute is outside the allowed range
          this initialization should _clamp_ it within the valid range

        Examples:
          if any value is negative, set the attribute to 0
          if red is above 255, set it to 255

        Preconditions: all non-self inputs are integers
        """
        assert type(red) == int
        assert type(green) == int
        assert type(blue) == int
        assert type(alpha) == int
        def set_proper(rgbval : int) -> int:
          if(rgbval > 255):
            return 255
          if(rgbval < 0):
            return 0
          return rgbval
        self.r = set_proper(red)
        self.g = set_proper(green)
        self.b = set_proper(blue)
        self.a = set_proper(alpha)

    
    def __str__(self) -> str:
        """
        Returns a string representation of this Pixel

        Example:
          str(Pixel(1, 2, 3, 4)) -> "(1, 2, 3, 4)"
        """
        return f'({self.r}, {self.g}, {self.b}, {self.a})'
        pass # PLACEHOLDER

    
    def __repr__(self) -> str:
        """
        Returns a debugging representation of this Pixel

        Example:
          repr(Pixel(1, 2, 3, 4)) -> "Pixel(1, 2, 3, 4)"
        """
        return f'Pixel{str(self)}'

    
    def __eq__(self, other : Pixel) -> bool:
        """
        Returns whether this and another pixel are the same color
          Note that this only occurs when all components are the same

        Precondition: other is a Pixel
        """
        assert type(other) == Pixel
        # l1 = [self.red,self.green,self.blue,self.alpha]
        # l2 = [other.red,other.green,other.blue,other.alpha]
        # for i in range(4):
        #   if l1[i] != l2[i]:
        #     return False
        # return True

        return self.r ==other.r and self.b ==other.b and other.g == self.g and self.a == other.a


    def __add__(self, other : Pixel) -> Pixel:
        """
        Returns the Pixel resulting from adding this Pixel to another
          Note that the resulting pixel will be clamped

        Example:
          Pixel(0, 255, 0, 20) + Pixel(255, 255, 0, 20)
            -> Pixel(255, 255, 0, 40)

        Precondition: other is a Pixel
        """
        assert type(other) == Pixel
        def clamp(val : int) -> int:
          if val > 255:
            return 255
          if val < 0:
            return 0
          return val
        return Pixel(clamp(self.r+other.r),clamp(self.g+other.g),
        clamp(self.b+other.b),clamp(self.a+other.a))



    def __mul__(self, other : float) -> Pixel:
        """
        Returns the Pixel resulting from multiplying each of
          this Pixel's non-alpha components by the amount 'other'
          when a non-integer value is produced, the result is rounded down

        Example:
          Pixel(10, 200, 0, 100) * 2.01
            -> Pixel(20, 255, 0, 100)

        Precondition: other is a int or float
        """
        assert type(other) in (int, float)
        def multalpha(val : int, mult : float) -> int:
          return int(mult * val)
        return Pixel(multalpha(self.r,other),multalpha(self.g,other),
        multalpha(self.b,other),self.a)


    def monochrome(self) -> Pixel:
        """
        Returns this pixel made black-and-white
          Note that this pixel should remained unchanged

        There are many ways to do this.  For simplicity,
          we will simply average the rgb intensity of this pixel
          if the average is not exact, round down
          note that alpha should not be changed

        Examples:
          Pixel(10, 10, 10, 255).monochrome() -> Pixel(10, 10, 10, 255)
          Pixel(0, 5, 12, 20).monochrome() -> Pixel(5, 5, 5, 20)
        """
        avg = int(((self.r+self.b+self.g)/3))
        return Pixel(avg,avg,avg,self.a)
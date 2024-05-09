"""
Testcases for a5image and a5pixel

To run these tests, simply run `python a5test.py`

If you add more tests, be sure to include your netids 
  in the author list and submit the updated test file

Author: dag368
Date: 7/22/2022
"""

# Comment this out if you want to test quickly
#   since writing images is slow
WRITE_IMAGES = True

import testcase
import a5helper
import a5image
import a5pixel

def test_pixel_init():
    print("\t\t" + "Testing Pixel initialization")
    # Basics
    p = a5pixel.Pixel(10, 20, 30, 5)
    testcase.assert_equals(10, p.r)
    testcase.assert_equals(20, p.g)
    testcase.assert_equals(30, p.b)
    testcase.assert_equals(5, p.a)

    # Clamping
    p = a5pixel.Pixel(-5, 300, 100, 256)
    testcase.assert_equals(0, p.r)
    testcase.assert_equals(255, p.g)
    testcase.assert_equals(100, p.b)
    testcase.assert_equals(255, p.a)

    # Precondition Testing
    testcase.assert_error(a5pixel.Pixel, "invalid", 0, 0, 0)
    testcase.assert_error(a5pixel.Pixel, 0, 5.5, 0, 0)
    testcase.assert_error(a5pixel.Pixel, 0, 0, [1, 2], 0)
    testcase.assert_error(a5pixel.Pixel, 0, 0, 0, False)

def test_pixel_reprs():
    print("\t\t" + "Testing Pixel representations")
    p1 = a5pixel.Pixel(3, 5, 7, 9)
    p2 = a5pixel.Pixel(100, 200, 300, 400)

    print("\t\t\t" + "pixel str")
    # __str__
    testcase.assert_equals("(3, 5, 7, 9)", str(p1))
    testcase.assert_equals("(100, 200, 255, 255)", str(p2))

    print("\t\t\t" + "pixel repr")
    # __repr__
    testcase.assert_equals("Pixel(3, 5, 7, 9)", repr(p1))
    testcase.assert_equals("Pixel(100, 200, 255, 255)", repr(p2))

def test_pixel_binary():
    print("\t\t" + "Testing Pixel binary operations")
    p0 = a5pixel.Pixel(0, 0, 0, 0)
    p1 = a5pixel.Pixel(10, 10, 10, 10)
    p2 = a5pixel.Pixel(300, 0, 100, 30)

    print("\t\t\t" + "pixel eq")
    # Equality
    # Note that assert_equals actually invokes '=='
    testcase.assert_equals(p0, p0) # Trivial, just to make sure
    testcase.assert_equals(a5pixel.Pixel(0, 0, 0, 0), p0)
    testcase.assert_equals(a5pixel.Pixel(10, 10, 10, 10), p1)
    # Also testing clamping
    testcase.assert_equals(a5pixel.Pixel(255, 0, 100, 30), p2)

    print("\t\t\t" + "pixel add")
    # Addition
    # Since we already tested equality, we can use it!
    testcase.assert_equals(a5pixel.Pixel(0, 0, 0, 0), p0 + p0)
    # Zero addition
    testcase.assert_equals(a5pixel.Pixel(10, 10, 10, 10), p0 + p1)
    # Testing commutativity
    testcase.assert_equals(a5pixel.Pixel(10, 10, 10, 10), p1 + p0)
    testcase.assert_equals(a5pixel.Pixel(20, 20, 20, 20), p1 + p1)
    # Clamping, once again
    testcase.assert_equals(a5pixel.Pixel(255, 10, 110, 40), p1 + p2)
    # Commutativity
    testcase.assert_equals(a5pixel.Pixel(255, 10, 110, 40), p2 + p1)
    # Chaining
    testcase.assert_equals(a5pixel.Pixel(30, 30, 30, 30), p1 + p1 + p1)
    testcase.assert_equals(a5pixel.Pixel(255, 20, 220, 80), (p1 + p2) + (p2 + p1))

    print("\t\t\t" + "pixel mul")
    # Multiplication
    # Multiply with/by 0
    testcase.assert_equals(a5pixel.Pixel(0, 0, 0, 0), p0 * 2.0)
    testcase.assert_equals(a5pixel.Pixel(0, 0, 0, 10), p1 * 0.0)
    # Multiply by integer with clamping
    testcase.assert_equals(a5pixel.Pixel(20, 255, 0, 100), 
        a5pixel.Pixel(10, 200, 0, 100) * 2)
    # Multiply by float with rounding
    testcase.assert_equals(a5pixel.Pixel(20, 255, 0, 100), 
        a5pixel.Pixel(10, 200, 0, 100) * 2.01)
    # Rounding down
    testcase.assert_equals(a5pixel.Pixel(10, 21, 32, 20),
        a5pixel.Pixel(5, 10, 15, 20) * 2.15)

def test_pixel_monochrome():
    print("\t\t" + "Testing Pixel monochrome")
    p0 = a5pixel.Pixel(0, 0, 0, 0)
    p1 = a5pixel.Pixel(10, 20, 30, 10)
    p2 = a5pixel.Pixel(0, 5, 12, 20)

    # Zero test
    testcase.assert_equals(a5pixel.Pixel(0, 0, 0, 0), p0.monochrome())

    # Averaging with alpha unchanged
    testcase.assert_equals(a5pixel.Pixel(20, 20, 20, 10), p1.monochrome())
    testcase.assert_equals(a5pixel.Pixel(20, 20, 20, 10), p1.monochrome().monochrome())

    # Correct rounding
    testcase.assert_equals(a5pixel.Pixel(5, 5, 5, 20), p2.monochrome())
    testcase.assert_equals(a5pixel.Pixel(11, 11, 11, 40), (p2 + p2).monochrome())

def test_image_init():
    print("\t\t" + "Testing Image initialization")
    
    # Basics
    data = [[a5pixel.Pixel(0, 0, 0, 0)]]
    image = a5image.Image(data, [1, 1])
    testcase.assert_equals(a5pixel.Pixel(0, 0, 0, 0), image._data[0][0])
    testcase.assert_equals([1, 1], image._resolution)

    # Rectangular data
    data = [[a5pixel.Pixel(0, 0, 0, 0), a5pixel.Pixel(0, 0, 0, 0)],
            [a5pixel.Pixel(1, 1, 1, 1), a5pixel.Pixel(1, 1, 1, 1)],
            [a5pixel.Pixel(2, 2, 2, 2), a5pixel.Pixel(2, 2, 2, 2)]]
    image = a5image.Image(data, [1, 2])
    testcase.assert_equals(data, image._data)
    testcase.assert_equals([1, 2], image._resolution)

    # Baseline image data
    image = a5helper.read_image("simple.bmp")
    data = [[a5pixel.Pixel(0, 0, 0, 0), a5pixel.Pixel(255, 0, 0, 0)],
                [a5pixel.Pixel(0, 255, 0, 0), a5pixel.Pixel(0, 0, 255, 0)]]
    resolution = [100, 100]
    testcase.assert_equals(data, image._data)
    testcase.assert_equals(resolution, image._resolution)

    # Large image data
    image = a5helper.read_image("python_logo.bmp")
    resolution = [3779, 3779]
    testcase.assert_equals(101, len(image._data))
    testcase.assert_equals(300, len(image._data[0]))
    testcase.assert_equals(resolution, image._resolution)

    # Data type assertions
    resolution = [1, 1]
    testcase.assert_error(a5image.Image, 5, resolution)
    testcase.assert_error(a5image.Image, [a5pixel.Pixel(0, 0, 0, 0)], resolution)
    testcase.assert_error(a5image.Image, [[5]], resolution)

    # Data size assertions
    testcase.assert_error(a5image.Image, [], resolution)
    testcase.assert_error(a5image.Image, [[]], resolution)
    # non-rectangular
    bad_data = [[a5pixel.Pixel(0, 0, 0, 0)], [a5pixel.Pixel(0, 0, 0, 0), a5pixel.Pixel(0, 0, 0, 0)]]
    testcase.assert_error(a5image.Image, bad_data, resolution)

    # Resolution type assertions
    data = [[a5pixel.Pixel(0, 0, 0, 0)]]
    testcase.assert_error(a5image.Image, data, 5)
    testcase.assert_error(a5image.Image, data, [False, 1])

def test_image_reprs():
    print("\t\t" + "Testing Image representations")
    image1 = a5image.Image([[a5pixel.Pixel(0, 0, 0, 0)]], [1, 1])
    image2 = a5image.Image([[a5pixel.Pixel(1, 2, 3, 4)], [a5pixel.Pixel(4, 3, 2, 1)]], [2, 3])

    print("\t\t\t" + "image str")
    # __str__
    testcase.assert_equals("1x1 Image", str(image1))
    testcase.assert_equals("2x1 Image", str(image2))

    print("\t\t\t" + "image repr")
    # __repr__
    testcase.assert_equals("Image([[Pixel(0, 0, 0, 0)]], [1, 1])", repr(image1))
    testcase.assert_equals("Image([[Pixel(1, 2, 3, 4)], [Pixel(4, 3, 2, 1)]], [2, 3])", repr(image2))

def assert_image_equals(expected : a5image.Image, received : a5image.Image):
    """
    Helper function for checking if two images have entirely equal components

    In particular, we are interested in seeing if the data and resolutions are the same 
    """
    # We can just compare the data since Pixels have __eq__ defined
    testcase.assert_equals(str(expected), str(received)) # Test dimensions first to help with debugging
    testcase.assert_equals(expected._data, received._data)
    '''
    mirror_horizontal
    assert_equals: expected 
    [[Pixel(3, 3, 3, 0), Pixel(4, 4, 4, 0)], 
    [Pixel(1, 1, 1, 0), Pixel(2, 2, 2, 0)]] 
    but instead got 
    [[Pixel(2, 2, 2, 0), Pixel(1, 1, 1, 0)], 
    [Pixel(4, 4, 4, 0), Pixel(3, 3, 3, 0)]]
    '''
    testcase.assert_equals(expected._resolution, received._resolution)

def test_image_shifts():
    print("\t\t" + "Testing Image Shifts")
    image1 = a5image.Image([[a5pixel.Pixel(0, 0, 0, 0)]], [1, 1])
    image2 = a5image.Image([[a5pixel.Pixel(1, 2, 3, 4), a5pixel.Pixel(1, 2, 3, 4)], 
        [a5pixel.Pixel(4, 3, 2, 1), a5pixel.Pixel(4, 3, 2, 1)]], [2, 3])

    print("\t\t\t" + "add_pixel")
    # add_pixel
    image1.add_pixel(a5pixel.Pixel(0, 0, 0, 0))
    assert_image_equals(a5image.Image([[a5pixel.Pixel(0, 0, 0, 0)]], [1, 1]), image1)
    image1.add_pixel(a5pixel.Pixel(1, 2, 3, 4))
    assert_image_equals(a5image.Image([[a5pixel.Pixel(1, 2, 3, 4)]], [1, 1]), image1)
    # applies to each pixel
    image2.add_pixel(a5pixel.Pixel(254, 1, 0, 1))
    assert_image_equals(a5image.Image([[a5pixel.Pixel(255, 3, 3, 5), a5pixel.Pixel(255, 3, 3, 5)], 
        [a5pixel.Pixel(255, 4, 2, 2), a5pixel.Pixel(255, 4, 2, 2)]], [2, 3]), image2)
    # assertion errors
    testcase.assert_error(image1.add_pixel, 0)

    # image test
    if WRITE_IMAGES:
        image = a5helper.read_image("dragon.bmp")
        image.add_pixel(a5pixel.Pixel(0, 50, 80, 0))
        a5helper.write_image("dragon_add_pixel.bmp", image)

    image1 = a5image.Image([[a5pixel.Pixel(0, 0, 0, 0)]], [1, 1])
    image2 = a5image.Image([[a5pixel.Pixel(1, 2, 3, 4), a5pixel.Pixel(1, 2, 3, 4)], 
        [a5pixel.Pixel(4, 3, 2, 1), a5pixel.Pixel(4, 3, 2, 1)]], [2, 3])

    print("\t\t\t" + "red_shift")
    # red_shift
    image1.red_shift(0)
    assert_image_equals(a5image.Image([[a5pixel.Pixel(0, 0, 0, 0)]], [1, 1]), image1)
    image1.red_shift(5)
    assert_image_equals(a5image.Image([[a5pixel.Pixel(5, 0, 0, 0)]], [1, 1]), image1)
    # applies to each pixel
    image2.red_shift(10)
    assert_image_equals(a5image.Image([[a5pixel.Pixel(11, 2, 3, 4), a5pixel.Pixel(11, 2, 3, 4)], 
        [a5pixel.Pixel(14, 3, 2, 1), a5pixel.Pixel(14, 3, 2, 1)]], [2, 3]), image2)
    # assertion errors
    testcase.assert_error(image1.red_shift, "0")
    testcase.assert_error(image1.red_shift, -5)

    # image test
    if WRITE_IMAGES:
        image = a5helper.read_image("dragon.bmp")
        image.red_shift(50)
        a5helper.write_image("dragon_red_shift.bmp", image)

    image1 = a5image.Image([[a5pixel.Pixel(10, 20, 30, 0)]], [1, 1])
    image2 = a5image.Image([[a5pixel.Pixel(1, 2, 3, 4), a5pixel.Pixel(1, 2, 3, 4)], 
        [a5pixel.Pixel(4, 3, 2, 1), a5pixel.Pixel(4, 3, 2, 1)]], [2, 3])

    print("\t\t\t" + "shift_brightness")
    # shift_brightness
    # No change with 1.0
    image1.shift_brightness(1.0)
    assert_image_equals(a5image.Image([[a5pixel.Pixel(10, 20, 30, 0)]], [1, 1]), image1)
    image1.shift_brightness(.5)
    assert_image_equals(a5image.Image([[a5pixel.Pixel(5, 10, 15, 0)]], [1, 1]), image1)
    image1.shift_brightness(2.0)
    assert_image_equals(a5image.Image([[a5pixel.Pixel(10, 20, 30, 0)]], [1, 1]), image1)
    # All pixels
    image2.shift_brightness(2.0)
    assert_image_equals(a5image.Image([[a5pixel.Pixel(2, 4, 6, 4), a5pixel.Pixel(2, 4, 6, 4)], 
        [a5pixel.Pixel(8, 6, 4, 1), a5pixel.Pixel(8, 6, 4, 1)]], [2, 3]), image2)
    # Rounding
    image2.shift_brightness(1.7)
    assert_image_equals(a5image.Image([[a5pixel.Pixel(3, 6, 10, 4), a5pixel.Pixel(3, 6, 10, 4)], 
        [a5pixel.Pixel(13, 10, 6, 1), a5pixel.Pixel(13, 10, 6, 1)]], [2, 3]), image2)

    # image test
    if WRITE_IMAGES:
        image = a5helper.read_image("dragon.bmp")
        image.shift_brightness(0.5)
        a5helper.write_image("dragon_darker.bmp", image)

def test_image_monochrome():
    print("\t\t" + "Testing Image Monochrome")
    image1 = a5image.Image([[a5pixel.Pixel(10, 20, 30, 0)]], [1, 1])
    image2 = a5image.Image([[a5pixel.Pixel(1, 2, 4, 4), a5pixel.Pixel(1, 2, 4, 4)], 
        [a5pixel.Pixel(4, 3, 4, 1), a5pixel.Pixel(4, 3, 4, 1)]], [2, 3])
    image_zero = a5image.Image([[a5pixel.Pixel(0, 0, 0, 0)]], [1, 1])

    # make_monochrome
    image1.make_monochrome()
    assert_image_equals(a5image.Image([[a5pixel.Pixel(20, 20, 20, 0)]], [1, 1]), image1)
    # reapplying should do nothing
    image1.make_monochrome()
    assert_image_equals(a5image.Image([[a5pixel.Pixel(20, 20, 20, 0)]], [1, 1]), image1)
    # all pixels + rounding
    image2.make_monochrome()
    assert_image_equals(a5image.Image([[a5pixel.Pixel(2, 2, 2, 4), a5pixel.Pixel(2, 2, 2, 4)], 
        [a5pixel.Pixel(3, 3, 3, 1), a5pixel.Pixel(3, 3, 3, 1)]], [2, 3]), image2)
    # zero case
    image_zero.make_monochrome()
    assert_image_equals(a5image.Image([[a5pixel.Pixel(0, 0, 0, 0)]], [1, 1]), image_zero)

    # image test
    if WRITE_IMAGES:
        image = a5helper.read_image("dragon.bmp")
        image.make_monochrome()
        a5helper.write_image("dragon_monochrome.bmp", image)

def test_image_mirrors():
    print("\t\t" + "Testing Image Mirroring")
    image1 = a5image.Image([[a5pixel.Pixel(0, 0, 0, 0)]], [1, 1])
    image2 = a5image.Image([[a5pixel.Pixel(1, 1, 1, 0), a5pixel.Pixel(2, 2, 2, 0)], 
        [a5pixel.Pixel(3, 3, 3, 0), a5pixel.Pixel(4, 4, 4, 0)]], [2, 3])
    image3 = a5image.Image([
        [a5pixel.Pixel(1, 1, 1, 0), a5pixel.Pixel(2, 2, 2, 0), a5pixel.Pixel(3, 3, 3, 0)], 
        [a5pixel.Pixel(4, 4, 4, 0), a5pixel.Pixel(5, 5, 5, 0), a5pixel.Pixel(6, 6, 6, 0)]], [2, 3])

    print("\t\t\t" + "mirror_horizontal")
    # mirror_horizontal
    image1.mirror_horizontal()
    assert_image_equals(a5image.Image([[a5pixel.Pixel(0, 0, 0, 0)]], [1, 1]), image1)
    image2.mirror_horizontal()
    assert_image_equals(a5image.Image([[a5pixel.Pixel(3, 3, 3, 0), a5pixel.Pixel(4, 4, 4, 0)],
        [a5pixel.Pixel(1, 1, 1, 0), a5pixel.Pixel(2, 2, 2, 0)]], [2, 3]), image2)
    image3.mirror_horizontal()
    assert_image_equals(a5image.Image([ 
        [a5pixel.Pixel(4, 4, 4, 0), a5pixel.Pixel(5, 5, 5, 0), a5pixel.Pixel(6, 6, 6, 0)],
        [a5pixel.Pixel(1, 1, 1, 0), a5pixel.Pixel(2, 2, 2, 0), a5pixel.Pixel(3, 3, 3, 0)]], [2, 3]), image3)

    # image test
    if WRITE_IMAGES:
        image = a5helper.read_image("dragon.bmp")
        image.mirror_horizontal()
        a5helper.write_image("dragon_mirrored_horizontal.bmp", image)
    
    image1 = a5image.Image([[a5pixel.Pixel(0, 0, 0, 0)]], [1, 1])
    image2 = a5image.Image([[a5pixel.Pixel(1, 1, 1, 0), a5pixel.Pixel(2, 2, 2, 0)], 
        [a5pixel.Pixel(3, 3, 3, 0), a5pixel.Pixel(4, 4, 4, 0)]], [2, 3])
    image3 = a5image.Image([
        [a5pixel.Pixel(1, 1, 1, 0), a5pixel.Pixel(2, 2, 2, 0), a5pixel.Pixel(3, 3, 3, 0)], 
        [a5pixel.Pixel(4, 4, 4, 0), a5pixel.Pixel(5, 5, 5, 0), a5pixel.Pixel(6, 6, 6, 0)]], [2, 3])

    print("\t\t\t" + "mirror_vertical")
    # mirror_vertical
    image1.mirror_vertical()
    assert_image_equals(a5image.Image([[a5pixel.Pixel(0, 0, 0, 0)]], [1, 1]), image1)
    image2.mirror_vertical()
    assert_image_equals(a5image.Image([[a5pixel.Pixel(2, 2, 2, 0), a5pixel.Pixel(1, 1, 1, 0)], 
        [a5pixel.Pixel(4, 4, 4, 0), a5pixel.Pixel(3, 3, 3, 0)]], [2, 3]), image2)
    image3.mirror_vertical()
    assert_image_equals(a5image.Image([
        [a5pixel.Pixel(3, 3, 3, 0), a5pixel.Pixel(2, 2, 2, 0), a5pixel.Pixel(1, 1, 1, 0)], 
        [a5pixel.Pixel(6, 6, 6, 0), a5pixel.Pixel(5, 5, 5, 0), a5pixel.Pixel(4, 4, 4, 0)]], [2, 3]), image3)

    # image test
    if WRITE_IMAGES:
        image = a5helper.read_image("dragon.bmp")
        image.mirror_vertical()
        a5helper.write_image("dragon_mirrored_vertical.bmp", image)

def test_image_noise():
    print("\t\t" + "Testing Image Noise")
    image1 = a5image.Image([[a5pixel.Pixel(100, 100, 100, 0)]], [1, 1])
    image2 = a5image.Image([[a5pixel.Pixel(100, 150, 200, 0), a5pixel.Pixel(100, 150, 200, 0)], 
        [a5pixel.Pixel(100, 150, 200, 0), a5pixel.Pixel(100, 150, 200, 0)]], [2, 3])

    # noise
    # No change
    image1.add_noise(0)
    assert_image_equals(a5image.Image([[a5pixel.Pixel(100, 100, 100, 0)]], [1, 1]), image1)
    image1.add_noise(5)
    # Check bounds (note that this is not perfect for testing)
    pixel = image1._data[0][0]
    testcase.assert_true(pixel.r in range(95, 106))
    testcase.assert_true(pixel.g in range(95, 106))
    testcase.assert_true(pixel.b in range(95, 106))
    # Check that things have changed for each pixel
    image2.add_noise(20)
    for row in image2._data:
        for pixel in row:
            # Technically this could randomly fail
            # But the odds are roughly 1/21 ** 3, which is pretty...unlikely
            testcase.assert_not_equals([pixel.r, pixel.g, pixel.b], [100, 150, 200])

    # assertion errors
    testcase.assert_error(image1.add_noise, "0")
    testcase.assert_error(image1.add_noise, -5)
    
    # image test
    if WRITE_IMAGES:
        image = a5helper.read_image("dragon.bmp")
        image.add_noise(50)
        a5helper.write_image("dragon_noisy.bmp", image)

def test_image_blur():
    print("\t\t" + "Testing Image Blurring")
    image1 = a5image.Image([[a5pixel.Pixel(10, 20, 30, 0)]], [1, 1])
    image2 = a5image.Image([[a5pixel.Pixel(1, 5, 9, 0), a5pixel.Pixel(2, 5, 8, 0)], 
        [a5pixel.Pixel(3, 5, 7, 0), a5pixel.Pixel(4, 5, 6, 0)]], [2, 3])
    image3 = a5image.Image([
        [a5pixel.Pixel(1, 1, 1, 0), a5pixel.Pixel(2, 2, 2, 0), a5pixel.Pixel(3, 3, 3, 0)], 
        [a5pixel.Pixel(4, 4, 4, 0), a5pixel.Pixel(5, 6, 7, 0), a5pixel.Pixel(6, 6, 6, 0)],
        [a5pixel.Pixel(7, 7, 7, 0), a5pixel.Pixel(8, 8, 8, 0), a5pixel.Pixel(9, 9, 9, 0)]], [2, 3])

    # blur
    # no change for single pixel
    image1.blur()
    assert_image_equals(a5image.Image([[a5pixel.Pixel(10, 20, 30, 0)]], [1, 1]), image1)
    # More complicated, but should all end up the same
    image2.blur()
    assert_image_equals(a5image.Image([[a5pixel.Pixel(2, 5, 7, 0), a5pixel.Pixel(2, 5, 7, 0)], 
        [a5pixel.Pixel(2, 5, 7, 0), a5pixel.Pixel(2, 5, 7, 0)]], [2, 3]), image2)
    # Repeated 2x2 blurring does nothing
    image2.blur()
    assert_image_equals(a5image.Image([[a5pixel.Pixel(2, 5, 7, 0), a5pixel.Pixel(2, 5, 7, 0)], 
        [a5pixel.Pixel(2, 5, 7, 0), a5pixel.Pixel(2, 5, 7, 0)]], [2, 3]), image2)
    # Finally, the big 3x3 test
    image3.blur()
    assert_image_equals(a5image.Image([
        [a5pixel.Pixel(3, 3, 3, 0), a5pixel.Pixel(3, 3, 3, 0), a5pixel.Pixel(4, 4, 4, 0)], 
        [a5pixel.Pixel(4, 4, 4, 0), a5pixel.Pixel(5, 5, 5, 0), a5pixel.Pixel(5, 5, 5, 0)], 
        [a5pixel.Pixel(6, 6, 6, 0), a5pixel.Pixel(6, 6, 6, 0), a5pixel.Pixel(7, 7, 7, 0)]], [2, 3]), image3)
    # Reblurring should actually change things here
    image3.blur()
    assert_image_equals(a5image.Image([
        [a5pixel.Pixel(3, 3, 3, 0), a5pixel.Pixel(4, 4, 4, 0), a5pixel.Pixel(4, 4, 4, 0)], 
        [a5pixel.Pixel(4, 4, 4, 0), a5pixel.Pixel(4, 4, 4, 0), a5pixel.Pixel(5, 5, 5, 0)], 
        [a5pixel.Pixel(5, 5, 5, 0), a5pixel.Pixel(5, 5, 5, 0), a5pixel.Pixel(5, 5, 5, 0)]], [2, 3]), image3)
    
    # image test
    if WRITE_IMAGES:
        image = a5helper.read_image("dragon.bmp")
        # Applying this 5 times makes sure there's enough "strength" of blur to see
        image.blur()
        image.blur()
        image.blur()
        image.blur()
        image.blur()
        a5helper.write_image("dragon_blur.bmp", image)

def test_pixel():
    """
    Tests all the Pixel class methods
    """
    print("\t" + "Testing Pixel class")
    test_pixel_init()
    test_pixel_reprs()
    test_pixel_binary()
    test_pixel_monochrome()
    print("\t" + "Pixel tests passed!")

def test_image():
    """
    Tests all the Image class methods
    """
    print("\t" + "Testing Image class")
    test_image_init()
    test_image_reprs()
    test_image_shifts()
    test_image_monochrome()
    test_image_mirrors()
    test_image_noise()
    test_image_blur()
    print("\t" + "Image tests passed!")

def main():
    # Driver function
    print("Starting tests")
    test_pixel()
    print()
    test_image()
    print("All tests passed!")

if __name__ == "__main__":
    main()
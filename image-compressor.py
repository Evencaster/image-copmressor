import math
import random
import numpy as np
import matplotlib.pylab as plt
import sys

from PIL import Image, ImageDraw

c_max = 255

def compute_color_value(c):
    return (2 * c / c_max) - 1

class Pixel:
    def __init__(self, x, y):
        self.c = None
        self.x, self.y = x, y
    def __call__(self):
        return self.x, self.y
    def __str__(self):
        return "({x},{y})".format(x = self.x, y = self.y)
        # return "Pixel({x},{y})".format(x = self.x, y = self.y)

class Square:
    def __init__(self, bounding_points):
        self.x_vector = []
        self.top_left, self.bottom_right = bounding_points
        self.pixels = []
        for y in range(self.top_left.y, self.bottom_right.y):
            for x in range(self.top_left.x, self.bottom_right.x):
                self.pixels.append(Pixel(x, y))

    def compute_x_vector(self):
        # print("computing x vector")
        self.x_vector = list(map(lambda pixel: pixel.x, self.pixels))

    def __str__(self):
        pixels_str = ""
        for pixel in self.pixels:
            pixels_str += "{} ".format(pixel)
        s = "Square({top_left},{bottom_right}) [{pixels_str}]".format(top_left = self.top_left, bottom_right = self.bottom_right, pixels_str = pixels_str)
        return s

class ImageProcessor:
    def __init__(self, image_source, square_size):
        self.image = Image.open(image_source)
        # crops image to 256x256 (optional)
        self.crop_image() 
        self.image_height = self.image.height
        self.image_width = self.image.width
        self.pixmap = self.image.load()
        self.square_width = square_size[0]
        self.square_heigth = square_size[1]

    def crop_image(self):
        self.image = self.image.crop((0, 0 , 256, 256))

    def divide_on_squares(self):
        self.squares = []
        for y in range(self.image_height):
            for x in range(self.image_width):
                if x % self.square_width == 0:
                    if y % self.square_heigth == 0:
                        self.squares.append(Square((Pixel(x, y), Pixel(x + self.square_width, y + self.square_heigth))))
    
    def compute_color_values(self):
        for square in self.squares:
            for pixel in square.pixels:
                color_value_red = compute_color_value(self.pixmap[pixel.x, pixel.y][0])
                color_value_green = compute_color_value(self.pixmap[pixel.x, pixel.y][1])
                color_value_blue = compute_color_value(self.pixmap[pixel.x, pixel.y][2])
                pixel.c = (color_value_red, color_value_green, color_value_blue)
            square.compute_x_vector()


    def draw_squares(self):
        draw = ImageDraw.Draw(self.image)
        for square in self.squares:
            draw.rectangle([square.top_left(), square.bottom_right()], None, (255, 0, 0, 0), 1)
        self.image.save("squares.jpg", "JPEG")
    
    def fill_squares(self):
        draw = ImageDraw.Draw(self.image)
        for square in self.squares:
            for pixel in square.pixels:
                draw.Pixel(pixel(), (255,0,0))

    def print_squares(self):
        for square in self.squares:
            print(square)

    def print_square(self, index):
        print(self.squares[index])
 
image = ImageProcessor(sys.argv[1],(8,8))
image.divide_on_squares()
image.print_square(0)
image.compute_color_values()
print(image.squares[0].x_vector)
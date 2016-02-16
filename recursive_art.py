""" TODO: Put your header comment here """

import random
from PIL import Image


def build_random_function(min_depth, max_depth):
    """ Builds a random function of depth at least min_depth and depth
        at most max_depth (see assignment writeup for definition of depth
        in this context)

        min_depth: the minimum depth of the random function
        max_depth: the maximum depth of the random function
        returns: the randomly generated function represented as a nested list
                 (see assignment writeup for details on the representation of
                 these functions)
    """
    branch_functions_1_input = ["cos_pi", "sin_pi", "arctan"]
    branch_functions_2_input = ["prod", "avg", "squared"]
    branch_functions = branch_functions_1_input + branch_functions_2_input
    leaf_functions = ["x", "y"]
    
    min_depth = max(1, min_depth);
    max_depth = max(min_depth+1, max_depth);
    depth = random.choice(range(min_depth, max_depth))
    full_function = []

    if depth == 1:
        random_function = random.choice(leaf_functions)
        full_function.append(random_function)
        return full_function
    else:
        random_function = random.choice(branch_functions)
        full_function.append(random_function)

        if random_function in branch_functions_2_input:
            a = build_random_function(min_depth-1, max_depth-1)
            b = build_random_function(min_depth-1, max_depth-1)
            full_function.append(a)
            full_function.append(b)
        else:
            a = build_random_function(min_depth-1, max_depth-1)
            full_function.append(a)
        return full_function


def evaluate_random_function(f, x, y):
    """ Evaluate the random function f with inputs x,y
        Representation of the function f is defined in the assignment writeup

        f: the function to evaluate
        x: the value of x to be used to evaluate the function
        y: the value of y to be used to evaluate the function
        returns: the function value

        >>> evaluate_random_function(["x"],-0.5, 0.75)
        -0.5
        >>> evaluate_random_function(["y"],0.1,0.02)
        0.02
        >>> evaluate_random_function(["avg",["x"], ["y"]], 1.0, 2.0)
        1.5
    """
    import math

    func = f[0]
    if func == "x":
        return x
    elif func == "y":
        return y
    elif func == "avg":
        a = evaluate_random_function(f[1], x, y)
        b = evaluate_random_function(f[2], x, y)
        return (a + b) / 2
    elif func == "prod":
        a = evaluate_random_function(f[1], x, y)
        b = evaluate_random_function(f[2], x, y)
        return a * b
    elif func == "squared":
        a = evaluate_random_function(f[1], x, y)
        return a * a
    elif func == "cos_pi":
        a = evaluate_random_function(f[1], x, y)
        return math.cos(math.pi*a)
    elif func == "sin_pi":
        a = evaluate_random_function(f[1], x, y)
        return math.sin(math.pi*a)
    elif func == "arctan":
        a = evaluate_random_function(f[1], x, y)
        return math.atan(a)
    else:
        print "I don't know that function..."
        print func


def remap_interval(val,
                   input_interval_start,
                   input_interval_end,
                   output_interval_start,
                   output_interval_end):
    """ Given an input value in the interval [input_interval_start,
        input_interval_end], return an output value scaled to fall within
        the output interval [output_interval_start, output_interval_end].

        val: the value to remap
        input_interval_start: the start of the interval that contains all
                              possible values for val
        input_interval_end: the end of the interval that contains all possible
                            values for val
        output_interval_start: the start of the interval that contains all
                               possible output values
        output_inteval_end: the end of the interval that contains all possible
                            output values
        returns: the value remapped from the input to the output interval

        >>> remap_interval(0.5, 0, 1, 0, 10)
        5.0
        >>> remap_interval(5, 4, 6, 0, 2)
        1.0
        >>> remap_interval(5, 4, 6, 1, 2)
        1.5
    """
    
    input_span = float(input_interval_end) - float(input_interval_start)
    output_span = float(output_interval_end) - float(output_interval_start)

    value_scaled = float(val - input_interval_start) / float(input_span)

    return output_interval_start + (value_scaled * output_span)


def color_map(val):
    """ Maps input value between -1 and 1 to an integer 0-255, suitable for
        use as an RGB color code.

        val: value to remap, must be a float in the interval [-1, 1]
        returns: integer in the interval [0,255]

        >>> color_map(-1.0)
        0
        >>> color_map(1.0)
        255
        >>> color_map(0.0)
        127
        >>> color_map(0.5)
        191
    """
    # NOTE: This relies on remap_interval, which you must provide
    color_code = remap_interval(val, -1, 1, 0, 255)
    return int(color_code)


def test_image(filename, x_size=350, y_size=350):
    """ Generate test image with random pixels and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (random.randint(0, 255),  # Red channel
                            random.randint(0, 255),  # Green channel
                            random.randint(0, 255))  # Blue channel

    im.save(filename)


def generate_art(filename, x_size=350, y_size=350):
    """ Generate computational art and save as an image file.

        filename: string filename for image (should be .png)
        x_size, y_size: optional args to set image dimensions (default: 350)
    """
    # Functions for red, green, and blue channels - where the magic happens!
    red_function = build_random_function(7,9)
    green_function = build_random_function(1,2)
    blue_function = build_random_function(7,9)

    # Create image and loop over all pixels
    im = Image.new("RGB", (x_size, y_size))
    pixels = im.load()
    for i in range(x_size):
        for j in range(y_size):
            x = remap_interval(i, 0, x_size, -1, 1)
            y = remap_interval(j, 0, y_size, -1, 1)
            pixels[i, j] = (
                    color_map(evaluate_random_function(red_function, x, y)),
                    color_map(evaluate_random_function(green_function, x, y)),
                    color_map(evaluate_random_function(blue_function, x, y))
                    )

    im.save(filename)

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    # Create some computational art!
    # TODO: Un-comment the generate_art function call after you
    #       implement remap_interval and evaluate_random_function
    generate_art("myart.png")

    # Test that PIL is installed correctly
    # TODO: Comment or remove this function call after testing PIL install
    # test_image("noise.png")

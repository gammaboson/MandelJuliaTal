# MandelJuliaTal

**Draws the Mandelbrot and Julia fractals in a window with pygame, allowing to play with parameters**

## Context 

- Author:   Stéphane (stp/gammaboson)
- Created:  2023/03/11
- Language: Python 3.6 - Pygame 1.9
- License:  GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007

## Usage

``./mandeljuliatal.py`` for general usage of the program.

``./mandeljuliatal.py -h`` for help on how to set command line parameters.

## Description

The Mandelbrot set is drawn on the left side, the Julia set is draw on the right.
You can zoom in the Mandelbrot or Julia set.
To select the zoom rectangle: hold down the left mouse button, move to another point and release mouse button.
To restore the original zoom: click the middle mouse button in the Mandelbrot or Julia set you want to restore.
To chose the point in the Mandelbrot set for which the Julia set is draw, click the right mouse button in the Mandelbrot.

*The following keys are used:*

- m: redraw the Mandelbrot set
- j: redraw the Julia set
- i: input prompt for a command json string
- p: increase the power of the iterative formula: z_new = z_old**POWER + c (decrease with SHIFT)
- d: increase the depth, i.e. the max number of iterations of the formula (decrease with SHIFT)
- a: increase the limit on abs(z) above which the iterations are stopped and the color chosen from number of iterations (decrease with SHIFT) 
- c: invert color for converging part where max number of iterations is reached, while abs(z) still below limit
- f: increase the color factor (decrease with SHIFT)
- e: increase the color exponent (decrease with SHIFT)
- r: increase the red   color component for non converging part (decrease with SHIFT)
- g: increase the green color component for non converging part (decrease with SHIFT)
- b: increase the blue  color component for non converging part (decrease with SHIFT)
- n: change the name of the matplotlib colormap used
- s: toggle to keep Square aspect ration during zoom (or not)
- backspace: redraw previous plot, read from the stack of command json strings

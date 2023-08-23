#!/usr/bin/env python3
#
# File:     mandeljuliatal.py
# Author:   Stéphane (stp/gammaboson)
# Created:  2023/03/11
# Language: Python 3.6 - Pygame 1.9
# License:  GNU GENERAL PUBLIC LICENSE, Version 3, 29 June 2007
#
# ------------------------------------------------------------------------------------
# Affichage la fractale de Mandelbrot et Julia dans une fenêtre avec pygame
# ------------------------------------------------------------------------------------
# souris bouton gauche pour zoomer dans Mandelbrot (à gauche) et Julia (à droite) et redessiner ces ensembles
# souris bouton de droite: définir la constante de Julia et redessiner l'ensemble de Julia (à droite)
# souris bouton du milieu: dézoomer dans Mandelbrot (à gauche) et Julia (à droite) et redessiner ces ensembles
# touche m: redessiner Mandelbrot
# touche j: redessiner Julia
# ------------------------------------------------------------------------------------
#
#
# Interesting related pages: 
#  - Arnaud https://www.math.univ-toulouse.fr/~cheritat/wiki-draw/index.php/Mandelbrot_set
#           http://images.math.cnrs.fr/L-ensemble-de-Mandelbrot.html
#  - Mathieu https://mathete.net/la-fractale-de-mandelbrot/
#

import pygame, sys, argparse, math
import matplotlib as mpl

# programme principal
def main(sys_args):
    
    # Constantes valeurs par défaut
    nmax = 100 # nombre d'itérations maximales avant de considérer que la suite diverge
    amax = 2 # maximum pour abs(z), au delà on considère avoir divergé
    LARGEUR, HAUTEUR = 700, 700 # taille de la fenêtre en pixels
    POWER = 2 # puissance dans l'itération
    SQUARE_ZOOM = True
    COLOR_CONV = (0,0,0)
    COLOR_MAP = mpl.colormaps['twilight']
    COLOR_EXPONENT = 1.3
    COLOR_FACTOR = 2.
    RED, GREEN, BLUE = 1, 1, 1 # multiplicateurs de couleur
    #COLOR_MAP = None
    #COLOR_EXPONENT = 1
    #COLOR_FACTOR = 1
    #RED, GREEN, BLUE = 3, 1, 10 # multiplicateurs de couleur

    # lecture des arguments de la ligne de commande
    parser = argparse.ArgumentParser(description="Draw Mandelbrot and Julia sets with zoom.")

    print("""
    
mandeljuliatal.py
-------------------------------------------------------------------------------------------------------------------------------
Draws the Mandelbrot and Julia fractals in a window with pygame, allowing to play with parameters
-------------------------------------------------------------------------------------------------------------------------------

The Mandelbrot set is drawn on the left side, the Julia set is draw on the right.
You can zoom in the Mandelbrot or Julia set.
To select the zoom rectangle: hold down the left mouse button, move to another point and release mouse button.
To restore the original zoom: click the middle mouse button in the Mandelbrot or Julia set you want to restore.
To chose the point in the Mandelbrot set for which the Julia set is draw, click the right mouse button in the Mandelbrot.

The following keys are used:
-m: redraw the Mandelbrot set
-j: redraw the Julia set
-i: input prompt for a command json string
-p: increase the power of the iterative formula: z_new = z_old**POWER + c (decrease with SHIFT)
-d: increase the depth, i.e. the max number of iterations of the formula (decrease with SHIFT)
-a: increase the limit on abs(z) above which the iterations are stopped and the color chosen from number of iterations (decrease with SHIFT) 
-c: invert color for converging part where max number of iterations is reached, while abs(z) still below limit
-f: increase the color factor (decrease with SHIFT)
-e: increase the color exponent (decrease with SHIFT)
-r: increase the red   color component for non converging part (decrease with SHIFT)
-g: increase the green color component for non converging part (decrease with SHIFT)
-b: increase the blue  color component for non converging part (decrease with SHIFT)
-n: change the name of the matplotlib colormap used
-s: toggle to keep Square aspect ration during zoom (or not)
-backspace: redraw previous plot, read from the stack of command json strings

Example colormap names:
cmaps = [('Perceptually Uniform Sequential', [
            'viridis', 'plasma', 'inferno', 'magma', 'cividis']),
         ('Sequential', [
            'Greys', 'Purples', 'Blues', 'Greens', 'Oranges', 'Reds',
            'YlOrBr', 'YlOrRd', 'OrRd', 'PuRd', 'RdPu', 'BuPu',
            'GnBu', 'PuBu', 'YlGnBu', 'PuBuGn', 'BuGn', 'YlGn']),
         ('Sequential (2)', [
            'binary', 'gist_yarg', 'gist_gray', 'gray', 'bone', 'pink',
            'spring', 'summer', 'autumn', 'winter', 'cool', 'Wistia',
            'hot', 'afmhot', 'gist_heat', 'copper']),
         ('Diverging', [
            'PiYG', 'PRGn', 'BrBG', 'PuOr', 'RdGy', 'RdBu',
            'RdYlBu', 'RdYlGn', 'Spectral', 'coolwarm', 'bwr', 'seismic']),
         ('Cyclic', ['twilight', 'twilight_shifted', 'hsv']),
         ('Qualitative', [
            'Pastel1', 'Pastel2', 'Paired', 'Accent',
            'Dark2', 'Set1', 'Set2', 'Set3',
            'tab10', 'tab20', 'tab20b', 'tab20c']),
         ('Miscellaneous', [
            'flag', 'prism', 'ocean', 'gist_earth', 'terrain', 'gist_stern',
            'gnuplot', 'gnuplot2', 'CMRmap', 'cubehelix', 'brg',
            'gist_rainbow', 'rainbow', 'jet', 'turbo', 'nipy_spectral',
            'gist_ncar'])]
""")

    parser.add_argument("-L", "--Largeur", help="largeur de la fenêtre")
    parser.add_argument("-H", "--Hauteur", help="hauteur de la fenêtre")
    parser.add_argument("-P", "--Power", help="power of the iteration formula: z = z**POWER + c")
    parser.add_argument("-D", "--Depth", help="depth of iterations nmax")
    parser.add_argument("-A", "--AbsLimit", help="limit on abs(z) above which the color is chosen from number of iterations")
    parser.add_argument("-C", "--ColorConv", help="color as string r,g,b of the converging zone of the iterative formula (Mandelbrot or Julia set)")
    parser.add_argument("-N", "--ColorName", help="name of the matplotlib colormap")
    parser.add_argument("-E", "--ColorExponent", help="exponent in the color mapping function ")    
    parser.add_argument("-F", "--ColorFactor", help="factor in the color mapping function ")    
    parser.add_argument("-R", "--Red", help="muliplicateur couleur Red")
    parser.add_argument("-G", "--Green", help="muliplicateur couleur Green")
    parser.add_argument("-B", "--Blue", help="muliplicateur couleur Blue")
    parser.add_argument("-S", "--SquareZoom", help="set to 0 not to impose square aspect ration in zoom, 1 otherwise")
    args = parser.parse_args(sys_args)
    

    # change valeurs par défaut en utilisant les args
    if args.Largeur:
        LARGEUR = int(args.Largeur)
    if args.Hauteur:
        HAUTEUR = int(args.Hauteur)
    if args.Red:
        RED = int(args.Red)
    if args.Green:
        GREEN = int(args.Green)
    if args.Blue:
        BLUE = int(args.Blue)
    if args.Depth:
        nmax = int(args.Depth)
    if args.Power:
        POWER = int(args.Power)
    if args.AbsLimit:
        amax = float(args.AbsLimit)
    if args.ColorConv:
        COLOR_CONV = tuple(map(int, args.ColorConv.split(',')))
    if args.ColorExponent:
        COLOR_EXPONENT = float(args.ColorExponent)
    if args.ColorFactor:
        COLOR_FACTOR = float(args.ColorFactor)
    if args.ColorName: # examples: 'viridis', 'plasma', 'inferno', 'magma', 'cividis'
        try:
            COLOR_MAP = mpl.colormaps[args.ColorName] # we will use matplotlib colormap
        except:
            COLOR_MAP = None # we will use our custom color mapping
    if args.SquareZoom:
        SQUARE_ZOOM = ( int(args.SquareZoom) == 1 )
        
    # autres Constantes
    if POWER == 2:
        m_xmin, m_xmax, m_ymin, m_ymax = -2, +0.5, -1.25, +1.25 # bornes du repère de Mandelbrot par défault
    else:
        m_xmin, m_xmax, m_ymin, m_ymax = -1.25, +1.25, -1.25, +1.25 # bornes du repère de Mandelbrot par défault
    j_xmin, j_xmax, j_ymin, j_ymax = -1.25, 1.25, -1.25, +1.25 # bornes du repère de Julia par défault
    j_cx, j_cy = 0.5,0 # constante de l'ensemble de Julia par défault

    # liste des commandes jstring
    jlist = []
    
    # Initialisation de pygame et création d'une fenêtre aux dimensions spécifiéés (LARGEUR et HAUTEUR sont celles du côté gauche de l'écran pour Mandelbrot)
    pygame.init()
    screen = pygame.display.set_mode((2*LARGEUR,HAUTEUR)) # 2*LARGEUR pour avoir le coté droit de l'écran pour Julia

    # fonction pour retourner les composantes RGB d'une couleur n dans une colormap cmap de matplotlib
    def getColorRGB(n, cmap):
        color = cmap.colors[int(n) % len(cmap.colors)] # map n into the length of the colormap (usually len = 256)
        return int(color[0]*255), int(color[1]*255), int(color[2]*255) # inde 0,1,2=R,G,B, multiply value (between 0 and 1) by 255 for real RGB value

    # fonction pour convertir la position sur l'écran en coordonnée dans le repère défini par xmin:xmax et ymin:ymax
    def getPosFromScr(XSCR, YSCR, xmin, xmax, ymin, ymax):
        x = (XSCR * (xmax - xmin) / LARGEUR + xmin)
        y = (YSCR * (ymin - ymax) / HAUTEUR + ymax)
        return x,y

    # convert positions of corners to min max of zoom box
    def getMinMaxFromPos(px0,px1,py0,py1):
        if SQUARE_ZOOM:
            center_x = (px0+px1)/2
            center_y = (py0+py1)/2
            radius = max(abs(px0-px1), abs(py0-py1))/2
            xmin = center_x - radius
            xmax = center_x + radius
            ymin = center_y - radius
            ymax = center_y + radius
        else:
            xmin = min(px0,px1)
            xmax = max(px0,px1)
            ymin = min(py0,py1)
            ymax = max(py0,py1)
        return xmin,xmax,ymin,ymax

    # itérations dans la suite de nombres complexes: z(n+1) = z(n)**2 + c
    def iterate(xn,yn,cx,cy,nmax):
        n = 0
        z = complex(xn,yn)
        c = complex(cx,cy)
        while abs(z) < amax and n < nmax:
            z = z**POWER + c
            n += 1
        #while (xn * xn + yn * yn) < 4 and n < nmax: # on teste que le carré de la norme du nombre complex zn est inférieur à 4 -> permet d'économiser un calcul de racine carrée coûteux en terme de performances
        #    xn,     yn     =     xn * xn - yn * yn + cx,     2 * xn * yn + cy
        #    n += 1
        if n == nmax:
            return -1
        else:
            return n
    
    # fonction donnant la couleur pour le nombre d'itérations n
    def color_of_iteration(n):
        n_scaled = COLOR_FACTOR*n**COLOR_EXPONENT
        if COLOR_MAP == None:
            #return ((RED * n) % 256, (GREEN * n) % 256, (BLUE * n) % 256)
            #return ((RED * math.sqrt(n)) % 256, (GREEN * math.sqrt(n)) % 256, (BLUE * math.sqrt(n)) % 256)
            #return ((RED * math.log(n)) % 256, (GREEN * math.log(n)) % 256, (BLUE * math.log(n)) % 256)
            #return ((RED * n**2) % 256, (GREEN * n**2) % 256, (BLUE * n**2) % 256)
            #return ((RED * n*math.log(n)) % 256, (GREEN * n*math.log(n)) % 256, (BLUE * n*math.log(n)) % 256)
            return ((RED * n_scaled) % 256, (GREEN * n_scaled) % 256, (BLUE * n_scaled) % 256)
        else:
            color = getColorRGB(n_scaled,COLOR_MAP) # apply exponent for changing color depth
            return ((RED * color[0]) % 256, (GREEN * color[1]) % 256, (BLUE * color[2]) % 256)
            #return color
            
    # fonction pour dessiner l'ensemble de Mandelbrot
    def plot_Mandelbrot(xmin,xmax,ymin,ymax,nmax):
        # Création de l'ensemble de Mandelbrot
        # Principe : on balaye l'écran pixel par pixel en convertissant le pixel en un point du plan de notre repère
        # Si la suite converge, le point appartient à l'ensemble de Mandelbrot et on colore le pixel en noir
        # Sinon la suite diverge, le point n'appartient pas à l'ensemble et on colore le pixel en couleur
        jstring = '{ ' + '"Dtyp": "PlotMandel", "xmin": {}, "xmax": {}, "ymin": {}, "ymax": {}, "nmax": {}'.format(xmin,xmax,ymin,ymax,nmax) + ' }'
        jlist.append(jstring)
        print(jstring)
        for YSCR in range(HAUTEUR):
            for XSCR in range(LARGEUR):
                # Associer à chaque pixel de l'écran de coordonnées (XSCR;YSCR)
                # un point C du plan de coordonnées (cx;cy) dans le repère défini par xmin:xmax et ymin:ymax
                cx, cy = getPosFromScr(XSCR, YSCR, xmin, xmax, ymin, ymax)
                # valeur initiale de la suite de nombres complexes de Mandelbrot
                xn, yn = 0, 0
                n = iterate(xn,yn,cx,cy,nmax)
                if n < 0:
                    screen.set_at((XSCR, YSCR), COLOR_CONV) # On colore le pixel en noir -> code RGB : (0,0,0)
                else:
                    screen.set_at((XSCR, YSCR), color_of_iteration(n))
                    #screen.set_at((XSCR, YSCR), (255, 255, 255)) # On colore le pixel en blanc -> code RGB : (255,255,255)
        pygame.display.flip() # Mise à jour et rafraîchissement de la fenêtre graphique pour affichage
        pygame.display.set_caption("Mandelbrot plot=({};{};{};{}) nmax={}".format(m_xmin,m_xmax,m_ymin,m_ymax,nmax))
        print("Ready.")

    # fonction pour dessiner l'ensemble de Julia
    def plot_Julia(xmin,xmax,ymin,ymax,nmax,cx=0.285,cy=0.01):
        # Création de l'ensemble de Julia
        # Principe : on balaye l'écran pixel par pixel en convertissant le pixel en un point du plan de notre repère
        # Si la suite converge, le point appartient à l'ensemble de Julia et on colore le pixel en noir
        # Sinon la suite diverge, le point n'appartient pas à l'ensemble et on colore le pixel en couleur
        jstring = '{ ' + '"Dtyp": "PlotJulia", "xmin": {}, "xmax": {}, "ymin": {}, "ymax": {}, "nmax": {}, "cx": {}, "cy": {} '.format(xmin,xmax,ymin,ymax,nmax,cx,cy) + ' }'
        print(jstring)
        jlist.append(jstring)
        for YSCR in range(HAUTEUR):
            for XSCR in range(LARGEUR):
                # Associer à chaque pixel de l'écran de coordonnées (XSCR;YSCR)
                # un point de coordonnées (xn;yn) dans le repère défini par xmin:xmax et ymin:ymax
                # avec la constante d'origine de Julia (cx;cy), relevé dans le plan de Mandelbrot
                xn, yn = getPosFromScr(XSCR, YSCR, xmin, xmax, ymin, ymax)
                n = iterate(xn,yn,cx,cy,nmax)
                if n < 0:
                    # +LARGEUR pour dessiner sur le côté droit de l'écran
                    screen.set_at((XSCR+LARGEUR, YSCR), COLOR_CONV) # On colore le pixel en noir -> code RGB : (0,0,0)
                else:
                    # +LARGEUR pour dessiner sur le côté droit de l'écran
                    screen.set_at((XSCR+LARGEUR, YSCR), color_of_iteration(n))
                    #screen.set_at((XSCR+LARGEUR, YSCR), (255, 255, 255)) # On colore le pixel en blanc -> code RGB : (255,255,255)
        pygame.display.flip() # Mise à jour et rafraîchissement de la fenêtre graphique pour affichage
        pygame.display.set_caption("Julia plot=({};{};{};{}) c=({};{}) nmax={}".format(m_xmin,m_xmax,m_ymin,m_ymax,j_cx,j_cy,nmax))
        print("Ready.")

    # fonction pour dessiner l'ensemble de Mandelbrot ou de Julia, selon ce qu'il ya dans le string json
    def execute_json_command(jstring):
        import json
        # define variables nonlocal, to use those known outside of this nested function (we could avoid this by making a class)
        nonlocal m_xmin,m_xmax,m_ymin,m_ymax,nmax 
        nonlocal j_xmin,j_xmax,j_ymin,j_ymax,nmax,j_cx,j_cy 
        try: # en cas de string qui ne se décode pas avec la prochaine ligne, l'exception JSONDecodeError est produite
            jdict = json.loads(jstring) # decoder le string jstring (supposé en format json) vers le dictionaire jdict
            if "Dtyp" in jdict:
                if jdict["Dtyp"] == "PlotMandel":
                    m_xmin,m_xmax,m_ymin,m_ymax,nmax = jdict["xmin"],jdict["xmax"],jdict["ymin"],jdict["ymax"],jdict["nmax"]
                    plot_Mandelbrot(m_xmin,m_xmax,m_ymin,m_ymax,nmax)
                elif jdict["Dtyp"] == "PlotJulia":
                    j_xmin,j_xmax,j_ymin,j_ymax,nmax,j_cx,j_cy = jdict["xmin"],jdict["xmax"],jdict["ymin"],jdict["ymax"],jdict["nmax"],jdict["cx"],jdict["cy"]
                    plot_Julia(j_xmin,j_xmax,j_ymin,j_ymax,nmax,j_cx,j_cy)
        except json.decoder.JSONDecodeError: # dans le cas de cette exception, simplemnt faire ce print, au lieu de planter le programme
            print("Error decoding json string: ", jstring)

    # dessiner Mandelbrot et Julia une 1ère fois
    plot_Mandelbrot(m_xmin,m_xmax,m_ymin,m_ymax,nmax)
    plot_Julia(j_xmin,j_xmax,j_ymin,j_ymax,nmax,j_cx, j_cy)

    # Boucle infinie de pygame, permettant de raffraichir la fenêtre graphique et d'interagir, de zoomer, etc
    loop = True
    while loop:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Pour quitter l'application en fermant la fenêtre
                loop = False
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1: # left button down
                    # relever le 1er point px0,py0 pour zoomer dans l'ensemble de Mandelbrot
                    PSCR = pygame.mouse.get_pos()
                    if PSCR[0] < LARGEUR:
                        m_px0, m_py0 = getPosFromScr(PSCR[0], PSCR[1], m_xmin, m_xmax, m_ymin, m_ymax)
                        print("m_p0=({};{})".format(m_px0,m_py0))
                    else:
                        j_px0, j_py0 = getPosFromScr(PSCR[0]-LARGEUR, PSCR[1], j_xmin, j_xmax, j_ymin, j_ymax)
                        print("j_p0=({};{})".format(j_px0,j_py0))
                    
                if event.button == 2: # middle button down
                    PSCR = pygame.mouse.get_pos()
                    if PSCR[0] < LARGEUR:
                        # remettre les bornes d'origine pour dezommer dans l'ensemble de Mandelbrot
                        if POWER == 2:
                            m_xmin, m_xmax, m_ymin, m_ymax = -2, +0.5, -1.25, +1.25 # bornes du repère
                        else:
                            m_xmin, m_xmax, m_ymin, m_ymax = -1.25, +1.25, -1.25, +1.25 # bornes du repère
                        # redessiner Mandelbrot
                        print("Reinit Mandelbrot with nmax=",nmax)
                        plot_Mandelbrot(m_xmin,m_xmax,m_ymin,m_ymax,nmax)
                    else:
                        # remettre les bornes d'origine pour dezommer dans l'ensemble de Julia
                        j_xmin, j_xmax, j_ymin, j_ymax = -1.25, 1.25, -1.25, +1.25 # bornes du repère de Julia
                        # redessiner Julia
                        print("Reinit Julia with nmax=",nmax)
                        plot_Julia(j_xmin, j_xmax, j_ymin, j_ymax,nmax,j_cx,j_cy)

                if event.button == 3: # right button down
                    # relever un point cx,cy dans l'ensemble de Mandelbrot pour dessiner Julia avec cette graine
                    PSCR = pygame.mouse.get_pos()
                    j_cx, j_cy = getPosFromScr(PSCR[0], PSCR[1], m_xmin, m_xmax, m_ymin, m_ymax)
                    print("j_c=({};{})".format(j_cx,j_cy))
                    # redissiner Julia avec ce point comme valeur initiale
                    print("Redraw Julia with nmax=",nmax)
                    plot_Julia(j_xmin, j_xmax, j_ymin, j_ymax,nmax,j_cx,j_cy)

            elif event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1: # left button up
                    # relever le 2ème point px1,py1 dans l'ensemble de Mandelbrot
                    PSCR = pygame.mouse.get_pos()
                    if PSCR[0] < LARGEUR:
                        m_px1, m_py1 = getPosFromScr(PSCR[0], PSCR[1], m_xmin, m_xmax, m_ymin, m_ymax)
                        print("m_p1=({};{})".format(m_px1,m_py1))
                        # redéfinir les bornes du plot de l'ensemble de Mandelbrot pour zoomer
                        m_xmin, m_xmax, m_ymin, m_ymax = getMinMaxFromPos(m_px0,m_px1,m_py0,m_py1)
                        # redessiner Mandelbrot
                        print("Zoom Mandelbrot with nmax=",nmax)
                        plot_Mandelbrot(m_xmin,m_xmax,m_ymin,m_ymax,nmax)
                    else:
                        j_px1, j_py1 = getPosFromScr(PSCR[0]-LARGEUR, PSCR[1], j_xmin, j_xmax, j_ymin, j_ymax)
                        print("j_p1=({};{})".format(j_px1,j_py1))
                        # redéfinir les bornes du plot de l'ensemble de Julia pour zoomer
                        j_xmin, j_xmax, j_ymin, j_ymax = getMinMaxFromPos(j_px0,j_px1,j_py0,j_py1)
                        # redessiner Mandelbrot
                        print("Zoom Julia with nmax=",nmax)
                        plot_Julia(j_xmin, j_xmax, j_ymin, j_ymax,nmax,j_cx,j_cy)
                    
            # checking if keydown event happened
            if event.type == pygame.KEYDOWN:

                # checking if key "m" was pressed
                if event.key == pygame.K_m:
                    print("Redraw Mandelbrot with nmax=",nmax)
                    plot_Mandelbrot(m_xmin,m_xmax,m_ymin,m_ymax,nmax)

                # checking if key "j" was pressed
                elif event.key == pygame.K_j:
                    print("Redraw Julia with nmax=",nmax)
                    plot_Julia(j_xmin, j_xmax, j_ymin, j_ymax,nmax,j_cx,j_cy)
                    
                # checking if key "SHIFT + d" was pressed
                elif (event.key == pygame.K_d and pygame.key.get_mods() & pygame.KMOD_SHIFT) or event.key == pygame.K_UP:
                    nmax = max(10, nmax-10) # on diminue la profondeur d'itératon, mais jamais moins de 10
                    print("Depth decreased to nmax=",nmax)

                # checking if key "d" was pressed
                elif event.key == pygame.K_d or event.key == pygame.K_DOWN:
                    nmax += 10 # on augmente la profondeur d'itératon
                    print("Depth increased to nmax=",nmax)

                # checking if key "SHIFT + p" was pressed
                elif event.key == pygame.K_p and pygame.key.get_mods() & pygame.KMOD_SHIFT or event.key == pygame.K_LEFT:
                    POWER = max(1,POWER-1)
                    print("Power decreased to POWER=",POWER)

                # checking if key "p" was pressed
                elif event.key == pygame.K_p or event.key == pygame.K_RIGHT:
                    POWER += 1
                    print("Power increased to POWER=",POWER)

                # checking if key "SHIFT + a" was pressed
                elif event.key == pygame.K_a and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    amax = max(0.5,amax-0.5)
                    print("Abs value max decreased to amax=",amax)

                # checking if key "a" was pressed
                elif event.key == pygame.K_a:
                    amax += 0.5
                    print("Abs value max increased to amax=",amax)

                # checking if key "SHIFT + r" was pressed
                elif event.key == pygame.K_r and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    RED = max(0,RED-1)
                    print("Color decreased to RED=",RED)

                # checking if key "r" was pressed
                elif event.key == pygame.K_r:
                    RED += 1
                    print("Color increased to RED=",RED)

                # checking if key "SHIFT + g" was pressed
                elif event.key == pygame.K_g and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    GREEN = max(0,GREEN-1)
                    print("Color decreased to GREEN=",GREEN)

                # checking if key "g" was pressed
                elif event.key == pygame.K_g:
                    GREEN += 1
                    print("Color increased to GREEN=",GREEN)

                # checking if key "SHIFT + b" was pressed
                elif event.key == pygame.K_b and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    BLUE = max(0,BLUE-1)
                    print("Color decreased to BLUE=",BLUE)

                # checking if key "b" was pressed
                elif event.key == pygame.K_b:
                    BLUE += 1
                    print("Color increased to BLUE=",BLUE)

                # checking if key "SHIFT + e" was pressed
                elif event.key == pygame.K_e and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    COLOR_EXPONENT = max(0.05,COLOR_EXPONENT-0.05)
                    print("ColorExponent decreased to ",COLOR_EXPONENT)

                # checking if key "e" was pressed
                elif event.key == pygame.K_e:
                    COLOR_EXPONENT += 0.05
                    print("ColorExponent indecreased to ",COLOR_EXPONENT)

                # checking if key "SHIFT + f" was pressed
                elif event.key == pygame.K_f and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                    COLOR_FACTOR = max(0.05,COLOR_FACTOR-0.05)
                    print("ColorFactor decreased to ",COLOR_FACTOR)

                # checking if key "f" was pressed
                elif event.key == pygame.K_f:
                    COLOR_FACTOR += 0.05
                    print("ColorFactor indecreased to ",COLOR_FACTOR)

                # checking if key "c" was pressed
                elif event.key == pygame.K_c:
                    COLOR_CONV = (255-COLOR_CONV[0], 255-COLOR_CONV[1], 255-COLOR_CONV[2]) 
                    print("Color for converging part inverted")

                # checking if key "i" was pressed
                elif event.key == pygame.K_i:
                    jstring=input("Enter command json string:\n") # entrer un string sur la console
                    execute_json_command(jstring) # appeler la fonction execute_json_command avec ce string

                # checking if key "backspace" was pressed
                elif event.key == pygame.K_BACKSPACE:
                    try:
                        jlist.pop()
                        jstring=jlist.pop()
                        execute_json_command(jstring) # appeler la fonction execute_json_command avec ce string        
                    except: # if the list is empty and pop returns an error, we do nothing
                        pass

                # checking if key "n" was pressed
                elif event.key == pygame.K_n:
                    cstring=input("Enter name of matplotlib colormap string:\n") # entrer un string sur la console
                    try:
                        COLOR_MAP = mpl.colormaps[cstring] # we will use matplotlib colormap
                    except:
                        COLOR_MAP = None # we will use our custom color mapping

                # checking if key "s" was pressed
                elif event.key == pygame.K_s:
                    SQUARE_ZOOM = not SQUARE_ZOOM
                    print("SquareZoom set to ",SQUARE_ZOOM)
                    
    # terminer pygame
    pygame.quit()

# appel du programme principal avec les arguments de la ligne de commande
if __name__ == "__main__":
    main(sys.argv[1:])

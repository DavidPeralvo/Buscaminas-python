import pygame



import os
import sys
import random
import time

import pygame.gfxdraw



SCREEN_WIDTH = 400
SCREEN_HEIGHT = 400

IMG_DIR = "images"
FNT_DIR = "fonts"

GRAY          = (127  , 127   , 127   , 255)
SILVER        = (192  , 192   , 192   , 255)
RED           = (255  , 0     , 0     , 255)
GREEN         = (0    , 255   , 0     , 255)
BLUE          = (0    , 0     , 255   , 255)
YELLOW        = (255  , 255   , 0     , 255)
CYAN          = (0    , 255   , 255   , 255)
MAGENTA       = (255  , 0     , 255   , 255)
BLACK         = (0    , 0     , 0     , 255)
WHITE         = (255  , 255   , 255   , 255)
DARK_RED      = (100  , 0     , 0     , 255)
DARK_GREEN    = (0    , 100   , 0     , 255)
DARK_BLUE     = (0    , 0     , 100   , 255)
DARK_YELLOW   = (100  , 100   , 0     , 255)
DARK_CYAN     = (0    , 100   , 100   , 255)
DARK_MAGENTA  = (100  , 0     , 100   , 255)
PURPLE        = (85   , 26    , 139   , 255)
GOLDEN        = (255  , 215   , 0     , 255)

# ------------------------------
# Funciones globales al programa
# ------------------------------

def cargar_imagen(nombre, dir_imagen, alpha=False):
    # Encontramos la ruta completa de la imagen
    ruta = os.path.join(dir_imagen, nombre)
    try:
        image = pygame.image.load(ruta)
    except:
        print "Error, no se puede cargar la imagen: ", ruta
        sys.exit(1)
    # Compruebo si la imagen tiene "canal alpha" (como los png)
    if alpha == True:
        image = image.convert_alpha()
    else:
        image = image.convert()
    return image

def cargar_tipoGrafia(nombre, dir_fuente, tamanyo):
    ruta = os.path.join(dir_fuente, nombre)
    # Intentar cargar el texto
    try:
        fuente = pygame.font.Font(ruta, tamanyo)
    except:
        print "Error, no se puede cargar la fuente: ", ruta
        sys.exit(1)
    return fuente

# ------------------------------
# Desarrollo del programa
# ------------------------------

# Clase Casilla

class Casilla():
    def __init__(self, x, y, size_x, size_y, text_font, text_size, status, value):
        self.fuente = cargar_tipoGrafia(text_font, FNT_DIR, text_size)
        self.x = x
        self.y = y
        self.size_x = size_x
        self.size_y = size_y
        self.text_color = [GRAY, RED, GREEN, YELLOW, CYAN, MAGENTA, PURPLE, GOLDEN, WHITE] # Color del valor del texto segun valor de la casilla
        self.status = status # Estado de la casilla SIN MARCAR, CURSOR_ENCIMA, MARCADA.
        self.value = value # Valor de la casilla ' ', '0'...'8' bomba

    def is_touched(self, x, y):
        if x >= self.x and x <= self.x + self.size_x and y > self.y and y < self.y + self.size_y:
            retorno = True
        else:
            retorno = False
        return retorno

    def set_status(self, status):
        self.status = status

    def get_status(self):
        return self.status

    def casilla_color(self, screen):
        if self.status == 1:# SIN MARCAR
            pygame.gfxdraw.box(screen, (self.x+1, self.y+1, self.size_x-1, self.size_y-1), BLUE)
            pygame.gfxdraw.vline(screen, self.x, self.y, self.y + self.size_y, WHITE)
            pygame.gfxdraw.hline(screen, self.x, self.x + self.size_x, self.y, WHITE)
            pygame.gfxdraw.vline(screen, self.x + self.size_x, self.y, self.y + self.size_y, GRAY)
            pygame.gfxdraw.hline(screen, self.x, self.x + self.size_x, self.y + self.size_y, GRAY)
        else:
            if self.status == 2: # CURSOR_ENCIMA
                pygame.gfxdraw.box(screen, (self.x+1, self.y+1, self.size_x-1, self.size_y-1), SILVER)
                pygame.gfxdraw.vline(screen, self.x, self.y, self.y + self.size_y, GRAY)
                pygame.gfxdraw.hline(screen, self.x, self.x + self.size_x, self.y, GRAY)
                pygame.gfxdraw.vline(screen, self.x + self.size_x, self.y, self.y + self.size_y, WHITE)
                pygame.gfxdraw.hline(screen, self.x, self.x + self.size_x, self.y + self.size_y, WHITE)
            else:
                if self.status == 3: # MARCADA
                    if self.value == 'x':
                        pygame.gfxdraw.box(screen, (self.x, self.y, self.size_x+1, self.size_y+1), RED)
                        bomb_img = cargar_imagen("mina.png",IMG_DIR)
                        screen.blit(bomb_img, (self.x + (self.size_x / 2) - (bomb_img.get_width()/2), self.y + (self.size_y / 2) - (bomb_img.get_height()/2)))
                    else:
                        pygame.gfxdraw.box(screen, (self.x, self.y, self.size_x+1, self.size_y+1), GRAY)
                        pygame.gfxdraw.vline(screen, self.x, self.y, self.y + self.size_y, WHITE)
                        pygame.gfxdraw.hline(screen, self.x, self.x + self.size_x, self.y, WHITE)
                        size = self.fuente.size(self.value)
                        texto = self.fuente.render(self.value, 1, self.text_color[int(self.value)])
                        screen.blit(texto, (self.x + (self.size_x / 2) - (size[0] / 2), self.y + (self.size_y / 2) - (size[1] / 2)))
    def mostrar_minas(self,screen):
        for c in range(self.max_x * self.max_y):
            if self.values== 'x':
                pygame.gfxdraw.box(screen, (self.x, self.y, self.size_x+1, self.size_y+1), RED)
                bomb_img = cargar_imagen("mina.png",IMG_DIR)
                screen.blit(bomb_img, (self.x + (self.size_x / 2) - (bomb_img.get_width()/2), self.y + (self.size_y / 2) - (bomb_img.get_height()/2)))

class Tablero:
    def __init__(self, max_x, max_y, factor, width, height):
        self.width = (width/10)
        self.height = (height/10)
        self.x0 = self.y0 = 10
        self.xx = self.yy = 10
        self.pushed = False
        self.start  = 0
        self.max_x = max_x
        self.max_y = max_y
        self.tabla   = []
        for x in range(max_x):
            for y in range(max_y):
                if random.random() < factor:
                    self.tabla.append('x')
                else:
                    self.tabla.append('0')
        c = 0
        for x in range(max_x):
            for y in range (max_y):
                if self.tabla[y*max_x+x] == '0':
                    if ( (y > 0) and (self.tabla[(y-1)*max_x+x] == 'x') ): c = c + 1
                    if ( (y < max_y-1) and (self.tabla[(y+1)*max_x+x] == 'x') ): c = c + 1
                    if ( (x > 0) and (self.tabla[y*max_x+x-1] == 'x') ): c = c + 1
                    if ( (x < max_x-1) and (self.tabla[y*max_x+x+1] == 'x') ): c = c + 1
                    if ( (y > 0) and (x > 0) and (self.tabla[(y-1)*max_x+x-1] == 'x') ): c = c + 1
                    if ( (y < max_y-1) and (x < max_x-1) and (self.tabla[(y+1)*max_x+x+1] == 'x') ): c = c + 1
                    if ( (y > 0) and (x < max_x-1) and (self.tabla[(y-1)*max_x+x+1] == 'x') ): c = c + 1
                    if ( (y < max_y-1) and  (x > 0) and (self.tabla[(y+1)*max_x+x-1] == 'x') ): c = c + 1
                    self.tabla[y*max_x+x] = c + int('0')
                    c = 0
	# Crea Array de objetos casilla en SIN MARCAR con el valor de tabla
	self.casilla = []
        for y in range(max_y):  #10
            for x in range(max_x): #10
                self.casilla.append(Casilla(x*self.width+1, y*self.height+1, self.width-1, self.height-1, "DroidSans-Bold.ttf", 10, 1, str(self.tabla[y*max_x+x])))

    def get_numeroCasillasTapadas(self):
        retorno = 0
        for c in range(self.max_x * self.max_y):
            if self.casilla[c].get_status() != 3: retorno = retorno + 1
	return retorno

    def get_numeroBombas(self):
        retorno = 0
        for c in range(self.max_x * self.max_y):
            if self.tabla[c] == 'x': retorno = retorno + 1
        return retorno



    def destapa(self, x, y):
        retorno = True
        self.casilla[y*self.max_x+x].set_status(3)
        if self.tabla[y*self.max_x+x] != 'x':
            retorno = False
            if self.tabla[y*self.max_x+x] == int('0'):
                for j in range(-1, 2):
                    for i in range(-1, 2):
                        if (x + j >= 0) and (x + j < self.max_x) and (y + i >= 0) and (y + i < self.max_y) :
                            if (self.casilla[(y+i)*self.max_x+x+j].get_status() != 3):
                                self.destapa(x+j, y+i)
        return retorno


    def print_tablero(self, screen):
        for y in range(self.max_y):
            for x in range(self.max_x):
                self.casilla[y*self.max_x+x].casilla_color(screen)

    def play(self, screen):
        retorno = False
        for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONDOWN:
                self.pushed = True
                self.start = time.clock()
                posicion = pygame.mouse.get_pos()
                self.xx = self.x0 = posicion[0] / self.width
                self.yy = self.y0 = posicion[1] / self.height
                if (self.casilla[self.yy*self.max_x+self.xx].get_status() < 3):
                    self.casilla[self.yy*self.max_x+self.xx].set_status(2)
            elif event.type == pygame.MOUSEMOTION:
                posicion = pygame.mouse.get_pos()
                x = (posicion[0] / self.width)
                y = (posicion[1] / self.height)
                if self.xx !=  x or self.yy != y:
                    if self.casilla[self.yy*self.max_x+self.xx].get_status() < 3:
                        self.casilla[self.yy*self.max_x+self.xx].set_status(1)
                    if (self.casilla[y*self.max_x+x].get_status() < 3):
                        self.casilla[y*self.max_x+x].set_status(2)
                    self.xx = x
                    self.yy = y
            elif event.type == pygame.MOUSEBUTTONUP:
                self.pushed = False
                posicion = pygame.mouse.get_pos()
                x = (posicion[0] / self.width)
                y = (posicion[1] / self.height)
                if self.x0 ==  x and self.y0 == y and self.casilla[y*self.max_x+x].get_status() < 3:
                    retorno = self.destapa(x, y)
            elif event.type == pygame.QUIT:
                sys.exit()
        self.print_tablero(screen)
        return retorno

def main():
    pygame.init()


    # Creacion de ventana
    width = SCREEN_WIDTH
    height = SCREEN_HEIGHT
    pygame.display.set_mode((width, height))
    screen = pygame.display.get_surface()
    pygame.display.set_caption("BUSCAMINAS-David Peralvo")

    # Creacion del tablero
    tablero = Tablero(13, 20, 0.18, width, height)


    # Creamos el objeto clock de la clase time.Clock
    clock = pygame.time.Clock()

    salir = False

    while (salir == False):
        clock.tick(60)
        salir = tablero.play(screen)
        if tablero.get_numeroCasillasTapadas() == tablero.get_numeroBombas():
            salir = True
        pygame.display.flip()

    fuente = cargar_tipoGrafia("B.ttf", FNT_DIR, 80)
    if tablero.get_numeroCasillasTapadas() == tablero.get_numeroBombas():
        size = fuente.size("GANASTE")
        texto = fuente.render("GANASTE", 1, GREEN)
        screen.blit(texto, ((width / 2) - (size[0] / 2), (height / 2) - (size[1] / 2)))
    else:
        size = fuente.size("PERDISTE")
        texto = fuente.render("PERDISTE", 1, RED)
        screen.blit(texto, ((width / 2) - (size[0] / 2), (height / 2) - (size[1] / 2)))
    pygame.display.flip()
    time.sleep(3)


if __name__ == "__main__":
    main()

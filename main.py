import pygame
import sys
import random

# Inicialización temprana para las constantes
pygame.init()

# Configuraciones y Colores
alto, ancho = 480, 480
tamaño_grilla = 20
alto_grilla = alto // tamaño_grilla
ancho_grilla = ancho // tamaño_grilla

gris1, gris2 = (120, 120, 120), (170, 170, 170)
verde, negro, rojo = (0, 255, 0), (0, 0, 0), (255, 0, 0)
up, down, left, right = (0, -1), (0, 1), (-1, 0), (1, 0)

fuente = pygame.font.SysFont("Arial", 30)

class Snake:
    def __init__(self):
        self.length = 1
        self.position = [(ancho // 2, alto // 2)]
        self.direction = random.choice([up, down, left, right])
        self.color = verde
        self.puntos=0

    def Cabeza(self):
        return self.position[0]
        
    def girar(self, point):
        # Evita que la serpiente se muerda a sí misma girando 180 grados
        if self.length > 1 and (point[0] * -1, point[1] * -1) == self.direction:
            return
        else:
            self.direction = point

    def movimiento(self):
        actual = self.Cabeza()
        x, y = self.direction
        nueva_x = actual[0] + (x*tamaño_grilla)
        nueva_y = actual[1] + (y*tamaño_grilla)
        nueva = (nueva_x,nueva_y)

        if (nueva_x<0 or nueva_x >= ancho or nueva_y <0 or nueva_y >= alto):
            self.reset()
            return
               
        if len(self.position) > 2 and nueva in self.position[2:]:
            self.reset()
        else:
            self.position.insert(0, nueva)
            if len(self.position) > self.length:
                self.position.pop()
        
    def reset(self):
        self.length = 1
        self.position = [(ancho // 2, alto // 2)]
        self.direction = random.choice([up, down, left, right])
        self.puntos=0


    def dibujar(self, escena):
        for pos in self.position:
            rect = pygame.Rect((pos[0], pos[1]), (tamaño_grilla, tamaño_grilla))
            pygame.draw.rect(escena, self.color, rect)
            pygame.draw.rect(escena, negro, rect, 1)

    def control(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: self.girar(up)
                elif event.key == pygame.K_DOWN: self.girar(down)
                elif event.key == pygame.K_RIGHT: self.girar(right)
                elif event.key == pygame.K_LEFT: self.girar(left)

class Comida:
    def __init__(self):
        self.position = (0, 0)
        self.color = rojo
        self.posicion_random()
    
    def posicion_random(self):
        self.position = (random.randint(0, ancho_grilla - 1) * tamaño_grilla,
                         random.randint(0, alto_grilla - 1) * tamaño_grilla)
    
    def dibujar(self, escena):
        rect = pygame.Rect((self.position[0], self.position[1]), (tamaño_grilla, tamaño_grilla))
        pygame.draw.rect(escena, self.color, rect)
        pygame.draw.rect(escena, negro, rect, 1)

def dibujar_grilla(escena):
    for y in range(int(alto_grilla)):
        for x in range(int(ancho_grilla)):
            rect = pygame.Rect((x * tamaño_grilla, y * tamaño_grilla), (tamaño_grilla, tamaño_grilla))
            color = gris1 if (x + y) % 2 == 0 else gris2
            pygame.draw.rect(escena, color, rect)

def main():
    screen = pygame.display.set_mode((ancho, alto))
    pygame.display.set_caption("Snake")
    escena = pygame.Surface(screen.get_size()).convert()
    timer = pygame.time.Clock()
    
    snake = Snake()
    comida = Comida()

    while True:
        timer.tick(10)
        snake.control()
        snake.movimiento()

        if snake.Cabeza() == comida.position:
            snake.length += 1
            snake.puntos += 1
            comida.posicion_random()
        
        dibujar_grilla(escena)
        snake.dibujar(escena)
        comida.dibujar(escena)
        
        screen.blit(escena, (0, 0))
        texto = fuente.render(f"Puntaje: {snake.puntos}", True, negro)
        screen.blit(texto, (5, 10))
        pygame.display.update()

if __name__ == "__main__":
    main()
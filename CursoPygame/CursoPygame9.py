from flask import Flask
from flask_ask import Ask, statement, question
import pygame, sys # También utilizamos el módulo sys
from queue import Queue
from threading import Thread

app = Flask(__name__)
ask = Ask(app, '/')

# Creamos una cola para compartir información entre los hilos
queue = Queue()

# Función que maneja el hilo de Pygame
def game_thread(queue):

    # Tamaño de la pantalla de Pygame en píxeles
    ANCHO = 800
    ALTO = 600

    # FPS
    FPS = 30

    # Paleta de colores en RGB
    NEGRO = (0,0,0)
    BLANCO = (255,255,255)
    ROJO = (255,0,0)
    H_FA2F2F = (250,47,47)
    VERDE = (0,255,0)
    AZUL = (0,0,255)
    H_50D2FE = (94,210,254)
    AZUL2 = (64,64,255)
    class Jugador(pygame.sprite.Sprite):

        # Sprite del jugador
        def __init__(self):

            # Heredamos el init de la clase Sprite de Pygame
            super().__init__()

            # Rectángulo (jugador), recordemos que las imágenes en Pygame son rectángulos
            self.image = pygame.image.load("Imagenes/nave.png").convert() # Convertimos la imagen a tipo Pygame para que el rendimiento mejore
            #self.image.fill(H_FA2F2F) # No indicamos ningún color al sprite porque queremos que se muestre la imagen

            self.image.set_colorkey(AZUL2) # Con esta función podemos eliminar el color indicado por parámetro de la imagen

            # Obtiene el rectángulo (sprite) de la imagen del jugador para poder manipularlo
            self.rect = self.image.get_rect()

            # Centra el rectángulo (sprite)
            self.rect.center = (ANCHO // 2, ALTO // 2) # Este operador devuelve el resultado (integer) de dividir, redondeando si sale float
            #self.rect.center = (400,600) # Podemos colocar el rectángulo en la posición inicial que queramos

            # Velocidad del personaje (inicial)
            self.velocidad_x = 0 # Inicialmente el objeto va a estar quieto
            self.velocidad_y = 0

        def update(self):

            # Velocidad predeterminada cada vuelta del bucle si no pulsas nada
            # ESTO PARA TRABAJAR POR VOZ SEGURAMENTE NO NOS INTERESA
            self.velocidad_x = 0 # Con esto se evita que el personaje se mueva de manera indefinida si no estamos pulsando nada
            self.velocidad_y = 0

            # Mantiene las teclas pulsadas
            teclas = pygame.key.get_pressed()

            # Mueve el personaje hacia la izquierda
            if teclas[pygame.K_a]:
                self.velocidad_x = -10 # Cada vez que se pulse la tecla se moverá 10px a la izquierda
            
            # Mueve el personaje hacia la derecha
            if teclas[pygame.K_d]:
                self.velocidad_x = 10

            # Mueve el personaje hacia arriba
            if teclas[pygame.K_w]:
                self.velocidad_y = -10 # Cada vez que se pulse la tecla se moverá 10px hacia arriba
            
            # Mueve el personaje hacia abajo
            if teclas[pygame.K_s]:
                self.velocidad_y = 10

            # Actualiza la posición del personaje
            self.rect.x += self.velocidad_x
            self.rect.y += self.velocidad_y

            # Limita el margen izquierdo
            if self.rect.left < 0: # Cada vez que toque el borde izquierdo e intente salir de la pantalla 
                self.rect.left = 0 # Se ajusta el personaje al borde izquierdo

            # Limita el margen derecho
            if self.rect.right > ANCHO:
                self.rect.right = ANCHO

            # Limita el margen inferior
            if self.rect.bottom > ALTO:
                self.rect.bottom = ALTO

            # Limita el margen superior
            if self.rect.top < 0:
                self.rect.top = 0

            """
            # Si queremos limitar aún más el recorrido y no hasta los bordes pues simplemente podemos hacerlo tal que así
            if self.rect.left < 300:
                self.rect.left = 300

            if self.rect.right > 500:
                self.rect.right = 500
            """

    # Iniciación de Pygame, creación de la ventana, título y control de reloj.
    pygame.init()
    pantalla = pygame.display.set_mode((ANCHO, ALTO))
    pygame.display.set_caption("Trabajando con sprites")
    clock = pygame.time.Clock() # Para controlar los FPS

    # Grupo de sprites, instanciación del objeto jugador.
    sprites = pygame.sprite.Group() # Se agrupan los sprites para que trabajen en un conjunto y se almacene en la variable que queramos
    jugador = Jugador()
    sprites.add(jugador) # Al grupo le añadimos jugador, para que tenga la imagen del jugador

    font = pygame.font.SysFont(None, 48)

    # Bucle de juego
    ejecutando = True
    while ejecutando:

        # Es lo que especifica la velocidad del bucle de juego
        clock.tick(FPS)

        # Eventos
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                ejecutando = False
                #pygame.quit()
                #sys.exit()

        # Actualización de sprites
        sprites.update() # Con esto podemos hacer que todos los sprites (imágenes) se vayan actualizando en la pantalla

        # Fondo de pantalla, dibujo de sprites y formas geométricas
        pantalla.fill(NEGRO) # Establecemos el color de fondo de la pantalla
        sprites.draw(pantalla) # Dibujamos los sprites en la pantalla
        pygame.draw.line(pantalla, H_50D2FE, (400, 0), (400, 800), 1)
        pygame.draw.line(pantalla, AZUL, (0, 300), (800, 300), 1)

        # Actualizamos el contenido de la pantalla
        pygame.display.flip() # Permite que solo una porción de la pantalla se actualice, en lugar de toda el área de la pantalla. Si no se pasan argumentos, se actualizará la superficie completa.

        if queue.qsize() > 0: # Nos aseguramos que la cola tenga elementos antes de intentar obtener uno de ellos

            mensaje = queue.get_nowait()

            # Si el mensaje es None, salimos del bucle y terminamos el hilo
            if mensaje is None:
                break
            # Si recibimos un mensaje de texto, lo mostramos en la pantalla
            if isinstance(mensaje, str):

                if mensaje == 'Clean': # Si se recibe el mensaje Clean es para indicarnos que se vacie la ventana de juego
                    #screen = pygame.display.get_surface()
                    #screen.fill(NEGRO)
                    pygame.quit()
                    sys.exit()
                    #pygame.display.update()
                else:
                    jugador.image.fill(VERDE) # Con esto modificamos el color del rectángulo (jugador) y verificamos que efectivamente podemos modificar en tiempo real el videojuego con peticiones de alexa
                    text = font.render(mensaje, True, (255, 255, 255))
                    screen = pygame.display.get_surface()
                    screen.blit(text, (200, 200))
                    pygame.display.update()

    pygame.quit()

# Creamos el hilo de Pygame y lo iniciamos
game_thread = Thread(target=game_thread, args=(queue,))
game_thread.start()

@ask.launch # Para cuando el usuario lanza la skill
def start_skill():
    return question('Bienvenido al videojuego Multihilo. Elige entre futbol y baloncesto.')

# Definimos la ruta para el intent HelloWorldIntent
@ask.intent('FootballIntent')
def football():
    # Añadimos un mensaje a la cola para que se muestre en la pantalla
    queue.put('Futbol')
    return question('Has elegido futbol.')

@ask.intent('BasketballIntent')
def basketball():
    # Añadimos un mensaje a la cola para que se muestre en la pantalla
    queue.put('BALONCESTO')
    return question('Has elegido baloncesto.')

@ask.intent('EndgameIntent')
def endgame():
    queue.put('Clean')
    return statement('Fin del juego.')

# Definimos la ruta para la página principal de la aplicación web
@app.route('/')
def index():
    return 'Esta es la homepage del videojuego Multihilo.'

if __name__ == '__main__':

    app.run(debug=False) # Si desactivamos el modo debug evitamos que nos abra 2 ventanas de pygame
    # Cuando la aplicación web se detiene, enviamos un mensaje None a la cola
    queue.put(None)
    # Esperamos a que el hilo de Pygame termine
    game_thread.join()
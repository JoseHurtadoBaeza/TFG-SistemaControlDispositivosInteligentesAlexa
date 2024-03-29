from flask import Flask, render_template # Importamos la clase Flask del módulo flask y la función render_template que permite renderizar plantillas HTML
from flask_ask import Ask, statement # Importamos la clase Ask del módulo flask_ask y la función statement que crea una respuesta a la solicitud de Alexa
import pygame # Importamos la librería Pygame, que se utilizará para crear el juego

app = Flask(__name__) # Creamos una instancia de la clase Flask, la cual representa la aplicación web
ask = Ask(app, '/') # Creamos una instancia de la clase Ask, la cual representa el servicio de Alexa, y le indicamos que use la ruta '/' para las solicitudes

@ask.launch # Para cuando el usuario lanza la skill
def start_skill():
    mensaje_bienvenida = 'Bienvenido al videojuego hola mundo'
    return statement(mensaje_bienvenida)

@app.route('/') # Se define la ruta (se puede definir otra ruta para otra página) a la homepage de la aplicación web de Flask
def homepage():
    return "Hola, estás en la homepage"

@ask.intent('HelloWorldIntent') # Se indica que la función que sigue es la que manejará las solicitudes del intent HelloWorldIntent 
def hello_world(): # Definimos la función que será ejecutada

    pygame.init() #  Inicializamos Pygame
    pygame.display.set_mode((640, 480)) # Establecemos el modo de visualización de Pygame con una resolución de 640x480 píxeles
    font = pygame.font.SysFont(None, 48) # Creamos un objeto de fuente de texto con el tamaño de 48 píxeles
    text = font.render ('Hola Mundo', True, (255, 255, 255)) # Creamos una superficie de texto que contiene la cadena "Hola Mundo" en blanco (255, 255, 255) sobre un fondo negro
    screen = pygame.display.get_surface() # Obtenemos la superficie de visualización actual de Pygame
    screen.blit(text, (200, 200)) # Dibujamos la superficie de texto en la posición (200, 200) de la superficie de visualización
    pygame.display.update() # Actualizamos la superficie de visualización para que se muestren los cambios realizados
    
    return statement('Hola Mundo') # Devolvemos una respuesta a la solicitud de Alexa con la cadena "Hola Mundo"

if __name__ == '__main__': # Verificamos si este archivo es el main que se está ejecutando
    app.run(port=5000, debug=True) # Iniciamos la aplicación web y habilitamos la depuración en caso de que ocurran errores

"""Pacman, classic arcade game.

Exercises

1. Change the board.
2. Change the number of ghosts.
3. Change where pacman starts.
4. Make the ghosts faster/slower.
5. Make the ghosts smarter.

"""

from random import choice
from turtle import *
from freegames import floor, vector
#se importan las librerias de turtle y freegames

state = {'score': 0} #inicia un diccionario para llevar el puntaje
path = Turtle(visible=False)
writer = Turtle(visible=False)
aim = vector(5, 0) #vector que determina la direccion a la que se mueven los personajes
pacman = vector(-40, -80) #vector del pacman
ghosts = [ #vector de los cuatro fantasmas
    [vector(-180, 160), vector(5, 0)],
    [vector(-180, -160), vector(0, 5)],
    [vector(100, 160), vector(0, -5)],
    [vector(100, -160), vector(-5, 0)],
]
tiles = [ #vector del tablero
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 0, 1, 0, 0, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 1, 1, 1, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 1, 1, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 1, 1, 0, 0, 0, 0,
    0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 1, 0, 1, 0, 1, 0, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 1, 0, 0, 0, 0, 0, 1, 0, 1, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0,
    0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
    0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
]

def square(x, y):
#funcion que define y dibuja el cuadrado del tablero
    "Draw square using path at (x, y)."
    path.up()
    path.goto(x, y)
    path.down()
    path.begin_fill()

#limitaciones
    for count in range(4):
        path.forward(20)
        path.left(90)

    path.end_fill()

def offset(point):
# para contar el puntaje de los puntitos que come el pacman
    "Return offset of point in tiles."
    x = (floor(point.x, 20) + 200) / 20
    y = (180 - floor(point.y, 20)) / 20
    index = int(x + y * 20)
    return index

def valid(point):
#dice si el tile a la que se va a mover es valida
    "Return True if point is valid in tiles."
    index = offset(point)

    if tiles[index] == 0:
        return False

    index = offset(point + 19)

    if tiles[index] == 0:
        return False

    return point.x % 20 == 0 or point.y % 20 == 0

def world():
#funcion que crea el tablero a partir del vector
    "Draw world using path."
    bgcolor('black') #colores
    path.color('blue')

    for index in range(len(tiles)):
        tile = tiles[index]

    #dibuja los puntitos blancos del tablero
        if tile > 0:
            x = (index % 20) * 20 - 200
            y = 180 - (index // 20) * 20
            square(x, y)

            if tile == 1:
                path.up()
                path.goto(x + 10, y + 10)
                path.dot(2, 'white')

def move():
#funcion del movimiento de los personajes
    "Move pacman and all ghosts."
    writer.undo()
    writer.write(state['score'])

    clear()

#mueve el pacman segun la tecla presionada
    if valid(pacman + aim):
        pacman.move(aim)

    index = offset(pacman)

    if tiles[index] == 1:
        tiles[index] = 2
        state['score'] += 1
        x = (index % 20) * 20 - 200
        y = 180 - (index // 20) * 20
        square(x, y)

    up()
    goto(pacman.x + 10, pacman.y + 10)
    dot(20, 'yellow')

#movimiento de los fantasmas
    for point, course in ghosts:
        if valid(point + course):
            point.move(course)
        else:
        #Los siguientes vectores determinan los movimientos permitidos de los fantasmas y su modificación los permite recorrer mayores distancias en el mismo tiempo 
            options = [
                vector(10, 0),
                vector(-10, 0),
                vector(0, 10),
                vector(0, -10),
            ]
            plan = choice(options)
            #para buscar al pacman y ver a donde debe ir el fantasma
            if((pacman.x > 0 and course.x > 0) or (pacman.x < 0 and course.x < 0)) and pacman.y > 0:
                plan = vector(0,10)
                if plan == course:
                    plan = choice(options)
            elif((pacman.x > 0 and course.x > 0) or (pacman.x < 0 and course.x < 0)) and pacman.y < 0:
                plan = vector(0,-10)
                if plan == course:
                    plan = choice(options)
            elif((pacman.y > 0 and course.y > 0) or (pacman.y < 0 and course.y < 0)) and pacman.x > 0:
                plan = vector(10,0)
                if plan == course:
                    plan = choice(options)
            elif((pacman.y > 0 and course.y > 0) or (pacman.y < 0 and course.y < 0)) and pacman.x < 0:
                plan = vector(-10,0)
                if plan == course:
                    plan = choice(options)
                
            course.x = plan.x #define la direccion a donde se van a mover los fantasmas
            course.y = plan.y

        up()
        goto(point.x + 10 , point.y + 10)
        dot(20, 'red')

    update()


    for point, course in ghosts:
        if abs(pacman - point) < 20:
            return

#ontimer repite la función que se le de en el primer argumento
# con la velocidad dada en milisegundos en el segundo argumento
    ontimer(move, 10)

def change(x, y):
#redirige al pacman cuando se dirige a un lugar invalido
    "Change pacman aim if valid."
    if valid(pacman + vector(x, y)):
        aim.x = x
        aim.y = y

setup(420, 420, 370, 0)
hideturtle()
tracer(False)
writer.goto(160, 160)
writer.color('white')
writer.write(state['score'])
listen()
#vincula las flechas con el movimiento del pacman
onkey(lambda: change(5, 0), 'Right')
onkey(lambda: change(-5, 0), 'Left')
onkey(lambda: change(0, 5), 'Up')
onkey(lambda: change(0, -5), 'Down')
world()
move()
done()

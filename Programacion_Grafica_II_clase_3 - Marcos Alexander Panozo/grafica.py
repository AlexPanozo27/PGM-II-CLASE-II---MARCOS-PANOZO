from vpython import *
import asyncio
import random

scene = canvas(title="Combinación de Conceptos en VPython", width=1600, height=1000, background=color.black)

def color_aleatorio():
    return vector(random.uniform(0.3, 1), random.uniform(0.3, 1), random.uniform(0.3, 1))

def crear_piramides(posicion, tamano, n):
    if n == 0:
        return []
    return [pyramid(pos=posicion + vector(-4 * i * tamano, 0, 0), size=vector(5 * (1 + 0.5 * i), 5 * (1 + 0.5 * i), 5 * (1 + 0.5 * i)), color=vector(1, 0.3 + 0.1 * i, 0)) for i in range(n)]

def crear_esferas(posicion, radio, n):
    if n == 0:
        return []
    return [sphere(pos=posicion + vector(6 * i * radio, 0, 0), radius=5 * (1 + 0.5 * i), color=vector(0.7 - 0.1 * i, 0, 1)) for i in range(n)]  

def crear_cilindros(posicion, radio, n):
    if n == 0:
        return []
    return [cylinder(pos=posicion + vector(0, (6.0 + 5.5 * i) * radio, 0), 
                     radius=5 * (1 + 0.5 * i),
                     axis=vector(0, 8 * (1 + 0.5 * i), 2),
                     color=vector(0, 0.5 + 0.1 * i, 1)) 
            for i in range(n)]

piramides = crear_piramides(vector(-20, 0, 0), 5, 5)
esferas = crear_esferas(vector(-8, 0, 0), 5, 5)
cilindros = crear_cilindros(vector(5, 0, 0), 5, 5)

posiciones_iniciales = {obj: vector(obj.pos) for obj in piramides + esferas + cilindros}

async def mover_objeto(objetos, eje, velocidad, limite_pos, limite_neg):
    direccion = 1 
    while True:
        for obj in objetos:
            obj.pos += eje * velocidad * direccion
        
        primer_obj = objetos[0]
        if primer_obj.pos.x > limite_pos or primer_obj.pos.y > limite_pos or primer_obj.pos.z > limite_pos:
            direccion = -1 
        elif primer_obj.pos.x < limite_neg or primer_obj.pos.y < limite_neg or primer_obj.pos.z < limite_neg:
            direccion = 1  
        
        await asyncio.sleep(0.02)  

async def main():
    asyncio.create_task(mover_objeto(piramides, vector(1, 0, 0), 0.2, -50, -10))  
    asyncio.create_task(mover_objeto(esferas, vector(1.2, 0, 0), 1.2, 100, -50)) 
    asyncio.create_task(mover_objeto(cilindros, vector(0, 0.7, 0), 0.8, 40, 0)) 
    while True:
        await asyncio.sleep(0.02)

def reset_pos():
    for obj in piramides + esferas + cilindros:
        obj.pos = posiciones_iniciales[obj]

def cambiar_colores():
    for obj in piramides + esferas + cilindros:
        obj.color = color_aleatorio()

def tecla_presionada(evt):
    tecla = evt.key.lower()
    if tecla == 'r':
        reset_pos()
    elif tecla == 's':
        cambiar_colores()

scene.bind("keydown", tecla_presionada)

asyncio.run(main())

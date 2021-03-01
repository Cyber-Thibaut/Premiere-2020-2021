from math import *
from ion import *
from kandinsky import *
from math import *
from random import randint
from time import monotonic

### PROGRAM CONSTANTS
# Display
SCREEN_WIDTH = 320
SCREEN_HEIGHT = 240
VIDEO_HALF_HEIGHT = SCREEN_HEIGHT // 2

COLUMN_WIDTH = 16
NUMBER_OF_COLUMNS = SCREEN_WIDTH // COLUMN_WIDTH
FOV = pi / 3
WALL_HEIGHT = SCREEN_HEIGHT // 4

# Movement
ROTATION_SPEED = 2*pi / 8
RUNNING_SPEED = 1

# Surfaces IDs
CEILING = 0
FLOOR = 1
WALL_EMPTY = 2
WALL_STANDARD = 3
WALL_FANCY = 4
WALL_SPECIAL_A = 5
WALL_SPECIAL_B = 6
WALL_SPECIAL_C = 7

MAZE_SIZE = 17
MAZES = [
    994639892451692017993627844655427188346119489096700102527510313302320457573868616417279,
    994639136329297165277925056994599494901591635504316814914476715640179960969549973159935,
    994638899191857351225063837897269868434453723710226411561032419934171038551468501237759,
    994638903127657620198142832056217335350998827328484167051085993695318850524015157706751,
        ]
HIGHLIGHTS = [WALL_FANCY, WALL_SPECIAL_A, WALL_SPECIAL_B, WALL_SPECIAL_C]
### IMAGES DEFINITION
def draw_sprite(rects, x, depth, xCenter, yCenter, scale, offset):
    invDepth = 1/depth
    ratio = int(scale * invDepth)
    y = VIDEO_HALF_HEIGHT + offset * invDepth
    for (px, py, dx, dy, color) in rects:
        fill_rect(int(x + ratio * (px - xCenter)), int(y + ratio * (py - yCenter)), int(dx * ratio), int(dy * ratio), color)

def sprite_key(x, depth):
    rects = [
            (2,0,1,9,(255,181,49)),
            (0,9,1,3,(255,181,49)),
            (4,9,1,3,(255,181,49)),
            (1,9,3,1,(255,181,49)),
            (1,11,3,1,(255,181,49)),
            (2,1,3,3,(255,181,49)),
            ]
    draw_sprite(rects, x, depth, 2.5, 6, 5, 0)
KEY = (sprite_key, 13)

def sprite_pumpkin(x, depth):
    rects = [
            (2,0,6,1,(204,102,51)),
            (2,7,6,1,(204,102,51)),
            (0,1,10,6,(204,102,51)),
            (8,3,1,1,(51,51,51)),
            (3,3,1,1,(51,51,51)),
            (4,1,1,2,(51,51,51)),
            (4,5,1,1,(51,51,51)),
            (5,6,1,1,(51,51,51)),
            (3,6,1,1,(51,51,51)),
            (2,5,1,1,(51,51,51)),
            (6,5,1,1,(51,51,51)),
            (7,6,1,1,(51,51,51)),
            (8,5,1,1,(51,51,51)),
            (7,2,1,2,(51,51,51)),
            ]
    draw_sprite(rects, x, depth, 5, 4, 5, 50)
PUMPKIN = (sprite_pumpkin, 25)

SPRITES = [((MAZE_SIZE - 0.5, MAZE_SIZE - 1.5), KEY)]
### HELPERS
def unit(x, y):
    n = sqrt(x**2 + y**2)
    return x/n, y/n

def rotate(x, y, angle):
    cosa, sina = cos(angle), sin(angle)
    return cosa * x - sina * y, sina * x + cosa * y

def buildLens(x, y, fov):
    ratio = tan(fov / 2.0)
    return (ratio * y, - ratio * x)

def blend(c1, c2, a = 0.5):
    b = 1 - a
    return (a * c1[0] + b * c2[0], a * c1[1] + b * c2[1], a * c1[2] + b * c2[2])

def angle(x, y, x2, y2):
    res = atan2(y, x) - atan2(y2, x2)
    while res < pi: res += 2*pi
    while res > pi: res -= 2*pi
    return res

def nThBit(x, n):
    return (x >> n) & 1

def numberOfSprites(): return len(SPRITES)
def spritePosition(index): return SPRITES[index][0]
def spriteImage(index): return SPRITES[index][1][0]
def spriteHalfWidth(index): return SPRITES[index][1][1]

def startingPosition(): return (0.5, 1.5), (1, 0)

def wall(mapId, x, y):
    if nThBit(MAZES[mapId], x + MAZE_SIZE * y) == 0: return WALL_EMPTY
    if x % 3 == 0 and y % 3 == 0: return HIGHLIGHTS[mapId]
    return WALL_STANDARD

def prompt(mapId, x, y):
    if (floor(x), floor(y)) == (MAZE_SIZE - 1, MAZE_SIZE - 2): return "Grab Key"
    return str(mapId) + "/4"

def interact(x, y):
    if (floor(x), floor(y)) == (MAZE_SIZE - 1, MAZE_SIZE - 2): return True
    return False

def randomSprites(mapId, n = 5):
    res = []
    for i in range(n):
        x, y = 0, 0
        while nThBit(MAZES[mapId], x + MAZE_SIZE * y) == 1:
            x, y = randint(0, MAZE_SIZE - 1), randint(0, MAZE_SIZE - 1)
        res.append(((x + 0.5, y + 0.5), PUMPKIN))
    return res

### DISPLAY MODULE
def transparent(wallId):
    return wallId == WALL_EMPTY

def color(wallId):
    if wallId == CEILING: return (33, 33, 33)
    elif wallId == FLOOR: return (48, 48, 48)
    elif wallId == WALL_STANDARD: return (62, 62, 62)
    elif wallId == WALL_FANCY: return (190, 110, 50)
    elif wallId == WALL_SPECIAL_A: return (50, 0, 80)
    elif wallId == WALL_SPECIAL_B: return (90, 255, 0)
    elif wallId == WALL_SPECIAL_C: return (255, 0, 0)
    return (247, 16, 247)

def castingParameters(x, y, rayX, rayY):
    stepX, stepY = None, None
    if rayX == 0: stepX, stepY = 1, 0
    elif rayY == 0: stepX, stepY = 0, 1
    else: stepX, stepY = abs(1/rayX), abs(1/rayY)

    travelX, tileStepX = ((x % 1) * stepX, -1) if rayX < 0 else ((1 - x % 1) * stepX, 1)
    travelY, tileStepY = ((y % 1) * stepY, -1) if rayY < 0 else ((1 - y % 1) * stepY, 1)

    return (stepX, stepY), (tileStepX, tileStepY), (travelX, travelY)

def castRay(x, y, camX, camY, lensX, lensY, angle, mapId):
    rayX, rayY = camX + angle * lensX, camY + angle * lensY
    tileX, tileY = floor(x), floor(y)

    (stepX, stepY), (tileStepX, tileStepY), (travelX, travelY) = castingParameters(x, y, rayX, rayY)

    hit = False
    hitVertical = False
    while not hit:
        if travelX < travelY:
            travelX += stepX
            tileX += tileStepX
            hitVertical = True
        else:
            travelY += stepY
            tileY += tileStepY
            hitVertical = False
        hit = not(transparent(wall(mapId, tileX, tileY)))

    dist = ((tileX - x + (1 - tileStepX) / 2) * stepX) if hitVertical else ((tileY - y + (1 - tileStepY) / 2) * stepY)
    dist *= sqrt(camX**2 + camY**2)

    return (tileX, tileY), abs(dist), hitVertical

def fetchSprites(x, y, camX, camY, lensX, lensY, mapId):
    number = numberOfSprites()
    res = []
    for index in range(number):
        spriteX, spriteY = spritePosition(index)
        spriteX, spriteY = spriteX - x, spriteY - y
        invDet = 1 / (lensX * camY - lensY * camX)
        transformX, transformY = invDet * (camY * spriteX - camX * spriteY), invDet * (lensX * spriteY - lensY * spriteX)
        if transformY > 0:
            spriteOnscreenX = int(SCREEN_WIDTH / 2 * (1 + transformX / transformY))
            column = spriteOnscreenX // COLUMN_WIDTH
            if column >= 0 and column < NUMBER_OF_COLUMNS:
                lastColumnOfSprite = (spriteOnscreenX + spriteHalfWidth(index) / transformY) // COLUMN_WIDTH + 1
                if lastColumnOfSprite >= NUMBER_OF_COLUMNS: lastColumnOfSprite = NUMBER_OF_COLUMNS - 1
                res.append((lastColumnOfSprite, transformY, spriteOnscreenX, column, index))
    res.sort()
    return res

def drawSurfacesAndSprites(x, y, camX, camY, mapId):
    zBuffer = [None] * NUMBER_OF_COLUMNS
    lensX, lensY = buildLens(camX, camY, FOV)
    sprites = fetchSprites(x, y, camX, camY, lensX, lensY, mapId)
    nextSprite = 0
    for column in range(NUMBER_OF_COLUMNS):
        (wallX, wallY), distance, hasHitNS = castRay(x, y, camX, camY, lensX, lensY, 2 * column / (NUMBER_OF_COLUMNS - 1) - 1, mapId)
        height = min(int(WALL_HEIGHT / distance), VIDEO_HALF_HEIGHT) if distance > 0 else VIDEO_HALF_HEIGHT
        fill_rect(column * COLUMN_WIDTH, 0, COLUMN_WIDTH, VIDEO_HALF_HEIGHT - height, color(CEILING))
        fill_rect(column * COLUMN_WIDTH, VIDEO_HALF_HEIGHT + height, COLUMN_WIDTH, VIDEO_HALF_HEIGHT - height, color(FLOOR))
        wallColor = color(wall(mapId, wallX, wallY))
        if (hasHitNS):
            wallColor = blend(wallColor, (0, 0, 0), 0.9)
        fill_rect(column * COLUMN_WIDTH, VIDEO_HALF_HEIGHT - height, COLUMN_WIDTH, 2 * height, wallColor)
        zBuffer[column] = distance
        feed = True
        while nextSprite < len(sprites) and feed:
            lastCol, depth, screenX, midCol, index = sprites[nextSprite]
            if lastCol == column:
                if depth < zBuffer[midCol]:
                    spriteImage(index)(screenX, depth)
                nextSprite += 1
            else:
                feed = False


def drawPrompt(x, y, camX, camY, mapId):
    message = prompt(mapId, x, y)
    draw_string(message, SCREEN_WIDTH - (len(message) + 1) * 10, SCREEN_HEIGHT - 46, 'white', 'black')

def drawFrame(x, y, camX, camY, mapId):
    drawSurfacesAndSprites(x, y, camX, camY, mapId)
    drawPrompt(x, y, camX, camY, mapId)

### GAMEPLAY MODULE
def move(x, y, dirX, dirY, speed, mapId):
    dx, dy = unit(dirX, dirY)
    xNew, yNew = x + speed * dx, y + speed * dy
    if transparent(wall(mapId, floor(xNew), floor(yNew))):
        return xNew, yNew
    return x, y

def handleKeys(dt, mapId, x, y, camX, camY):
    redraw = False
    if keydown(KEY_LEFTPARENTHESIS):
        camX, camY = rotate(camX, camY, dt * ROTATION_SPEED)
        redraw = True
    elif keydown(KEY_RIGHTPARENTHESIS):
        camX, camY = rotate(camX, camY, - dt * ROTATION_SPEED)
        redraw = True

    if keydown(KEY_UP):
        x, y = move(x, y, camX, camY, dt * RUNNING_SPEED, mapId)
        redraw = True
    elif keydown(KEY_DOWN):
        x, y = move(x, y, camX, camY, - dt * RUNNING_SPEED, mapId)
        redraw = True
    if keydown(KEY_LEFT):
        x, y = move(x, y, camY, - camX, - dt * RUNNING_SPEED, mapId)
        redraw = True
    elif keydown(KEY_RIGHT):
        x, y = move(x, y, camY, - camX, dt * RUNNING_SPEED, mapId)
        redraw = True

    if keydown(KEY_OK):
        if interact(x, y):
            redraw, mapId, ((x, y), (camX, camY)) = True, (mapId + 1), startingPosition()
            del SPRITES[1:]
            if mapId < len(MAZES):
                SPRITES.extend(randomSprites(mapId))

    return (redraw, x, y, camX, camY, mapId)

### MAIN
def main():
    # Init
    game_map = 0
    (game_x, game_y), (game_camX, game_camY) = startingPosition()
    SPRITES.extend(randomSprites(game_map))

    redraw = True
    time, dt = monotonic(), 0

    # Run loop
    while game_map < len(MAZES):
        if redraw:
            drawFrame(game_x, game_y, game_camX, game_camY, game_map)
            redraw = False

        dt = monotonic() - time
        time += dt
        redraw, game_x, game_y, game_camX, game_camY, game_map = handleKeys(dt, game_map, game_x, game_y, game_camX, game_camY)

    draw_string("You escaped the labyrinth.", 30, 111, 'white', 'black')

print("Launch with 'main()'.\nArrow keys to move.\nParentheses to look around.\nFind the four keys to escape.")

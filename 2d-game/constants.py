import pyglet

# window properties
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 600
LEFT_BORDER = 9
RIGHT_BORDER = 755
BOTTOM_BORDER = 10
TOP_BORDER = 585
# spaceship properties
SPACESHIP_SPEED = 3
SPACESHIP_HEIGHT = 48
SPACESHIP_WIDTH = 48
# game elements properties
ROCKET_SPEED = 6
ENEMY_SPEED = 6
GAME_OVER_X = WINDOW_WIDTH/2 - 300
GAME_OVER_Y = WINDOW_HEIGHT/2 + 100
# game over properties
LINE_HEIGHT = 60
FONT_SIZE = 24

batch = pyglet.graphics.Batch()
batch_game_over = pyglet.graphics.Batch()
background = pyglet.graphics.Group(0)
foreground = pyglet.graphics.Group(1)
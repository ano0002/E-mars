import math

def sprite_distance(sprite1,sprite2):
    return math.sqrt((sprite1.rect.centerx-sprite2.rect.centerx)**2+(sprite1.rect.centery-sprite2.rect.centery)**2)

def x_y_components(angle,length):
    angle = math.radians(angle)
    return [math.cos(angle)*length,math.sin(angle)*length]
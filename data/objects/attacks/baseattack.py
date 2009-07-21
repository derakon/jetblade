import jetblade
import physicsobject
import polygon
import logger
from vector2d import Vector2D

import pygame

def getClassName():
    return 'BaseAttack'

## This class represents a simple melee attack, with a bounding polygon, a 
# duration, a positional offset from another object, and a damage rating.
# Note that this attack does not have any associated graphics (hence why we're
# working with Polygons directly instead of Sprites). 
class BaseAttack(physicsobject.PhysicsObject):
    ## Instantiate a BaseAttack
    def __init__(self, points, offset, owner, duration, damage):
        ## Time left until this object should die
        self.remainingTime = duration
        ## Damage dealt on contact
        self.damage = damage
        ## Positional offset from owner
        self.offset = offset
        ## Owner of the attack
        self.owner = owner
        physicsobject.PhysicsObject.__init__(self, owner.loc.add(offset), 'empty')
        ## Bounding polygon
        newPolygon = polygon.Polygon([Vector2D(p) for p in points])
        self.sprite.overridePolygon(newPolygon)


    ## Update. Keep our location up to date and check our counter
    def update(self):
        logger.debug("Updating base attack at",self.loc)
        self.loc = self.owner.loc.add(self.offset)
        self.remainingTime -= 1
        if self.remainingTime <= 0:
            return False
        return True

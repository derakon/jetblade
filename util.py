import jetblade
import constants
import line
import logger
from vector2d import Vector2D

import math
import os
import pygame
from pygame.locals import *
import sys
import random

## @package util
# The functions in util are general utility functions that are not tied to any
# specific class.


## Retrieves the location of the user's home directory, depending on OS.
def getHomePath():
    if sys.platform in ['win32', 'cygwin']:
        return os.environ.get('APPDATA')
    else: # Assume OSX/Linux; both should work
        return os.environ.get('HOME')


## Retrieve the text from the clipboard, using different methods depending on
# OS.
def getClipboardText():
    if sys.platform in ['win32', 'cygwin']:
        import win32clipboard
        win32clipboard.OpenClipboard()
        text = ''
        if win32clipboard.IsClipboardFormatAvailable(win32clipboard.CF_TEXT):
            text = win32clipboard.GetClipboardData()
        win32clipboard.CloseClipboard()
        return text
    else:
        import subprocess
        p = subprocess.Popen(['pbpaste'], stdout=subprocess.PIPE)
        retcode = p.wait()
        data = p.stdout.read()
        return data


## Create the display surface. 
def setupScreen():
    mode = 0
    if jetblade.configManager.getConfigValue('fullscreen'):
        mode = pygame.FULLSCREEN
    screen = pygame.display.set_mode((constants.sw, constants.sh), mode)
    if screen is None:
        # Give up on fullscreen mode
        screen = pygame.display.set_mode((constants.sw, constants.sh))
    return screen


## Fade the given surface by the given alpha amount.
def fadeAlpha(surface, alpha):
    if alpha < 255:
        if alpha < 0:
            alpha = 0
        # \todo: This is TERRIBLE. Figure out why pixels_alpha occasionally
        # throws an exception
        try:
            pixels_alpha = pygame.surfarray.pixels_alpha(surface)
            pixels_alpha[...] = (pixels_alpha * (alpha / 255.0)).astype(Numeric.UInt8)
            del pixels_alpha
        except Exception, e:
            return

## Adjust the passed-in location so that it is relative to the upper-left
# corner of the passed-in rect.
def adjustLocForRect(loc, rect):
    result = Vector2D(loc.x - rect.topleft[0], loc.y - rect.topleft[1])
    return result


## As adjustLocForRect, but move the rect so it is centered at the given
# location first.
def adjustLocForCenter(loc, center, rect):
    rect.centerx = center.x
    rect.centery = center.y
    return adjustLocForRect(loc, rect)


## Get an image from the list based on the provided index.
def getDrawFrame(index, surfaces):
    return surfaces[int(index) % len(surfaces)]


## Limit angles to the range [0, 2pi].
def clampDirection(dir):
    result = dir % (math.pi * 2)
    return result


## Select one of a group of options that are provided as a dict, mapping option
# to the weight for that option. For example, if all weights are 1, then every
# option has an equal chance of being chosen. If one weight were 5, then the
# corresponding object would be 5 times more likely to be chosen than its 
# neighbors. 
def pickWeightedOption(options):
    if options is None:
        return None
    totalWeights = 0
    for type, weight in options.iteritems():
        totalWeights += weight
    index = random.randint(0, totalWeights)
    for type, weight in options.iteritems():
        index -= weight
        if index <= 0:
            return type
    print "Failed to select an option from",options
    return None


## Convert a 3x3 array of 0s, 1s, and 2s into a list of scalar values:
# - 0: add zero to result
# - 1: add 2^index to result
# - 2: represents "either 0 or 1", so duplicate the results and add 2^index
# to half the elements.
# This is used to quickly represent which spaces that are adjacent to a given
# block are occupied.
def adjacencyArrayToSignatures(kernel):
    # First, convert the 2D array into a 1D array
    array = []
    for row in kernel:
        array.extend(row)

    result = [0]
    for i in range(0, len(array)):
        temp = []
        if array[i] == 2:
            temp.extend(result)
        if array[i] in [1, 2]:
            result = [x + 2**i for x in result]
        result.extend(temp)
    # Uniquify list on our way out.
    return dict().fromkeys(result).keys()


## Load a class from the named module. Assumes that the module includes a
# function getClassName() that indicates the name of the class to load.
def loadDynamicClass(path):
    try:
        logger.debug("Loading module",path)
        # In order to allow arbitrary naming of these classes, we first 
        # import a function that tells us the name of the class, then we 
        # import the class itself.
        # \todo: seems like this could be done better somehow.
        nameFuncModule = __import__(path, globals(), locals(), ['getClassName'])
        className = nameFuncModule.getClassName()
        classModule = __import__(path, globals(), locals(), [className])
        initFunc = getattr(classModule, className)
        return initFunc
    except Exception, e:
        logger.fatal("Failed to load module",path,":",e)


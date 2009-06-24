import util
import constants
import jetblade

## Animations are sequences of images and the logic needed to know when, where, 
# and how to display them. Every animation is tied to a single polygon for 
# collision detection. Animations may loop, may change the location of the 
# animated object after completing, and may have specialized logic for
# when to change animation frames.
class Animation:
    ## Create a new Animation instance.
    def __init__(self, group, name, polygon, shouldLoop, 
                 updateRate, updateFunc, drawOffset, moveOffset):
        
        ## The collection of animations that this one is a part of. For example,
        # in "player/run-l" the group would be "player"
        self.group = group
        
        ## The specific animation name, e.g. "run-l"
        self.name = name

        ## The polygon that is used for all frames of the animation.
        self.polygon = polygon

        ## If true, the animation will automatically loop when it runs out of
        # frames, and will therefore never complete.
        # If false, then once the final frame is reached, the animation will
        # stay on that frame indefinitely.
        self.shouldLoop = shouldLoop

        ## If this is not None, then it specifies how rapidly animation frames
        # update in terms of physics updates (1 => 1 frame advanced per 
        # physics update).
        self.updateRate = updateRate

        ## If this is not None, then it specifies a function that accepts the
        # object being animated and returns the number of frames to advace the
        # animation.
        self.updateFunc = updateFunc

        ## A positional offset used when drawing.
        self.drawOffset = tuple(drawOffset)

        ## The amount to move the animated object after the animation completes.
        # This value is never used if the animation is set to loop, as the
        # animation never completes.
        self.moveOffset = tuple(moveOffset)

        ## Individual frames of the animation.
        self.frames = jetblade.imageManager.loadAnimation(self.group + '/' + self.name)
        ## Current frame of animation; an index into self.frames.
        self.frame = 0
        
        ## Tracks if we've reached the end of the animation.
        self.isComplete = 0

    ## Advance self.frames. If self.updateFunc is specified, use that;
    # otherwise, use self.updateRate. Return True if the animation is complete,
    # False otherwise.
    def update(self, owner):
        util.debug("Updating animation",self.name,"from frame",self.frame,)
        if self.frame < len(self.frames) - 1 or self.shouldLoop:
            if self.updateFunc is not None:
                self.frame += self.updateFunc(owner)
            else:
                self.frame += self.updateRate
        if (not self.shouldLoop and not self.isComplete and 
                self.frame >= len(self.frames) - 1):
            # Animation done
            return True
        util.debug("to frame",self.frame)
        return False

    ## Our owner calls this if the animation is complete; we update its state
    # as necessary now. Currently that just means applying self.moveOffset
    def completeAnimation(self, owner):
        if not self.isComplete:
            owner.loc[0] += self.moveOffset[0]
            owner.loc[1] += self.moveOffset[1]
            self.isComplete = 1

    ## Draw the animation to screen, taking self.drawOffset into account.
    def draw(self, screen, camera, loc, scale = 1):
        drawLoc = loc
        if self.drawOffset != (0, 0) or scale != 1:
            drawLoc = util.roundVector([(loc[0] + self.drawOffset[0]) * scale, 
                                        (loc[1] + self.drawOffset[1]) * scale])
        surface = util.getDrawFrame(self.frame, self.frames)
        jetblade.imageManager.drawGameObjectAt(screen, surface, drawLoc, camera, scale)
        if jetblade.logLevel == constants.LOG_DEBUG:
            self.polygon.draw(screen, loc, camera)
            gridLoc = util.realspaceToGridspace(loc)
            jetblade.imageManager.drawText(screen,
                    ['%d' % gridLoc[0],
                     '%d' % gridLoc[1],
                     '%d' % loc[0],
                     '%d' % loc[1]],
                    util.adjustLocForCenter((drawLoc[0] + 25, drawLoc[1] + 25), camera, screen.get_rect()),
                    0, constants.tinyFontSize)

    ## Reset internal state so the animation can be cleanly re-run.
    def reset(self):
        util.debug("Animation",self.name,"resetting")
        self.frame = 0
        self.isComplete = 0
            
    def getPolygon(self):
        return self.polygon

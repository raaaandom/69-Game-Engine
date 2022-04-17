from pygame.transform import scale

#GameObject class
class GameObject():

    # used to resize an object texture by a f(factor) amount
    def resizeTexture(self, fx, fy):
        self.texture = scale(self.texture, (self.texture.get_width()*fx, self.texture.get_height()*fy))

    def setTextureSize(self, x, y):
        self.texture = scale(self.texture, (x, y))

    def __init__(
        
        self,
        x = 0, y = 0, z = 0,
        on = False, texture = None,
        overwritable = False,
        movedByKeyboard = False, movementSpeedX = 0, movementSpeedY = 0,
        causesCollision = False, receivesCollision = False,
        animationState = None, animationCounter = 0, animationFrame = 0, animationLastState = 0,
        fontContent = None, fontType = None, fontColor = (255,255,255),
        groupID = 0,
        levelEditorSelected = False, levelEditorSelectable = False

    ) -> None:
        
        self.x = x # X position of the object, default = 0

        self.y = y # Y position of the object, default = 0

        self.z = z # Z position of the object, default = 0
                   # Can only go from 0 to Z_LAYERS

        self.on = on # Determines if the object should be rendered, default = False
                     # False = Not rendered, True = Rendered

        self.texture = texture # Defines the texture that the object should be rendered with, default = None
                               # None = No texture, pygame.Surface = Has texture

        self.overwritable = overwritable # Defines if an object can be overwrited when needed, default = False
                                         # False = Can't be overwrited, True = Can be overwrited

        self.movedByKeyboard = movedByKeyboard # Defines if an object should be moved when movement keys are pressed, default = False
                                               # False = Not moved by keyboard, True = Moved by keyboard

        self.movementSpeedX = movementSpeedX # Defines the movement speed of objects that get moved by keyboard, default = 0
        self.movementSpeedY = movementSpeedY # Can be any numerical value (possibly integer)

        self.causesCollision = causesCollision # Defines if the object should be an obstacle to the other objects, default = False
                                               # False = It isn't an obstacle, True = It is an obstacle

        self.receivesCollision = receivesCollision # Defines if the object should be obstacled by the other objects, default = False
                                                   # False = It isn't obstacled, True = It is obstacled
                                                   
        self.animationState = animationState # Defines the animationset to consider when animating an object 

        self.animationCounter = animationCounter # Contains the elapsed frames since the last frameswitch

        self.animationFrame = animationFrame # Contains the number of the frame which is currently being printed

        self.animationLastState = animationLastState # Contains the animation state from the last frame

        self.fontContent = fontContent # The value of the text, default None
                                       # None = object is not a text, "text" = object is a text

        self.fontType = fontType # Defines the font used when rendering the fontContent string, default = None
                                 # None = no font, index of fontList = yes font (viva allah)
        
        self.fontColor = fontColor # The color of the font, default white (255,255,255 // 0xffffff)
                                   # Can be any tuple with 3 numerical value elements ranging from 0 to 255

        self.groupID = groupID # Defines the group of the obj, default = 0
                               # Can be any integer

        self.levelEditorSelected = levelEditorSelected # Defines if the object is selected in the level editor
        self.levelEditorSelectable = levelEditorSelectable # Defines if the object can selected in the level editor
#GameObject class
class GameObject():

    def __init__(
        
        self,
        x = 0, y = 0, z = 0,
        on = False, texture = None,
        overwritable = False,
        movedByKeyboard = False, movementSpeedX = 0, movementSpeedY = 0,

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
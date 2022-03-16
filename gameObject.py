#GameObject class
class GameObject():

    def __init__(
        
        self,
        x = 0, y = 0, z = 0,
        on = False, texture = None,
        overwritable = False

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
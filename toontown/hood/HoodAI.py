# Embedded file name: toontown.hood.HoodAI


class HoodAI:
    """
    AI-side representation of everything in a single neighborhood.
    
    One subclass of this class exists for every type neighborhood(safezone, coghq) 
    in the game.
    HoodAIs are responsible for spawning all SuitPlanners, BuildingMgrs,
    and other hood objects, etc.
    """
    HOOD = None

    def __init__(self, air):
        self.air = air

    def createZone(self):
        pass

    def spawnObjects(self):
        pass
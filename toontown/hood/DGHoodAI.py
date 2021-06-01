# Embedded file name: toontown.hood.DGHoodAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedDGFlowerAI import DistributedDGFlowerAI
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.safezone import ButterflyGlobals
from toontown.safezone.DistributedButterflyAI import DistributedButterflyAI
from toontown.classicchars import DistributedDaisyAI

class DGHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.DaisyGardens

    def createZone(self):
        self.notify.info('Creating zone... Daisy Gardens')
        self.classicChar = None
        SZHoodAI.createZone(self)
        self.butterflies = []
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-daisy', True):
                self.createClassicChar()
        self.spawnObjects()
        self.flower = DistributedDGFlowerAI(self.air)
        self.flower.generateWithRequired(self.HOOD)
        self.createButterflies()
        return

    def createButterflies(self):
        playground = ButterflyGlobals.DG
        for area in range(ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for b in range(ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                butterfly = DistributedButterflyAI(self.air)
                butterfly.setArea(playground, area)
                butterfly.setState(0, 0, 0, 1, 1)
                butterfly.generateWithRequired(self.HOOD)
                self.butterflies.append(butterfly)

    def createClassicChar(self):
        self.classicChar = DistributedDaisyAI.DistributedDaisyAI(self.air)
        self.classicChar.generateWithRequired(self.safezone)
        self.classicChar.start()
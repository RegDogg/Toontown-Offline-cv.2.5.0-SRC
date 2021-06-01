# Embedded file name: toontown.hood.BRHoodAI
from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.classicchars import DistributedPlutoAI

class BRHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.TheBrrrgh

    def createZone(self):
        self.notify.info('Creating zone... The Brrrgh')
        self.classicChar = None
        SZHoodAI.createZone(self)
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-pluto', True):
                self.createClassicChar()
        self.spawnObjects()
        return

    def createClassicChar(self):
        self.classicChar = DistributedPlutoAI.DistributedPlutoAI(self.air)
        self.classicChar.generateWithRequired(self.safezone)
        self.classicChar.start()
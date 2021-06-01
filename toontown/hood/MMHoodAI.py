# Embedded file name: toontown.hood.MMHoodAI
from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.classicchars import DistributedMinnieAI

class MMHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.MinniesMelodyland

    def createZone(self):
        self.notify.info("Creating zone... Minnie's Melodyland")
        self.classicChar = None
        SZHoodAI.createZone(self)
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-minnie', True):
                self.createClassicChar()
        self.spawnObjects()
        return

    def createClassicChar(self):
        self.classicChar = DistributedMinnieAI.DistributedMinnieAI(self.air)
        self.classicChar.generateWithRequired(self.safezone)
        self.classicChar.start()
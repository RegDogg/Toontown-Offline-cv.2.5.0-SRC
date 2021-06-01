# Embedded file name: toontown.hood.DLHoodAI
from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.toon import NPCToons
from toontown.classicchars import DistributedDonaldAI

class DLHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.DonaldsDreamland

    def createZone(self):
        self.notify.info("Creating zone... Donald's Dreamland")
        self.classicChar = None
        SZHoodAI.createZone(self)
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-donald-dreamland', True):
                self.createClassicChar()
        self.spawnObjects()
        return

    def createClassicChar(self):
        self.classicChar = DistributedDonaldAI.DistributedDonaldAI(self.air)
        self.classicChar.generateWithRequired(self.safezone)
        self.classicChar.start()
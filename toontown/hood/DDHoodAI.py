# Embedded file name: toontown.hood.DDHoodAI
from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedFishingSpotAI import DistributedFishingSpotAI
from toontown.safezone.DistributedBoatAI import DistributedBoatAI
from toontown.classicchars import DistributedDonaldDockAI
from toontown.toon import NPCToons
from SZHoodAI import SZHoodAI

class DDHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.DonaldsDock

    def createZone(self):
        self.notify.info("Creating zone... Donald's Dock")
        self.classicChar = None
        SZHoodAI.createZone(self)
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-donald-dock', True):
                self.createClassicChar()
        self.spawnObjects()
        self.boat = DistributedBoatAI(self.air)
        self.boat.generateWithRequired(self.safezone)
        return

    def createClassicChar(self):
        self.classicChar = DistributedDonaldDockAI.DistributedDonaldDockAI(self.air)
        self.classicChar.generateWithRequired(self.safezone)
        self.classicChar.start()
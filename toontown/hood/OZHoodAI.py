# Embedded file name: toontown.hood.OZHoodAI
from SZHoodAI import SZHoodAI
from toontown.toonbase import ToontownGlobals
from toontown.distributed.DistributedTimerAI import DistributedTimerAI
from toontown.classicchars import DistributedChipAI
from toontown.classicchars import DistributedDaleAI

class OZHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.OutdoorZone

    def createZone(self):
        self.notify.info("Creating zone... Chip 'n Dale's Acorn Acres")
        self.classicCharChip = None
        self.classicCharDale = None
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-chip-and-dale', True):
                self.createClassicChars()
        SZHoodAI.createZone(self, False)
        self.timer = DistributedTimerAI(self.air)
        self.timer.generateWithRequired(self.HOOD)
        self.spawnObjects()
        return

    def spawnObjects(self):
        SZHoodAI.spawnObjects(self)
        filename = self.air.genDNAFileName(self.HOOD)
        self.air.dnaSpawner.spawnObjects(filename, self.HOOD)

    def createClassicChars(self):
        self.classicCharChip = DistributedChipAI.DistributedChipAI(self.air)
        self.classicCharChip.generateWithRequired(self.safezone)
        self.classicCharChip.start()
        self.classicCharDale = DistributedDaleAI.DistributedDaleAI(self.air, self.classicCharChip.doId)
        self.classicCharDale.generateWithRequired(self.safezone)
        self.classicCharDale.start()
        self.classicCharChip.setDaleId(self.classicCharDale.doId)
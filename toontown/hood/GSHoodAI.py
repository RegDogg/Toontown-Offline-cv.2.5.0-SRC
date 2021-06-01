# Embedded file name: toontown.hood.GSHoodAI
from toontown.toonbase import ToontownGlobals
from toontown.hood import HoodAI
from toontown.building.DistributedBuildingMgrAI import DistributedBuildingMgrAI
from toontown.classicchars import DistributedGoofySpeedwayAI

class GSHoodAI(HoodAI.HoodAI):
    notify = directNotify.newCategory('HoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.GoofySpeedway

    def __init__(self, air):
        HoodAI.HoodAI.__init__(self, air)
        self.notify.info('Creating zone... Goofy Speedway')
        self.classicChar = None
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-goofy', True):
                self.createClassicChar()
        self.createZone()
        self.spawnObjects()
        return

    def createZone(self):
        HoodAI.HoodAI.createZone(self)
        self.air.dnaStoreMap[self.HOOD] = self.air.loadDNA(self.air.genDNAFileName(self.HOOD)).generateData()
        self.buildingMgr = DistributedBuildingMgrAI(self.air, self.HOOD, self.air.dnaStoreMap[self.HOOD], self.air.trophyMgr)

    def spawnObjects(self):
        HoodAI.HoodAI.spawnObjects(self)
        filename = self.air.genDNAFileName(self.HOOD)
        self.air.dnaSpawner.spawnObjects(filename, self.HOOD)

    def createClassicChar(self):
        self.classicChar = DistributedGoofySpeedwayAI.DistributedGoofySpeedwayAI(self.air)
        self.classicChar.generateWithRequired(self.HOOD)
        self.classicChar.start()
# Embedded file name: toontown.hood.GZHoodAI
from toontown.hood.HoodAI import *
from toontown.toonbase import ToontownGlobals
from toontown.safezone.DistributedGolfKartAI import DistributedGolfKartAI
from toontown.golf import GolfGlobals

class GZHoodAI(HoodAI):
    notify = directNotify.newCategory('HoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.GolfZone

    def __init__(self, air):
        HoodAI.__init__(self, air)
        self.notify.info("Creating zone... Chip 'n Dale's MiniGolf")
        self.golfKarts = []
        self.createZone()

    def createZone(self):
        self.spawnObjects()

    def spawnObjects(self):
        HoodAI.spawnObjects(self)
        filename = self.air.genDNAFileName(self.HOOD)
        self.air.dnaSpawner.spawnObjects(filename, self.HOOD)
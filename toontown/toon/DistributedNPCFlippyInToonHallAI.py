# Embedded file name: toontown.toon.DistributedNPCFlippyInToonHallAI
from DistributedNPCToonAI import *

class DistributedNPCFlippyInToonHallAI(DistributedNPCToonAI):

    def __init__(self, air, npcId, questCallback = None, hq = 0):
        DistributedNPCToonAI.__init__(self, air, npcId, questCallback)
# Embedded file name: toontown.hood.TTHoodAI
from toontown.toonbase import ToontownGlobals
from SZHoodAI import SZHoodAI
from toontown.safezone import ButterflyGlobals
from toontown.safezone.DistributedButterflyAI import DistributedButterflyAI
from toontown.toon import NPCToons
from toontown.election.DistributedElectionEventAI import DistributedElectionEventAI
from toontown.classicchars import DistributedMickeyAI
from direct.task import Task
import time

class TTHoodAI(SZHoodAI):
    notify = directNotify.newCategory('SZHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.ToontownCentral

    def createZone(self):
        self.notify.info('Creating zone... Toontown Central')
        SZHoodAI.createZone(self)
        self.spawnObjects()
        self.butterflies = []
        self.createButterflies()
        self.classicChar = None
        if simbase.config.GetBool('want-classic-chars', True):
            if simbase.config.GetBool('want-mickey', True):
                if not config.GetBool('want-doomsday', False):
                    self.createClassicChar()
        if self.air.config.GetBool('want-doomsday', False):
            self.spawnElection()
        return

    def spawnElection(self):
        election = self.air.doFind('ElectionEvent')
        if election is None:
            election = DistributedElectionEventAI(self.air)
            election.generateWithRequired(self.HOOD)
        election.b_setState('Idle')
        if self.air.config.GetBool('want-hourly-doomsday', False):
            self.__startElectionTick()
        return

    def __startElectionTick(self):
        ts = time.time()
        nextHour = 3600 - ts % 3600
        taskMgr.doMethodLater(nextHour, self.__electionTick, 'election-hourly')

    def __electionTick(self, task):
        task.delayTime = 3600
        toons = self.air.doFindAll('DistributedToon')
        if not toons:
            return task.again
        election = self.air.doFind('ElectionEvent')
        if election:
            state = election.getState()
            if state[0] == 'Idle':
                taskMgr.doMethodLater(10, election.b_setState, 'election-start-delay', extraArgs=['Event'])
        if not election:
            election = DistributedElectionEventAI(self.air)
            election.generateWithRequired(self.HOOD)
            election.b_setState('Idle')
            taskMgr.doMethodLater(10, election.b_setState, 'election-start-delay', extraArgs=['Event'])
        return task.again

    def createButterflies(self):
        playground = ButterflyGlobals.TTC
        for area in range(ButterflyGlobals.NUM_BUTTERFLY_AREAS[playground]):
            for b in range(ButterflyGlobals.NUM_BUTTERFLIES[playground]):
                butterfly = DistributedButterflyAI(self.air)
                butterfly.setArea(playground, area)
                butterfly.setState(0, 0, 0, 1, 1)
                butterfly.generateWithRequired(self.HOOD)
                self.butterflies.append(butterfly)

    def createClassicChar(self):
        self.classicChar = DistributedMickeyAI.DistributedMickeyAI(self.air)
        self.classicChar.generateWithRequired(self.safezone)
        self.classicChar.start()
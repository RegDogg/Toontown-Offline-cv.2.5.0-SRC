# Embedded file name: toontown.ai.DistributedGreenToonEffectMgrAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedGreenToonEffectMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedGreenToonEffectMgrAI')

    def addGreenToonEffect(self):
        pass
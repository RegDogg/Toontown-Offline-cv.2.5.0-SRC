# Embedded file name: toontown.ai.DistributedPolarPlaceEffectMgrAI
from direct.directnotify import DirectNotifyGlobal
from direct.distributed.DistributedObjectAI import DistributedObjectAI

class DistributedPolarPlaceEffectMgrAI(DistributedObjectAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPolarPlaceEffectMgrAI')

    def addPolarPlaceEffect(self):
        pass
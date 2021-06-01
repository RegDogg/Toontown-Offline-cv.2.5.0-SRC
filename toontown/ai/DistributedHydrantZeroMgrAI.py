# Embedded file name: toontown.ai.DistributedHydrantZeroMgrAI
from direct.directnotify import DirectNotifyGlobal
from toontown.ai.DistributedPhaseEventMgrAI import DistributedPhaseEventMgrAI

class DistributedHydrantZeroMgrAI(DistributedPhaseEventMgrAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedHydrantZeroMgrAI')
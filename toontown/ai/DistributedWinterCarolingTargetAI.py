# Embedded file name: toontown.ai.DistributedWinterCarolingTargetAI
from direct.directnotify import DirectNotifyGlobal
from toontown.ai.DistributedScavengerHuntTargetAI import DistributedScavengerHuntTargetAI

class DistributedWinterCarolingTargetAI(DistributedScavengerHuntTargetAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedWinterCarolingTargetAI')
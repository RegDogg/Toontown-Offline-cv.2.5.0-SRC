# Embedded file name: toontown.pets.PetActionFSM
from direct.directnotify import DirectNotifyGlobal
from direct.fsm import FSM
from direct.interval.IntervalGlobal import *
from direct.task import Task
from direct.distributed.ClockDelta import globalClockDelta
from direct.showbase.PythonUtil import lerp
from toontown.pets import PetTricks
from toontown.toon import DistributedToonAI

class PetActionFSM(FSM.FSM):
    notify = DirectNotifyGlobal.directNotify.newCategory('PetActionFSM')

    def __init__(self, pet):
        FSM.FSM.__init__(self, PetActionFSM.__name__)
        self.pet = pet
        self.trickSerialNum = 0

    def destroy(self):
        self.cleanup()

    def enterChase(self, target):
        PetActionFSM.notify.debug('enterChase: %s' % target)
        self.pet.unstickFSM.request('on')

    def exitChase(self):
        self.pet.unstickFSM.request('off')

    def enterFlee(self, chaser):
        PetActionFSM.notify.debug('enterFlee: %s' % chaser)
        self.pet.unstickFSM.request('on')

    def exitFlee(self):
        self.pet.unstickFSM.request('off')

    def enterInspectSpot(self, spot):
        PetActionFSM.notify.debug('enterInspectSpot')
        self.pet.unstickFSM.request('on')

    def exitInspectSpot(self):
        self.pet.unstickFSM.request('off')

    def enterHeal(self, avatar):
        PetActionFSM.notify.debug('enterHeal')
        avatar.toonUp(3)

    def enterTrick(self, avatar, trickId):
        PetActionFSM.notify.debug('enterTrick')
        if not self.pet.isLockedDown():
            self.pet.lockPet()
        self.pet.sendUpdate('doTrick', [trickId, globalClockDelta.getRealNetworkTime()])

        def finish(avatar = avatar, trickId = trickId, self = self):
            if hasattr(self.pet, 'brain'):
                healRange = PetTricks.TrickHeals[trickId]
                aptitude = self.pet.getTrickAptitude(trickId)
                healAmt = int(lerp(healRange[0], healRange[1], aptitude))
                if healAmt:
                    for avId, av in self.pet._getFullNearbyToonDict().items():
                        if isinstance(av, DistributedToonAI.DistributedToonAI):
                            av.toonUp(healAmt)

                self.pet._handleDidTrick(trickId)
                if not self.pet.isLockedDown():
                    self.pet.unlockPet()
                messenger.send(self.getTrickDoneEvent())

        self.trickDoneEvent = 'trickDone-%s-%s' % (self.pet.doId, self.trickSerialNum)
        self.trickSerialNum += 1
        self.trickFinishIval = Sequence(WaitInterval(PetTricks.TrickLengths[trickId]), Func(finish), name='petTrickFinish-%s' % self.pet.doId)
        self.trickFinishIval.start()

    def getTrickDoLaterName(self):
        return 'petTrickDoLater-%s' % self.pet.doId

    def getTrickDoneEvent(self):
        return self.trickDoneEvent

    def exitTrick(self):
        if self.trickFinishIval.isPlaying():
            self.trickFinishIval.finish()
        del self.trickFinishIval
        if self.pet.isLockedDown():
            self.pet.unlockPet()
        del self.trickDoneEvent
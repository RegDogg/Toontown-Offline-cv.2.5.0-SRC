# Embedded file name: toontown.coghq.FactoryExterior
from direct.directnotify import DirectNotifyGlobal
from toontown.battle import BattlePlace
from direct.gui.DirectGui import *
from direct.fsm import ClassicFSM, State
from direct.fsm import State
from otp.distributed.TelemetryLimiter import RotationLimitToH, TLGatherAllAvs
from toontown.toonbase import ToontownGlobals, TTLocalizer
from toontown.building import Elevator
from pandac.PandaModules import *
from toontown.toon import NPCToons
from toontown.dna import DNAUtil
from otp.nametag import NametagGlobals

class FactoryExterior(BattlePlace.BattlePlace):
    notify = DirectNotifyGlobal.directNotify.newCategory('FactoryExterior')
    dnaFile = 'phase_9/dna/cog_hq_sellbot_11200.xml'

    def __init__(self, loader, parentFSM, doneEvent):
        BattlePlace.BattlePlace.__init__(self, loader, doneEvent)
        self.parentFSM = parentFSM
        self.elevatorDoneEvent = 'elevatorDone'
        self.visInterest = None
        self.visGroups = None
        return

    def load(self):
        self.fsm = ClassicFSM.ClassicFSM('FactoryExterior', [State.State('start', self.enterStart, self.exitStart, ['walk',
          'tunnelIn',
          'teleportIn',
          'doorIn']),
         State.State('walk', self.enterWalk, self.exitWalk, ['stickerBook',
          'teleportOut',
          'tunnelOut',
          'DFA',
          'doorOut',
          'elevator',
          'stopped',
          'WaitForBattle',
          'battle']),
         State.State('stopped', self.enterStopped, self.exitStopped, ['walk', 'teleportOut', 'elevator']),
         State.State('stickerBook', self.enterStickerBook, self.exitStickerBook, ['walk',
          'DFA',
          'WaitForBattle',
          'battle',
          'elevator']),
         State.State('WaitForBattle', self.enterWaitForBattle, self.exitWaitForBattle, ['battle', 'walk']),
         State.State('battle', self.enterBattle, self.exitBattle, ['walk', 'teleportOut', 'died']),
         State.State('DFA', self.enterDFA, self.exitDFA, ['DFAReject', 'teleportOut', 'tunnelOut']),
         State.State('DFAReject', self.enterDFAReject, self.exitDFAReject, ['walk']),
         State.State('teleportIn', self.enterTeleportIn, self.exitTeleportIn, ['walk']),
         State.State('teleportOut', self.enterTeleportOut, self.exitTeleportOut, ['teleportIn', 'final', 'WaitForBattle']),
         State.State('doorIn', self.enterDoorIn, self.exitDoorIn, ['walk']),
         State.State('doorOut', self.enterDoorOut, self.exitDoorOut, ['walk']),
         State.State('died', self.enterDied, self.exitDied, ['quietZone']),
         State.State('tunnelIn', self.enterTunnelIn, self.exitTunnelIn, ['walk']),
         State.State('tunnelOut', self.enterTunnelOut, self.exitTunnelOut, ['final']),
         State.State('elevator', self.enterElevator, self.exitElevator, ['walk', 'stopped']),
         State.State('final', self.enterFinal, self.exitFinal, ['start'])], 'start', 'final')
        self.parentFSM.getStateNamed('factoryExterior').addChild(self.fsm)
        BattlePlace.BattlePlace.load(self)

    def unload(self):
        self.parentFSM.getStateNamed('factoryExterior').removeChild(self.fsm)
        del self.fsm
        BattlePlace.BattlePlace.unload(self)

    def enter(self, requestStatus):
        self.zoneId = requestStatus['zoneId']
        self.updateVis(self.zoneId)
        BattlePlace.BattlePlace.enter(self)
        self.fsm.enterInitialState()
        base.playMusic(self.loader.music, looping=1, volume=0.8)
        self.loader.geom.reparentTo(render)
        self.nodeList = [self.loader.geom]
        self.loader.hood.startSky()
        self._telemLimiter = TLGatherAllAvs('FactoryExterior', RotationLimitToH)
        self.accept('doorDoneEvent', self.handleDoorDoneEvent)
        self.accept('DistributedDoor_doorTrigger', self.handleDoorTrigger)
        NametagGlobals.setMasterArrowsOn(1)
        self.createNPC()
        self.tunnelOriginList = base.cr.hoodMgr.addLinkTunnelHooks(self, self.nodeList, self.zoneId)
        how = requestStatus['how']
        self.fsm.request(how, [requestStatus])

    def exit(self):
        self._telemLimiter.destroy()
        del self._telemLimiter
        self.loader.hood.stopSky()
        self.fsm.requestFinalState()
        self.loader.music.stop()
        for node in self.tunnelOriginList:
            node.removeNode()

        del self.tunnelOriginList
        del self.nodeList
        self.removeNPC()
        self.ignoreAll()
        if self.visInterest:
            base.cr.removeInterest(self.visInterest)
        BattlePlace.BattlePlace.exit(self)

    def enterTunnelOut(self, requestStatus):
        fromZoneId = self.zoneId - self.zoneId % 100
        tunnelName = base.cr.hoodMgr.makeLinkTunnelName(self.loader.hood.id, fromZoneId)
        requestStatus['tunnelName'] = tunnelName
        BattlePlace.BattlePlace.enterTunnelOut(self, requestStatus)

    def enterTeleportIn(self, requestStatus):
        base.localAvatar.setPosHpr(-34, -350, 0, -28, 0, 0)
        BattlePlace.BattlePlace.enterTeleportIn(self, requestStatus)

    def enterTeleportOut(self, requestStatus):
        BattlePlace.BattlePlace.enterTeleportOut(self, requestStatus, self.__teleportOutDone)

    def __teleportOutDone(self, requestStatus):
        hoodId = requestStatus['hoodId']
        zoneId = requestStatus['zoneId']
        avId = requestStatus['avId']
        shardId = requestStatus['shardId']
        if hoodId == self.loader.hood.hoodId and zoneId == self.zoneId and shardId == None:
            self.fsm.request('teleportIn', [requestStatus])
        elif hoodId == ToontownGlobals.MyEstate:
            self.getEstateZoneAndGoHome(requestStatus)
        else:
            self.doneStatus = requestStatus
            messenger.send(self.doneEvent)
        return

    def exitTeleportOut(self):
        BattlePlace.BattlePlace.exitTeleportOut(self)

    def enterElevator(self, distElevator, skipDFABoard = 0):
        self.accept(self.elevatorDoneEvent, self.handleElevatorDone)
        self.elevator = Elevator.Elevator(self.fsm.getStateNamed('elevator'), self.elevatorDoneEvent, distElevator)
        if skipDFABoard:
            self.elevator.skipDFABoard = 1
        distElevator.elevatorFSM = self.elevator
        self.elevator.load()
        self.elevator.enter()

    def exitElevator(self):
        self.ignore(self.elevatorDoneEvent)
        self.elevator.unload()
        self.elevator.exit()
        del self.elevator

    def detectedElevatorCollision(self, distElevator):
        self.fsm.request('elevator', [distElevator])

    def handleElevatorDone(self, doneStatus):
        self.notify.debug('handling elevator done event')
        where = doneStatus['where']
        if where == 'reject':
            if hasattr(base.localAvatar, 'elevatorNotifier') and base.localAvatar.elevatorNotifier.isNotifierOpen():
                pass
            else:
                self.fsm.request('walk')
        elif where == 'exit':
            self.fsm.request('walk')
        elif where == 'factoryInterior':
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        elif where == 'stageInterior':
            self.doneStatus = doneStatus
            messenger.send(self.doneEvent)
        else:
            self.notify.error('Unknown mode: ' + where + ' in handleElevatorDone')

    def updateVis(self, zone):
        if not self.visGroups:
            dna = loader.loadDNA(self.dnaFile)
            self.visGroups = DNAUtil.getVisGroups(dna)
        visZones = []
        for vg in self.visGroups:
            if vg.getZone() == zone:
                visZones = vg.getVisibleZones()
                visZones.append(ToontownGlobals.SellbotFactoryExt)
                break

        if not self.visInterest:
            self.visInterest = base.cr.addInterest(base.localAvatar.defaultShard, visZones, 'cogHQVis')
        else:
            base.cr.alterInterest(self.visInterest, base.localAvatar.defaultShard, visZones)

    def doEnterZone(self, newZoneId):
        self.updateVis(newZoneId)
        if newZoneId != self.zoneId:
            if newZoneId != None:
                base.cr.sendSetZoneMsg(newZoneId)
                self.notify.debug('Entering Zone %d' % newZoneId)
            self.zoneId = newZoneId
        return

    def createNPC(self):
        if not config.GetBool('want-fnaf', True):
            return
        else:
            self.npc = NPCToons.createLocalNPC(7010)
            self.npc.reparentTo(self.loader.geom)
            self.npc.setPos(13, -77, 0)
            self.npc.setH(180)
            self.npc.putOnSuit('mb', False, False)
            cNode = CollisionNode('fnaf-npc')
            cNode.addSolid(CollisionSphere(0, 0, 0, 1))
            cNode.setCollideMask(ToontownGlobals.WallBitmask)
            cnp = self.npc.attachNewNode(cNode)
            self.accept('enterfnaf-npc', self.__handleNPC)
            self.panel = aspect2d.attachNewNode(CardMaker('fnaf-npc-panel').generate())
            self.panel.setTexture(loader.loadTexture('phase_9/maps/tt_fnaf_news.jpg'))
            self.panel.setScale(2, 1, 1.5)
            self.panel.setPos(-1, 0, -0.75)
            guiButton = loader.loadModel('phase_3/models/gui/quit_button')
            imageList = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR'))
            playButton = DirectButton(text='Accept this job', image=imageList, relief=None, text_scale=0.05, command=self.__handleNPCPanelStatus, extraArgs=[1])
            exitButton = DirectButton(text=TTLocalizer.FishingExit, image=imageList, relief=None, text_scale=0.05, command=self.__handleNPCPanelStatus, extraArgs=[0])
            playButton.wrtReparentTo(self.panel)
            exitButton.wrtReparentTo(self.panel)
            playButton.setPos(playButton, (0.69, 0, -0.69))
            exitButton.setPos(exitButton, (-0.69, 0, -0.69))
            self.panel.stash()
            return

    def __handleNPC(self, entry):
        self.fsm.request('stopped')
        self.panel.unstash()

    def __handleNPCPanelStatus(self, mode = 0):
        if mode:
            base.cr.fnafMgr.enterMinigame()
        else:
            self.panel.stash()
            self.fsm.request('walk')

    def removeNPC(self):
        if not config.GetBool('want-fnaf', True):
            return
        self.npc.cleanup()
        self.npc.removeNode()
        self.panel.removeNode()
        del self.npc

    def enterZoneStreetBattle(self, newZoneId):
        pass

    def debugStartMinigame(self, zoneId, minigameId):
        self.doneStatus = {'loader': 'minigame',
         'where': 'minigame',
         'hoodId': self.loader.hood.id,
         'zoneId': zoneId,
         'shardId': None,
         'minigameId': minigameId}
        messenger.send(self.doneEvent)
        return
# Embedded file name: toontown.hood.SellbotHQAI
from CogHoodAI import CogHoodAI
from toontown.toonbase import ToontownGlobals
from toontown.suit.DistributedSellbotBossAI import DistributedSellbotBossAI
from toontown.coghq.DistributedFactoryElevatorExtAI import DistributedFactoryElevatorExtAI
from toontown.building.DistributedVPElevatorAI import DistributedVPElevatorAI
from toontown.coghq.DistributedCogHQDoorAI import DistributedCogHQDoorAI
from toontown.building import DoorTypes
from toontown.building import FADoorCodes

class SellbotHQAI(CogHoodAI):
    notify = directNotify.newCategory('CogHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.SellbotHQ

    def __init__(self, air):
        CogHoodAI.__init__(self, air)
        self.notify.info('Creating zone... Sellbot HQ')
        self.createZone()

    def createDoor(self):
        interiorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.INT_COGHQ, ToontownGlobals.SellbotHQ, doorIndex=0)
        for i in range(4):
            exteriorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, ToontownGlobals.SellbotLobby, doorIndex=i, lockValue=FADoorCodes.SB_DISGUISE_INCOMPLETE)
            exteriorDoor.setOtherDoor(interiorDoor)
            exteriorDoor.zoneId = ToontownGlobals.SellbotHQ
            exteriorDoor.generateWithRequired(ToontownGlobals.SellbotHQ)
            exteriorDoor.sendUpdate('setDoorIndex', [i])
            self.doors.append(exteriorDoor)

        interiorDoor.setOtherDoor(self.doors[0])
        interiorDoor.zoneId = ToontownGlobals.SellbotLobby
        interiorDoor.generateWithRequired(ToontownGlobals.SellbotLobby)
        interiorDoor.sendUpdate('setDoorIndex', [0])
        self.doors.append(interiorDoor)

    def createZone(self):
        CogHoodAI.createZone(self)
        self.createLobbyManager(DistributedSellbotBossAI, ToontownGlobals.SellbotLobby)
        self.vpElevator = self.createElevator(DistributedVPElevatorAI, self.lobbyMgr, ToontownGlobals.SellbotLobby, ToontownGlobals.SellbotLobby, boss=True)
        self.createDoor()
        self.createSuitPlanner(self.HOOD)
        self.createSuitPlanner(ToontownGlobals.SellbotFactoryExt)
        mins = ToontownGlobals.FactoryLaffMinimums[0]
        self.frontEntrance = self.createElevator(DistributedFactoryElevatorExtAI, self.air.factoryMgr, ToontownGlobals.SellbotFactoryExt, ToontownGlobals.SellbotFactoryInt, 0, minLaff=mins[0])
        self.sideEntrance = self.createElevator(DistributedFactoryElevatorExtAI, self.air.factoryMgr, ToontownGlobals.SellbotFactoryExt, ToontownGlobals.SellbotFactoryInt, 1, minLaff=mins[1])
        self.createBoardingGroup(self.air, [self.vpElevator.doId], ToontownGlobals.SellbotLobby, 8)
        self.factories = [self.frontEntrance.doId, self.sideEntrance.doId]
        self.createBoardingGroup(self.air, self.factories, ToontownGlobals.SellbotFactoryExt)
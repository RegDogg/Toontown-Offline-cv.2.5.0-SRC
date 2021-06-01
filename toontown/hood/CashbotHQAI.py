# Embedded file name: toontown.hood.CashbotHQAI
from CogHoodAI import CogHoodAI
from toontown.toonbase import ToontownGlobals
from toontown.suit.DistributedCashbotBossAI import DistributedCashbotBossAI
from toontown.coghq.DistributedMintElevatorExtAI import DistributedMintElevatorExtAI
from toontown.building.DistributedCFOElevatorAI import DistributedCFOElevatorAI
from toontown.coghq.DistributedCogHQDoorAI import DistributedCogHQDoorAI
from toontown.building import DoorTypes
from toontown.building import FADoorCodes

class CashbotHQAI(CogHoodAI):
    notify = directNotify.newCategory('CogHoodAI')
    notify.setInfo(True)
    HOOD = ToontownGlobals.CashbotHQ

    def __init__(self, air):
        CogHoodAI.__init__(self, air)
        self.notify.info('Creating zone... Cashbot HQ')
        self.createZone()

    def createDoor(self):
        interiorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.INT_COGHQ, self.HOOD, doorIndex=0)
        exteriorDoor = DistributedCogHQDoorAI(self.air, 0, DoorTypes.EXT_COGHQ, ToontownGlobals.CashbotLobby, doorIndex=0, lockValue=FADoorCodes.CB_DISGUISE_INCOMPLETE)
        exteriorDoor.setOtherDoor(interiorDoor)
        exteriorDoor.zoneId = self.HOOD
        exteriorDoor.generateWithRequired(self.HOOD)
        exteriorDoor.sendUpdate('setDoorIndex', [0])
        self.doors.append(exteriorDoor)
        interiorDoor.setOtherDoor(exteriorDoor)
        interiorDoor.zoneId = ToontownGlobals.CashbotLobby
        interiorDoor.generateWithRequired(ToontownGlobals.CashbotLobby)
        interiorDoor.sendUpdate('setDoorIndex', [0])
        self.doors.append(interiorDoor)

    def createZone(self):
        CogHoodAI.createZone(self)
        self.createLobbyManager(DistributedCashbotBossAI, ToontownGlobals.CashbotLobby)
        self.cfoElevator = self.createElevator(DistributedCFOElevatorAI, self.lobbyMgr, ToontownGlobals.CashbotLobby, ToontownGlobals.CashbotLobby, boss=True)
        self.createDoor()
        self.createSuitPlanner(self.HOOD)
        mins = ToontownGlobals.FactoryLaffMinimums[1]
        self.cointMint = self.createElevator(DistributedMintElevatorExtAI, self.air.mintMgr, self.HOOD, ToontownGlobals.CashbotMintIntA, 0, minLaff=mins[0])
        self.dollarMint = self.createElevator(DistributedMintElevatorExtAI, self.air.mintMgr, self.HOOD, ToontownGlobals.CashbotMintIntB, 1, minLaff=mins[1])
        self.bullionMint = self.createElevator(DistributedMintElevatorExtAI, self.air.mintMgr, self.HOOD, ToontownGlobals.CashbotMintIntC, 2, minLaff=mins[2])
        self.createBoardingGroup(self.air, [self.cfoElevator.doId], ToontownGlobals.CashbotLobby, 8)
        self.mints = [self.cointMint.doId, self.dollarMint.doId, self.bullionMint.doId]
        self.createBoardingGroup(self.air, self.mints, ToontownGlobals.CashbotHQ)
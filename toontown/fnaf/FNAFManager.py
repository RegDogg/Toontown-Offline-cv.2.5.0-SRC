# Embedded file name: toontown.fnaf.FNAFManager
from pandac.PandaModules import *
from direct.showbase.DirectObject import *
from direct.gui.DirectGui import *
from toontown.toonbase import ToontownGlobals
from toontown.toonbase import TTLocalizer

class FNAFManager(DirectObject):

    def __init__(self):
        self._isPlaying = False
        self.won = False

    def enterMinigame(self):
        place = base.cr.playGame.getPlace()
        if not hasattr(place, 'debugStartMinigame'):
            base.cr.doFind('DistributedSuitInvasionManager').displayMsgs(['ERROR: Redeem this code at a playground!'])
            return
        self._isPlaying = True
        localAvatar.b_setParent(ToontownGlobals.SPHidden)
        self.__hoodId = place.loader.hood.id
        place.debugStartMinigame(1, 1234)
        localAvatar.laffMeter.obscure(1)
        localAvatar.chatMgr.fsm.request('otherDialog')
        base.camera.reparentTo(render)
        base.camera.iPosHprScale()
        self.accept('FNAF-gameComplete', self.__handleGameDone)
        base.startGame()

    def __handleGameDone(self):
        self.bgm = loader.loadMusic('phase_9/audio/bgm/fnaf_end.ogg')
        self.bgm.setLoopCount(0)
        self.bgm.play()
        self.panel = aspect2d.attachNewNode(CardMaker('fnaf-npc-panel').generate())
        self.panel.setTexture(loader.loadTexture('phase_9/maps/tt_fnaf_paycheck.jpg'))
        self.panel.setScale(2, 1, 1.5)
        self.panel.setPos(-1, 0, -0.75)
        self.infoText = OnscreenText(text="Enter code 'paycheck' for one time payment", align=TextNode.ARight, pos=(-0.3, -0.1), parent=base.a2dTopRight, fg=(1, 1, 1, 1), font=base.cogFont)
        guiButton = loader.loadModel('phase_3/models/gui/quit_button')
        imageList = (guiButton.find('**/QuitBtn_UP'), guiButton.find('**/QuitBtn_DN'), guiButton.find('**/QuitBtn_RLVR'))
        exitButton = DirectButton(text=TTLocalizer.FishingExit, image=imageList, relief=None, text_scale=0.05, command=self.leaveMinigame, extraArgs=[])
        exitButton.wrtReparentTo(self.panel)
        exitButton.setPos(exitButton, (-0.69, 0, -0.69))
        base.transitions.irisIn()
        self.won = True
        return

    def leaveMinigame(self):
        base.leaveGame()
        self.ignore('FNAF-gameComplete')
        self._isPlaying = False
        if self.won:
            self.panel.removeNode()
            self.bgm.stop()
            self.infoText.removeNode()
        base.cam.iPosHprScale()
        localAvatar.laffMeter.obscure(0)
        localAvatar.chatMgr.fsm.request('mainMenu')
        base.cr.playGame.enter(self.__hoodId, self.__hoodId, 0)

    def isPlaying(self):
        return self._isPlaying
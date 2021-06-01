# Embedded file name: toontown.fnaf.Camera
from direct.gui.DirectGui import *
from direct.gui.OnscreenImage import OnscreenImage
from direct.fsm.FSM import FSM
from panda3d.core import *
import random, math
from direct.interval.IntervalGlobal import *
from toontown.toonbase import ToontownGlobals
CameraPoints = (((66.6, -20.7, 7.2), (0, 0, 0), 'Hallway'),
 ((-112.694, -35.0187, 23.3818), (-3.71871, -19.9784, -0.604477), 'Left Room'),
 ((-110, 95, 40), (0, -25.9784, -0.604477), 'Control Room (Camera 1)'),
 ((-130, 95, 40), (0, -25.9784, -0.604477), 'Control Room (Camera 2)'),
 ((65.0658, 195.454, 13.3796), (-3.71871, -19.9784, -0.604477), 'Safe Room'))
CameraButtonPos = {'Hallway': (0.825, 0, 0.15),
 'LeftRoom': (0.28, 0, 0.2),
 'SafeRoom': (0.825, 0, 0.865),
 'ControlRoomCamera1': (0.38, 0, 0.625),
 'ControlRoomCamera2': (0.2, 0, 0.625)}

class CameraBrowser(NodePath):

    def __init__(self, controls):
        NodePath.__init__(self, 'CameraBrowser')
        self.reparentTo(render2d)
        self.controls = controls
        frameColor = (1, 1, 1, 0.95)
        leftFrame = DirectFrame(frameSize=(-0.98, -0.96, -0.98, 0.98), frameColor=frameColor, parent=self)
        rightFrame = DirectFrame(frameSize=(0.96, 0.98, -0.98, 0.98), frameColor=frameColor, parent=self)
        bottomFrame = DirectFrame(frameSize=(-0.98, 0.98, -0.98, -0.96), frameColor=frameColor, parent=self)
        topFrame = DirectFrame(frameSize=(-0.98, 0.98, 0.98, 0.96), frameColor=frameColor, parent=self)
        self.title = OnscreenText(parent=topFrame, pos=(-0.6, 0.8), fg=(1, 1, 1, 1), text='', font=base.cogFont, scale=0.16)
        self.titleCircle = OnscreenImage(image='phase_9/maps/rec.png', parent=self.title, pos=(-0.85, 0, 0.84), scale=0.07)
        self.exitButton = DirectButton(text='Close', text_fg=(1, 1, 1, 1), scale=0.07, pos=(0, 0, -0.9), text_bg=(0, 0, 0, 0.75), text_font=base.cogFont, command=self.controls.request, extraArgs=['Flashlight'])
        self.titleCircle.setTransparency(1)

    def load(self):
        self.map = base.a2dBottomRight.attachNewNode(CardMaker('fnaf-map').generate())
        texture = 'phase_9/maps/tt_fnaf_map.png'
        self.map.setTexture(loader.loadTexture(texture))
        self.map.setTransparency(1)
        self.map.setPos(self.map, (-1.25, 0, 0))
        self.map.setScale(1.15)
        self.map.stash()
        self.cameras = []
        for index, (pos, hpr, name) in enumerate(CameraPoints):
            self.createCamera(index, pos, hpr, name)

        self.__cameraIndex = 0

    def setCamera(self, index):
        self.disableCurrentCamera()
        self.__cameraIndex = index
        self.enableCurrentCamera()

    def disableCurrentCamera(self):
        name, button, camNP = self.cameras[self.__cameraIndex]
        base.camera.reparentTo(render)
        base.camera.setPos(render, 0, 0, 0)
        button['state'] = DGG.NORMAL

    def enableCurrentCamera(self):
        name, button, camNP = self.cameras[self.__cameraIndex]
        if name == 'Left Room':
            if random.randrange(1, 201) == 200 and not base.mickeySpawned:
                base.mickeySpawned = True
                base.level.poster.stash()
                base.level.posterpn.unstash()
                base.pnspawn.play()
        base.camera.reparentTo(camNP)
        base.camera.setPos(camNP, 0, 30, -10)
        if random.randrange(1, 101) == 100:
            base.unnerve.play()
        cleanName = name.replace(' ', '')
        cleanName = cleanName.replace('(', '')
        cleanName = cleanName.replace(')', '')
        messenger.send('cameraSeeing%s' % cleanName)
        button['state'] = DGG.DISABLED

    def createCamera(self, index, pos, hpr, name):
        camNP = render.attachNewNode(Camera('cam'))
        camNP.setPos(pos)
        camNP.setHpr(hpr)
        cleanName = name.replace(' ', '')
        cleanName = cleanName.replace('(', '')
        cleanName = cleanName.replace(')', '')
        pos = CameraButtonPos.get(cleanName)
        button = DirectFrame(parent=self.map, frameColor=(1, 1, 1, 0), frameSize=(-0.16, 0.29, -0.15, 0.15), pos=pos, scale=0.2, state=DGG.NORMAL)
        button.bind(DGG.B1PRESS, lambda x: self.setCamera(index))
        button.setTextureOff()
        self.cameras.append((name, button, camNP))

    def blinkCircle(self, task):
        time = int(task.time)
        method = (self.titleCircle.hide, self.titleCircle.show)[time % 2]
        method()
        return task.cont

    def show(self):
        NodePath.show(self)
        self.exitButton.unstash()
        self.map.unstash()
        self.titleCircle.show()
        taskMgr.doMethodLater(1, self.blinkCircle, 'fnaf-camera-blinkCircle')
        self.enableCurrentCamera()

    def hide(self):
        NodePath.hide(self)
        self.exitButton.stash()
        if hasattr(self, 'map'):
            self.map.stash()
            self.disableCurrentCamera()
        taskMgr.remove('fnaf-camera-blinkCircle')


class CameraControls(FSM):

    def __init__(self):
        FSM.__init__(self, 'CameraControls')
        self.taskName = 'CameraControls-task'
        self.jump = loader.loadModel('phase_9/models/gui/morky_jump')
        self.jump.setScale(3)
        self.browser = CameraBrowser(self)
        self.browser.hide()
        self.browserButton = DirectButton(text='Cameras', text_fg=(1, 1, 1, 1), scale=0.07, pos=(0, 0, -0.9), text_bg=(0, 0, 0, 0.75), text_font=base.cogFont, command=self.request, extraArgs=['Browser'])
        self.browserButton.hide()

    def load(self):
        self.leaveGameButton = DirectButton(text='Quit', text_fg=(1, 1, 1, 1), scale=0.07, pos=(-0.4, 0, -0.9), text_bg=(0, 0, 0, 0.75), text_font=base.cogFont, command=base.cr.fnafMgr.leaveMinigame)

    def unload(self):
        self.leaveGameButton.destroy()

    def enter(self):
        self.demand('Flashlight')
        self.browser.setCamera(0)
        self.browser.disableCurrentCamera()

    def exit(self):
        self.demand('Off')

    def enterFlashlight(self):
        base.cam.setPos(0, -27, 5)
        base.cam.setH(0)
        if not base.mickeySpawned:
            taskMgr.add(self.updateTask, self.taskName)
            self.browserButton.show()
        else:
            self.leaveGameButton.hide()
            base.pncard.unstash()
            jumpIval = Sequence(SoundInterval(base.pnsee, loop=0), Parallel(Func(base.pncard.stash), Func(base.static.unstash), Func(base.timer.exit), Func(base.staticsnd.play), Func(base.level.bgm.stop)), Wait(5), Parallel(Func(base.staticsnd.stop), Func(self.startJump)), Wait(1), Parallel(Func(base.static.reparentTo, aspect2d), Func(self.jump.reparentTo, hidden), Func(base.staticsnd.play), Func(self.jump.stash)), Wait(10), Func(self.finJump))
            jumpIval.start()

    def exitFlashlight(self):
        taskMgr.remove(self.taskName)
        self.browserButton.hide()

    def enterBrowser(self):
        base.timer.addEnergyConsumption('cameraBrowser', 2)
        self.browser.show()

    def exitBrowser(self):
        base.timer.removeEnergyConsumption('cameraBrowser')
        self.browser.hide()

    def startJump(self):
        base.level.exit()
        base.setBackgroundColor(0, 0, 0, 1)
        base.ignore('ranOutOfEnergy')
        base.ignore('gameFailed')
        self.jump.reparentTo(aspect2d)
        self.jump.unstash()
        base.static.reparentTo(hidden)

    def finJump(self):
        base.staticsnd.stop()
        base.static.stash()
        base.setBackgroundColor(ToontownGlobals.DefaultBackgroundColor)
        base.static.reparentTo(hidden)
        base.cr.killClientPNMickey()
        self.exit()

    def updateTask(self, task):
        m = base.mouseWatcherNode
        if m.hasMouse():
            x = m.getMouseX()
            offset = 45
            h = min((x + 1) * offset, 2 * offset)
            h = max(h, -offset)
            h = offset - h
            base.cam.setH(h)
        return task.cont
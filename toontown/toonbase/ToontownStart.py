from pandac.PandaModules import *
import __builtin__
import os
print 'ToontownStart: Loading settings.'
from toontown.toonbase.GameSettings import GameSettings
settings = GameSettings()
settings.loadFromSettings()
from panda3d.core import VirtualFileSystem, ConfigVariableList, Filename
loadPrcFile('config/Config.prc')
vfs = VirtualFileSystem.getGlobalPtr()
mounts = ConfigVariableList('vfs-mount')
for mount in mounts:
    mountfile, mountpoint = (mount.split(' ', 2) + [None, None, None])[:2]
    vfs.mount(Filename(mountfile), Filename(mountpoint), 0)

import glob
for file in glob.glob('resources/*.mf'):
    mf = Multifile()
    mf.openReadWrite(Filename(file))
    names = mf.getSubfileNames()
    for name in names:
        ext = os.path.splitext(name)[1]
        if ext not in ('.jpg', '.jpeg', '.ogg', '.rgb'):
            mf.removeSubfile(name)

    vfs.mount(mf, Filename('/'), 0)

class game:
    name = 'toontown'
    process = 'client'


__builtin__.game = game()
import time
import sys
import random
import __builtin__
try:
    launcher
except:
    from toontown.launcher.TTOffLauncher import TTOffLauncher
    launcher = TTOffLauncher()
    __builtin__.launcher = launcher

print 'ToontownStart: Starting the game.'
if launcher.isDummy():
    http = HTTPClient()
else:
    http = launcher.http
tempLoader = Loader()
backgroundNode = tempLoader.loadSync(Filename('phase_3/models/gui/loading-background'))
from direct.gui import DirectGuiGlobals
print 'ToontownStart: Setting the default font.'
import ToontownGlobals
DirectGuiGlobals.setDefaultFontFunc(ToontownGlobals.getInterfaceFont)
launcher.setPandaErrorCode(7)
import ToonBase
ToonBase.ToonBase()
from pandac.PandaModules import *
if base.win == None:
    print 'Unable to open window; aborting.'
    sys.exit()
launcher.setPandaErrorCode(0)
launcher.setPandaWindowOpen()
ConfigVariableDouble('decompressor-step-time').setValue(0.01)
ConfigVariableDouble('extractor-step-time').setValue(0.01)
backgroundNodePath = aspect2d.attachNewNode(backgroundNode, 0)
backgroundNodePath.setPos(0.0, 0.0, 0.0)
backgroundNodePath.setScale(render2d, VBase3(1))
backgroundNodePath.find('**/fg').setBin('fixed', 20)
backgroundNodePath.find('**/bg').setBin('fixed', 10)
base.graphicsEngine.renderFrame()
DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
DirectGuiGlobals.setDefaultClickSound(base.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
DirectGuiGlobals.setDefaultDialogGeom(loader.loadModel('phase_3/models/gui/dialog_box_gui'))
import TTLocalizer
from otp.otpbase import OTPGlobals
OTPGlobals.setDefaultProductPrefix(TTLocalizer.ProductPrefix)
if base.musicManagerIsValid:
    if config.GetBool('want-tto-theme', False):
        music = base.musicManager.getSound('phase_3/audio/bgm/tt_theme.ogg')
    else:
        music = base.musicManager.getSound('phase_3/audio/bgm/ttr_theme.ogg')
    if music:
        music.setLoop(1)
        music.setVolume(0.9)
        music.play()
    print 'ToontownStart: Loading the default GUI sounds.'
    DirectGuiGlobals.setDefaultRolloverSound(base.loadSfx('phase_3/audio/sfx/GUI_rollover.ogg'))
    DirectGuiGlobals.setDefaultClickSound(base.loadSfx('phase_3/audio/sfx/GUI_create_toon_fwd.ogg'))
else:
    music = None
import ToontownLoader
from direct.gui.DirectGui import *
serverVersion = config.GetString('server-version', 'no_version_set')
buildVersion = 'cv.%s' % config.GetString('build-version', 'no_version_set')
print 'ToontownStart: Build Version:', buildVersion
credit = OnscreenText(text='Powered by Toontown Rewritten', pos=(1.3, 0.935), scale=0.06, fg=Vec4(0, 0, 1, 0.6), align=TextNode.ARight)
credit.setPos(-0.033, -0.065)
credit.reparentTo(base.a2dTopRight)
build = OnscreenText(buildVersion, pos=(-1.3, -0.975), scale=0.06, fg=Vec4(0, 0, 1, 0.6), align=TextNode.ALeft)
build.setPos(0.033, 0.025)
build.reparentTo(base.a2dBottomLeft)
loader.beginBulkLoad('init', TTLocalizer.LoaderLabel, 138, 0, TTLocalizer.TIP_NONE)
from ToonBaseGlobal import *
from direct.showbase.MessengerGlobal import *
from toontown.distributed import ToontownClientRepository
cr = ToontownClientRepository.ToontownClientRepository(serverVersion, launcher)
cr.music = music
del music
base.initNametagGlobals()
base.cr = cr
loader.endBulkLoad('init')
from otp.friends import FriendManager
from otp.distributed.OtpDoGlobals import *
cr.generateGlobalObject(OTP_DO_ID_FRIEND_MANAGER, 'FriendManager')
if not launcher.isDummy() and config.GetBool('want-mini-server', False):
    print 'ToontownStart: Mini-server mode enabled! Using defined game server...'
    base.startShow(cr, launcher.getGameServer())
else:
    print 'ToontownStart: Mini-server mode disabled! Using localhost...'
    base.startShow(cr)
backgroundNodePath.reparentTo(hidden)
backgroundNodePath.removeNode()
del backgroundNodePath
del backgroundNode
del tempLoader
credit.cleanup()
del credit
build.cleanup()
del build
base.loader = base.loader
__builtin__.loader = base.loader
autoRun = ConfigVariableBool('toontown-auto-run', 1)
if autoRun:
    try:
        run()
    except SystemExit:
        raise
    except:
        from direct.showbase import PythonUtil
        print PythonUtil.describeException()
        raise
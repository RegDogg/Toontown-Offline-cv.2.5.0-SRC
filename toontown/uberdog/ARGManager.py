# Embedded file name: toontown.uberdog.ARGManager
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from toontown.toonbase import ToontownGlobals
from otp.speedchat import SpeedChatGlobals
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.hood import ZoneUtil
from pandac.PandaModules import Vec3
Hood2Details = {2665: [(6, 7, 9), 103, 2665],
 1832: [(6, 7, 9), 103, 1832],
 5502: [(6, 7, 9), 103, 5502],
 4612: [(6, 7, 9), 103, 4612],
 3636: [(6, 7, 9), 103, 3636],
 9705: [(6, 7, 9), 103, 9705],
 3823: [(6, 7, 9), 103, 3823]}
Interior2Messages = {2665: ["Mary: Oh, Hello! Oh, Hello! Say, that's the keyword that Doctor Surlee told myself and other shopkeepers just like me to remember. I take it he sent you?", "Mary: The word I'm supposed to remember is 'Sillyness'"],
 1832: ["Melville: Say, you don't look like Doctor Surlee. That is the trigger phrase, though...", "Melville: He told me to remember 'Lafter'"],
 5502: ["HQ Officer: Oh, Surlee sent you? Keep this key safe, he said it's going to be important later on.", "HQ Officer: The word is 'Springy Partlicles' -- Whatever that means."],
 4612: ["Dr. Fret: Aahhh, brilliant. Surlee is up to something again, I'm sure.", "Dr. Fret: He told me to remember 'Creating Equiment'"],
 3636: ["Gus Gooseburger: Keep it down! Surlee didn't give me these gloves to just give the word away.", "Gus Gooseburger: Just kidding! I have no idea why he wanted me to remember this word. It's 'Portil'"],
 9705: ["Drowsy Dave: Huh? Oh, oh! Hi. Surlee's word, right. Uhh...", 'Drowsy Dave: I seem to have dozed off... Professor Flake is a good friend of the Doc, though. I bet he knows.'],
 3823: ['Professor Flake: Hmm? So soon? Surlee told me that something big would be happening whenever he needed this...', 'Professor Flake: I hope that you have a photographic memory like myself, because this is a long one.']}

class ARGManager(DistributedObjectGlobal):
    """
    This is a client-view of the manager that handles everything to do
    with the portable hole ARG event.
    """
    notify = directNotify.newCategory('ARGManager')

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        self.setupPortableHoleEvent()

    def disable(self):
        self.cleanupPortableHoleEvent()
        DistributedObjectGlobal.disable(self)

    def delete(self):
        self.cleanupPortableHoleEvent()
        DistributedObjectGlobal.delete(self)

    def setupPortableHoleEvent(self):

        def phraseSaid(phraseId):
            position, speedchatIndex, destination = Hood2Details.get(base.cr.playGame.getPlace().getZoneId(), [None, None, None])
            if not position or not speedchatIndex or not destination:
                return
            elif speedchatIndex != phraseId:
                return
            else:
                msgBefore, msgAfter = Interior2Messages.get(destination, [None, None])
                if not msgBefore:
                    self.notify.warning('Interior %d has no message definitions!' % destination)
                    return
                taskMgr.doMethodLater(2, base.localAvatar.setSystemMessage, self.uniqueName('arg-before-msg'), extraArgs=[0, msgBefore])
                taskMgr.doMethodLater(7, base.localAvatar.setSystemMessage, self.uniqueName('arg-after-msg'), extraArgs=[0, msgAfter])
                if destination == 3823:
                    taskMgr.doMethodLater(15, base.localAvatar.setSystemMessage, self.uniqueName('arg-after-after-msg'), extraArgs=[0, "'ttr://assets/LL-memo-607630003555.txt'. Keep it safe. I have no idea what it means, but Surlee certainly will."])
                return

        self.accept(SpeedChatGlobals.SCStaticTextMsgEvent, phraseSaid)

    def cleanupPortableHoleEvent(self):
        self.ignore(SpeedChatGlobals.SCStaticTextMsgEvent)
# Embedded file name: toontown.parties.DistributedPartyValentineJukeboxActivityAI
from direct.directnotify import DirectNotifyGlobal
from toontown.parties.DistributedPartyJukeboxActivityBaseAI import DistributedPartyJukeboxActivityBaseAI

class DistributedPartyValentineJukeboxActivityAI(DistributedPartyJukeboxActivityBaseAI):
    notify = DirectNotifyGlobal.directNotify.newCategory('DistributedPartyValentineJukeboxActivityAI')
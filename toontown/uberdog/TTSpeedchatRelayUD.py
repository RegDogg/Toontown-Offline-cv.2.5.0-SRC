# Embedded file name: toontown.uberdog.TTSpeedchatRelayUD
from direct.directnotify import DirectNotifyGlobal
from otp.uberdog.SpeedchatRelayUD import SpeedchatRelayUD

class TTSpeedchatRelayUD(SpeedchatRelayUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTSpeedchatRelayUD')
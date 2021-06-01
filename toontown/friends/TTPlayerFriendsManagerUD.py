# Embedded file name: toontown.friends.TTPlayerFriendsManagerUD
from direct.directnotify import DirectNotifyGlobal
from otp.friends.PlayerFriendsManagerUD import PlayerFriendsManagerUD

class TTPlayerFriendsManagerUD(PlayerFriendsManagerUD):
    notify = DirectNotifyGlobal.directNotify.newCategory('TTPlayerFriendsManagerUD')
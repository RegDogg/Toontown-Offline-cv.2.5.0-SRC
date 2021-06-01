# Embedded file name: toontown.distributed.ShardStatus
import time
from panda3d.core import *
from toontown.toonbase import TTLocalizer
from toontown.battle import SuitBattleGlobals
import gc
import thread
try:
    from psutil import cpu_percent, virtual_memory
    HAS_PSUTIL = True
except ImportError:
    HAS_PSUTIL = False

shard_status_interval = ConfigVariableInt('shard-status-interval', 20, 'How often to send shard status update messages.')
shard_heap_interval = ConfigVariableInt('shard-heap-interval', 60, 'How often to recount objects on the heap (and in garbage).')
shard_status_timeout = ConfigVariableInt('shard-status-timeout', 30, 'The maximum time between receiving shard status update messages before the receiver assumes the shard is no longer online.')

class ShardStatusSender:

    def __init__(self, air):
        self.air = air
        self.interval = None
        self.heap_status = {'objects': 0,
         'garbage': 0}
        return

    def update_heap(self):
        lastUpdate = 0
        while taskMgr.running:
            if lastUpdate < time.time() - shard_heap_interval.getValue():
                self.heap_status = {'objects': len(gc.get_objects()),
                 'garbage': len(gc.garbage)}
                lastUpdate = time.time()
            time.sleep(1.0)

    def start(self):
        globalClock.setAverageFrameRateInterval(shard_status_interval.getValue())
        offlineStatus = {'channel': self.air.ourChannel,
         'offline': True}
        dg = self.air.netMessenger.prepare('shardStatus', [offlineStatus])
        self.air.addPostRemove(dg)
        thread.start_new_thread(self.update_heap, ())
        self.sendStatus()

    def sendStatus(self):
        invasion = None
        if self.air.suitInvasionManager.getInvading():
            cogType = self.air.suitInvasionManager.suitName
            cogName = SuitBattleGlobals.SuitAttributes[cogType]['name']
            if self.air.suitInvasionManager.specialSuit == 1:
                cogName += ' (' + TTLocalizer.Skeleton + ')'
            elif self.air.suitInvasionManager.specialSuit == 2:
                cogName = TTLocalizer.SkeleReviveCogName % {'cog_name': cogName}
            invasion = (cogName, '%d/%d' % (self.air.suitInvasionManager.spawnedSuits, self.air.suitInvasionManager.numSuits))
        status = {'channel': self.air.ourChannel,
         'districtId': self.air.distributedDistrict.doId,
         'districtName': self.air.distributedDistrict.name,
         'population': self.air.districtStats.getAvatarCount(),
         'avg-frame-rate': round(globalClock.getAverageFrameRate(), 5),
         'invasion': invasion,
         'heap': self.heap_status}
        if HAS_PSUTIL:
            status['cpu-usage'] = cpu_percent(interval=None, percpu=True)
            status['mem-usage'] = virtual_memory().percent
        self.air.netMessenger.send('shardStatus', [status])
        if self.interval is not None:
            self.interval.remove()
        self.interval = taskMgr.doMethodLater(shard_status_interval.getValue(), self.__interval, 'ShardStatusInterval')
        return

    def __interval(self, task):
        self.interval = None
        self.sendStatus()
        return task.done


class ShardStatusReceiver:

    def __init__(self, air):
        self.air = air
        self.shards = {}
        self.air.netMessenger.accept('shardStatus', self, self._handleStatus)

    def _handleStatus(self, status):
        channel = status.get('channel')
        if channel is None:
            return
        elif status.get('offline'):
            if channel in self.shards:
                del self.shards[channel]
            return
        else:
            status['lastSeen'] = int(time.time())
            self.shards[channel] = status
            return

    def getShards(self):
        expiryTime = int(time.time()) - shard_status_timeout.getValue()
        result = []
        for shard in self.shards.values():
            if shard['lastSeen'] < expiryTime:
                continue
            result.append(shard)

        return result
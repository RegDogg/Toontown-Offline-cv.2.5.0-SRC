# Embedded file name: toontown.quest.QuestManagerAI
import Quests
from direct.directnotify.DirectNotifyGlobal import directNotify
from toontown.toonbase import ToontownBattleGlobals
import random

class QuestManagerAI:
    notify = directNotify.newCategory('QuestManagerAI')

    def __init__(self, air):
        self.air = air

    def __testPercentage(self, percentage):
        """
        Generate a random number and test it against the percentage chance specified.
        
        Returns TRUE or FALSE, depending on if the generated number is within the
        percentage specified.
        """
        return random.randint(1, 100) <= percentage

    def __incrementQuestProgress(self, quest):
        """
        Increment the supplied quest's progress by 1.
        """
        quest[4] += 1

    def __toonQuestsList2Quests(self, quests):
        return [ Quests.getQuest(x[0]) for x in quests ]

    def toonKilledCogs(self, toon, suitsKilled, zoneId, activeToons):
        """
        Called in battleExperience to alert the quest system that a toon has
        killed some cogs.
        """
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.CogQuest):
                for suit in suitsKilled:
                    for x in xrange(quest.doesCogCount(toon.getDoId(), suit, zoneId, activeToons)):
                        self.__incrementQuestProgress(toon.quests[index])

        toon.updateQuests()

    def recoverItems(self, toon, suitsKilled, zoneId):
        """
        Called in battleExperience to alert the quest system that a toon should
        test for recovered items.
        
        Returns a tuple of two lists:
            Index 0: a list of recovered items.
            Index 1: a list of unrecovered items.
        """
        recovered, notRecovered = ([] for i in xrange(2))
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.RecoverItemQuest):
                isComplete = quest.getCompletionStatus(toon, toon.quests[index])
                if isComplete == Quests.COMPLETE:
                    continue
                if quest.isLocationMatch(zoneId):
                    if quest.getHolder() == Quests.Any or quest.getHolderType() in ('type', 'track', 'level'):
                        for suit in suitsKilled:
                            if quest.getCompletionStatus(toon, toon.quests[index]) == Quests.COMPLETE:
                                break
                            if quest.getHolder() == Quests.Any or quest.getHolderType() == 'type' and quest.getHolder() == suit['type'] or quest.getHolderType() == 'track' and quest.getHolder() == suit['track'] or quest.getHolderType() == 'level' and quest.getHolder() <= suit['level']:
                                progress = toon.quests[index][4] & pow(2, 16) - 1
                                completion = quest.testRecover(progress)
                                if completion[0]:
                                    recovered.append(quest.getItem())
                                    self.__incrementQuestProgress(toon.quests[index])
                                else:
                                    notRecovered.append(quest.getItem())

        toon.updateQuests()
        return (recovered, notRecovered)

    def toonKilledBuilding(self, toon, track, difficulty, floors, zoneId, activeToons):
        """
        This method is called whenever a toon defeats a cog building.
        N.B: This is called once for each toon that defeated the building.
        """
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.BuildingQuest):
                if quest.isLocationMatch(zoneId):
                    if quest.getBuildingTrack() == Quests.Any or quest.getBuildingTrack() == track:
                        if floors >= quest.getNumFloors():
                            for x in xrange(quest.doesBuildingCount(toon.getDoId(), activeToons)):
                                self.__incrementQuestProgress(toon.quests[index])

        toon.updateQuests()

    def toonKilledCogdo(self, toon, difficulty, floors, zoneId, activeToons):
        pass

    def toonRecoveredCogSuitPart(self, toon, zoneId, toonList):
        pass

    def toonDefeatedFactory(self, toon, factoryId, activeToonVictors):
        """
        This method is called whenever a toon defeats a Sellbot HQ factory.
        N.B: This is called once for each toon that defeated the factory.
        """
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.FactoryQuest):
                for x in xrange(quest.doesFactoryCount(toon.getDoId(), factoryId, activeToonVictors)):
                    self.__incrementQuestProgress(toon.quests[index])

        toon.updateQuests()

    def toonDefeatedMint(self, toon, mintId, activeToonVictors):
        """
        This method is called whenever a toon defeats a Cashbot HQ mint.
        N.B: This is called once for each toon that defeated the mint.
        """
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.MintQuest):
                for x in xrange(quest.doesMintCount(toon.getDoId(), mintId, activeToonVictors)):
                    self.__incrementQuestProgress(toon.quests[index])

        toon.updateQuests()

    def toonDefeatedStage(self, toon, stageId, activeToonVictors):
        pass

    def toonRodeTrolleyFirstTime(self, toon):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.TrolleyQuest):
                self.__incrementQuestProgress(toon.quests[index])

        toon.updateQuests()

    def toonCalledClarabelle(self, toon):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.PhoneQuest):
                self.__incrementQuestProgress(toon.quests[index])

        toon.updateQuests()

    def completeQuest(self, toon, questId):
        """
        This is called whenever a toon completes a single quest in a toontask.
        
        So far, this currently toons them up and removes the quest from their
        quest list, although it may be needed for more in the future.
        """
        toon.toonUp(toon.getMaxHp())
        toon.removeQuest(questId)

    def giveReward(self, toon, rewardId):
        """
        This is called when a toon completes a whole toontask.
        
        This grabs the reward from Quests via rewardId and issues the reward
        to the toon.
        """
        reward = Quests.getReward(rewardId)
        if reward:
            reward.sendRewardAI(toon)

    def npcGiveQuest(self, npc, toon, questId, rewardId, toNpcId, storeReward = False):
        """
        This is called when an NPC wants to assign a quest to the toon.
        """
        rewardId = Quests.transformReward(rewardId, toon)
        finalReward = rewardId if storeReward else 0
        progress = 0
        toon.addQuest((questId,
         npc.getDoId(),
         toNpcId,
         rewardId,
         progress), finalReward)
        npc.assignQuest(toon.getDoId(), questId, rewardId, toNpcId)

    def requestInteract(self, toonId, npc):
        toon = self.air.doId2do.get(toonId)
        if not toon:
            return
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            questId, fromNpcId, toNpcId, rewardId, toonProgress = toon.quests[index]
            isComplete = quest.getCompletionStatus(toon, toon.quests[index], npc)
            if isComplete != Quests.COMPLETE:
                continue
            if toonId in self.air.tutorialManager.avId2fsm.keys():
                self.air.tutorialManager.avId2fsm[toonId].demand('Tunnel')
            if isinstance(quest, Quests.DeliverGagQuest):
                track, level = quest.getGagType()
                toon.inventory.setItem(track, level, toon.inventory.numItem(track, level) - quest.getNumGags())
                toon.b_setInventory(toon.inventory.makeNetString())
            nextQuest = Quests.getNextQuest(questId, npc, toon)
            if nextQuest == (Quests.NA, Quests.NA):
                if isinstance(quest, Quests.TrackChoiceQuest):
                    npc.presentTrackChoice(toonId, questId, quest.getChoices())
                    return
                rewardId = Quests.getAvatarRewardId(toon, questId)
                npc.completeQuest(toonId, questId, rewardId)
                self.completeQuest(toon, questId)
                self.giveReward(toon, rewardId)
                return
            self.completeQuest(toon, questId)
            nextQuestId = nextQuest[0]
            nextRewardId = Quests.getFinalRewardId(questId, 1)
            nextToNpcId = nextQuest[1]
            self.npcGiveQuest(npc, toon, nextQuestId, nextRewardId, nextToNpcId)
            return

        if len(self.__toonQuestsList2Quests(toon.quests)) >= toon.getQuestCarryLimit():
            self.notify.debug('Rejecting toonId %d because their quest inventory is full.' % toonId)
            npc.rejectAvatar(toonId)
            return
        if toonId in self.air.tutorialManager.avId2fsm.keys():
            if toon.getRewardHistory()[0] == 0:
                self.npcGiveQuest(npc, toon, 101, Quests.findFinalRewardId(101)[0], Quests.getQuestToNpcId(101), storeReward=True)
                self.air.tutorialManager.avId2fsm[toonId].demand('Battle')
                return
        tier = toon.getRewardHistory()[0]
        if Quests.avatarHasAllRequiredRewards(toon, tier):
            if not Quests.avatarWorkingOnRequiredRewards(toon):
                if tier != Quests.LOOPING_FINAL_TIER:
                    tier += 1
                toon.b_setRewardHistory(tier, [])
            else:
                self.notify.debug('Rejecting toonId %d because they are still working on their current tier.' % toonId)
                npc.rejectAvatarTierNotDone(toonId)
                return
        suitableQuests = Quests.chooseBestQuests(tier, npc, toon)
        if not suitableQuests:
            self.notify.debug('Rejecting toonId %d because there are no quests available!' % toonId)
            npc.rejectAvatar(toonId)
            return
        npc.presentQuestChoice(toonId, suitableQuests)

    def avatarCancelled(self, toonId):
        """
        This method is called by an NPCToon to tell the quest system that
        a toon decided to cancel the interaction.
        """
        pass

    def avatarChoseQuest(self, toonId, npc, questId, rewardId, toNpcId):
        """
        This method is called by an NPCToon to tell the quest system that
        a toon has chosen a quest from the list supplied.
        """
        toon = self.air.doId2do.get(toonId)
        if not toon:
            return
        self.notify.debug('toonId %d chose quest %d with rewardId %d to hand to npcId %d.' % (toonId,
         questId,
         rewardId,
         toNpcId))
        self.npcGiveQuest(npc, toon, questId, rewardId, toNpcId, storeReward=True)

    def avatarChoseTrack(self, toonId, npc, questId, trackId):
        """
        This method is called by an NPCToon to tell the quest system that
        a toon has decided on the new track that they want to train for.
        
        This is a special moment for any toon, as it determines how they
        will play the game for the rest of their time at TTR. :D
        """
        toon = self.air.doId2do.get(toonId)
        if not toon:
            return
        self.notify.debug('toonId %d chose trackId %d to train.' % (toonId, trackId))
        if trackId in [ToontownBattleGlobals.THROW_TRACK, ToontownBattleGlobals.SQUIRT_TRACK]:
            self.notify.warning('toonId %s attempted to select trackId %d, which is a default track!' % (toonId, trackId))
            self.air.writeServerEvent('suspicious', avId=toonId, issue='QMAI.avatarChoseTrack Attempted to train trackId %d, which is a default track!' % trackId)
            return
        rewardId = 401 + trackId
        npc.completeQuest(toonId, questId, rewardId)
        self.completeQuest(toon, questId)
        self.giveReward(toon, rewardId)

    def toonMadeFriend(self, toon, otherToon):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.FriendQuest):
                self.__incrementQuestProgress(toon.quests[index])

        toon.updateQuests()

    def toonFished(self, toon, zoneId):
        """
        This method is called by the FishManagerAI whenever a toon catches
        a fish. This checks for any "fishing" quests that are in progress,
        and determines if they caught any items.
        """
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            if isinstance(quest, Quests.RecoverItemQuest):
                if quest.getCompletionStatus(toon, toon.quests[index]) == Quests.COMPLETE:
                    continue
                if quest.isLocationMatch(zoneId):
                    if quest.getHolder() == Quests.AnyFish:
                        progress = toon.quests[index][4] & pow(2, 16) - 1
                        completion = quest.testRecover(progress)
                        if completion[0]:
                            self.__incrementQuestProgress(toon.quests[index])
                            toon.updateQuests()
                            return quest.getItem()

        return 0

    def hasTailorClothingTicket(self, toon, npc):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            isComplete = quest.getCompletionStatus(toon, toon.quests[index], npc)
            if isComplete == Quests.COMPLETE:
                return True

        return False

    def removeClothingTicket(self, toon, npc):
        for index, quest in enumerate(self.__toonQuestsList2Quests(toon.quests)):
            questId, fromNpcId, toNpcId, rewardId, toonProgress = toon.quests[index]
            isComplete = quest.getCompletionStatus(toon, toon.quests[index], npc)
            if isComplete == Quests.COMPLETE:
                toon.removeQuest(questId)
                return True

        return False
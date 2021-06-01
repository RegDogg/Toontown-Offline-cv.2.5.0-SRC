# Embedded file name: toontown.shtiker.WordPage
from pandac.PandaModules import *
import ShtikerPage
import ShtikerBook
from direct.gui.DirectGui import *
from direct.directnotify import DirectNotifyGlobal
from pandac.PandaModules import *
from toontown.toonbase import TTLocalizer
import os
import string
from toontown.toonbase import ToontownGlobals

class WordPage(ShtikerPage.ShtikerPage):

    def __init__(self):
        ShtikerPage.ShtikerPage.__init__(self)
        self.textRolloverColor = Vec4(1, 1, 0, 1)
        self.textDownColor = Vec4(0.5, 0.9, 1, 1)
        self.textDisabledColor = Vec4(0.4, 0.8, 0.4, 1)

    def load(self):
        ShtikerPage.ShtikerPage.load(self)
        self.title = DirectLabel(parent=self, relief=None, text=TTLocalizer.WordPageTitle, text_scale=0.12, textMayChange=0, pos=(0, 0, 0.6))
        self.helpText = DirectLabel(parent=self, relief=None, text=TTLocalizer.WordPageHelp, text_scale=0.06, text_wordwrap=12, text_align=TextNode.ALeft, textMayChange=1, pos=(0.058, 0, 0.403))
        gui = loader.loadModel('phase_3.5/models/gui/friendslist_gui')
        self.scrollList = DirectScrolledList(parent=self, relief=None, forceHeight=0.07, pos=(-0.5, 0, 0), incButton_image=(gui.find('**/FndsLst_ScrollUp'),
         gui.find('**/FndsLst_ScrollDN'),
         gui.find('**/FndsLst_ScrollUp_Rllvr'),
         gui.find('**/FndsLst_ScrollUp')), incButton_relief=None, incButton_scale=(1.3, 1.3, -1.3), incButton_pos=(0.08, 0, -0.6), incButton_image3_color=Vec4(1, 1, 1, 0.2), decButton_image=(gui.find('**/FndsLst_ScrollUp'),
         gui.find('**/FndsLst_ScrollDN'),
         gui.find('**/FndsLst_ScrollUp_Rllvr'),
         gui.find('**/FndsLst_ScrollUp')), decButton_relief=None, decButton_scale=(1.3, 1.3, 1.3), decButton_pos=(0.08, 0, 0.52), decButton_image3_color=Vec4(1, 1, 1, 0.2), itemFrame_pos=(-0.237, 0, 0.41), itemFrame_scale=1.0, itemFrame_relief=DGG.SUNKEN, itemFrame_frameSize=(-0.05, 0.66, -0.98, 0.07), itemFrame_frameColor=(0.85, 0.95, 1, 1), itemFrame_borderWidth=(0.01, 0.01), numItemsVisible=13, items=['', ''])
        gui.removeNode()
        return

    def unload(self):
        ShtikerPage.ShtikerPage.unload(self)
        del self.title
        del self.helpText
        self.scrollList.destroy()
        del self.scrollList
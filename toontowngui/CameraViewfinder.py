# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.toontowngui.CameraViewfinder
from panda3d.core import Camera, Lens, NodePath, Point2
from direct.gui.DirectGui import *
from direct.showbase.DirectObject import DirectObject
from toontown.toonbase import TTLocalizer, ToontownGlobals
import math

class CameraViewfinder(NodePath, DirectObject):

    def __init__(self):
        NodePath.__init__(self, 'cameraViewfinder')
        self.reparentTo(aspect2d)
        self.viewfinder = loader.loadModel('phase_4/models/minigames/photo_game_viewfinder')
        self.viewfinder.reparentTo(self)
        self.viewfinder.setScale(0.55, 1.0, 0.55)
        self.viewfinder.setY(-1.0)
        self.viewfinder.setTransparency(True)
        self.viewfinder.setDepthWrite(True)
        self.viewfinder.setDepthTest(True)
        self.goontownLabel = DirectLabel(self, relief=None, text=TTLocalizer.MonsterGame, text_scale=0.09, text_font=ToontownGlobals.getMinnieFont(), pos=(0, 0, 0.3), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.goontownLabel.hide()
        self.infoLabel = DirectLabel(self, relief=None, text='', text_wordwrap=9, text_font=ToontownGlobals.getMinnieFont(), text_scale=0.09, pos=(0, 0, -0.375), text_fg=(1, 1, 1, 1), text_shadow=(0, 0, 0, 1))
        self.infoLabel.hide()
        self.target = None
        self.foundSfx = loader.loadSfx('phase_3/audio/sfx/found_monster.ogg')
        self.applauseSfx = loader.loadSfx('phase_6/audio/sfx/Golf_Crowd_Applause.ogg')
        taskMgr.add(self.__checkMonsters, self.uniqueName('checkMonsters'))
        for monster in base.monsters:
            monster.actor.show()

        self.accept('mouse3', base.disableScreenShotCam)
        self.accept('mouse1', base.takeScreenShot)
        self.accept('takeScreenShot', self.__takeScreenShot)
        return

    def uniqueName(self, name):
        return '%s-%s' % (name, id(self))

    def removeNode(self):
        if not self.viewfinder:
            return
        else:
            self.viewfinder.removeNode()
            self.viewfinder = None
            self.goontownLabel.destroy()
            self.goontownLabel = None
            self.infoLabel.removeNode()
            self.infoLabel = None
            self.foundSfx.stop()
            self.applauseSfx.stop()
            self.foundSfx = None
            self.applauseSfx = None
            NodePath.removeNode(self)
            taskMgr.remove(self.uniqueName('checkMonsters'))
            for monster in base.monsters:
                monster.actor.hide()

            self.ignoreAll()
            return

    def isInView(self, object):
        p1 = base.cam.getRelativePoint(render, object.getPos())
        return base.camLens.project(p1, Point2())

    def __checkMonsters(self, task):
        for monster in base.monsters:
            if self.distance(monster.actor.getPos(), base.localAvatar.getPos()) <= 625 and self.isInView(monster.actor):
                if monster != self.target:
                    self.target = monster
                    self.goontownLabel.show()
                    self.infoLabel['text'] = '%s\n%s\n%s JBs' % (self.target.actor.getName(), TTLocalizer.MonsterTypes[self.target.getType()], self.target.getReward())
                    self.infoLabel.show()
                    self.foundSfx.play()
                return task.again

        self.goontownLabel.hide()
        self.infoLabel.hide()
        self.target = None
        return task.again

    def distance(self, loc1, loc2):
        return (loc1.getX() - loc2.getX()) ** 2 + (loc1.getY() - loc2.getY()) ** 2 + (loc1.getZ() - loc2.getZ()) ** 2

    def __takeScreenShot(self):
        if self.target:
            self.applauseSfx.play()
            self.target.d_catchMonster()
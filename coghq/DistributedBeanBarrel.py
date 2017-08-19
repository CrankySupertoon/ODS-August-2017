# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.coghq.DistributedBeanBarrel
from DistributedBarrelBase import DistributedBarrelBase

class DistributedBeanBarrel(DistributedBarrelBase):

    def delete(self):
        self.gagModel.removeNode()
        del self.gagModel
        DistributedBarrelBase.delete(self)

    def applyLabel(self):
        purchaseModels = loader.loadModel('phase_4/models/gui/purchase_gui')
        self.gagModel = purchaseModels.find('**/Jar')
        self.gagModel.reparentTo(self.gagNode)
        self.gagModel.setScale(3)
        self.gagModel.setPos(0, -0.1, 0)
        purchaseModels.removeNode()

    def setGrab(self, avId, reward):
        DistributedBarrelBase.setGrab(self, avId, reward)
        if not avId or not reward:
            return
        av = self.cr.doId2do.get(avId)
        if av:
            av.showHpText(reward, 2)
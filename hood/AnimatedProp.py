# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.hood.AnimatedProp
from direct.showbase.DirectObject import DirectObject

class AnimatedProp(DirectObject):
    notify = directNotify.newCategory('AnimatedProp')

    def __init__(self, node):
        self.node = node

    def delete(self):
        pass

    def uniqueName(self, name):
        return name + '-' + str(self.node.this)

    def enter(self):
        self.notify.debug('enter')

    def exit(self):
        self.notify.debug('exit')
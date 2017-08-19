# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNAGroup
import DNAUtil

class DNAGroup:
    COMPONENT_CODE = 1

    def __init__(self, name):
        self.name = name
        self.children = []
        self.parent = None
        self.visGroup = None
        self.loadVis = True
        return

    def add(self, child):
        self.children += [child]

    def remove(self, child):
        self.children.remove(child)

    def at(self, index):
        return self.children[index]

    def setParent(self, parent, dnaStore):
        self.parent = parent
        self.visGroup = parent.getVisGroup()

    def getParent(self):
        return self.parent

    def clearParent(self):
        self.parent = None
        self.visGroup = None
        return

    def isRoot(self):
        return self.parent is None

    def getVisGroup(self):
        return self.visGroup

    def getNumChildren(self):
        return len(self.children)

    def getName(self):
        return self.name

    def setName(self, name):
        self.name = name

    def makeFromDGI(self, dgi):
        self.name = DNAUtil.dgiExtractString8(dgi)

    def traverse(self, nodePath, dnaStorage):
        nodePath = nodePath.attachNewNode(self.name, 0)
        for child in self.children:
            if self.loadVis or not hasattr(child, 'visibles'):
                child.loadVis = self.loadVis
                child.traverse(nodePath, dnaStorage)

        return nodePath

    def destroy(self):
        for child in self.children:
            child.destroy()

        del self.children[:]
        self.parent = None
        self.visGroup = None
        return
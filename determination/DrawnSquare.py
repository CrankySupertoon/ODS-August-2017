# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.determination.DrawnSquare
from panda3d.core import CardMaker, LineSegs, NodePath
from direct.showbase.DirectObject import DirectObject
EDGE_LINES = [[(0, 0, 0), (1, 0, 0)],
 [(0, 0, 1), (1, 0, 1)],
 [(1, 0, 0), (1, 0, 1)],
 [(0, 0, 0), (0, 0, 1)]]

class DrawnSquare(DirectObject):

    def __init__(self, parent = aspect2d, pos = (0, 0, 0), scale = (1, 0, 0.75), color = (0, 0, 0, 1), edgeColor = (1, 1, 1, 1)):
        cardMaker = CardMaker('drawnSquare')
        self.card = NodePath(cardMaker.generate())
        self.card.reparentTo(parent)
        self.card.setColor(*color)
        self.card.setScale(0)
        self.card.setPos(*pos)
        self.scale = scale
        self.edgeColor = edgeColor
        self.lines = LineSegs()
        self.lines.setThickness(5)
        self.initLines()
        self.linesNp = self.card.attachNewNode(self.lines.create())

    def uniqueName(self, name):
        return '%s-%s' % (name, id(self))

    def drawLines(self, lineSeg, lines):
        for line in lines:
            fromPos, toPos = line
            lineSeg.moveTo(fromPos)
            lineSeg.drawTo(toPos)

    def initLines(self):
        self.lines.setColor(*self.edgeColor)
        self.drawLines(self.lines, EDGE_LINES)

    def destroy(self):
        if not hasattr(self, 'card'):
            return
        self.card.removeNode()
        del self.card
        del self.lines
        del self.linesNp
        return True
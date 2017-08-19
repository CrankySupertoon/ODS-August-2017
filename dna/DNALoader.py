# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNALoader
from panda3d.core import Datagram, DatagramIterator, LVector3, LVector3f, NodePath, Texture
from direct.distributed.PyDatagramIterator import PyDatagramIterator
from direct.distributed.PyDatagram import PyDatagram
from direct.directnotify import DirectNotifyGlobal
from direct.stdpy.file import *
from otp.util.AESCipher import AESCipher
from DNAAssetStorage import DNAAssetStorage
import DNAUtil
import DNAAnimProp
import DNACornice
import DNADoor
import DNAFlatBuilding
import DNAFlatDoor
import DNAGroup
import DNAInteractiveProp
import DNALandmarkBuilding
import DNANode
import DNAProp
import DNASign
import DNASignBaseline
import DNASignGraphic
import DNASignText
import DNAStreet
import DNAVisGroup
import DNAWall
import DNAWindows
import DNABattleCell
import DNASuitPoint
import zlib
import sys
sys.setrecursionlimit(10000)
compClassTable = {1: DNAGroup.DNAGroup,
 2: DNAVisGroup.DNAVisGroup,
 3: DNANode.DNANode,
 4: DNAProp.DNAProp,
 5: DNASign.DNASign,
 6: DNASignBaseline.DNASignBaseline,
 7: DNASignText.DNASignText,
 8: DNASignGraphic.DNASignGraphic,
 9: DNAFlatBuilding.DNAFlatBuilding,
 10: DNAWall.DNAWall,
 11: DNAWindows.DNAWindows,
 12: DNACornice.DNACornice,
 13: DNALandmarkBuilding.DNALandmarkBuilding,
 14: DNAAnimProp.DNAAnimProp,
 15: DNAInteractiveProp.DNAInteractiveProp,
 16: DNADoor.DNADoor,
 17: DNAFlatDoor.DNAFlatDoor,
 18: DNAStreet.DNAStreet}
childlessComps = (7, 11, 12, 16, 17, 18)
binaryHeader = chr(4) + chr(20)

class DNALoader:
    notify = DirectNotifyGlobal.directNotify.newCategory('DNALoader')
    cipher = None

    def handleAssetStorageData(self, dnaStorage, dgi):
        numRoots = dgi.getUint16()
        for _ in xrange(numRoots):
            root = DNAUtil.dgiExtractString8(dgi)
            numCodes = dgi.getUint16()
            for i in xrange(numCodes):
                code = DNAUtil.dgiExtractString8(dgi)
                dnaStorage.storeCatalogCode(root, code)

        numTextures = dgi.getUint16()
        for _ in xrange(numTextures):
            code = DNAUtil.dgiExtractString8(dgi)
            filename = DNAUtil.dgiExtractString8(dgi)
            dnaStorage.storeTexture(code, loader.loadTexture(filename, okMissing=True))

        numNodes = dgi.getUint16()
        for _ in xrange(numNodes):
            code = DNAUtil.dgiExtractString8(dgi)
            path = DNAUtil.dgiExtractString8(dgi)
            node = DNAUtil.dgiExtractString8(dgi)
            dnaStorage.storeNode(code, path, node)

    def handleStorageData(self, dnaStorage, dgi):
        numBlocks = dgi.getUint16()
        for _ in xrange(numBlocks):
            number = dgi.getUint8()
            zone = dgi.getUint16()
            title = DNAUtil.dgiExtractString8(dgi)
            bldgType = DNAUtil.dgiExtractString8(dgi)
            dnaStorage.storeBlock(number, title, bldgType, zone)

        numPoints = dgi.getUint16()
        for _ in xrange(numPoints):
            index = dgi.getUint16()
            pointType = dgi.getUint8()
            x, y, z = (dgi.getInt32() / 100.0 for i in xrange(3))
            landmarkBuildingIndex = dgi.getInt8()
            dnaStorage.storeSuitPoint(DNASuitPoint.DNASuitPoint(index, pointType, LVector3f(x, y, z), landmarkBuildingIndex))

        numEdges = dgi.getUint16()
        for _ in xrange(numEdges):
            index = dgi.getUint16()
            numPoints = dgi.getUint16()
            for i in xrange(numPoints):
                endPoint = dgi.getUint16()
                zoneId = dgi.getUint16()
                dnaStorage.storeSuitEdge(index, endPoint, zoneId)

        numCells = dgi.getUint16()
        for _ in xrange(numCells):
            w = dgi.getUint8()
            h = dgi.getUint8()
            x, y, z = (dgi.getInt32() / 100.0 for i in xrange(3))
            dnaStorage.storeBattleCell(DNABattleCell.DNABattleCell(w, h, LVector3f(x, y, z)))

    def handleCompData(self, dnaStorage, dgi):
        compProp = None
        while True:
            propCode = dgi.getUint8()
            if propCode == 255:
                if not compProp:
                    raise Exception('Unexpected 255 found.')
                prop = compProp.getParent()
                if prop:
                    compProp = prop
            elif propCode in compClassTable:
                propClass = compClassTable[propCode]
                if propClass.__init__.func_code.co_argcount > 1:
                    newComp = propClass('unnamed_comp')
                else:
                    newComp = propClass()
                if propCode == 2:
                    newComp.makeFromDGI(dgi, dnaStorage)
                    dnaStorage.storeDNAVisGroup(newComp)
                else:
                    newComp.makeFromDGI(dgi)
            else:
                raise Exception('Invalid prop code: %d' % propCode)
            if not dgi.getRemainingSize():
                return compProp
            if propCode == 255:
                continue
            if compProp is not None:
                newComp.setParent(compProp, dnaStorage)
                compProp.add(newComp)
            if propCode not in childlessComps:
                compProp = newComp

        return

    def loadDNAFileAI(self, dnaStorage, file):
        dnaFile = open(file, 'rb')
        dnaData = dnaFile.read()
        dnaFile.close()
        if dnaData[:2] != binaryHeader:
            raise Exception('Invalid header.')
        if not self.cipher:
            self.cipher = AESCipher(config.GetString('dna-key'))
        try:
            dnaData = zlib.decompress(self.cipher.decrypt(dnaData[2:]))
        except:
            raise Exception('Invalid key. You cannot play the game.')

        dg = PyDatagram(dnaData)
        dgi = PyDatagramIterator(dg)
        if isinstance(dnaStorage, DNAAssetStorage):
            self.handleAssetStorageData(dnaStorage, dgi)
            return
        self.handleStorageData(dnaStorage, dgi)
        return self.handleCompData(dnaStorage, dgi)

    def loadDNAFile(self, dnaStorage, file, loadVis = True):
        self.notify.info('Loading Binary DNA file: ' + file[1:])
        prop = self.loadDNAFileAI(dnaStorage, file)
        nodePath = NodePath('dna')
        prop.loadVis = loadVis
        prop.traverse(nodePath, dnaStorage)
        return (prop, nodePath)
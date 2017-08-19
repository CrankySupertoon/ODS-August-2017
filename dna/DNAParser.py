# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNAParser
from DNALoader import DNALoader
from DNAAssetStorage import DNAAssetStorage
from DNADoor import DNADoor
from DNAStorage import DNAStorage
from DNASuitPoint import DNASuitPoint
from DNAGroup import DNAGroup
from DNAVisGroup import DNAVisGroup
import __builtin__
dnaLoader = DNALoader()
__builtin__.assetStorage = DNAAssetStorage()

def setupAssetStorage():
    print 'Loading DNA asset storage...'
    loadDNAFileAI(assetStorage, 'phase_3/dna/storage.bdna')


def loadDNAFileAI(dnaStorage, file):
    return dnaLoader.loadDNAFileAI(dnaStorage, '/' + file)


def loadDNAFile(dnaStorage, file, loadVis = True):
    return dnaLoader.loadDNAFile(dnaStorage, '/' + file, loadVis)


def setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color):
    try:
        block = int(str(block).split('_')[0])
    except:
        dnaLoader.notify.warning('Error parsing: ' + block)
        block = 9999

    DNADoor.setupDoor(doorNodePath, parentNode, doorOrigin, dnaStore, block, color)
# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.dna.DNAAssetStorage
from panda3d.core import ModelPool, Texture, TexturePool
from direct.directnotify import DirectNotifyGlobal
from DNATransformers import AllTransformers
import gc

class DNAModelCache:

    def __init__(self):
        self.models = {}
        self.transformers = AllTransformers

    def clear(self):
        for path in self.models:
            self.models[path].removeNode()
            self.models[path].clear()

        self.models.clear()
        ModelPool.garbageCollect()

    def fetch(self, code, path, node, name):
        if path in self.models:
            modelNode = self.models[path]
            if node:
                np = modelNode.find('**/' + node).copyTo(hidden)
            else:
                np = modelNode.copyTo(hidden)
            np.setTag('DNACode', code)
            if code in self.transformers:
                self.transformers[code].apply(np, name)
            return np
        self.models[path] = loader.loadModel(path, noCache=True)
        return self.fetch(code, path, node, name)


class DNAAssetStorage:
    notify = DirectNotifyGlobal.directNotify.newCategory('DNAAssetStorage')

    def __init__(self):
        self.modelCache = DNAModelCache()
        self.nodes = {}
        self.textures = {}
        self.catalogCodes = {}

    def resetModelCache(self):
        self.modelCache.clear()

    def resetNodes(self):
        self.nodes.clear()

    def resetTextures(self):
        self.textures.clear()

    def resetCatalogCodes(self):
        self.catalogCodes.clear()

    def cleanup(self):
        self.resetModelCache()
        self.resetNodes()
        self.resetTextures()
        self.resetCatalogCodes()
        ModelPool.garbageCollect()
        TexturePool.garbageCollect()
        gc.collect()

    def findNode(self, code, name = ''):
        if code in self.nodes:
            path, node = self.nodes[code]
            return self.modelCache.fetch(code, path, node, name)
        self.notify.warning('Unknown node code: ' + code)

    def storeNode(self, code, path, node):
        self.nodes[code] = (path, node)

    def storeTexture(self, name, texture):
        self.textures[name] = texture

    def storeCatalogCode(self, category, code):
        if category not in self.catalogCodes:
            self.catalogCodes[category] = []
        self.catalogCodes[category].append(code)

    def getNumCatalogCodes(self, category):
        if category not in self.catalogCodes:
            return -1
        return len(self.catalogCodes[category])

    def getCatalogCode(self, category, index):
        return self.catalogCodes[category][index]

    def findTexture(self, name):
        if name in self.textures:
            return self.textures[name]
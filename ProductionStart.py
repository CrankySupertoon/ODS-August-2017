# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: ProductionStart
import __builtin__, os, sys, glob
from panda3d.core import Filename, Multifile, StringStream, VirtualFile, VirtualFileSystem, loadPrcFile, loadPrcFileData
import aes
import ODSGlobals
import niraidata
prc = niraidata.SPECIALPLACE
iv, key, prc = prc[:32], prc[32:64], prc[64:]
prc = aes.decrypt(prc, key[::-1], iv)
for line in prc.split('\n'):
    line = line.strip()
    if line:
        loadPrcFileData('', line)

del prc
del iv
del key
__builtin__.dcStream = StringStream()
dc = niraidata.PICTUREOFASTUPIDDOG
iv, key, dc = dc[:32], dc[32:64], dc[64:]
dc = aes.decrypt(dc, key, iv[::-1])
dcStream.setData(dc)
del dc
del iv
del key
vfs = VirtualFileSystem.getGlobalPtr()

def mountWithSignature(filename):
    if not os.path.isfile(filename):
        return False
    mf = Multifile()
    mf.openRead(Filename(filename))
    if mf.getNumSignatures() != 1:
        return False
    if mf.getSignaturePublicKey(0) != ODSGlobals.getmfssl():
        return False
    if filename.endswith('.ef'):
        mf.setEncryptionPassword(ODSGlobals.getmfkey(filename))
    return vfs.mount(mf, Filename('/'), 0)


for mf in [3,
 3.5,
 4,
 5,
 5.5,
 6,
 7,
 8,
 9,
 10,
 11,
 12,
 13]:
    filenameBase = 'resources/default/phase_%s' % mf
    if sys.platform == 'android':
        filenameBase = '/sdcard/ODS/' + filenameBase
    if not mountWithSignature(filenameBase + '.mf') or not mountWithSignature(filenameBase + '.ef'):
        print 'Unable to mount phase_%s.' % mf
        sys.exit()
        break

filenameBase = 'resources'
if sys.platform == 'android':
    filenameBase = '/sdcard/ODS/' + filenameBase
for pack in os.listdir(filenameBase):
    if pack == 'default':
        continue
    directory = os.path.join(filenameBase, pack)
    if not os.path.isdir(directory):
        continue
    print 'Loading content pack %s...' % pack
    for file in glob.glob('%s/%s/*.mf' % (filenameBase, pack)):
        mf = Multifile()
        mf.openReadWrite(Filename(file))
        names = mf.getSubfileNames()
        for name in names:
            ext = os.path.splitext(name)[1]
            if ext not in ('.jpg', '.jpeg', '.ogg', '.rgb', '.png'):
                mf.removeSubfile(name)

        vfs.mount(mf, Filename('/'), 0)

import toontown.toonbase.ToontownStart
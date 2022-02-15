# pylint: disable=pointless-string-statement
import os
import subprocess

# ---------------
# Troubleshooting
#   Error cli.add() 
#   Error from archivebox.main import add
# Workaround
#   Shell command `archivebox add`
from archivebox import cli

#-----------------------
# Redirect stdout to buf
import io
from contextlib import redirect_stdout

"""--------+---------+---------+---------+---------+---------+---------+---------+---------|
|                                    M A I N   C L A S S                                   |
|----------+---------+---------+---------+---------+---------+---------+---------+-------"""
class clsArchiveso():

    """--------+---------+---------+---------+---------+---------+---------+---------+---------|
    |                                   C O N S T R U C T O R                                  |
    |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
    def __init__(self, strPath):
        #----------------------------
        # initialize class _CONSTANTS
        self._init_meta()
        os.chdir(strPath)

    """--------+---------+---------+---------+---------+---------+---------+---------+---------|
    |                                 C L A S S   M E T H O D S                                |
    |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
    def get_version(self):
        return self._strMETAVERSION

    def get_cli_version(self):
        #-----------------------
        # Redirect stdout to buf
        buf = io.StringIO()
        with redirect_stdout(buf):
            cli.version()
        return buf.getvalue().splitlines()[0]

    def add_url(self, strUrl):
        try:
            strCmd = 'archivebox add ' + strUrl
            strResult = subprocess.check_output(strCmd, stderr=subprocess.STDOUT, shell=True)
        except subprocess.CalledProcessError as e:
            strOutput = e.output.decode('utf-8')
            # directory not found
            if "archivebox init" in strOutput:
              return "Archivebox index not found", 503
            # command not found
            return "Archivebox not installed", 503

        return strResult.decode('utf-8'), 200

    """--------+---------+---------+---------+---------+---------+---------+---------+---------|
    |                                C L A S S   M E T A D A T A                               |
    |----------+---------+---------+---------+---------+---------+---------+---------+-------"""
    def _init_meta(self):
        """
        | _strMETACLASS, _strMETAVERSION, _strMETAFILE used to save() and load() members
        """
        self._strMETACLASS = str(self.__class__).split('.')[1][:-2]
        self._strMETAVERSION = "0.3.0"
        """
        | Filename "_Class_Version_"
        """
        self._strMETAFILE = "_" + self._strMETACLASS + "_" + self._strMETAVERSION + "_"
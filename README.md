## python toolbox metadata add-on
Python toolbox metadata add-on or pyt_meta is a module that contains classes and functions that enable automated xml metadata file generation for ArcGIS toolboxes and/or any tools contained in a given toolbox. The pyt_meta module enables default metadata value generation based on the toolbox and tool class attributes/properties and the ArcGIS portal user profile. When geospatial developers wish to override and explicitly control metadata or values, the module enables developers to have full control and access to the xml metadata keys directly within the python toolbox code. As an added benefit among toolbox/tool deployments, the maintenance and packaging of XML support file documents can be eliminated from the process. This results in less file dependencies and increased toolbox deployment reliability and efficient.

### Origin
pyt_meta was developed at the National Geospatial-Intelligence Agency (NGA) by a federal government employee in the course of their official duties, so it is <strong>not</strong> subject to copyright protection and is in the public domain in the United States. 

You are free to use the core public domain portions of pyt_meta for any purpose. Modifications back to the cores of any dependency functions are subject to the original licenses and are separate from the core public domain work of pyt_meta. 

### Transparency
NGA is posting code created by government officers in their official duties in transparent platforms to increase the impact and reach of taxpayer-funded code.

### Pull Requests
If you'd like to contribute to this project, please make a pull request. We'll review the pull request and discuss the changes. This project is in the public domain within the United States and all changes to the core public domain portions will be released back into the public domain. By submitting a pull request, you are agreeing to comply with this waiver of copyright interest. Modifications to dependencies under copyright-based open source licenses are subject to the original license conditions.

### Requirements
The pyt_meta package is an addon feature to ArcGIS python toolboxes.  As such, ArcGIS Desktop or ArcGIS Pro with python 3.6 or higher is required to take advantage of the package capabilities.

    python 3.6+
    ArcGIS desktop 10.8+
        or
    ArcGIS Pro 2.0+ 

### Quick-start

Install:

    For explicit instructions on your local system, download the pyt_meta_pip_helper.py script below.  
    Once downloaded, right click on the script, and select 'Run with ArcGIS Pro'.
    The script will create tailored instructions based on the location of the local ArcGIS install and active virtual environment.

        https://github.com/ngageoint/python-toolbox-metadata-addon/blob/main/pyt_meta_pip_helper.py

    Alternatively follow the instructions below to pip install pyt_meta: 
      Locate the active python environment/venv for ArcGIS:

        Open IDLE from a local ArcGIS install

        In the python shell run: 

            >>> import sys, os

            >>> print(os.path.dirname(os.path.realpath(sys.executable)))


      pyt_meta can then be installed from the command line using pip:

        cd to the active python env identified in the step above

          Ex. $ cd "C:\Users\...\Pro\bin\Python\envs\arcgispro-py3"

        (optional) ensure the latest version of pip:

          $ pip install --upgrade pip

        Perform the pip install from the GitHub repo:

          $ pip install git+https://github.com/ngageoint/python-toolbox-metadata-addon

Usage:

    Import:
    
        Key behavior: 
            - In create_tb_meta, "__file__" is the current file path for the .pyt (python toolbox)
            - In create_tb_meta, True allows pyt_meta to overwrite existing xml metadata files if they exist.  
            
        ***Note: See “helloWorldToolbox.pyt” toolbox for detailed import statement usage***
        
        Import statement example for python toolbox:
        ##--------------------------------------------------------## 
        if __name__ == "__main__":     
            # call to generate metadata from toolbox     
            from pyt_meta import create_tb_meta     
            tb_meta = create_tb_meta(__file__, True)
        ##--------------------------------------------------------##


    Defining XML Element Properties:
    
        Key behavior: 
            - Tags can be added or removed to sync with other metadata styles. 
                - To alter the metadata style, modifiy the default xml structure variables:
                    - DEFAULT_TOOLBOX_XML_STRUCT
                    - DEFAULT_TOOL_XML_STRUCT
            - Metadata declared at the tool level will override toolbox level metadata. 
            - In absence of explicit values, pyt_meta will apply default / derived metadata values.

        ***Note: See “helloWorldToolbox.pyt” toolbox for both tool and toolbox property code samples***
        
        Example of defining metadata properties within the toolbox object:
        ##--------------------------------------------------------##
        class Toolbox(object):
            def __init__(self):
                self.idPurp = '''Some description of the toolbox
                                               that is a multiline string'''
                self.searchKeys = ['hello', 'world', 'toolbox']
                self.idAbs = '''Some abstract of the toolbox
                                             that is a multiline string'''
                self.idCredit = '''Point of Contact (POC): Jane Doe
                                               Organization: Hoolie INC.
                                               Email: Jane.Doe@hoolie.co'''
                 self.useLimit = '''Copyright Notice: Hoolie explicitly owns
                                               all rights to this toolbox.'''
                 self.formatName = 'ArcToolbox Toolbox'
                 self.mdDateSt = '20210701'
       ##--------------------------------------------------------##
       
### Dependencies
Most dependencies listed below are licensed under the Python Software Foundation (PSF) as distributed with the python 3 standard library.  No changes were made directly to the core packages below. The original function was simply called or re-used. The arcpy package is an optional dependency of pyt_meta, but highly encouraged to enhance default metadata attribution.

importlib

xml

os

sys

re

time (Zope Public License)

datetime

inspect

pathlib (MIT)

collections

subprocess

shutil

warnings

arcpy (ESRI) -- Optional


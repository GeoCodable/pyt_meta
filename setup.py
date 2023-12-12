import setuptools

with open('README.md', 'r') as fh:
    long_description = fh.read()

setuptools.setup(
    name='pyt_meta',                        # name of the package
    version='1.0.0',                        # release version
    author='GeoCodable',                    # org/author
    description=\
         '''
        Description:
            The pyt_meta module contains classes and functions that enable automated
            xml metadata file generation for ArcGIS toolboxes and/or any tools contained
            in a given toolbox.   The pyt_meta module enables default metadata
            value generation based on the toolbox and tool class attributes/properties
            and the ArcGIS portal user profile. When geospatial developers wish to override
            and explicitly control metadata, values, the module enables developers full control
            and access to the xml metadata directly within the python toolbox code.  As an
            added benefit among toolbox/tool deployments, maintenance and packaging of xml
            support file documents can be eliminated from the process.  This results in less file
            dependencies and can make toolbox deployments more reliable and efficient.
        ''',
    long_description=long_description,      # long description read from the the readme file
    long_description_content_type='text/markdown',
    packages=setuptools.find_packages(),    # list of all python modules to be installed
    classifiers=[                           # information to filter the project on PyPi website
                        'Programming Language :: Python :: 3',
                        'License :: OSI Approved :: MIT License',
                        'Operating System :: OS Independent',
                        'Natural Language :: English',
                        'Programming Language :: Python :: 3.6',
                        'Programming Language :: Python :: 3.7',
                        'Programming Language :: Python :: 3.8',
                        'Programming Language :: Python :: 3.9',
                        'Programming Language :: Python :: 3.10',
                        ],                                      
    python_requires='>=3.6',                # minimum version requirement of the package
    py_modules=['pyt_meta'],                # name of the python package
    package_dir={'':'src'},                 # directory of the source code of the package
    install_requires=[                      # package dependencies
        
                        ## Python 3 Standard Library Members 
                        ##-----------------------------------------
                        ##                            'importlib',                     
                        ##                            'xml',
                        ##                            'os',
                        ##                            'sys',
                        ##                            're',
                        ##                            'time',
                        ##                            'datetime',
                        ##                            'inspect',
                        ##                            'pathlib',
                        ##                            'collections',
                        ##                            'subprocess',
                        ##                            'shutil',
                        ##                            'warnings'
                        ##-----------------------------------------
                ]
    )

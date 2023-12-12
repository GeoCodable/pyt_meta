# -*- coding: utf-8 -*-

# -----------------------------------------------------------------------------

import importlib.util
import os
import sys
import re
import time
import inspect
import warnings
from pathlib import Path
from collections import OrderedDict
from datetime import datetime
from xml.etree.ElementTree import \
     ElementTree as et_root, \
     Element as et_elm, \
     SubElement as et_se
# -----------------------------------------------------------------------------

__name__ =  'pyt_meta'

__info__ = \
    '''
Description:
        The pyt_meta module contains classes and functions that enable automated
        xml metadata file generation for ArcGIS toolboxes and/or any tools contained
        in a given toolbox.   The pyt_meta module enables default metadata
        value generation based on the toolbox and tool class attributes/properties
        and the ArcGIS portal user profile. When geospatial developers wish to override
        and explicitly control metadata, values, the module enables developers to have full control
        and access to the xml metadata keys directly within the python toolbox code.  As an
        added benefit among toolbox/tool deployments, maintenance, and packaging of xml
        support file documents can be eliminated from the process.  This results in less file
        dependencies and can make toolbox deployments more reliable and efficient.
    '''
__alias__ = 'pyt_meta'

__author__ = 'A. Hampton'

__version__ = '0.0.1'

__create_date__ = '20201124'

__modified_date__ = '20210727'

__all__ = \
    [
        'import_toolbox',
        'get_file_dates',
        'py_text_to_html',
        'create_tb_meta'
    ]

# module constants
# -----------------------------------------------------------------------------

# constant for the xml root default attributes 
DEFAULT_XML_ATTRIBS= \
    {
        "metadata": {"xml:lang": "en"},
        "ScopeCd": {"value": "005"},
        "mdDateSt": {"Sync": "TRUE"}
    }

# constant for the default toolbox xml structure 
DEFAULT_TOOLBOX_XML_STRUCT = \
    OrderedDict(
        {
            "metadata": "None",
            "Esri": "metadata",
            "CreaDate": "Esri",
            "CreaTime": "Esri",
            "ArcGISFormat": "Esri",
            "SyncOnce": "Esri",
            "ModDate": "Esri",
            "ModTime": "Esri",
            "scaleRange": "Esri",
            "minScale": "scaleRange",
            "maxScale": "scaleRange",
            "ArcGISProfile": "Esri",
            "toolbox": "metadata",
            "arcToolboxHelpPath": "toolbox",
            "dataIdInfo": "metadata",
            "idCitation": "dataIdInfo",
            "resTitle": "idCitation",
            "idPurp": "dataIdInfo",
            "searchKeys": "dataIdInfo",
            "idAbs": "dataIdInfo",
            "idCredit": "dataIdInfo",
            "resConst": "dataIdInfo",
            "Consts": "resConst",
            "useLimit": "Consts",
            "distInfo": "metadata",
            "distributor": "distInfo",
            "distorFormat": "distributor",
            "formatName": "distorFormat",
            "mdHrLv": "metadata",
            "ScopeCd": "mdHrLv",
            "mdDateSt": "metadata",
        }
    )

# constant for the default tool xml structure 
DEFAULT_TOOL_XML_STRUCT = \
    OrderedDict(
        {
            "metadata": "None",
            "Esri": "metadata",
            "CreaDate": "Esri",
            "CreaTime": "Esri",
            "ArcGISFormat": "Esri",
            "SyncOnce": "Esri",
            "ModDate": "Esri",
            "ModTime": "Esri",
            "scaleRange": "Esri",
            "minScale": "scaleRange",
            "maxScale": "scaleRange",
            "tool": "metadata",
            "arcToolboxHelpPath": "tool",
            "summary": "tool",
            "usage": "tool",
            "scriptExamples": "tool",
            "parameters": "tool",
            "dataIdInfo": "metadata",
            "idCitation": "dataIdInfo",
            "resTitle": "idCitation",
            "idCredit": "dataIdInfo",
            "searchKeys": "dataIdInfo",
            "resConst": "dataIdInfo",
            "Consts": "resConst",
            "useLimit": "Consts",
            "distInfo": "metadata",
            "distributor": "distInfo",
            "distorFormat": "distributor",
            "formatName": "distorFormat",
            "mdHrLv": "metadata",
            "ScopeCd": "mdHrLv",
            "mdDateSt": "metadata",
        }
    )

# constants for default Esri Toolbox metadata values
TOOLBOX_FORMAT_NAME = "ArcToolbox Toolbox"
ARC_GIS_FORMAT = "1.0"
SYNC_ONCE = "TRUE"
MIN_SCALE = "150000000"
MAX_SCALE = "5000"
ARC_GIS_PROFILE = "ItemDescription"

# constants for default Esri Tool metadata values
TOOL_FORMAT_NAME = "ArcToolbox Tool"

# -----------------------------------------------------------------------------


def import_toolbox(toolbox_path):
    """Function imports an ArcGIS python toolbox by name
    from the current script directory and returns
    the Toolbox class object.
    :param - toolbox_path - python toolbox path
    :returns -pyt.Toolbox - ArcGIS python Toolbox class object"""
    if toolbox_path.endswith('.pyt'):
        importlib.machinery.SOURCE_SUFFIXES.append('pyt')
    toolbox_name = os.path.splitext(
        os.path.basename(toolbox_path))[0]    
    spec = importlib.util.spec_from_file_location(
         toolbox_name, toolbox_path)
    pyt = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(pyt)
    return pyt

# -----------------------------------------------------------------------------


def get_file_dates(file_path, date_fmt ='%Y%m%d', time_fmt='%H%M%S%S'):
    '''Function returns created, modified, and last accessed
    date and time values along with the last modified date.
    and time for a given file in UTC.
    :param - file_path  - path to a file
    :param - date_fmt  - desired string date format
    :param - time_fmt  - desired string time format
    :returns - dt_vals - a tuple of file dates and times, see example
            ex. ( created date,created time,
                modified date, modified time,
                last accessed date, last accessed time,
                current date, current time)
    '''
    gt = time.gmtime
    # get the last modified date time
    mtime = os.path.getmtime(file_path)
    mod_date = \
             time.strftime(date_fmt, gt(mtime))
    mod_time = \
             time.strftime(time_fmt, gt(mtime)) 

    # get the created date time
    ctime = os.path.getctime(file_path)
    create_date = \
                time.strftime(date_fmt, gt(ctime))
    create_time = \
        time.strftime(time_fmt, gt(ctime)) 

    # get the last accessed date time
    atime = os.path.getctime(file_path)
    access_date = \
                time.strftime(date_fmt, gt(atime))
    access_time = \
        time.strftime(time_fmt, gt(atime)) 

    # get the current accessed date time
    cur_time = datetime.utcnow()
    cur_date = cur_time.strftime(date_fmt)
    cur_time = cur_time.strftime(time_fmt)

    dt_vals = (create_date, create_time,
                       mod_date, mod_time,
                       access_date, access_time,
                       cur_date, cur_time)
    return dt_vals


# -----------------------------------------------------------------------------


def py_text_to_html(str_value):
    """Function returns a multiline string variable from python
    as a html block. The inspect.cleandoc method is used to
    clean up indentation from python docstrings that are
    indented to line up within blocks of python code. All
    leading whitespaces are removed from the first line.
    Any leading whitespace that can be uniformly removed
    from the second line onwards are removed. Empty lines
    at the beginning and end are subsequently removed. Also,
    all tabs are expanded to spaces.
    :param - str_value  - string (multiline string)
    :returns -rtn_text- reformatted string value"""
    rtn_text = str_value
    rtn_text = inspect.cleandoc(str_value)
    rtn_text = "<br></br>".join(
        ["<span>{0}</span>".format(l) for l in rtn_text.splitlines()]
        )
    return rtn_text


# -----------------------------------------------------------------------------


def set_default_keywords(strs=[]):
    """Function returns search keywords from
    a list of strings.
    :param - strs  - list of string values to build keywords from
    :returns - fmt_kws - list object containing keywords"""
    kws = [kw for kw in re.split("[^a-zA-Z]", " ".join(strs)) if kw.isalnum()]
    kws = [(kw if any(e.isupper() for e in kw) else kw.upper()) for kw in kws]
    kws = list(set(kws))
    fmt_kws = []
    for t in kws:
        matches = re.findall(t, str(kws), re.IGNORECASE)
        if len(matches) > 1:
            for m in matches:
                if m != m.upper():
                    fmt_kws.append(m)
        if t.upper() not in [x.upper() for x in fmt_kws]:
            fmt_kws.append(t)
    fmt_kws = list(set(fmt_kws))
    return fmt_kws


# -----------------------------------------------------------------------------


def create_credits_list(user_name="", org_name="", email=""):
    """Function returns the ArcGIS portal user
    name , org, and email info (if logged in) as a list.
    Otherwise, just  the system user name will be
    returned.
    :param - user_name  - default user name
    :param - org_name  - default org name
    :param - email  - default email
    :returns - user_info - list object"""

    if user_name == "":
        try:
            import getpass
            userId = getpass.getuser()
        except:
            userId == "Unknown"
        
    try:
        if user_name == "" or org_name == "" or email == "":
            import arcpy

            active_portal = arcpy.GetActivePortalURL()
            portal_info = arcpy.GetPortalDescription(active_portal)
            # get the user name
            if user_name == "":
                userId = portal_info["user"]["fullName"]
            else:
                userId == user_name
                # get the org name
            if org_name == "":
                org_name = portal_info["name"]
                # get the user's email
            if email == "":
                email = portal_info["user"]["email"]
    except BaseException:
        # create the output json object
        pass
    user_info = [
                                "<b> Point of Contact (POC):{0}</b> ".format(userId),
                                "<b> Organization: {0}</b> ".format(org_name),
                                "<b> Email: {0}</b> ".format(email)
                          ]
    return user_info


# -----------------------------------------------------------------------------


def get_class_attrib(co, prop_name, default_value="",
                         attrib_multiline=True, dflt_multiline=True):
    """Function retrieves an object property value
    if it exists. Otherwise the default value is returned.
    Options for format the return value as an html block
    and/or remove multiline spacing are available.
    :param - co - input class/object
    :param - prop_name  - object property by name
    :param - default_value  - default for non-existent property
    :param - attrib_multiline - option to format class attribute as multiline text
    :param - dflt_multiline - option to format default value as multiline text"""

    if hasattr(co, prop_name):
        val = getattr(co, prop_name)
        if isinstance(val, str):
            if inspect.cleandoc(val) != val and attrib_multiline:
                val = py_text_to_html(val)
    else:
        val = default_value
        if isinstance(default_value, str):
            if inspect.cleandoc(default_value) != default_value and dflt_multiline:
                val = py_text_to_html(default_value)
    return val


# -----------------------------------------------------------------------------


def build_metadata_structure(metadata_dict, xml_attrib_dict):
    """Function generates a metadata xml etree structure
    given a ordered dictionary object representing
    the hierarchical structure/node order. See example below:
            ex. { 'root_elem': 'None',
                    'child_elem':'root_elem' }
    :param - metadata_dict    - Ordered dictionary; see example above
    returns - (xml_root, xml_elms)- a tuple containing the root xml element
                and a dictionary of all xml elements"""

    xml_elms = {}
    xml_root = None
    for elm, elm_par in metadata_dict.items():
        if str(elm_par) == "None":
            # make the root element
            xml_elms[elm] = et_elm(elm)
            if elm in xml_attrib_dict.keys():
                for attrib, val in xml_attrib_dict[elm].items():
                    xml_elms[elm].set(attrib, val)
            xml_root = xml_elms[elm]
            continue
        else:
            # make the sub element structures
            xml_elms[elm] = et_se(xml_elms[elm_par], elm)
            if elm in xml_attrib_dict.keys():
                for attrib, val in xml_attrib_dict[elm].items():
                    xml_elms[elm].set(attrib, val)
    return (xml_root, xml_elms)


# -----------------------------------------------------------------------------


def set_xml_text_by_class_attrib(class_inst, xml_elms, overwrite=False):
    """Function sets the text value for each xml element in
    a dictionary of xml elements when there is a
    corresponding  xml tag and class attribute in
    the class instance.
    :param - class_inst  - instance of a python object/class
    :param - xml_elms  - dictionary of xml etree elements
                                            ex. {xml_tag: etree_element}
    :param - overwrite  - allow existing xml text values to
                                            be overwritten
    :returns - xml_elms - dictionary of xml etree elements"""
    for tag, elm in xml_elms.items():
        class_attrib = get_class_attrib(class_inst, tag, "")
        if isinstance(class_attrib, str):
            if bool(class_attrib):
                if not elm.text or not bool(elm.text):
                    elm.text = class_attrib
                elif overwrite:
                    elm.text = class_attrib
    return xml_elms


# -----------------------------------------------------------------------------


class toolMetadata(object):
    def __init__(self, tb_metadata, tb_tool):
        self.tb_meta = tb_metadata
        self.tb_tool = tb_tool

        # get general tool information
        # ------------------------------------------------------------------------
        # get the tool name
        self.tool_name = self.tb_tool.__name__
        # get the xml path
        tb_pardir = os.path.abspath(os.path.join(
            self.tb_meta.toolbox_path,
            os.pardir))
        
        self.xml_path =  os.path.abspath(
            r'{0}\{1}.{2}.pyt.xml'.format(
                tb_pardir,
                self.tb_meta.toolbox_name,
                self.tool_name
                )
            )
        
        # create an instance of the tool
        self.tool_inst = self.tb_tool()

        # get tool level metadata from tool instance attributes
        # ------------------------------------------------------------------------
        # tool label
        self.label = get_class_attrib(self.tool_inst, "label", self.tool_name)
        # toolbox alias
        self.alias = self.tb_meta.alias
        # toolbox keywords
        self.toolbox_keywords = " ".join(self.tb_meta.keywords)
        # tool category
        self.category = get_class_attrib(self.tool_inst, "category", "Uncategorized")
        # summary/description text
        dflt_summary = """{0} is an ArcGIS python toolbox tool.
                                              Contact POC below for more information.""".format(
                                              self.tool_name)
        self.summary = get_class_attrib(self.tool_inst, "description", dflt_summary)
        # tool usage text
        self.usage = get_class_attrib(self.tool_inst, "usage", self.summary)
        # set derived tool metadata variables
        self.resTitle = "{0}.({1})".format(self.alias, self.category)
        
        # check for tool searchKeys in the tool attributes
        self.keywords = get_class_attrib(self.tool_inst, "searchKeys", [])
        # generate default keywords from the toolbox
        if not isinstance(self.keywords, list) or not bool(self.keywords):
            self.keywords = set_default_keywords(
                [self.label, self.tool_name, self.toolbox_keywords, self.category]
                )
        
        self.tb_meta.keyword_master.extend(self.keywords)
        # generate a default code sample from the toolbox and tool
        self.code_ex = get_class_attrib(self.tool_inst, "scriptExamples", {})
        self.code_ex = self.validate_code_examples()

    # set default Esri tool metadata values:
    # ---------------------------------------------------------------------------
    formatName = TOOL_FORMAT_NAME
    # --------------------------------------------------------------------------

    def gen_default_code(self):
        """Function generates a default code sample for an arcGIS tool.
        :param - self - arcGIS toolbox metadata object/class
        :returns - code_text- a text code sample"""

        param_text = ""

        tb_import = [
            "# import the toolbox as a module",
            "import arcpy",
            "arcpy.ImportToolbox(r'{0}',".format(
                self.tb_meta.toolbox_path),
            "{0}r'{1}')".format(" " * 20, self.tb_meta.alias),
            ]

        tool_call = "result = arcpy.{0}_{1}".format(
            self.tool_name, self.tb_meta.alias)
        lead_sp = " " * 11
        if hasattr(self.tool_inst, "getParameterInfo"):
            t_args = self.tool_inst.getParameterInfo()
            max_p_len = max([len(a.name) for a in t_args])
            p_sep = ",\n" + lead_sp
            param_text = p_sep.join(
                    [
                    "{0}{1}#{2}- Type({3})".format(
                        a.name,
                        " " * (max_p_len + 4 - len(a.name)),
                        a.displayName,
                        a.datatype)
                    for a in t_args
                    ]
                )
        tool_code = [
            "# call the tool and return the output",
            "{0}(\n{1}{2}\n{1})".format(tool_call, lead_sp, param_text)
            ]
        code_text = '{0}\n\n{1}'.format(
                                                        '\n'.join(tb_import),
                                                        '\n'.join(tool_code)
                                                        )
        return code_text

    # --------------------------------------------------------------------------

    def validate_code_examples(self):
        """Function to parse and validate code description json objects.
        See example json properly formatted object below:
        Ex. JSON object
            {'Code Sample 1' : {
                       'para' : 'Sample of tool code in python:',
                       'code' : ['def hello_world_func():',
                                        '    print("Hello World!")']
                    }
            }
        If the input object is not properly formatted or absent, the default
        code sample will be returned.
        :param - self - arcGIS toolbox metadata object/class
        :returns - rtn_json- a validated code sample json object"""
        rtn_json = {}
        try:
            # if any error due to null or improper formatting,
            # skip to except and return the default code example only
            if self.code_ex == {}:
                raise ValueError("Code example is not available")
            for (title, details) in self.code_ex.items():
                title_str = title
                desc_str_ = details["para"]
                code_str ="\n".join(details["code"])
                if title_str.strip() == "":
                    title_str = "{0}: Code Sample)".format(self.label)
                if desc_str_.strip() == "":
                    details["para"] = "Sample Description: {0}".format(self.summary)
                if not bool(code_str):
                    raise ValueError("Code example is not available")
                rtn_json[title] = {"para": desc_str_, "code": code_str}
            return rtn_json
        except BaseException:
            # generate the default code sample
            title_str = "{0}: Code Sample (1)".format(self.label)
            desc_str_ = '''
                                    <em>    <b>Note</b> : Calling custom toolboxes is only available</em>
                                    <em>    within external python interpreters and script files!</em>
                                    <em>    Code sample will not work in ArcGIS python windows.</em>
                                    <em>    Code sample will not work in ArcGIS python notebooks.</em>'''
            code_str = self.gen_default_code()
            rtn_json = {title_str: {"para": desc_str_, "code": code_str}}
        return rtn_json

# ------------------------------------------------------------------------------


class toolboxMetadata(object):
    def __init__(
        self,
        toolbox_path,
        overwrite=False,
        toolbox_xml_dict={},
        toolbox_xml_attrib_dict={},
        tool_xml_dict={},
        tool_xml_attrib_dict={}):

        source_path = str(Path(toolbox_path).resolve())
        # ------------------------------------------------------------------------
        # set the path property to the toolbox (.pyt file)
        self.toolbox_path = source_path
        # set the toolbox name property
        self.toolbox_name = os.path.splitext(
            os.path.basename(toolbox_path))[0]
        # set the object overwrite property
        self.overwrite = overwrite

        # set the default xml structure dictionaries
        # ------------------------------------------------------------------------
        if not bool(tool_xml_dict):
            # use a default xml structure
            self.tool_xml_dict = DEFAULT_TOOL_XML_STRUCT
        else:
            self.tool_xml_dict = tool_xml_dict
        if not bool(toolbox_xml_dict):
            # use a default xml structure
            self.toolbox_xml_dict = DEFAULT_TOOLBOX_XML_STRUCT
        else:
            self.toolbox_xml_dict = toolbox_xml_dict
        # set the default xml attribute dictionaries
        # ------------------------------------------------------------------------

        self.toolbox_xml_attrib_dict = toolbox_xml_attrib_dict
        if not bool(self.toolbox_xml_attrib_dict):
            self.toolbox_xml_attrib_dict = DEFAULT_XML_ATTRIBS
        self.tool_xml_attrib_dict = tool_xml_attrib_dict
        if not bool(self.tool_xml_attrib_dict):
            self.tool_xml_attrib_dict = DEFAULT_XML_ATTRIBS
        # get general toolbox information
        # ------------------------------------------------------------------------
        # get the name of the current script/module file
        self.mod_name = os.path.splitext(os.path.basename(__file__))[0]

        # import  the Toolbox class object
        self.tb = import_toolbox(self.toolbox_path).Toolbox
        
        # create an instance of the Toolbox
        self.tb_inst = self.tb()

        # get a list of the tools in the Toolbox instances
        self.tb_tools = [t for t in self.tb_inst.tools]
        
        # get the ArcGIS help resources path
        self.arcToolboxHelpPath = os.path.join(
            os.path.abspath(os.path.join(sys.path[0], os.pardir)), "Help\\gp")

        # get toolbox level metadata from toolbox instance attributes
        # ------------------------------------------------------------------------
        # toolbox alias
        self.alias = get_class_attrib(self.tb_inst, "alias", self.toolbox_name)
        # toolbox idPurp/description text
        dflt_idPurp =   '''{0} is an ArcGIS python toolbox.
                                       Contact POC below for more information.'''.format(
                                        self.toolbox_name)

        self.idPurp = get_class_attrib(self.tb_inst, "description", dflt_idPurp)
        # toolbox idAbs/abstract text
        dflt_idAbs = '{0}{1}{2}'.format(
                                self.idPurp,
                                "<br></br>" * 2,
                                self.create_abstract_tool_text(self.tb_tools)
                                )

        self.idAbs = get_class_attrib(self.tb_inst, "idAbs", dflt_idAbs)
        # set derived tool metadata variables
        self.resTitle = self.toolbox_name
        # check for toolbox searchKeys in the toolbox attributes
        self.keyword_master = []
        self.keywords = get_class_attrib(self.tb_inst, "searchKeys", [])

        # generate default keywords from the toolbox
        if not isinstance(self.keywords, list) or not bool(self.keywords):
            self.keywords = set_default_keywords([self.alias, self.toolbox_name])
        self.keyword_master = self.keywords.copy()
        # get the toolbox created and mod date/times
        self.toolbox_dates = get_file_dates(self.toolbox_path)
        self.CreaDate = self.toolbox_dates[1]
        self.CreaTime = self.toolbox_dates[0]
        self.ModDate = self.toolbox_dates[2]
        self.ModTime = self.toolbox_dates[3]
        self.mdDateSt = self.toolbox_dates[6]

        # create default credit info from the ArcGIS portal session
        self.creditsList = create_credits_list()
        dflt_idCredit = "<br></br>".join(self.creditsList)
        self.idCredit = get_class_attrib(self.tb_inst, "idCredit", dflt_idCredit)
        # build a default usage limits statement
        dflt_useLimit =  '''<b>For questions regarding usage limitations, contact:</b>
                                           {0}
                                           {1}
                                           {2}
                                        <br></br>
                                        <b>Disclaimer: **Metadata auto generated with module {3}**</b>
                                        <b>    -For detailed release notes, contact the POC above!</b>
                                        '''.format(
            self.creditsList[0], self.creditsList[1], self.creditsList[2], self.mod_name)
        self.useLimit = get_class_attrib(self.tb_inst, "useLimit", dflt_useLimit)
        # holders for tool metadata objects and xml root objects
        self.def_tool_metas = []
        self.xml_roots = {}
        
        # set default Esri Toolbox metadata values:
        # ------------------------------------------------------------------------
        self.formatName = TOOLBOX_FORMAT_NAME
        self.ArcGISFormat = ARC_GIS_FORMAT
        self.SyncOnce = SYNC_ONCE
        self.minScale = MIN_SCALE
        self.maxScale = MAX_SCALE
        self.ArcGISProfile = ARC_GIS_PROFILE        
        # ------------------------------------------------------------------------

    def generate_toolbox_metadata(self):
        """Method imports creates a toolbox xml metadata object
        given the toolbox metadata structure as an ordered dictionary,
        a dictionary of element attribute values, an instance of the toolbox
        and a toolbox metadata object (self). 
        :param - self - toolbox metadata object
        :returns -tb_meta_dict - dictionary of toolbox metadata path
                                                and root elements
                                 Ex. {xml output path, etree root element}"""               
        if "toolbox" not in self.toolbox_xml_attrib_dict.keys():
            self.toolbox_xml_attrib_dict["toolbox"] = {
                "name": self.toolbox_name,
                "alias": self.alias
                }
        # --------------------------------------------------------------------
        # build the xml metadata structure
        xml_root, xml_elms = build_metadata_structure(
            self.toolbox_xml_dict, self.toolbox_xml_attrib_dict)
        # --------------------------------------------------------------------
        # set the xml element text  with text values from the toolbox class
        xml_elms = set_xml_text_by_class_attrib(self.tb_inst, xml_elms)
        # set the xml element text with text via the toolbox metadata co
        xml_elms = set_xml_text_by_class_attrib(self, xml_elms)
        # --------------------------------------------------------------------
        # create and set the searchKeys sub-element 'keyword' values
        self.keyword_master = set_default_keywords([" ".join(self.keyword_master)])
        for kw in self.keyword_master:
            et_se(xml_elms["searchKeys"], "keyword").text = kw
        tb_meta_dict = {self.toolbox_path + '.xml': xml_root}
        return tb_meta_dict

    # ------------------------------------------------------------------------

    def generate_tool_metadata(self):
        """Method creates a tool xml metadata object
        given the tool metadata structure as an ordered dictionary,
        a dictionary of element attribute values, an instance of the
        tool, an instance of the toolbox, the tool metadata object
        and the toolbox metadata object (self). 
        :param - self - toolbox metadata object
        :returns -xml_roots - dictionary of tool metadata path
                                                and root elements
                                    Ex. {xml output path, etree root element}"""          
        # begin creating the xml data for the tools in the toolbox
        for tb_tool in self.tb_tools:
            def_tool_meta = toolMetadata(self, tb_tool)
            tool_inst = tb_tool()
        
            if "tool" not in self.tool_xml_attrib_dict.keys():
                self.tool_xml_attrib_dict["tool"] = {
                    "xmlns": "",
                    "name": tb_tool.__name__,
                    "displayname": def_tool_meta.label,
                    "toolboxalias": self.alias
                    }
            # --------------------------------------------------------------------
            # build the xml metadata structure
            xml_root, xml_elms = build_metadata_structure(
                self.tool_xml_dict, self.tool_xml_attrib_dict)
            # --------------------------------------------------------------------
            # attribute the  xml element text with values from a tool instance
            xml_elms = set_xml_text_by_class_attrib(tool_inst, xml_elms)
            # attribute the  xml element text with values from a toolbox instance
            xml_elms = set_xml_text_by_class_attrib(self.tb_inst, xml_elms)

            # attribute the remaining  null xml element text items with default values
            # values set in the toolbox/tool code override the defaults
            # set default values from the tool metadata co
            xml_elms = set_xml_text_by_class_attrib(def_tool_meta, xml_elms)
            # set default values from the toolbox metadata co
            xml_elms = set_xml_text_by_class_attrib(self, xml_elms)
            # --------------------------------------------------------------------
            # create and set the searchKeys sub-element 'keyword' values
            for kw in def_tool_meta.keywords:
                et_se(xml_elms["searchKeys"], "keyword").text = kw
            # --------------------------------------------------------------------
            # create and set the code example metadata
            for (title, details) in def_tool_meta.code_ex.items():
                scriptExample = et_se(
                    xml_elms["scriptExamples"], "scriptExample")
                et_se(scriptExample, "title").text = title
                et_se(scriptExample, "para").text = py_text_to_html(
                    details["para"] )
                et_se(scriptExample, "code").text = details["code"]
            # --------------------------------------------------------------------
            # loop the tool's input arguments/params, for each arg:
            # create and set the tool sub-element 'parameters' attributes and values
            if hasattr(tool_inst, "getParameterInfo"):
                t_args = tool_inst.getParameterInfo()
                for a in t_args:
                    # create an new parameter elm and set the xml attributes
                    p_elm = et_se(
                        xml_elms["parameters"],
                        "param", type = a.parameterType, datatype = a.datatype,
                        name = a.name, displayname = a.displayName,
                        direction = a.direction,
                        )
                    # get/set the parameter sub-element 'dialogReference' values
                    et_se(
                        p_elm, "dialogReference").text = py_text_to_html(
                            '<em>' + get_class_attrib(a, "dialogReference", a.displayName
                            ) + '</em><br></br>'
                        )
                    # get p_elm dependencies
                    p_depen = 'N/A'
                    if hasattr(a, 'parameterDependencies'):                    
                        if bool(a.parameterDependencies):
                            p_depen = a.parameterDependencies
                    p_depen = '<u>Dependencies:</u> {0}'.format(p_depen)
                    
                    # get p_elm default
                    p_def = '<u>Default Value:</u> N/A'
                    if hasattr(a, 'valueAsText'):
                        if bool(a.valueAsText):
                            p_def = '<u>Default Value:</u> {0}'.format(a.value)
                        

                    # get p_elm allowed values (up to 10 values)
                    p_filter_type = ''
                    p_filter_list = ''
                    if hasattr(a, 'filter'):
                        if bool(a.filter.type):
                            p_filter_type = a.filter.type
                        if p_filter_type == 'ValueList' and bool(a.filter.list):

                            lead_space = '&#160; ' * 8
                            p_filter_prefix =  '\n<span>{0}-</span>'.format(lead_space)
                            p_filter_list = '<u>Allowed Values:</u>' + \
                                            ((p_filter_prefix).join([''] + a.filter.list[0:10]))
                            if len(a.filter.list) > 10:
                                msg_prefix =  '\n<span>{0}</span>'.format(lead_space)
                                p_filter_list = p_filter_list + (msg_prefix + '<b>*Only first 10 values displayed...*</b>')
                                p_filter_list = p_filter_list + (msg_prefix + '  <b>*See tool parameter for full list...*</b>')
                        if p_filter_type == 'Range' and len(a.filter.list) == 2:
                            p_filter_list = '<u>Allowed Range:</u> Min({0}),  Max ({1})'.format(
                                a.filter.list[0],
                                a.filter.list[1])
                            
                    # create the default pythonReference text
                    py_ref = (
                        '''<u>Python variable name:</u> (<em>{0}</em>)
                           <u>Description:</u> {1} {2} value representing the tool
                           {8}"<em>{3}</em>" {4} parameter.
                           {5}
                           {6}
                            {7}'''.format(
                            a.name, a.parameterType, a.datatype.lower(),
                            a.displayName, a.direction, p_depen, p_def,
                            p_filter_list, (10 * '&#160; '))
                        )

                    # get/set the p_elm sub-element 'pythonReference' attributes
                    et_se(
                        p_elm, "pythonReference").text = py_text_to_html(
                        get_class_attrib(a, "pythonReference", py_ref
                        )
                    )
            # --------------------------------------------------------------------
            # retain metadata and xml variables as attributes for debugging
            self.def_tool_metas.append(def_tool_meta)
            self.xml_roots[def_tool_meta.xml_path] = xml_root
        return self.xml_roots

    # --------------------------------------------------------------------------
    
    def create_abstract_tool_text(self, tb_tools):
        """Method creates the default toolbox metadata abstract
        text statement.  The resulting statement has provides an
        overview and lists out the tools contained in the toolbox. 
        :param - self - toolbox metadata object
        :param - tb_tools - list of toolbox tool classes
        :returns -rtn_text - display text for the toolbox abstract"""         
        tool_lines = ["<b>Included Tools:</b>"]
        for tb_tool in tb_tools:
            tool_inst = tb_tool()
            tool_name = get_class_attrib(tool_inst, "label", tb_tool.__name__)
            tool_cat = get_class_attrib(tool_inst, "category", "None")
            tool_desc = get_class_attrib(tool_inst, "description", "", False, False)
            if not bool(tool_desc):
                tool_desc = get_class_attrib(tool_inst, "usage", "", False, False)
            tool_lines.append(
                "<br></br><b>    - {0}</b> (Category: {1})".format(tool_name, tool_cat)
            )
            for line in tool_desc.splitlines():
                tool_lines.append("<em>        {0}</em>".format(line.strip()))
        rtn_text = "<br></br>".join(tool_lines)
        return rtn_text

    # --------------------------------------------------------------------------
    
    def xml_tree_to_file(self, out_path, xml_root):
        """Method creates or overwrites an xml document
        with the xml etree object provided at the given path. 
        :param - self - toolbox metadata object
        :param - out_path - output path
        :param - xml_root - xml etree root element
        :returns -none - """            
        # skip creating  metadata if the xml exists and overwrite == False
        if (not os.path.exists(out_path)) or self.overwrite:
            t = et_root(xml_root)
            t.write(out_path, encoding="utf-8", xml_declaration=True)
            print(out_path)
        return
    
    # --------------------------------------------------------------------------
    
    def write_tool_xml_metadata(self):
        """Method writes each tool xml element
        to an output path derived from the 
        generate_tool_metadata method. 
        :param - self - toolbox metadata object
        :returns -none - """             
        xml_roots = self.generate_tool_metadata()
        for out_path, xml_root in xml_roots.items():
            self.xml_tree_to_file(out_path, xml_root)
        return
    
    # --------------------------------------------------------------------------
    
    def write_toolbox_xml_metadata(self):
        """Method writes the toolbox xml element
        to an output path derived from the 
        generate_tool_metadata method. 
        :param - self - toolbox metadata object
        :returns -none - """          
        xml_roots = self.generate_toolbox_metadata()
        for out_path, xml_root in xml_roots.items():
            self.xml_tree_to_file(out_path, xml_root)
        return
    
    # --------------------------------------------------------------------------
    
    def write_all_xml_metadata(self):
        """Method writes the xml metadata for
        the toolbox and all  tools belonging to the
        toolbox to the toolbox (pyt) directory. 
        :param - self - toolbox metadata object
        :returns -none - """           
        self.write_tool_xml_metadata()
        self.write_toolbox_xml_metadata()
        return

# -----------------------------------------------------------------------------

def create_tb_meta(toolbox_path,overwrite=False):
    """Function calls a process that writes
    xml metadata for all toolbox class objects. 
    :param - toolbox_path - path to the toolbox file (.pyt)
    :returns -Boolean - True on success """               
    rtn_val = False
    if not toolbox_path.endswith('.pyt'):
        return
    source_path = str(Path(toolbox_path).resolve())
    try:
        toolboxMetadata(
                                source_path,
                                overwrite
                                ).write_all_xml_metadata()            
        rtn_val =  True
    except:
        warnings.warn('Failed to generate toolbox metadata!')
    return rtn_val

# -----------------------------------------------------------------------------

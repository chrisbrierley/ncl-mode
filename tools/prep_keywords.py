#!/usr/bin/env python
'''
Download and collect Ncl keywords from Ncl website
'''

DATE     = "Friday, February 15 2013"
AUTHOR   = "Yagnesh Raghava Yakkala"
WEBSITE  = "http://yagnesh.org/yyr/ncl-mode"
LICENSE  = "GPL v3 or later"

import sys
import os
import pickle
import inspect
import urllib2
from bs4 import BeautifulSoup

file_path = os.path.abspath(os.path.split(inspect.getfile(inspect.currentframe()))[0])
DATA_DIR = os.path.join(file_path,'../data')
base_url = "http://www.ncl.ucar.edu/Document/"

def get_save_page(url,local_file = ''):
    """fetch given url and save it to data directory.
    """
    if not os.path.exists(DATA_DIR):
        os.makedirs(DATA_DIR)

    local_file = os.path.join(DATA_DIR , url.split('/')[-1] )
    print("Fetching.. " + url)

    if os.path.exists(local_file):
        fh = open(local_file, "rb")
        print(local_file + " is already exists, skipping ..")
        page = fh.read()
        return page

    else:
        fh = open(local_file, "wb")
        user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        r = urllib2.Request(url=url,headers={'User-Agent' : user_agent})
        try:
            oh = urllib2.urlopen(r)
            page = oh.read()
            fh.write(page)
            return page
        except urllib2.URLError, e:
            print("URLError: %s" % e)
            sys.exit()
        except Exception:
            import traceback
            print('Generic exception: ' + traceback.format_exc())
            sys.exit()


class NclKeywordFetcher(object):
    """Fetches and stores ncl keywords.
    """
    def __init__(self, down_from_web = False):
        self.down_from_web = down_from_web
        self.ncl_functions = self.ncl_procs_and_funcs()
        self.ncl_resources = self.ncl_resources()

    def ncl_procs_and_funcs(self):
        """ Fetch and save ncl procedures/function names.
        """
        url = "http://www.ncl.ucar.edu/Document/Functions/list_alpha_browse.shtml"
        cats = [["builtin"    , "ncl built-in functions"                           , "/Document/Functions/Built-in/"]         ,
                ["contrib"    , "contributed functions"                            , "/Document/Functions/Contributed/"]      ,
                ["diag"       , "diagnostics functions"                            , "/Document/Functions/Diagnostics/" ]     ,
                ["pop"        , "pop_remap functions"                              , "/Document/Functions/Pop_remap/"]        ,
                ["shea"       , "shea_util functions"                              , "/Document/Functions/Shea_util/"]        ,
                ["skewt"      , "skewt functions"                                  , "/Document/Functions/Skewt_func/"]       ,
                ["user"       , "user_contributed functions"                       , "/Document/Functions/User_contributed/"] ,
                ["wrfarw"     , "wrf_arw functions"                                , "/Document/Functions/WRF_arw/"]          ,
                ["wrfcontrib" , "wrf_contributed functions"                        , "/Document/Functions/WRF_contributed/"]  ,
                ["windrose"   , "wind_rose functions"                              , "/Document/Functions/Wind_rose/"]        ,
                ["gsn"        , "gsn csm plot templates and special gsn functions" , "/Document/Graphics/Interfaces/"]]
        page = get_save_page()
        return functions

    def ncl_resources(self):
        """ Fetch and save ncl resources.
        """
        url = "http://www.ncl.ucar.edu/Document/Graphics/Resources/list_alpha_res.shtml"
        page = get_save_page(url)

    def ncl_keywords(self):
        url   = "http://www.ncl.ucar.edu/Document/Manuals/Ref_Manual/NclKeywords.shtml"
        page = get_save_page(url)

    def ncl_operators(self):
        operators = ["(/","/)","\ ",".eq.",".ne.",".lt.",".le.",".gt.",
                     ".ge.",".and.",".or.",".not.",".xor."]


class KeywordWriter(object):
    """update to ncl-keyword
    """
    def __init__(self,elisp_file):
        self.elisp_file = elisp_file
        self.elisp_file_lines = open(elisp_file).read()
        self.update_elisp_file()

    def elisp_lines(self):
        fetcher = NclKeywordFetcher()
        fetcher.get_ncl_keywords()

    def update_elisp_file(self):
        pass


def main():
    elisp_file = os.path.join(file_path, "../lisp/ncl-mode-keywords.el")
    if os.path.exists(elisp_file):
        elf = KeywordWriter(elisp_file)
    else:
        print(elisp_file + " is not available.")
        sys.exit(2)

if __name__ == '__main__':
    main()

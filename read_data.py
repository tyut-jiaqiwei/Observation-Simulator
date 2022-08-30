import random
import ephem

random.seed(1314)
"""
卫星的数据批量读取
"""

def read_tle(flie_name):
    with open(flie_name,"r") as f :
        linenumber = 0
        star_tle = []
        the_tle = dict()
        for line in f.readlines():
            linenumber += 1
            if linenumber % 3 == 1:
                the_tle.update({'line1': line})
            if linenumber % 3 == 2:
                the_tle.update({'line2': line})
            if linenumber % 3 == 0:
                the_tle.update({'line3': line})
                star_tle.append(the_tle.copy())
                the_tle.clear()
    return star_tle


"""
彗星的数据批量读取
"""
def read_ddb(flie_name):
    with open(flie_name,"r") as f :
        linenumber = 0
        star_ddb = []
        the_ddb = dict()
        for line in f.readlines():
            linenumber += 1
            if linenumber % 2 == 0:
                the_ddb.update({'ddb': line})
                star_ddb.append(the_ddb.copy())
                the_ddb.clear()
    return star_ddb

"""
恒星的数据批量读取
"""
def read_fix(file_name):
    with open(file_name,"r") as f :
        star_fix = []
        the_ddc = dict()
        for line in f.readlines():
            the_ddc.update({'ddc': line})
            star_fix.append(the_ddc.copy())
            the_ddc.clear()
    return star_fix


"""
小行星（Bright and CritList and Distant and Unusual）的数据批量读取
"""
def read_minorplanet(flie_name):
    with open(flie_name,"r") as f :
        linenumber = 0
        star_dde = []
        the_dde = dict()
        for line in f.readlines():
            linenumber += 1
            if linenumber % 2 == 0:
                the_dde.update({'dde': line})
                star_dde.append(the_dde.copy())
                the_dde.clear()
    return star_dde








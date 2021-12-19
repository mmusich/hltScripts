#! /usr/bin/env python3
import cx_Oracle
import sys

def getConfDBdescr(configBase, addLink=True, fixCapital=True, run3=True):
    ## Connect to confDB
    if run3:
        connstr = 'cms_hlt_v3_r/convertMe!@cmsr'
    else:
        connstr = 'cms_hlt_gdr_r/convertMe!@cmsr'
    conn = cx_Oracle.connect(connstr)
    curs = conn.cursor()
    curs.arraysize=50

    confDBdescr = []
    ## Loop on HLT versions
    for version in range(1,1000):
        configuration = configBase + "/V"+str(version)
        ### get only Config description
        # query="select a.description from u_confversions a where a.name='"+configuration+"'"
        ### get only Config description and release
        query="SELECT u_confversions.description, u_softreleases.releaseTag FROM u_confversions, u_softreleases WHERE u_confversions.id_release = u_softreleases.id AND u_confversions.name='%s'"%(configuration)
        curs.execute(query)
        curs_copy=curs
        ## get first row (curs_copy contains only one element here)
        for rows in curs_copy:
            ## get description, if it is not empty
            try:
                description = rows[0].read()
            except:
                description =""
            
            ## get release, if it is not empty
            try:
                release = rows[1]
            except:
                release =""
            
            ## add link to JIRA tickets
            if addLink:
                posInit = description.find("CMSHLT-")
                if posInit>=0:
                    posFinal = posInit+7
                    while (posFinal<len(description) and description[posFinal].isdigit()): posFinal+=1
                    cmshlt = description[posInit:posFinal]
                    description = description.replace(cmshlt,"[[https://its.cern.ch/jira/browse/%s][%s]]"%(cmshlt,cmshlt))
             
            ## add '!' in front of capital letters
            if fixCapital:
                for i in range(len(description)):
                    if description[i].isupper() and (i==0 or description[i-1]==" "):
                        description = description[:i]+"!"+description[i:]
            
            # add release in teh configuration description (eg. /dev/CMSSW_12_3_0/HLT/V18 (CMSSW_12_3_0_pre2) )
            configuration = configuration + " (%s)"%(release)
            ## fill confDBdescr
            confDBdescr.append((configuration,description))

    confDBdescr.reverse()
    return confDBdescr

#if __name__ == "__main__":
#    confDBdescr = getConfDBdescr(sys.argv[1])
#    print('''---+ !HLT menus in !ConfDB:
#---++ !HLT Developments in !ConfDB %s'''%(sys.argv[1]))
#    for address,description in confDBdescr:
#           print("   * =%s=: %s"%(address,description))

import sys

print("python3 makeConfDBXXXTWiki.py /dev/CMSSW_12_3_0/HLT")
run3=True
condDBbase = sys.argv[1]

confDBdescr = getConfDBdescr(condDBbase, run3=run3)

### Loop in releases
twiki ="""
---+ !HLT menus in !ConfDB: pp menus for "Run3" preparation (12_4_X)


---++ !HLT Developments in !ConfDB %s
"""%(condDBbase)
for (configuration, description) in confDBdescr:
    ### download the html and parse it
        twiki += "   * =%s=: %s\n"%(configuration,description)

print(twiki)

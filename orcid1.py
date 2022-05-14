import urllib.request
from xml.dom import minidom
import sys
import numpy as np

print('Please type the identifier of your scientist: ')
orcid=str(input())

with urllib.request.urlopen("https://pub.orcid.org/{}".format(orcid)) as f:
    info = f.read().decode("utf-8")


data=minidom.parseString(info)


name=data.getElementsByTagName('personal-details:given-names')[0].firstChild.data
surname=data.getElementsByTagName('personal-details:family-name')[0].firstChild.data
#print(info)
print('NAME:',name)
print('SURNAME:',surname)
fullname='{}_{}'.format(name,surname)


txt=open('{}.txt'.format(fullname),'w')

works = data.getElementsByTagName("activities:works")[0]
print('PAPERS:')
txt.write('PAPERS')
txt.write("\n")
for work in works.getElementsByTagName("activities:group"):
    title = work.getElementsByTagName("common:title")[0].firstChild.data
    year = work.getElementsByTagName("common:year")[0].firstChild.data
    idtyp= work.getElementsByTagName("common:external-id-type")[0].firstChild.data
    idval=str(work.getElementsByTagName("common:external-id-normalized")[0].firstChild.data)
    url= work.getElementsByTagName("common:url")[0].firstChild.data
    print('TITLE: ',title)
    tititle='TITLE: {}'.format(title)
    print('YEAR OF PUBLISHMENT: ',year)
    yeyear='YEAR OF PUBLISHMENT: {}'.format(year)
    print('AUTORZY: ')
    txt.write(tititle)
    txt.write("\n")
    txt.write(yeyear)
    txt.write("\n")
    txt.write('AUTHORS: ')
    txt.write("\n")
    if idtyp=='doi':
        req = urllib.request.Request("https://doi.org/{}".format(idval))
        req.add_header("Accept", "application/rdf+xml")
        with urllib.request.urlopen(req) as f:
            doinfo = f.read().decode("utf-8")
        doidata=minidom.parseString(doinfo)
        author=doidata.getElementsByTagName('j.0:creator')
        for i in author:
            name=i.getElementsByTagName('j.3:name')[0].firstChild.data
            print(name)
            
            txt.write(name)
            txt.write("\n")
    elif idtyp=='arxiv':
        with urllib.request.urlopen("http://export.arxiv.org/api/query?id_list={}".format(idval)) as f:
            arxinfo = f.read().decode("utf-8")
        arxdata= minidom.parseString(arxinfo)
        authors=arxdata.getElementsByTagName('author')
        for i in authors:
            author=i.getElementsByTagName('name')[0].firstChild.data
            print(author)

            txt.write(author)
            txt.write("\n")
    elif idtyp!='doi' and idtyp!='arxiv':
        print('no info')
        txt.write('no info')
        txt.write("\n")

    print(idtyp,':',idval)
    print(url)
    print('**********************************************')
    idtypes='{}: {}'.format(idtyp,idval)
    txt.write(idtypes)
    txt.write("\n")
    txt.write(url)
    txt.write("\n")
    txt.write('**********************************************')
    txt.write("\n")
f.close()




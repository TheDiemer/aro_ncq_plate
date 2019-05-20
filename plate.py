#! /opt/app-root/bin/python3
import sys
sys.path.append('/opt/app-root/src/config/')
from sso import sso
import requests
import time
import json


def main():
    url = 'https://hydra.ext.paas.redhat.com/hydra/rest/cases/?status=Waiting%'
    url += '20on%20Red%20Hat%2CWaiting%20on%20Customer&sbrGroups=Shift%20Hoste'
    url += 'd&fields=caseNumber,contact.timezone,tags,subject,strategic,initia'
    url += 'lServiceLevel,severity,priorityScore,sbt,fts,caseOwner.name,needsN'
    url += 'ewOwner,createdDate,lastModifiedDate,status,caseType,critSit,isEsc'
    url += 'alated'
    try:
        r = requests.get(
                  url,
                  auth=(
                         sso.username,
                         sso.password
                         ),
                  verify=False
                  )
    except Exception as e:
        return failed()
    if r.status_code == 200:
        # Do More Things
        plate = '<!doctype html>\n<html>\n<head>\n <style>\n  table, th,'
        plate += ' td {   border: 1px solid black;   border-collapse: coll'
        plate += 'apse;  }  th, td {   padding: 5px;  }  #value {   font-w'
        plate += 'eight: bold;  }\n </style>\n</head>\n<body>\n  <h1>This is the current plate of ARO tagged cases:</h1>\n  <table>'
        plate = formatString(r.json(), plate)
        plate += '\n  </table>\n <h3>This was collected at: {0} UTC</h3>\n</body>\n</html>'.format(time.strftime("%Y/%m/%d - %H:%M:%s",time.gmtime()))
        return plate
    else:
        return failed()


def failed():
    return '<!doctype html>\n<html>\n<h1>Sorry, but I seem to have had an issue! Can you refresh the page to try again?\n</h1>\n</body>\n</html>'

def formatString(cases, plate):
    # To make sure everything has a SBT
    for sbtCase in cases:
        try:
            sbtCase['sbt'] = int(sbtCase['sbt'])
        except KeyError:
            sbtCase['sbt'] = 0
    plate += '<tr>'
    for header in ['Case Numb','contact.timezone','tags','subject','strategic','initialServiceLevel','severity','priorityScore','sbt','fts','caseOwner','needs new owner?','createdDate','lastModifiedDate','status','caseType','critSit','isEscalated']:
        plate += '<th>{0}</th>'.format(header)
    plate += '</tr>'
    # To sort by SBT
    for singleCase in sorted(cases, key=lambda x: int(x['sbt'])):
        if 'azure_sre' in str(singleCase.get('tags')):
            if (singleCase.get('status') is not None) and ('customer' in singleCase.get('status').lower()):
                color = 'rgb(0,153,255,0.5)'
            else:
                if int(singleCase['sbt']) < 0:
                    color = 'rgb(255, 99, 71, 0.5);font-weight:bold'
                elif int(singleCase['sbt']) < 60:
                    color = 'rgb(255, 99, 71, 0.5)'
                elif int(singleCase['sbt']) <= 240:
                    color = 'rgb(255,165,0,0.5)'
                else:
                    color = 'rgb(0,128,0,0.5)'
            plate += '<tr style="background-color:{0}">'.format(color)
            fields = []
            fields.append('<a href="https://access.redhat.com/support/cases/#/case/{0}">{0}</a>'.format(singleCase['caseNumber']))
            fields.append(singleCase.get('contact.timezone'))
            fields.append(singleCase.get('tags'))
            fields.append(singleCase.get('subject'))
            fields.append(singleCase.get('strategic'))
            fields.append(singleCase.get('initialServiceLevel'))
            fields.append(singleCase.get('severity'))
            fields.append(singleCase.get('priorityScore'))
            fields.append(singleCase.get('sbt'))
            fields.append(singleCase.get('fts'))
            fields.append(singleCase.get('caseOwner.name'))
            fields.append(singleCase.get('needsNewOwner'))
            fields.append(singleCase.get('createdDate'))
            fields.append(singleCase.get('lastModifiedDate'))
            fields.append(singleCase.get('status'))
            fields.append(singleCase.get('caseType'))
            fields.append(singleCase.get('critSit'))
            fields.append(singleCase.get('isEscalated'))
            for field in fields:
                plate += '<td>{0}</td>'.format(field)
            # Include the case
            plate += '</tr>\n'
        else:
            pass
    return plate


if __name__ == '__main__':
    main()

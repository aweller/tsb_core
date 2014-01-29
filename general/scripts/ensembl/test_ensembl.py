import httplib2, sys
 
http = httplib2.Http(".cache")
 
server = "http://beta.rest.ensembl.org"
ext = "/vep/human/12:25380276:25380276/C/consequences?"
resp, content = http.request(server+ext, method="GET", headers={"Content-Type":"application/json"})
 
if not resp.status == 200:
  print "Invalid response: ", resp.status
  sys.exit()
  
  
def flatten(l):
    out = []
    if isinstance(l, (list, tuple)):
        for item in l:
            out.extend(flatten(item))
    elif isinstance(l, (dict)):
        for dictkey in l.keys():
            out.extend(flatten(l[dictkey]))
    elif isinstance(l, (str, int, unicode)):
        out.append(l)
    return out  

import json

decoded = json.loads(content)

for item in flatten(decoded):
    print item

# for k,v in decoded.iteritems():
#     for a in v:
#         for t in a["transcripts"]:
#             print t
#             print "================================="
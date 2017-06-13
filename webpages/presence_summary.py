#!/usr/bin/python
import glob
import gviz_api
import datetime
import cgi
import cgitb

def loadmap():
   mapfilename="/home/pi/PresenzeApolloni/macddrlist.txt"
   mapfile = open(mapfilename)
   line = mapfile.readline()
   while len(line):
     macmap=line.split()
     if len(macmap)>1:
       macmaps.append(macmap)
     line =mapfile.readline()
   mapfile.close()

def findowner(macaddr):
   foundmap=next((macmap for macmap in macmaps if macmap[0]==macaddr),["","Sconosciuto"])        
   return foundmap[1]

form=cgi.FieldStorage()

macmaps=[]
loadmap()

tqxstring = form.getvalue("tqx")
searchstring="/home/pi/macaddr_apolloni_"+form.getvalue('month')+"-*"
files = glob.glob(searchstring)
monthlypresences=[]
presences={}
timestampstring=""

for filename in files:
  file = open(filename)
  line = file.readline()
  while len(line):
     timestampline = line.split()
     if timestampline[0]=="---":
       if len(timestampstring):
#          print presences
          monthlypresences.append(presences)
       timestampstring=timestampline[1]+" "+timestampline[2]
       timestamp = datetime.datetime.strptime(timestampstring,"%Y-%m-%d %H:%M:%S")
       presences={'Timestamp':timestamp,'Andrea':0,'Fabrizio':0,'Franco':0,'Giacomo':0,'Giovanni':0,'Vitaliano':0,'Ospite':0,'Sconosciuto':0}
     else:
       name=findowner(timestampline[0])
       if name != "***":
         presences[name]=presences[name]+1
     line = file.readline()
#  print presences
  monthlypresences.append(presences)

  file.close()

#print monthlypresences

description = {"Timestamp":("datetime","Data"),
               "Andrea":("number","Andrea"),
               "Fabrizio":("number","Fabrizio"),
               "Franco":("number","Franco"),
               "Giacomo":("number","Giacomo"),
               "Giovanni":("number","Giovanni"),
               "Vitaliano":("number","Vitaliano"),
               "Ospite":("number","Ospite"),
               "Sconosciuto":("number","Sconosciuto")}
data = monthlypresences

data_table=gviz_api.DataTable(description)
data_table.LoadData(data)
print "Content-type: text/plain"
print
#print data_table.ToJSonResponse(columns_order=("Timestamp","Andrea","Fabrizio","Franco","Giacomo","Giovanni","Vitaliano","Sconosciuto"),
#                                order_by="Timestamp")
print data_table.ToResponse(columns_order=("Timestamp","Andrea","Fabrizio","Franco","Giacomo","Giovanni","Vitaliano","Ospite","Sconosciuto"),
                                order_by="Timestamp",tqx=tqxstring)

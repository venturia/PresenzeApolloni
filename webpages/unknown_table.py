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
monthlyunknowns=[]
unknowns={}
timestampstring=""

for filename in files:
  file = open(filename)
  line = file.readline()
  while len(line):
     timestampline = line.split()
     if timestampline[0]=="---":
#       if len(timestampstring):
       timestampstring=timestampline[1]+" "+timestampline[2]
       timestamp = datetime.datetime.strptime(timestampstring,"%Y-%m-%d %H:%M:%S")
       presences={'Timestamp':timestamp,'Andrea':0,'Fabrizio':0,'Franco':0,'Giacomo':0,'Giovanni':0,'Vitaliano':0,'Rudy':0,'MarcoR':0,'Ospite':0,'Sconosciuto':0}
     else:
       name=findowner(timestampline[0])
       if name == "Sconosciuto":
         monthlyunknowns.append({'Timestamp':timestamp,'macaddress':timestampline[0]})
     line = file.readline()

  file.close()

description = {"Timestamp":("datetime","Data"),
               "macaddress":("string","Sconosciuti")}
data = monthlyunknowns

data_table=gviz_api.DataTable(description)
data_table.LoadData(data)
print "Content-type: text/plain"
print
#print data_table.ToJSonResponse(columns_order=("Timestamp","Andrea","Fabrizio","Franco","Giacomo","Giovanni","Vitaliano","Rudy","MarcoR","Sconosciuto"),
#                                order_by="Timestamp")
print data_table.ToResponse(columns_order=("Timestamp","macaddress"),order_by="Timestamp",tqx=tqxstring)

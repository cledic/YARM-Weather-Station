#!/usr/bin/python

# -*- coding: utf-8 -*-
import string
import feedparser
import os
import re

while 1:
  print'.',
  d = feedparser.parse('http://www.ansa.it/sito/ansait_rss.xml')
  idx = len(d['items'])
  if idx > 0:
    break

tmp_path="/tmp/images/"

if ( idx < 10):
  myidx=idx
else:
  myidx=10
  
while( myidx):
  idx1 = 0
  e = d['items'][ myidx]

  titolo=e['title'].encode('utf-8','replace')
  titolo = re.sub("\"", '\'', titolo)
  descrizione=e['description'].encode('utf-8','replace')
  descrizione = re.sub("\"", '\'', descrizione)
  #idx1 = string.find( descrizione, "<img ", idx1)
  #descrizione = descrizione[0:idx1]
  #print e['title']
  #print e['description']

  myfile=tmp_path+"ansa_news-"+str(myidx)+".txt"
  myimg=tmp_path+"ansa_news-"+str(myidx)+".rgb"

  fansa = open(myfile, 'wb+')
  #titolo_out = '{ \"titolo\":\"'+titolo.encode('utf-8', 'replace')+'\",'
  titolo_out = '{ \"titolo\":\"'+titolo+'\",'
  #titolo_out = '{:<112}'.format(titolo_out)
  fansa.write( titolo_out)

  #descrizione_out = '\"testo\":\"'+descrizione.encode('utf-8', 'replace')+'\"}'
  descrizione_out = '\"testo\":\" '+descrizione+'\"}'
  #descrizione_out = '{:<224}'.format(descrizione_out)
  fansa.write( descrizione_out)
  fansa.close()

  #os.system("/usr/bin/convert -background lightblue  -fill blue -pointsize 14 -size 131x131   caption:@"+myfile+" -depth 8 -flip "+myimg)

  print titolo_out
  print " "+descrizione_out+"\n"

  myidx=myidx-1




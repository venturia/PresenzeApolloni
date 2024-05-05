#!/bin/bash

WEBDIR=/var/www/html
CGIDIR=/usr/lib/cgi-bin

read -p "web server file directory [$WEBDIR]" chosenwebdir

if [ ${#chosenwebdir} != 0 ]; then
  WEBDIR=$chosenwebdir
fi

echo "Web page file directory $WEBDIR"
echo "Installation directory ${PWD}"

# copy the web pages in the web server subdirectory "presenzeapolloni"

if [ ! -d "${WEBDIR}/presenzeapolloni" ]
then
  echo "creating ${WEBDIR}/presenzeapolloni directory"
  mkdir ${WEBDIR}/presenzeapolloni
fi
echo "copying html files"
cp -v webpages/display_presenze.html ${WEBDIR}/presenzeapolloni/.

if [ ! -d "${CGIDIR}/presenzeapolloni" ]
then
  echo "creating ${CGIDIR}/presenzeapolloni directory"
  mkdir ${CGIDIR}/presenzeapolloni
fi
echo "copying py files"
cp -v webpages/*.py ${CGIDIR}/presenzeapolloni/.
chmod +x ${CGIDIR}/presenzeapolloni/presence_summary.py
chmod +x ${CGIDIR}/presenzeapolloni/unknown_table.py

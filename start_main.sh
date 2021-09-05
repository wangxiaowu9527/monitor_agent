#!/bin/bash

function start(){
    uwsgi wsgi.ini
}

# If monitor kafka,you need set the JAVA_HOME
# Then start app with this script
# set JAVA_HOME to your own
# readonly JAVA_HOME="/usr/local/jdk1.8.0_221"
if [[  "X$JAVA_HOME" != "X" ]]; then
    PATH="${JAVA_HOME}/bin:$PATH"
    if [[ -d ${JAVA_HOME}/bin ]]; then
       start
    fi
else
    start
fi


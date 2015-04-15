#!/bin/bash
#
# Run our web service
#


export PINTEREST_HOME="$( cd "$( dirname "${BASH_SOURCE[0]}/"/)" && cd .. && pwd )"

echo -e "\n** starting service from $PINTEREST_HOME **\n"

# configuration
export PYTHONPATH=${PINTEREST_HOME}/pinterest:${PYTHONPATH}

# run
python ${PINTEREST_HOME}/pinterest/run.py ${PINTEREST_HOME} ${PINTEREST_HOME}/conf/pinterest.conf

#!/bin/bash

source ~/.bashrc
UUID=$1
CLUSTER=${UUID:0:5}
arvswitch $CLUSTER > /dev/null
OUTDIR=/home/bcosc/crunchstat_summaries
#source ~/10359-crunchstat-summary-serial/bin/activate
if [ ! -d $OUTDIR/$UUID ]; then
  mkdir $OUTDIR/$UUID
fi

if [[ $UUID =~ d1hrv ]]; then
  source ~/10359-crunchstat-summary-serial/bin/activate
  ~/arvados/tools/crunchstat-summary/bin/crunchstat-summary --pipeline-instance $UUID --format html > $OUTDIR/$UUID/$UUID.html
  ~/arvados/tools/crunchstat-summary/bin/crunchstat-summary --pipeline-instance $UUID --format text > $OUTDIR/$UUID/$UUID.txt
fi

if [[ $UUID =~ 8i9sb ]]; then
  source ~/cs/bin/activate
  ~/arvados/tools/crunchstat-summary/bin/crunchstat-summary --job $UUID --format html > $OUTDIR/$UUID/$UUID.html
  ~/arvados/tools/crunchstat-summary/bin/crunchstat-summary --job $UUID --format text > $OUTDIR/$UUID/$UUID.txt
fi

scp -r -P12345 $OUTDIR/$UUID/ 127.0.0.1:$OUTDIR

echo "$OUTDIR/$UUID/$UUID.html $OUTDIR/$UUID/$UUID.txt"

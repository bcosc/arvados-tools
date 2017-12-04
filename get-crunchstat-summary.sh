#!/bin/bash

# Gets a crunchstat summary of a pipeline instance or job and scps into my local machine

source ~/.bashrc
UUID=$1
CLUSTER=${UUID:0:5}
arvswitch $CLUSTER > /dev/null
OUTDIR=/home/bcosc/crunchstat_summaries
#source ~/cs-1128
#source ~/10359-crunchstat-summary-serial/bin/activate
if [ ! -d $OUTDIR/$UUID ]; then
  mkdir $OUTDIR/$UUID
fi

if [[ $UUID =~ d1hrv ]]; then
  #source ~/cs-1128/bin/activate
  source ~/10359-crunchstat-summary-serial-2/bin/activate
  ~/gitrepos/arvados/tools/crunchstat-summary/bin/crunchstat-summary --pipeline-instance $UUID --format html #> $OUTDIR/$UUID/$UUID.html
  ~/gitrepos/arvados/tools/crunchstat-summary/bin/crunchstat-summary --pipeline-instance $UUID --format text #> $OUTDIR/$UUID/$UUID.txt
fi

if [[ $UUID =~ 8i9sb ]]; then
  #source ~/cs-1128/bin/activate
  #source ~/cs/bin/activate
  ~/gitrepos/arvados/tools/crunchstat-summary/bin/crunchstat-summary --job $UUID --format html > $OUTDIR/$UUID/$UUID.html
  ~/gitrepos/arvados/tools/crunchstat-summary/bin/crunchstat-summary --job $UUID --format text > $OUTDIR/$UUID/$UUID.txt
fi

if [[ $UUID =~ xvhdp ]]; then
  #source ~/cs-1128/bin/activate
  source ~/cs/bin/activate
  ~/gitrepos/arvados/tools/crunchstat-summary/bin/crunchstat-summary --container-request $UUID --format html > $OUTDIR/$UUID/$UUID.html
  ~/gitrepos/arvados/tools/crunchstat-summary/bin/crunchstat-summary --container-request $UUID --format text > $OUTDIR/$UUID/$UUID.txt
fi

scp -r -P12345 $OUTDIR/$UUID/ 127.0.0.1:$OUTDIR

echo "$OUTDIR/$UUID/$UUID.html $OUTDIR/$UUID/$UUID.txt"

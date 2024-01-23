#!/bin/bash

FILE="esej"
INTERVAL=2 # seconds between updates
PREV_COUNT=0

while true; do
    pdflatex -interaction=nonstopmode $FILE.tex > /dev/null 2>&1
    CURRENT_COUNT=$(pdftotext $FILE.pdf - | wc -m)

    if [ "$CURRENT_COUNT" -ne "$PREV_COUNT" ]; then
        clear
        echo "Character count: $CURRENT_COUNT"
        PREV_COUNT=$CURRENT_COUNT
    fi

    sleep $INTERVAL
done


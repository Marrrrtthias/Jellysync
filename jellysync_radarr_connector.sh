#!/bin/bash

echo "JELLYSYNC_RADARR_CONNECTOR: received event $radarr_eventtype"

if [[ "$radarr_eventtype" = "Download" || "$radarr_eventtype" = "Rename" || "$radarr_eventtype" = "Delete" ]]; then
    rm -f /jellysync/*.sync
    echo "" > "/jellysync/full_refresh.sync"
    echo "JELLYSYNC_$RADARR_CONNECTOR: created file 'full_refresh.sync'"
fi

if [[ "$radarr_eventtype" = "Test" || "$radarr_eventtype" = "Test" ]]; then
    echo "" > "/jellysync/test.sync"
    echo "JELLYSYNC_$RADARR_CONNECTOR: created file 'test.sync'"
fi

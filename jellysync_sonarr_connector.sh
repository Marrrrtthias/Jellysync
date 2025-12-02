#!/bin/bash

echo "JELLYSYNC_SONARR_CONNECTOR: received event $sonarr_eventtype"

if [[ "$sonarr_eventtype" = "Download" || "$sonarr_eventtype" = "Rename" || "$sonarr_eventtype" = "EpisodeFileDelete" ]]; then
    echo "$sonarr_eventtype" > "/jellysync/update_$sonarr_series_tvdbid.sync"
    echo "JELLYSYNC_SONARR_CONNECTOR: created file 'update_$sonarr_series_tvdbid.sync'"
fi

if [[ "$sonarr_eventtype" = "SeriesDelete" || "$sonarr_eventtype" = "EpisodeFileDelete" ]]; then
    rm -f /jellysync/*.sync
    echo "" > "/jellysync/full_refresh.sync"
    echo "JELLYSYNC_SONARR_CONNECTOR: created file 'full_refresh.sync'"
fi

if [[ "$sonarr_eventtype" = "Test" ]]; then
    echo "" > "/jellysync/test.sync"
    echo "JELLYSYNC_SONARR_CONNECTOR: created file 'test.sync'"
fi

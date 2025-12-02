# Jellysync 

Simple way to automatically let Sonarr tell Jellyfin that a show has been updated without the two communicating directly.

## Working Principle

- Every time Sonarr updates a show, a file will be created in a jellysync folder
- a watcher container regularly checks the folder when there are files in the folder it will call the jellyfin API to notify jellyfin about the library update

## Setup

TODO
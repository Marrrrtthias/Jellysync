# Jellysync 

Automatically update your Jellyfin library from Sonarr without direct communication between the two. Useful when real time monitoring of libraries is not available like on some Ugreen NAS models.

## Working Principle

- Every time Sonarr updates a show, an automatic script creates a file in a jellysync folder
- The jellysync watcher application running in a different container also has access to this jellysync folder and regularly checks it. If there are files in the folder it will call the jellyfin API to notify jellyfin about the library update

## Reason why I am doing this

For some reason the Jellyfin real time monitoring of libraries does not work for me (Ugreen NAS DXP4800 Plus). But I also don't want to use the Jellyfin connector inside sonarr because I am running sonarr in a fully isolated environment wher it can not access the Jellyfin API itself. So this project is a way to work around those limitations and avoid having to update my library manually.


## Setup

### Sonarr

Follow these steps to add a custom-script connection to sonarr. The script is very simple and will just create a file everytime it is ran, the existence of this file can then be used to trigger an update of your Jellyfin library. You can configure for which events the script should be run.

1. create a folder on your machine and mount it as a volume in you sonarr container. This folder can be anywhere on your host machin but has to be mounted at /jellysync inside the container
    ```yml
    services:
        sonarr:
            ...
            volumes:
            - /path/to/jellysync:/jellysync
    ```
2. place jellysync_sonarr_connector.sh in the created folder so sonarr can access it
3. open the UI of your sonarr instance, navigate to Settings > Connect and click on the plus, select custom script and select the .sh file in the /jellysync folder
4. Test the script by clicking "Test". A file named test.sync should be created in the jellysync folder


### Jellysync

The Jellysync application will regularly check the jellysync folder and trigger a library refresh via the jellyfin API when required.

1. add the jellysync service and the jellysync-nw network from docker-compose.yml to the docker-compose of your jellyfin instance (You can of course also put Jellysync in its own docker-compose file, it just has to be able to reach the API of your Jellyfin instance)
   ```yml
    jellysync:
        image: marrrrtthias/jellysync
        container_name: jellysync
        networks:
        - jellysync-nw
        environment:
        - FULL_REFRESH_ENDPOINT=http://jellyfin:8096/Library/Refresh
        - JELLYFIN_API_KEY=your_api_key
        - POLL_INTERVAL=10
        volumes:
        - /path/to/jellysync:/jellysync
    ```
2. edit the path to the jellysync folder so the jellysync container has the same folder mounted that you used in the sonarr setup
4. in the Jellyfin UI create a new API key for jellysync and put it to the docker-compose
5. start the jellysync container and observe its logs. It should pick up the test.sync file that was previously created by the jellysync_sonarr_connector script and delete it
   ```
   jellysync  | Found sync files: ['test.sync']
   jellysync  | Deleted test file  test.sync
   ```


## Conclusion

Whenever sonarr adds a new episode or otherwise updates your library it will now run the jellysync_sonarr_connector script which creates a file called full_refresh.sync. At the next time the jellysync application checks the jellysync folder it will see this file and make an API call to Jellyfin to trigger a library scan.

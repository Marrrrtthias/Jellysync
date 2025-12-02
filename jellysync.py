import os
import time
import requests
import sys

# ---------- CONFIG ----------
JELLYSYNC_FOLDER = "/jellysync"
FULL_REFRESH_FILENAME = "full_refresh.sync"

# REST endpoints# Read endpoint from environment variable
FULL_REFRESH_ENDPOINT = os.getenv("FULL_REFRESH_ENDPOINT")
if not FULL_REFRESH_ENDPOINT:
    print("ERROR: Environment variable FULL_REFRESH_ENDPOINT is not set.")
    sys.exit(1)

# API key for Jellyfin
JELLYFIN_API_KEY = os.getenv("JELLYFIN_API_KEY")
if not JELLYFIN_API_KEY:
    print("ERROR: JELLYFIN_API_KEY must be set")
    sys.exit(1)

# Poll interval in seconds
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", default=5))
# ----------------------------

HEADERS = {
    "Authorization": f"MediaBrowser Token=\"{JELLYFIN_API_KEY}\", Client=\"jellysync\"",
    "Content-Type": "application/json"
}

def list_sync_files():
    """Return a list of all *.sync files in the folder."""
    return [f for f in os.listdir(JELLYSYNC_FOLDER) if f.endswith(".sync")]


def handle_full_refresh():
    print("Full refresh triggered! Calling ", FULL_REFRESH_ENDPOINT)
    try:
        response = requests.post(FULL_REFRESH_ENDPOINT, headers=HEADERS)
        response.raise_for_status()
        print("Full refresh REST call successful.")
    except Exception as e:
        print("Error calling full refresh endpoint:", e)
        return

    # Delete all *.sync files
    for file in list_sync_files():
        try:
            os.remove(os.path.join(JELLYSYNC_FOLDER, file))
        except Exception as e:
            print("Error deleting file", file, ":", e)

def main():
    print("Watcher started. Monitoring folder ", JELLYSYNC_FOLDER, " at an interval of ", POLL_INTERVAL, " seconds.")

    while True:
        sync_files = list_sync_files()

        if sync_files:
            print("Found sync files:", sync_files)

            if FULL_REFRESH_FILENAME in sync_files:
                handle_full_refresh()

            if "test.sync" in sync_files:
                print("teleting test file")

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()

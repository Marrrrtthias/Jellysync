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
INCREMENTAL_ENDPOINT = os.getenv("INCREMENTAL_ENDPOINT")
if not INCREMENTAL_ENDPOINT:
    print("ERROR: Environment variable INCREMENTAL_ENDPOINT is not set")
    sys.exit(1)

# Poll interval in seconds
POLL_INTERVAL = int(os.getenv("POLL_INTERVAL", default=5))
# ----------------------------


def list_sync_files():
    """Return a list of all *.sync files in the folder."""
    return [f for f in os.listdir(JELLYSYNC_FOLDER) if f.endswith(".sync")]


def handle_full_refresh():
    print("Full refresh triggered! Calling ", FULL_REFRESH_ENDPOINT)
    try:
        response = requests.post(FULL_REFRESH_ENDPOINT)
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


def handle_incremental(sync_files):
    for fname in sync_files:
        if fname == FULL_REFRESH_FILENAME:
            continue

        # test file created when testing the script in Sonarr
        if fname == "test.sync":
            try:
                os.remove(os.path.join(JELLYSYNC_FOLDER, fname))
            except Exception as e:
                print("Error deleting file", fname, ":", e)
            print("Deleted test file ", fname)
            continue


        id_without_ext = fname.replace(".sync", "")
        print(f"Calling {INCREMENTAL_ENDPOINT} with tvdbId: {id_without_ext}")

        try:
            resp = requests.post(
                INCREMENTAL_ENDPOINT,
                json={"tvdbId": id_without_ext}
            )
            resp.raise_for_status()
            print(f"Incremental REST call for {id_without_ext} successful.")
        except Exception as e:
            print(f"Error sending incremental update for {id_without_ext}:", e)

        # Delete the file after processing
        try:
            os.remove(os.path.join(JELLYSYNC_FOLDER, fname))
        except Exception as e:
            print("Error deleting file", fname, ":", e)


def main():
    print("Watcher started. Monitoring folder ", JELLYSYNC_FOLDER, " at an interval of ", POLL_INTERVAL, " seconds.")

    while True:
        sync_files = list_sync_files()

        if sync_files:
            print("Found sync files:", sync_files)

            if FULL_REFRESH_FILENAME in sync_files:
                handle_full_refresh()
            else:
                handle_incremental(sync_files)

        time.sleep(POLL_INTERVAL)


if __name__ == "__main__":
    main()

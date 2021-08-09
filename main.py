import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3


DATABASE_LOCATION = "sqlite:///my_played_tracks.sqlite"
USER_ID = "koyuboy"  # your Spotify username
TOKEN = "BQB20k3QRptb6yeYbIDzDrae4EBqUVrBP4pBfiC4Hv3_t7FVO0yEHcG6Zq1bPt3RdoM7kmbdR5mcwQYS6Pbf61orimKvwDbgc-JpPAjs7vB0jSfp3CmCnzNHfTo0v9kYouJvMu5zMxvwXcS-"  # your Spotify API token


def check_if_valid_data(df: pd.DataFrame) -> bool:

    if df.empty:
        print("No songs downloaded.")
        return False

    # Primary key check. Our primary key is "played_at" column.

    if pd.Series(df["played_at"]).is_unique:
        pass
    else:
        raise Exception("Primary key check is violated!")

    if df.isnull().values.any():
        raise Exception("Null values found!")

    # 2021-08-08 21:20:36.818849
    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday = yesterday.replace(
        hour=0, minute=0, second=0, microsecond=0)  # 2021-08-08 00:00:00

    today = datetime.datetime.now()
    today = today.replace(hour=0, minute=0, second=0, microsecond=0)

    # To verify that our data came in the last 24 hours
    timestamps = df["timestamp"].tolist()
    for timestamp in timestamps:
        if (datetime.datetime.strptime(timestamp, '%Y-%m-%d') != yesterday) and (datetime.datetime.strptime(timestamp, '%Y-%m-%d') != today):
            raise Exception(
                "At least one of the timestamps does not belong to yesterday")

    return True


if __name__ == '__main__':

    ####
    # EXTRACT
    # Take the data from vendor

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    yesterday = datetime.datetime.now() - datetime.timedelta(days=1)
    yesterday_unix_timestamp = int(yesterday.timestamp())*1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(
        time=yesterday_unix_timestamp), headers=headers)

    data = r.json()

    song_names = []
    artist_names = []
    played_at_list = []
    timestamps = []

    # Extracting only the relevant bits of data from the json object
    """
    print(data.keys())  #['items', 'next', 'cursors', 'limit', 'href']
    print(data["items"][0].keys())  # ['track', 'played_at', 'context']
    print(data["items"][0]["track"].keys())  # ['album', 'artists', 'available_markets', 'disc_number', 'duration_ms', 'explicit', 'external_ids', 'external_urls', 'href', 'id', 'is_local', 'name', 'popularity', 'preview_url', 'track_number', 'type', 'uri']
    print(data["items"][0]["track"]["name"])
    """

    for song in data["items"]:
        song_names.append(song["track"]["name"])
        artist_names.append(song["track"]["album"]["artists"][0]["name"])
        played_at_list.append(song["played_at"])
        timestamps.append(song["played_at"][0:10])

        # Prepare a dictionary in order to turn it into a pandas dataframe below
    song_dict = {
        "song_name": song_names,
        "artist_name": artist_names,
        "played_at": played_at_list,
        "timestamp": timestamps
    }

    song_df = pd.DataFrame(song_dict, columns=[
                           "song_name", "artist_name", "played_at", "timestamp"])

    print(song_df)

    ####
    ####    TRANSFORM (VALIDATION)
    #Data vendor might send empty file, duplicated data etc. We need to clean up this mess before uploading it to the database.

    if check_if_valid_data(song_df):
        print("Data transformation is successful!")

    ####
    ####    LOAD
    ####

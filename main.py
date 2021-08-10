import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3


DATABASE_LOCATION = "sqlite:///played_tracks.sqlite"
USER_ID = "koyuboy"  # your Spotify username
TOKEN = "BQDiuc2AkyVTZLfF61iNJCzfbbNzb632o3BDsJSlZ6ixyCI68fTC0QNmIU1TV8-GwcDH8KY0kABFk4IpveDRpyryXAGEzmWJhWSkNQ4aFCEwi6JOxdT3QX8IOAVrMzUaFavqLTrHSrH00XsB"  # your Spotify API token

INTERVAL = 5


def extract() -> pd.DataFrame: ### Take the data from vendor

    headers = {
        "Accept": "application/json",
        "Content-Type": "application/json",
        "Authorization": "Bearer {token}".format(token=TOKEN)
    }

    days_to_extract = datetime.datetime.now() - datetime.timedelta(days=INTERVAL)
    days_to_extract_unix_timestamp = int(days_to_extract.timestamp())*1000

    r = requests.get("https://api.spotify.com/v1/me/player/recently-played?limit=50&after={time}".format(
        time=days_to_extract_unix_timestamp), headers=headers)

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

    return song_df


def generate_date_interval(day_interval:int = 1) -> list:
    
    datetime_list = []
    for day in range(day_interval + 1):
        # 2021-08-08 21:20:36.818849
        day = datetime.datetime.now() - datetime.timedelta(days=day)
        day = day.replace(
            hour=0, minute=0, second=0, microsecond=0)  # 2021-08-08 00:00:00
        datetime_list.append(day)

    return datetime_list


def is_interal_valid(df: pd.DataFrame) -> bool:

    dates = generate_date_interval(day_interval= INTERVAL)

    # To verify that our data came in the given interval
    timestamps = df["timestamp"].tolist()

    for timestamp in timestamps:
        parsed_datetime = datetime.datetime.strptime(timestamp, '%Y-%m-%d')

        if all(parsed_datetime != d for d in dates):
            raise Exception(
                "At least one of the timestamps does not belong to the time interval!")
            
    return True


def check_df_status(df: pd.DataFrame) -> bool:

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
  
    return True
    

def check_if_valid_data(df: pd.DataFrame) -> bool:

    if check_df_status(df):
        if is_interal_valid(df):
            return True

    return False


def transform(song_df: pd.DataFrame): ###Data vendor might send empty file, duplicated data etc. We need to clean up this mess before uploading it to the database.
    if check_if_valid_data(song_df):
        print("Data transformation is successful!")
    else:
        print("Data transformation failed!")


def load(song_df: pd.DataFrame): ###Load clear data into database

    engine = sqlalchemy.create_engine(DATABASE_LOCATION)
    conn = sqlite3.connect('played_tracks.sqlite')
    cursor = conn.cursor()

    sql_query = """
    CREATE TABLE IF NOT EXISTS played_tracks(
        song_name VARCHAR(200),
        artist_name VARCHAR(200),
        played_at VARCHAR(200),
        timestamp VARCHAR(200),
        CONSTRAINT primary_key_constraint PRIMARY KEY (played_at)
    )
    """

    cursor.execute(sql_query)
    print("Database is successfully opened.")

    try:
        song_df.to_sql("played_tracks", engine, index=False, if_exists='append') #table_name, sqlalhchemmy_engine, false mean don't add df index to the table, append to don't overwrite the table
    except:
        print("Data already exists in the database")

    conn.close()
    print("Close database successfully")
    


if __name__ == '__main__':
    
    song_df = extract()

    print(song_df)

    transform(song_df)

    load(song_df)

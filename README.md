# ETL_pipeline_with_Spotify
ETL(Extract-Transform-Load) process on Spotify user data

# Step 1 - Extract

We can extract data with FTP(File Transfer Protocol) or API(Application Programming Interface). I used an API that provided by Spotify. I got Current User's Recently Played Tracks. We need a token to access the API. This token provided by spotify (need a Spotify account) => https://developer.spotify.com/console/get-recently-played/

- Limit is max items(songs here) to return daily. default=20, min=1, max=50.
- After is a date but specified in unix milliseconds format. This mean download listened songs after this date. 
- Before is reverse of after. Download listened songs before this date. 
- Using only before or after is enough.
- Then click the get token button, select below option and clic request token.
- 
![image](https://user-images.githubusercontent.com/35155252/128636477-eedac6db-26be-43a9-99e0-eb0eb42a7b0f.png)

### After extract our data looks like that

![image](https://user-images.githubusercontent.com/35155252/128752047-c8773e52-b8c5-4ad1-902c-a936c98b634d.png)

# Step 2 - Transform(Validation)

Some times data vendors might send empty file, duplicated data, null columns or row  etc. We need to clean up this mess(dirty data) before uploading it to the database. Because working with dirty data gives us false information. "Garbage in, garbage out."

![image](https://user-images.githubusercontent.com/35155252/128757553-d349a2d7-d513-4b5c-8de2-e1e9abb2a69d.png)

In this code only checked basic things with "check_if_valid_data()" function. You can look at below images to see the most common transform types.

![image](https://user-images.githubusercontent.com/35155252/128758721-6a5b4f53-52a5-4fd8-82a9-560b9ef2510c.png)
![image](https://user-images.githubusercontent.com/35155252/128758751-f13a898a-9b2f-4cb1-9563-417d71b6ab8f.png)

After calling the "check_if_valid_data()" function you will see this output if everything is alright.

![image](https://user-images.githubusercontent.com/35155252/128757167-339518b5-0b02-4059-a39f-4e17da3a73a9.png)

# Step 3 - Load





Resources:
- https://www.stitchdata.com/etldatabase/etl-transform/
- https://github.com/karolina-sowinska/free-data-engineering-course-for-beginners/blob/master/main.py


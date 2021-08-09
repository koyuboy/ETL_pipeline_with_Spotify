# ETL_pipeline_with_Spotify
ETL(Extract-Transform-Load) process on Spotify user data

# Step 1 - Extract

We can extract data with FTP(File Transfer Protocol) or API(Application Programming Interface). I used an API that provided by Spotify. I got Current User's Recently Played Tracks. We need a token to access the API. This token provided by spotify (need a Spotify account) => https://developer.spotify.com/console/get-recently-played/

- Limit is max items(songs here) to return daily. default=20, min=1, max=50.
- After is a date but specified in unix milliseconds format. This mean download listened songs after this date. 
- Before is reverse of after. Download listened songs before this date. 
- Using only before or after is enough.
- Then click the get token button, select below option and clic request token.
![image](https://user-images.githubusercontent.com/35155252/128636477-eedac6db-26be-43a9-99e0-eb0eb42a7b0f.png)

### After extract our data looks like that
![image](https://user-images.githubusercontent.com/35155252/128752047-c8773e52-b8c5-4ad1-902c-a936c98b634d.png)


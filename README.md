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


                                    song_name      artist_name                 played_at   timestamp

0                              To Let Myself Go       The Avener  2021-08-09T10:17:00.394Z  2021-08-09
1                                  Self Control   Laura Branigan  2021-08-09T09:36:13.274Z  2021-08-09
2                                        Zombie  The Cranberries  2021-08-09T09:32:06.364Z  2021-08-09
3                                         Crush           Lane 8  2021-08-09T09:26:59.455Z  2021-08-09
4                                  Toosie Slide            Drake  2021-08-09T09:19:41.210Z  2021-08-09

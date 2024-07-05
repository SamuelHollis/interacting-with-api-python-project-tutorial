import os
import pandas as pd
import seaborn as sns
from dotenv import load_dotenv
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

# load the .env file variables
load_dotenv()

#Safe credentials
client_id = os.environ.get("CLIENT_ID")
client_secret = os.environ.get("CLIENT_SECRET")
spotify = spotipy.Spotify(auth_manager = SpotifyClientCredentials(client_id = client_id, client_secret = client_secret))

#saving artist url
response = spotify.artist_top_tracks("5me0Irg2ANcsgc93uaYrpb")

#Taking interest information
keys_of_interest = {"name", "popularity", "duration_ms"}

new_tracks = []

if response:
    tracks = response["tracks"]
    for track in tracks:
        new_track = {}
        for k, v in track.items():
            if k in keys_of_interest:
                if k == "duration_ms":
                    new_track["duration_min"] = round((v / (1000 * 60)) % 60, 2)
                else:
                    new_track[k] = v
        new_tracks.append(new_track)

    tracks = new_tracks

#Create a dataframe
df_tracks = pd.DataFrame(new_tracks)
df_tracks = df_tracks.sort_values(by="popularity", ascending=False)

print(df_tracks)

#Create a scatter plot
scatter_plot = sns.scatterplot(data = df_tracks, x = 'popularity', y = 'duration_min')
fig = scatter_plot.get_figure() 
fig.savefig('scatter_plot.png') 

#Conclusion
print("#### CONCLUSIÓN ####\nPodemos observar a partir del scatter plot que no existe una relación de la duración de las canciones con su popularidad.")
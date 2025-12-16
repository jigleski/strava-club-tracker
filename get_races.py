from stravalib import Client
from client import get_client, save_current_token
from datetime import datetime, timedelta
from tqdm.auto import tqdm

def get_races(client: Client, after:datetime=None):
    athlete = client.get_athlete()
    stats = client.get_athlete_stats()
    races = []
    for activity in tqdm(client.get_activities(after=after), desc="Searching for races", unit=" activities", leave=True):
        if activity.sport_type.root == "Run" and activity.workout_type == 1:
            races.append(activity)
            #tqdm.write(f"{activity.name}\t{activity.distance/1609.34:.2f}\t{timedelta(seconds=activity.elapsed_time)}")
    return races

if __name__ == "__main__":
    client = get_client()
    races = get_races(client, after=datetime.fromisoformat("2025-01-01T01:00:00"))
    pass
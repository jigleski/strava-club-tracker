from stravalib import Client
from client import get_client, save_current_token
import json

CLUB_ID = 1116339

def get_club_details(client: Client):
    club = client.get_club(CLUB_ID)
    return club


def get_club_activities(client: Client):
    itr = client.get_club_activities(CLUB_ID)
    limit = 10000
    activities = [a for i, a in enumerate(itr) if i < limit]
    return activities

    


if __name__ == "__main__":
    client = get_client()
    club = get_club_details(client)
    activities = get_club_activities(client)
    pass
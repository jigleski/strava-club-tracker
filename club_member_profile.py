from stravalib import Client
from stravalib.model import (
    DetailedAthlete,
    AthleteStats,
    SummaryActivity,
)

from client import get_client, save_current_token
from datetime import datetime, timedelta
from tqdm.auto import tqdm
from pydantic import BaseModel


class ClubMember(BaseModel):
    athlete: DetailedAthlete
    stats: AthleteStats
    races: list[SummaryActivity]


def get_club_member(client: Client) -> ClubMember:
    athlete = client.get_athlete()
    athlete.model_dump_json(indent=2)
    stats = client.get_athlete_stats()
    stats.model_dump_json(indent=2)
    races = []
    for activity in tqdm(client.get_activities(), desc="Searching for races", unit=" activities", leave=True):
        if activity.sport_type.root == "Run" and activity.workout_type == 1:
            races.append(activity)
            activity.model_dump_json(indent=2)
    return ClubMember(athlete=athlete, stats=stats, races=races)





if __name__ == "__main__":
    # client = get_client()
    # member = get_club_member(client)
    # save_current_token(client)

    with open(f"ClubMember_{14045511}.json", "r") as fid:
        _member = ClubMember.model_validate_json(fid.read())
    with open(f"ClubMember_{14045511}.json", "w") as fid:
        fid.write(_member.model_dump_json(indent=2, ensure_ascii=True, exclude_none=True))
    pass

import requests
import os

# Your API key for The Blue Alliance
api_key = my_secret = os.environ['API_KEY']

# Function to fetch teams for the 2024 season from The Blue Alliance API
def fetch_teams_for_2024():
    teams = []
    page_num = 0
    while True:
        response = requests.get(f'https://www.thebluealliance.com/api/v3/teams/{page_num}/keys',
                                headers={'X-TBA-Auth-Key': api_key})
        if response.status_code != 200 or not response.json():
            break
        teams.extend(response.json())
        page_num += 1
    return teams

# Fetch all teams for 2024
teams_2024 = fetch_teams_for_2024()

max_teams = []
max_gp = -1

for team in teams_2024:
  gp_count = 0
  response = requests.get(f'https://www.thebluealliance.com/api/v3/team/{team}/awards',
    headers={'X-TBA-Auth-Key': api_key})
  resp = response.json()
  if (len(resp) < max_gp):
    continue
  for award in resp:
    if award.get('award_type') == 11:
      gp_count += 1
  if gp_count > max_gp:
    max_gp = gp_count
    max_teams = [team]
  elif gp_count == max_gp:
    max_teams.append(team)

print(max_teams, max_gp)
  #GP is 11

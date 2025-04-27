import requests
import os
from dotenv import load_dotenv
import bisect

load_dotenv()

api_key = os.environ['TBA_API_KEY']

print("Enter the number of teams you want: ", end='')
k = int(input())
teams = [(-1, '')] # sorted list of (gp awards, [team keys])

page_num = 0

while True:
  response = requests.get(f'https://www.thebluealliance.com/api/v3/teams/{page_num}/keys', headers={'X-TBA-Auth-Key': api_key})
  if response.status_code != 200 or not response.json():
    break
  for key in response.json():
    response = requests.get(f'https://www.thebluealliance.com/api/v3/team/{key}/awards', headers={'X-TBA-Auth-Key': api_key})
    resp = response.json()
    if len(teams) < k: #insert
      gp_count = sum(1 for aw in resp if aw.get('award_type') in (11, 19))
      idx = bisect.bisect_left([(-c, '') for c, t in teams], (-gp_count, '')) #we always want an early insert
      if (teams[idx][0] == gp_count): # we do a little appending
        teams[idx][1].append(key)
      else:
        teams.insert(idx, (gp_count, [key]))
      # print(teams)
    else:
      if (len(resp) < teams[-1][0]):
        continue
      gp_count = sum(1 for aw in resp if aw.get('award_type') in (11, 19))
      if gp_count >= teams[-1][0]:
        idx = bisect.bisect_left([(-c, '') for c, t in teams], (-gp_count, '')) #we always want an early insert
        if (teams[idx][0] == gp_count): # we do a little appending
          teams[idx][1].append(key)
        else:
          teams.insert(idx, (gp_count, [key]))
          del teams[-1]
        # print(teams)
  page_num += 1

print(teams)
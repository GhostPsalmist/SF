#!/usr/bin/env python3
import sys
import csv
import pandas as pd

# Be sure to insert your Instagram User Name here
login_name = 'YOUR USER NAME'

# Allows passing in the Target User Name
target_profile = sys.argv[1]

from instaloader import Instaloader, Profile
loader = Instaloader()

# Login
try:
    loader.load_session_from_file(login_name)
except FileNotFoundError:
    loader.context.log("Session file does not exist yet - Logging in.")
if not loader.context.is_logged_in:
    loader.interactive_login(login_name)
    loader.save_session_to_file()

# Obtain Followers and Followees from Target User Name
profile = Profile.from_username(loader.context, target_profile)
followers = profile.get_followers()
following = profile.get_followees()

# Establish List Names
followerNameList = []
followerUserNameList = []
followeeNameList = []
followeeUserNameList = []
followerName = None
followeeName = None

# Begin display of data in Terminal
loader.context.log()
loader.context.log('Profile {} has {} followers:'.format(profile.username, profile.followers))
loader.context.log()
loader.context.log("Full Name:, User Name:", flush=True)

# Iterate through Followers and append to a list
for follower in followers:
    loader.context.log(follower.full_name, ", ", follower.username, flush=True)
    followerName = follower.full_name
    followerNameList.append(followerName)
    followerUserName = follower.username
    followerUserNameList.append(followerUserName)

# Display Followers in Terminal
loader.context.log()
loader.context.log('Profile {} is following {} users:'.format(profile.username, profile.followees))
loader.context.log()
loader.context.log("Full Name:, User Name:", flush=True)

# Determine Total of followers and followees
totalFollowers = 'Total: ' + str(profile.followers) + '\n'
totalFollowees = 'Total: ' + str(profile.followees) + '\n'

# Iterate through Followees and append to a list
for follows in following:
    loader.context.log(follows.full_name, ", ", follows.username, flush=True)
    followeeName = follows.full_name
    followeeNameList.append(followeeName)
    followeeUserName = follows.username
    followeeUserNameList.append(followeeUserName)

# Generate our csv file name
fileName = "{}_Follow_List.csv".format(target_profile)

# Save Followers to CSV
df = pd.DataFrame(data={"Follower Full Name: ": followerNameList, "Follower User Name: ": followerUserNameList})
df.to_csv(fileName, sep=',',index=False)

# Append Total and blank line to the CSV file
with open(fileName, 'a') as f:
    f.write(totalFollowers)

# Insert a new row
new_row = ['', '']

# Write the new row to the CSV file
with open(fileName, 'a') as f:
    f.write(','.join(new_row) + '\n')

# Save the Followees to the CSV
df = pd.DataFrame(data={"Following Full Name: ": followeeNameList, "Following User Name: ": followeeUserNameList})
df.to_csv(fileName, mode='a', sep=',',index=False, header=True)

# Append Total to end of Followees
with open(fileName, 'a') as f:
    f.write(totalFollowees)
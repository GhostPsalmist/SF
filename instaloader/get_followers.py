#!/usr/bin/env python3
import sys

login_name = 'ENTER YOUR INSTA USERNAME'

target_profile = sys.argv[1] # pass in target profile as argument

from instaloader import Instaloader, Profile
loader = Instaloader()

# login
try:
    loader.load_session_from_file(login_name)
except FileNotFoundError:
    loader.context.log("Session file does not exist yet - Logging in.")
if not loader.context.is_logged_in:
    loader.interactive_login(login_name)
    loader.save_session_to_file()

profile = Profile.from_username(loader.context, target_profile)
followers = profile.get_followers()
following = profile.get_followees()
loader.context.log()
loader.context.log('Profile {} has {} followers:'.format(profile.username, profile.followers))
loader.context.log()

for follower in followers:
    loader.context.log(follower.username, flush=True)

loader.context.log()
loader.context.log('Profile {} is following {} users:'.format(profile.username, profile.followees))
loader.context.log()

for follows in following:
	loader.context.log(follows.username, flush=True)

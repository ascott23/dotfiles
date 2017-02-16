from uwaterlooapi import UWaterlooAPI as uwAPI

API_KEY = "cb33df05db1f11bc51f3e00c26daac88"

uw = uwAPI(API_KEY)

courses = uw.courses()
k = set()

for course in courses:
   str = course["subject"] + " " + course["catalog_number"]
   if not str in k:
      print(str)
      k.add(str)

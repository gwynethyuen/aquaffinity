from django.db import models
from django.shortcuts import render
import urllib.parse
import json
import sqlite3
import random
import sys
from bs4 import BeautifulSoup
import re
import string
import requests
from urllib.request import urlopen
import math

CAT_CHOICES = [(1, "Announcements"), (2, "Team Events"), (3, "Academics"), (4, "Swim/Dive"), (5, "Misc")]

class Swimmer(models.Model):
    swimmer_id = models.CharField(max_length=7)
    name = models.CharField(max_length=50, default="John Doe")
    hometown = models.CharField(max_length=50, default="Troy, NY")
    class_year = models.CharField(max_length=2, default="FR")
    event_list = models.TextField(null=True, default="There are no recent events.")

class Category(models.Model):
    name = models.CharField(max_length=20)

class Post(models.Model):
    title = models.CharField(max_length=60, default="Your Post Title")
    body = models.TextField(default="Your Post Text")
    created_on = models.DateTimeField(auto_now_add=True)
    last_modified = models.DateTimeField(auto_now=True)
    author = models.CharField(max_length=1000, default="John Doe")
    category = models.CharField(max_length=1, default=5, choices=CAT_CHOICES)

class Comment(models.Model):
    author = models.CharField(max_length=60)
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey('Post', on_delete=models.CASCADE)

# def normalizeName(name):
#     nameParts = name.strip().split(',')
#     return nameParts[1].strip() + " " + nameParts[0].strip()

# def parse_swimmer_data(url, swimmerId):
#     page = urlopen(url)
#     source = page.read()
#     soup = BeautifulSoup(source, 'html.parser')
#     events = {}
#     selection = soup.find("select", class_="form-control input-sm js-event-id-selector")
#     swimmerEvents = []
#     if selection:
#         for option in selection.find_all("option", class_="event"):
#             thisEvent = option["value"]
#             if thisEvent != "perf":
#                 swimmerEvents.append(thisEvent)

#     for event in swimmerEvents:
#         new_url = "https://www.swimcloud.com/swimmer/" + swimmerId + "/times/byeventid/" + event
#         results = [obj for obj in requests.get(new_url).json()]
#         swim = requests.get(new_url).json()[-1]
#         splitDate = swim["dateofswim"].split('-')
#         date = splitDate[1] + "/" + splitDate[2] + "/" + splitDate[0]
#         sec = float(swim["time"])
#         minutes = int(math.floor(sec / 60))
#         sec = int(math.floor(sec % 60))
#         milli = swim["time"][-2:]
#         if minutes == 0:
#             time = "{:02d}.{}".format(sec, milli)
#         time = "{}:{:02d}.{}".format(minutes, sec, milli)
#         if event[0] == "1":
#             event = event[1:] + " Freestyle"
#         elif event[0] == "2":
#             event = event[1:] + " Backstroke"
#         elif event[0] == "3":
#             event = event[1:] + " Breaststroke"
#         elif event[0] == "4":
#             event = event[1:] + " Butterfly"
#         elif event[0] == "5":
#             event = event[1:] + " IM"
#         # print(event, time)
#         return event + " " + time

# def parse_team_data(url):
#     page = urlopen(url)
#     source = page.read()
#     soup = BeautifulSoup(source, 'html.parser')
#     team = {}
#     team["name"] = soup.find("h1", class_="c-toolbar__title").text.strip()
#     tableBody = soup.find("table", class_="c-table-clean c-table-clean--middle table table-hover").tbody
#     for tableRow in tableBody.find_all("tr"):
#         swimmerId = tableRow.a["href"].split("/")[-1]
#         swimmerName = normalizeName(tableRow.a.string)
#         swimmerHome = tableRow.find("td", class_="u-text-truncate").string.strip()
#         swimmerClass = tableRow.find_all("td", class_="c-table-clean__col-fit")[1].string.strip()
#         if(len(Swimmer.objects.filter(name=swimmerName)) < 1):
#             swimmer_url = "https://www.swimcloud.com/swimmer/" + swimmerId
#             event_data = parse_swimmer_data(swimmer_url, swimmerId)
#             print(event_data)
#             s = Swimmer(name=swimmerName, hometown=swimmerHome, class_year=swimmerClass, event_list=event_data)
#             s.save()

# swimmers = []
# base = 'https://www.swimcloud.com'
# url = base + '/api/search/?q=' + urllib.parse.quote('Rensselaer Polytechnic Institute')
# results = [obj for obj in requests.get(url).json() if 'team' in obj['id']]
# if len(results) >= 1:
#     swimmerData = []
#     swimmerEvents = []
#     women_url = base + results[0]['url'] + '/roster/?page=1&gender=F&season_id=24&sort=name'
#     parse_team_data(women_url)
#     men_url = base + results[0]['url'] + '/roster/?page=1&gender=M&season_id=24&sort=name'
#     parse_team_data(men_url)

    # print(new_url)
    # page = urlopen(new_url)
    # source = page.read()
    # soup = BeautifulSoup(source, 'html.parser')
    # team = {}
    # # 'gets a list of (Name, swimmerId) tuples and the team name for a given teamId'
    # team["name"] = soup.find("h1", class_="c-toolbar__title").text.strip()
    # tableBody = soup.find("table", class_="c-table-clean c-table-clean--middle table table-hover").tbody
    # # team["roster"] = []
    # for tableRow in tableBody.find_all("tr"):
    # #   print(tableRow)
    #     swimmerId = tableRow.a["href"].split("/")[-1]
    #     # print(swimmerId)
    #     swimmerName = normalizeName(tableRow.a.string)
    #     swimmerHome = tableRow.find("td", class_="u-text-truncate").string.strip()
    #     swimmerClass = tableRow.find_all("td", class_="c-table-clean__col-fit")[1].string.strip()
    #     # print(swimmerName)
    #     # team["roster"].append((swimmerName, swimmerId))
    #     # swimmers.append(swimmerName)
    #     if(len(Swimmer.objects.filter(name=swimmerName)) < 1):
    #         s = Swimmer(name=swimmerName, hometown=swimmerHome, class_year=swimmerClass)
    #         s.save()
# users/views.py

from django.contrib.auth import login
from django.shortcuts import redirect, render
from django.urls import reverse
from users.forms import CustomUserCreationForm, CreatePostForm, CommentForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from users.models import Post, Comment
from users.models import Swimmer
from users.models import CAT_CHOICES
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

# def auth_login(request):
#     return render(request, 'registration/login.html')

# the dashboard function renders the homepage, but requires a login
@login_required
def dashboard(request):
    return render(request, "users/homepage.html")

# the homepage function renders the homepage with 
# def homepage(request):
#     return render(request, "homepage.html")

# the register function allows a user to register
def register(request):
    if request.method == "GET":
        return render(
            request, "users/register.html",
            {"form": CustomUserCreationForm}
        )
    elif request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("dashboard"))

# the see_request function allows staff to see the user request
@user_passes_test(lambda user: user.is_staff)
def see_request(request):
    text = f"""
        Some attributes of the HttpRequest object:

        scheme: {request.scheme}
        path:   {request.path}
        method: {request.method}
        GET:    {request.GET}
        user:   {request.user}
    """

    return HttpResponse(text, content_type="text/plain")

# the user_info function allows staff to see the user info
@user_passes_test(lambda user: user.is_staff)
def user_info(request):
    text = f"""
        Selected HttpRequest.user attributes:

        username:     {request.user.username}
        is_anonymous: {request.user.is_anonymous}
        is_staff:     {request.user.is_staff}
        is_superuser: {request.user.is_superuser}
        is_active:    {request.user.is_active}
    """

    return HttpResponse(text, content_type="text/plain")

# the add_messages function allows a user to add a message once logged in
@login_required
def add_messages(request):
    username = request.user.username
    messages.add_message(request, messages.INFO, f"Hello {username}")
    messages.add_message(request, messages.WARNING, "DANGER WILL ROBINSON")

    return HttpResponse("Messages added", content_type="text/plain")

@login_required
def discussion_index(request):
    posts = Post.objects.all().order_by('-created_on')
    form = CreatePostForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            p = Post(title=form.cleaned_data["title"], body=form.cleaned_data["body"], author=form.cleaned_data["author"], category=form.cleaned_data["category"])
            p.save()
    context = {
        "posts": posts,
        "form": form,
    }
    return render(request, "discussion/discussion_index.html", context)

@login_required
def discussion_category(request, category):
    posts = Post.objects.filter(
        category__contains=category
    ).order_by(
        '-created_on'
    )
    context = {
        "category": posts[0].get_category_display,
        "posts": posts
    }
    return render(request, "discussion/discussion_category.html", context)

@login_required
def discussion_detail(request, pk):
    post = Post.objects.get(pk=pk)

    form = CommentForm()
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = Comment(
                author=form.cleaned_data["author"],
                body=form.cleaned_data["body"],
                post=post
            )
            comment.save()

    comments = Comment.objects.filter(post=post)
    context = {
        "post": post,
        "comments": comments,
        "form": form,
    }
    return render(request, "discussion/discussion_detail.html", context)

@login_required
def team_index(request):
    # if len(Swimmer.objects.all()) < 1:
    base = 'https://www.swimcloud.com'
    url = base + '/api/search/?q=' + urllib.parse.quote('Rensselaer Polytechnic Institute')
    results = [obj for obj in requests.get(url).json() if 'team' in obj['id']]
    if len(results) >= 1:
        swimmerData = []
        swimmerEvents = []
        women_url = base + results[0]['url'] + '/roster/?page=1&gender=F&season_id=24&sort=name'
        parse_team_data(women_url)
        # men_url = base + results[0]['url'] + '/roster/?page=1&gender=M&season_id=24&sort=name'
        # parse_team_data(men_url)

    swimmers = Swimmer.objects.all()
    context = {
        'swimmers': swimmers
    }
    return render(request, 'swimmers/team_index.html', context)

@login_required
def swimmer_detail(request, pk):
    swimmer = Swimmer.objects.get(pk=pk)
    url = "https://www.swimcloud.com/swimmer/" + swimmer.swimmer_id
    swimmer.event_list = parse_swimmer_data(url, swimmer.swimmer_id)
    swimmer.save()
    return render(request, 'swimmers/swimmer_detail.html', {'swimmer': swimmer})

@login_required
def discussion_create(request):
    form = CreatePostForm()
    if request.method == 'POST':
        form = CreatePostForm(request.POST)
        if form.is_valid():
            p = Post(title=form.cleaned_data["title"], body=form.cleaned_data["body"], author=form.cleaned_data["author"], category=form.cleaned_data["category"])
            p.save()
    context= {"form": form}
    return render(request, 'discussion/discussion_create.html', context)

def normalizeName(name):
    nameParts = name.strip().split(',')
    return nameParts[1].strip() + " " + nameParts[0].strip()

def parse_swimmer_data(url, swimmerId):
    page = urlopen(url)
    source = page.read()
    soup = BeautifulSoup(source, 'html.parser')
    events = ""
    selection = soup.find("select", class_="form-control input-sm js-event-id-selector")
    swimmerEvents = []
    if selection:
        for option in selection.find_all("option", class_="event"):
            thisEvent = option["value"]
            if thisEvent != "perf":
                swimmerEvents.append(thisEvent)

    for event in swimmerEvents:
        new_url = "https://www.swimcloud.com/swimmer/" + swimmerId + "/times/byeventid/" + event
        results = [obj for obj in requests.get(new_url).json()]
        swim = requests.get(new_url).json()[-1]
        splitDate = swim["dateofswim"].split('-')
        date = splitDate[1] + "/" + splitDate[2] + "/" + splitDate[0]
        sec = float(swim["time"])
        minutes = int(math.floor(sec / 60))
        sec = int(math.floor(sec % 60))
        milli = swim["time"][-2:]
        if minutes == 0:
            time = "{:02d}.{}".format(sec, milli)
        else:
            time = "{}:{:02d}.{}".format(minutes, sec, milli)
        if event[0] == "1":
            event = event[1:] + " Freestyle"
        elif event[0] == "2":
            event = event[1:] + " Backstroke"
        elif event[0] == "3":
            event = event[1:] + " Breaststroke"
        elif event[0] == "4":
            event = event[1:] + " Butterfly"
        elif event[0] == "5":
            event = event[1:] + " IM"
        # print(event, time)
        events += event + " " + time + "\n"
    return events

def parse_team_data(url):
    page = urlopen(url)
    source = page.read()
    soup = BeautifulSoup(source, 'html.parser')
    team = {}
    team["name"] = soup.find("h1", class_="c-toolbar__title").text.strip()
    tableBody = soup.find("table", class_="c-table-clean c-table-clean--middle table table-hover").tbody
    for tableRow in tableBody.find_all("tr"):
        swimmerId = tableRow.a["href"].split("/")[-1]
        swimmerName = normalizeName(tableRow.a.string)
        swimmerHome = tableRow.find("td", class_="u-text-truncate").string.strip()
        swimmerClass = tableRow.find_all("td", class_="c-table-clean__col-fit")[1].string.strip()
        if(len(Swimmer.objects.filter(name=swimmerName)) < 1):
            swimmer_url = "https://www.swimcloud.com/swimmer/" + swimmerId
            # event_data = parse_swimmer_data(swimmer_url, swimmerId)
            # print(event_data)
            s = Swimmer(swimmer_id=swimmerId, name=swimmerName, hometown=swimmerHome, class_year=swimmerClass)
            s.save()
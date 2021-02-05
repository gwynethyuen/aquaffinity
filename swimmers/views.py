from django.shortcuts import render
from models import Swimmer
import urllib.parse
import requests

def team_index(request):
    # swimmers = Swimmer.objects.all()
    swimmers = []
    base = 'https://www.swimcloud.com'
    url = base + '/api/search/?q=' + urllib.parse.quote('Rensselaer Polytechnic Institute')
    results = [obj for obj in requests.get(url).json() if 'team' in obj['id']]
    if len(results) == 1:
        swimmerData = []
        swimmerEvents = []
        new_url = base + results[0]['url'] + '/roster/??season=24&gender=M'
        # print(new_url)
        page = urlopen(new_url)
        source = page.read()
        soup = BeautifulSoup(source, 'html.parser')
        team = {}
        # 'gets a list of (Name, swimmerId) tuples and the team name for a given teamId'
        team["name"] = soup.find("h1", class_="c-toolbar__title").text.strip()
        tableBody = soup.find("table", class_="c-table-clean c-table-clean--middle table table-hover").tbody
        team["roster"] = []
        for tableRow in tableBody.find_all("tr"):
        #   print(tableRow)
            swimmerId = tableRow.a["href"].split("/")[-1]
            # print(swimmerId)
            swimmerName = normalizeName(tableRow.a.string)
            # print(swimmerName)
            team["roster"].append((swimmerName, swimmerId))
            swimmers.append(swimmerName)
        # print(team["roster"])
    context = {
        'swimmers': swimmers
    }
    return render(request, 'team_index.html', context)

def swimmer_detail(request, pk):
    swimmer = Swimmer.objects.get(pk=pk)
    context = {
        'swimmer': swimmer
    }
    return render(request, 'swimmer_detail.html', context)
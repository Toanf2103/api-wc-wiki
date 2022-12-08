import requests
from lxml import html
import datetime

#import sys
# caution: path[0] is reserved for script path (or '' in REPL)
#sys.path.insert(1, 'python.api-wc/module')
from module import xu_li

url = "https://en.wikipedia.org/wiki/2022_FIFA_World_Cup"


class Team(object):
    def __init__(self):
        self.icon = None
        self.name = None

    def setName(self, name):
        self.name = name

    def setIcon(self, icon):
        self.icon = 'https:'+icon


class Goal(object):
    def __init__(self):
        self.player = None
        self.timeG = None
        self.type = None

    def setPlayer(self, player):
        self.player = player

    def setTimeG(self, timeG):
        self.timeG = timeG

    def setType(self, type):
        self.type = type.rstrip('.')


class Match(object):
    def __init__(self):
        self.scorePen = None

    def setDate(self, date):
        self.date = date

    def setTime(self, time):
        self.time = time

    def setScore(self, score):
        self.score = score

    def setHomeT(self, homeT: object):
        self.homeT = homeT

    def setHomeG(self, homeG: list):
        self.homeG = homeG

    def setAwayT(self, awayT: object):
        self.awayT = awayT

    def setAwatG(self, awayG: list):
        self.awayG = awayG

    def setScorePen(self, scorePen):
        self.scorePen = scorePen

    def setStage(self, stage):
        self.stage = stage

    def setNameStage(self, nameStage):
        if ('_2' in nameStage):
            nameStage = nameStage.replace('_2', "")
        self.nameStage = nameStage


class Stage(object):
    def __init__(self,):
        self.stage = None
        self.nameStage = None

    def setStage(self, stage):
        self.stage = stage

    def setNameStage(self, nameStage):
        self.nameStage = nameStage


def getDate(match):
    return xu_li.formatTime(match['date'], match['time'], None)


def getTimeGoal(goal):
    return goal['timeG']


def checkStage(stage, nameStage):
    page = requests.get(url)
    document = html.fromstring(page.content)
    data = document.xpath(
        '//*[@class="footballbox"]')
    for line in data:
        t = line.xpath(
            'preceding-sibling::h2//span[@class="mw-headline"]//@id')[-1]
        if (stage.lower() == t.lower()):
            if (nameStage is None):
                return True
            else:
                nS = line.xpath(
                    'preceding-sibling::h3//span[@class="mw-headline"]//@id')[-1]
                if (nameStage.lower() == nS.lower()):
                    return True
    return False


def getMatch(status):
    listMatch = []
    page = requests.get(url)
    document = html.fromstring(page.content)
    data = document.xpath(
        '//*[@class="footballbox"]')

    for line in data:
        m = Match()

        # Lấy ngày đấu
        date = line.xpath(
            './/span[@class="bday dtstart published updated"]//text()')

        # Lấy giờ đấu
        time = line.xpath('.//div[@class="ftime"]//text()')

        # Lấy múi giờ
        utc = line.xpath('.//div[@class="ftime"]//a[2]//text()')

        # Chuyển qua việt nam
        if (len(utc) == 0):
            utc = []
            utc.append('UTC+3')

        kq = str(xu_li.formatTime(date[0], time[0], utc[0])).split(' ')
        m.setDate(kq[0])
        m.setTime(kq[1])

        # Lấy tên vòng
        test = line.xpath(
            'preceding-sibling::h3//span[@class="mw-headline"]//@id')[-1]
        m.setNameStage(test)

        # Lấy vòng
        t = line.xpath(
            'preceding-sibling::h2//span[@class="mw-headline"]//@id')[-1]
        m.setStage(t)

        # Lấy tỉ số
        score = line.xpath('.//th[@class="fscore"]//a//text()')
        if ('Match' in score[0]):
            score[0] = None
        if (score[0] == None and status == True):
            continue
        if (score[0] != None and status == False):
            continue
        m.setScore(score[0])

        # Lấy đội nhà
        hTeam = Team()
        hometeam = line.xpath(
            './/th[@class="fhome"]//span//a//text()|.//th[@class="fhome"]//span//text()')
        hTeam.setName(hometeam[0])
        iconhome = line.xpath(
            './/th[@class="fhome"]//span[@class="flagicon"]//img//@src')
        if (len(iconhome) != 0):
            hTeam.setIcon(xu_li.lam_net_anh(iconhome[0], '500'))
        m.setHomeT(hTeam.__dict__)

        # Lấy đội khách
        aTeam = Team()
        awayteam = line.xpath(
            './/th[@class="faway"]//span//a//text()|.//th[@class="faway"]//span//text()')

        aTeam.setName(awayteam[len(awayteam)-1])
        iconaway = line.xpath(
            './/th[@class="faway"]//span[@class="flagicon"]//img//@src')
        if (len(iconaway) != 0):
            aTeam.setIcon(xu_li.lam_net_anh(iconaway[0], '5000'))
        m.setAwayT(aTeam.__dict__)

        # Lấy bàn thắng home Team
        listHomeG = []
        gHome = line.xpath('.//tbody//tr[2]//td[@class="fhgoal"]//li')
        # gHome=data[7].xpath('.//tbody//tr[2]//td[@class="fhgoal"]//li')

        for g in gHome:
            time = g.xpath('./span[@class="fb-goal"]/span/text()')
            i = 1
            for x in time:
                if (not (")" in x or "(" in x)):
                    goal = Goal()
                    player = g.xpath('./a/text()')
                    goal.setPlayer(player[0])
                    goal.setTimeG(x)
                    typegoal = g.xpath(
                        './span[@class="fb-goal"]/span[{}]/a/text()'.format(i))
                    i = i+1
                    if (len(typegoal)):
                        goal.setType(typegoal[0])
                    listHomeG.append(goal.__dict__)
        listHomeG.sort(key=getTimeGoal)
        m.setHomeG(listHomeG)

        # Lấy bàn thắng đội khách
        listAwayG = []
        gAway = line.xpath('.//tbody//tr[2]//td[@class="fagoal"]//li')

        for g in gAway:
            time = g.xpath('./span[@class="fb-goal"]/span/text()')

            for x in time:
                if (not (")" in x or "(" in x)):
                    goal = Goal()
                    player = g.xpath('./a/text()')
                    goal.setPlayer(player[0])
                    goal.setTimeG(x)
                    typegoal = g.xpath(
                        './span[@class="fb-goal"]/span/a/text()')
                    if (len(typegoal)):
                        goal.setType(typegoal[0])
                    listAwayG.append(goal.__dict__)
        listAwayG.sort(key=getTimeGoal)
        m.setAwatG(listAwayG)

        # Lấy tỉ số pen
        scorePen = line.xpath('.//tbody//tr[4]/th/text()')
        if (len(scorePen) != 0):
            m.setScorePen(scorePen[0])

        listMatch.append(m.__dict__)

    # Sắp xếp list trận đấu theo ngày
    if (status):
        listMatch.sort(key=getDate, reverse=True)
    else:
        listMatch.sort(key=getDate, reverse=False)

    return listMatch


def getMatchStage(stage, nameStage, status):

    listMatch = []

    page = requests.get(url)
    document = html.fromstring(page.content)
    data = document.xpath(
        '//*[@class="footballbox"]')

    for line in data:
        m = Match()
        # Lấy ngày đấu
        date = line.xpath(
            './/span[@class="bday dtstart published updated"]//text()')
        # Lấy giờ đấu
        time = line.xpath('.//div[@class="ftime"]//text()')
        # Lấy múi giờ
        utc = line.xpath('.//div[@class="ftime"]//a[2]//text()')
        # Chuyển qua việt nam

        if (len(utc) == 0):
            utc = []
            utc.append('UTC+3')

        kq = str(xu_li.formatTime(date[0], time[0], utc[0])).split(' ')
        m.setDate(kq[0])
        m.setTime(kq[1])

        # Lấy vòng
        v = line.xpath(
            'preceding-sibling::h2//span[@class="mw-headline"]//@id')[-1]
        m.setStage(v)
        # Check stage có giống hay không
        if (v.lower() != stage.lower()):
            continue

        # Lấy tên vòng
        nameS = line.xpath(
            'preceding-sibling::h3//span[@class="mw-headline"]//@id')[-1]
        # Check nếu có nameStage và kiểm tra có giống hay không
        if (not (nameStage is None) and (nameS.lower() != nameStage.lower())):
            continue
        m.setNameStage(nameS)

        # Lấy tỉ số
        score = line.xpath('.//th[@class="fscore"]//a//text()')
        if ('Match' in score[0]):
            score[0] = None
        if (score[0] == None and status == True):
            continue
        if (score[0] != None and status == False):
            continue
        m.setScore(score[0])

        # Lấy đôi nhà
        hTeam = Team()
        hometeam = line.xpath(
            './/th[@class="fhome"]//span//a//text()|.//th[@class="fhome"]//span//text()')
        hTeam.setName(hometeam[0])
        iconhome = line.xpath(
            './/th[@class="fhome"]//span[@class="flagicon"]//img//@src')
        if (len(iconhome) != 0):
            hTeam.setIcon(xu_li.lam_net_anh(iconhome[0], '500'))
        m.setHomeT(hTeam.__dict__)

        # Lấy đội khách
        aTeam = Team()
        awayteam = line.xpath(
            './/th[@class="faway"]//span//a//text()|.//th[@class="faway"]//span//text()')

        aTeam.setName(awayteam[len(awayteam)-1])
        iconaway = line.xpath(
            './/th[@class="faway"]//span[@class="flagicon"]//img//@src')
        if (len(iconaway) != 0):
            aTeam.setIcon(xu_li.lam_net_anh(iconaway[0], '500'))
        m.setAwayT(aTeam.__dict__)

        # Lấy bàn thắng home Team
        listHomeG = []
        gHome = line.xpath('.//tbody//tr[2]//td[@class="fhgoal"]//li')
        # gHome=data[7].xpath('.//tbody//tr[2]//td[@class="fhgoal"]//li')

        for g in gHome:

            time = g.xpath('./span[@class="fb-goal"]/span/text()')
            i = 1
            for x in time:
                if (not (")" in x or "(" in x)):
                    goal = Goal()
                    player = g.xpath('./a/text()')
                    goal.setPlayer(player[0])
                    goal.setTimeG(x)
                    typegoal = g.xpath(
                        './span[@class="fb-goal"]/span[{}]/a/text()'.format(i))
                    i = i+1
                    if (len(typegoal)):
                        goal.setType(typegoal[0])
                    listHomeG.append(goal.__dict__)
        listHomeG.sort(key=getTimeGoal)
        m.setHomeG(listHomeG)

        # Lấy bàn thắng đội khách
        listAwayG = []
        gAway = line.xpath('.//tbody//tr[2]//td[@class="fagoal"]//li')

        for g in gAway:

            time = g.xpath('./span[@class="fb-goal"]/span/text()')

            for x in time:
                if (not (")" in x or "(" in x)):
                    goal = Goal()
                    player = g.xpath('./a/text()')
                    goal.setPlayer(player[0])
                    goal.setTimeG(x)
                    typegoal = g.xpath(
                        './span[@class="fb-goal"]/span/a/text()')
                    if (len(typegoal)):
                        goal.setType(typegoal[0])
                    listAwayG.append(goal.__dict__)
        listAwayG.sort(key=getTimeGoal)
        m.setAwatG(listAwayG)

        # Láy tỉ số pen
        scorePen = line.xpath('.//tbody//tr[4]/th/text()')
        if (len(scorePen) != 0):
            m.setScorePen(scorePen[0])

        listMatch.append(m.__dict__)

    # Sắp xếp theo ngày
    listMatch.sort(key=getDate, reverse=False)

    return listMatch


def getNameStage():
    page = requests.get(url)
    document = html.fromstring(page.content)
    data = document.xpath(
        '//div[@id="toc"]//ul//a[contains(@href,"stage")]')
    listStage = []
    for dong in data:

        name = dong.xpath(
            '..//a[contains(@href,"stage")]//@href')[0].strip('#')
        xp = dong.xpath('..//ul//li//a//@href')
        stage = Stage()
        listName = []
        for x in xp:
            if (not ('Bracket' in x)):
                listName.append(x.strip('#'))
        stage.setStage(name)
        stage.setNameStage(listName)
        print(listName)
        listStage.append(stage.__dict__)
    return listStage


def getTop(top, status):
    list = getMatch(status)
    size = len(list)
    top = int(top)
    if (top <= size):
        return list[:(top)]
    else:
        return list


def getByDay(day):
    listMatch = []
    page = requests.get(url)
    document = html.fromstring(page.content)
    data = document.xpath(
        '//*[@class="footballbox"]')

    for line in data:
        m = Match()

        # Lấy ngày đấu
        date = line.xpath(
            './/span[@class="bday dtstart published updated"]//text()')

        # Lấy giờ đấu
        time = line.xpath('.//div[@class="ftime"]//text()')

        # Lấy múi giờ
        utc = line.xpath('.//div[@class="ftime"]//a[2]//text()')

        # Chuyển qua việt nam
        if (len(utc) == 0):
            utc = []
            utc.append('UTC+3')

        kq = str(xu_li.formatTime(date[0], time[0], utc[0])).split(' ')
        m.setDate(kq[0])
        m.setTime(kq[1])
        if (kq[0] != day):
            continue

        # Lấy tên vòng
        test = line.xpath(
            'preceding-sibling::h3//span[@class="mw-headline"]//@id')[-1]
        m.setNameStage(test)

        # Lấy vòng
        t = line.xpath(
            'preceding-sibling::h2//span[@class="mw-headline"]//@id')[-1]
        m.setStage(t)

        # Lấy tỉ số
        score = line.xpath('.//th[@class="fscore"]//a//text()')
        if ('Match' in score[0]):
            score[0] = None

        m.setScore(score[0])

        # Lấy đội nhà
        hTeam = Team()
        hometeam = line.xpath(
            './/th[@class="fhome"]//span//a//text()|.//th[@class="fhome"]//span//text()')
        hTeam.setName(hometeam[0])
        iconhome = line.xpath(
            './/th[@class="fhome"]//span[@class="flagicon"]//img//@src')
        if (len(iconhome) != 0):
            hTeam.setIcon(xu_li.lam_net_anh(iconhome[0], '500'))
        m.setHomeT(hTeam.__dict__)

        # Lấy đội khách
        aTeam = Team()
        awayteam = line.xpath(
            './/th[@class="faway"]//span//a//text()|.//th[@class="faway"]//span//text()')

        aTeam.setName(awayteam[len(awayteam)-1])
        iconaway = line.xpath(
            './/th[@class="faway"]//span[@class="flagicon"]//img//@src')
        if (len(iconaway) != 0):
            aTeam.setIcon(xu_li.lam_net_anh(iconaway[0], '5000'))
        m.setAwayT(aTeam.__dict__)

        # Lấy bàn thắng home Team
        listHomeG = []
        gHome = line.xpath('.//tbody//tr[2]//td[@class="fhgoal"]//li')
        # gHome=data[7].xpath('.//tbody//tr[2]//td[@class="fhgoal"]//li')

        for g in gHome:
            time = g.xpath('./span[@class="fb-goal"]/span/text()')
            i = 1
            for x in time:
                if (not (")" in x or "(" in x)):
                    goal = Goal()
                    player = g.xpath('./a/text()')
                    goal.setPlayer(player[0])
                    goal.setTimeG(x)
                    typegoal = g.xpath(
                        './span[@class="fb-goal"]/span[{}]/a/text()'.format(i))
                    i = i+1
                    if (len(typegoal)):
                        goal.setType(typegoal[0])
                    listHomeG.append(goal.__dict__)
        listHomeG.sort(key=getTimeGoal)
        m.setHomeG(listHomeG)

        # Lấy bàn thắng đội khách
        listAwayG = []
        gAway = line.xpath('.//tbody//tr[2]//td[@class="fagoal"]//li')

        for g in gAway:
            time = g.xpath('./span[@class="fb-goal"]/span/text()')

            for x in time:
                if (not (")" in x or "(" in x)):
                    goal = Goal()
                    player = g.xpath('./a/text()')
                    goal.setPlayer(player[0])
                    goal.setTimeG(x)
                    typegoal = g.xpath(
                        './span[@class="fb-goal"]/span/a/text()')
                    if (len(typegoal)):
                        goal.setType(typegoal[0])
                    listAwayG.append(goal.__dict__)
        listAwayG.sort(key=getTimeGoal)
        m.setAwatG(listAwayG)

        # Lấy tỉ số pen
        scorePen = line.xpath('.//tbody//tr[4]/th/text()')
        if (len(scorePen) != 0):
            m.setScorePen(scorePen[0])

        listMatch.append(m.__dict__)
        listMatch.sort(key=getDate, reverse=False)

    # Sắp xếp list trận đấu theo ngày

    return listMatch

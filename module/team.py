from lxml import html
import requests
from module.xu_li import lam_net_anh


class team_class(object):
    # constructor
    def __init__(self, link_html):
        self.__link_html = link_html

    # method
    def get_name(self):
        name = self.__link_html.xpath('./th//a//text()')[0]
        return name

    def get_link_image(self):
        link_image = self.__link_html.xpath('./th//img/@src')[0]
        link_image = lam_net_anh(link_image, '5000')
        return link_image

    def get_position(self):
        position = self.__link_html.xpath('./td[1]//text()')[0]
        return position[0]

    def get_played(self):
        played = self.__link_html.xpath('./td[2]//text()')[0]
        return played[0]

    def get_won(self):
        won = self.__link_html.xpath('./td[3]//text()')[0]
        return won[0]

    def get_drawn(self):
        drawn = self.__link_html.xpath('./td[4]//text()')[0]
        return drawn[0]

    def get_lost(self):
        lost = self.__link_html.xpath('./td[5]//text()')[0]
        return lost[0]

    def get_goal_difference(self):
        goal_difference = self.__link_html.xpath('./td[6]//text()')[0]
        return goal_difference[0]

    def get_points(self):
        points = self.__link_html.xpath('./td[9]//text()')[0]
        return points[0]

    # export
    def get_all(self):
        self.name = self.get_name()
        self.image = self.get_link_image()
        self.position = self.get_position()
        self.played = self.get_played()
        self.won = self.get_won()
        self.drawn = self.get_drawn()
        self.lost = self.get_lost()
        self.goal_difference = self.get_goal_difference()
        self.points = self.get_points()


def get_all():
    page = requests.get('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup')
    tree = html.fromstring(page.content)

    list_group_id_html = tree.xpath(
        '//ul[preceding-sibling::a[@href="#Group_stage"]]/li/a/@href')

    list_group = []

    group = {}
    for group_id_html in list_group_id_html:
        group_id = group_id_html[1:]

        # lay ten group
        name_group_html = tree.xpath(
            '//span[@id="{}"]'.format(group_id))[0]

        # tro toi vi tri html cua team
        table_html = name_group_html.xpath(
            '../following-sibling::table[1]')[0]
        # lay team
        list_team = get_team(table_html)

        # them vao group
        group['group_name'] = name_group_html.text
        group['team'] = list_team

        # them vao list group
        list_group.append(group.copy())

    return list_group


def get_by_group(id_group):
    page = requests.get('https://en.wikipedia.org/wiki/2022_FIFA_World_Cup')
    tree = html.fromstring(page.content)

    if (checkStage(id_group, tree) != 1):
        list_group = {
            'status': 'Error',
            'message': 'Group is not correct'
        }
        return list_group

    group_name_html = tree.xpath('//h3/span[@id="{}"]'.format(id_group))[0]

    # lay ten group
    name_group = group_name_html.text

    list_group = {
        'status': 'success',
    }

    table_html = group_name_html.xpath('../following-sibling::table[1]')[0]
    # lay team
    list_team = get_team(table_html)

    # them vao list
    list_group['group_name'] = name_group
    list_group['team'] = list_team

    return list_group


def get_team(table_html):
    list_team = []

    list_team_html = table_html.xpath('.//tr[td]')

    for team_html in list_team_html:
        team = team_class(team_html)
        team.get_all()
        team.__dict__.pop('_team_class__link_html')
        list_team.append(team.__dict__.copy())

    return list_team


def checkStage(id_group, tree):
    group = tree.xpath(
        '//ul[preceding-sibling::a[@href="#Group_stage"]][.//a[@href="#{}"]]'.format(id_group))

    return len(group)

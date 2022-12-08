from flask import Flask, render_template, jsonify, request
from module import team
from module import match
from module import xu_li


app = Flask(__name__)


@app.route("/", methods=["GET"])
def getWelcome():
    listStage = match.getNameStage()
    return render_template('welcome.html', listStage=listStage)


@app.route("/team/get-all", methods=["GET"])
def getTeam():
    return team.get_all()


@app.route("/team/get-by-group/<id_group>", methods=["GET"])
def getTeamByGroup(id_group):
    return team.get_by_group(id_group)


@app.route("/match/get-all", methods=["GET"])
def getAll():
    data = {
        'status': 'success',
        'data': match.getMatch(None)
    }
    return data


@app.route("/match/get-by-status", methods=["GET"])
def getMatchByDate():
    rq = request.args

    if ('status' not in rq):
        data = {
            'status': 'success',
            'data': match.getMatch(None)
        }
    else:
        if (xu_li.isNum(rq['status']) or xu_li.isBool(rq['status']) == False):
            data = {
                'status': 'error',
                'data': 'status is bool'
            }
        else:
            todo = eval(rq['status'].title())

            data = {
                'status': 'success',
                'data': match.getMatch(todo)
            }

    return data


@app.route("/match/stage/<stage>", methods=["GET"])
def getMatchStage(stage):
    rq = request.args
    if (not match.checkStage(stage, None)):
        data = {
            'status': 'Error',
            'message': 'Stage is not correct'
        }
    elif ('status' not in rq):
        data = {
            'status': 'Success',
            'data': match.getMatchStage(stage, None, None)
        }
    elif (xu_li.isNum(rq['status']) or xu_li.isBool(rq['status']) == False):
        data = {
            'status': 'Error',
            'message': 'status is bool'
        }
    else:
        status = eval(rq['status'].title())

        data = {
            'status': 'Success',
            'data': match.getMatchStage(stage, None, status)
        }

    return data


@app.route("/match/stage/<stage>/<nameStage>", methods=["GET"])
def getMatchNameStage(stage, nameStage):
    rq = request.args

    if (not match.checkStage(stage, nameStage)):
        data = {
            'status': 'Error',
            'message': 'Stage is not correct'
        }
    elif ('status' not in rq):
        data = {
            'status': 'Success',
            'data': match.getMatchStage(stage, nameStage, None)
        }
    elif (xu_li.isNum(rq['status']) or xu_li.isBool(rq['status']) == False):
        data = {
            'status': 'Error',
            'message': 'Status is bool'
        }
    else:
        status = eval(rq['status'].title())

        data = {
            'status': 'Success',
            'data': match.getMatchStage(stage, nameStage, status)
        }

    return data


@app.route("/stage/get-all")
def getAllStage():
    return match.getNameStage()


@app.route("/match/top/<top>", methods=["GET"])
def getTop10(top):
    rq = request.args
    if ('status' not in rq):
        data = {
            'status': 'Error',
            'message': 'Need variable status'
        }
    elif (xu_li.isNum(rq['status']) or xu_li.isBool(rq['status']) == False):
        data = {
            'status': 'Error',
            'message': 'Status must be bool'
        }
    elif ((not xu_li.isNum(top)) or int(top) <= 0):
        data = {
            'status': 'Error',
            'message': 'Top is Number and Than 0'
        }
    else:
        status = eval(rq['status'].title())
        data = {
            'status': 'Success',
            'data': match.getTop(top, status)
        }
    return data


@app.route("/match/date", methods=["GET"])
def getByDate():
    rq = request.args
    if ('date' not in rq):
        data = {
            'status': 'Error',
            'message': 'Need variable date'
        }
    elif (not xu_li.isDay(rq['date'])):
        data = {
            'status': 'Error',
            'message': 'date format YYYY-mm-dd'
        }
    else:
        data = {
            'status': 'Success',
            'data': match.getByDay(rq['date'])
        }
    return data


if __name__ == "__main__":
    app.run()

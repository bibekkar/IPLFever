from django.shortcuts import render
from django.http import HttpResponseRedirect
import pandas as pd
from .models import Usertable
from .models import fixtures
from django.db.models import Count,Sum
from .models import betting
from django.contrib.auth import (authenticate,logout,login,get_user_model)
from dateutil import parser
import datetime
from django.contrib import messages
from django.contrib.auth.models import User
from itertools import chain


import xlrd
# Create your views here.

User = get_user_model()
def login_page(request):
    return render(request, 'login.html')

def user_login(request):

    # todayDate = todayDate + datetime.timedelta(days=4)
    # 2018 - 04 - 07
    user_name = request.POST.get('username')
    pwd = request.POST.get('password')
    print(user_name)
    # print(pwd)
    # user_data = Usertable(user_id ='hari', pwd = 'hari@1')
    # user_data.save()
    # user_data = Usertable.objects.filter(user_id = user_name, pwd = pwd)
    # print(user_data)
    check_user = User.objects.filter(username = user_name)
    if not check_user:
        messages.warning(request, 'user does not exist')
        return render(request, 'login.html')


    user = authenticate(username=user_name, password=pwd)
    # print('user value----',user)

    # print('user value----', user)
    if user is None:
        messages.warning(request, 'wrong password')
        return render(request, 'login.html')
    if user.is_authenticated:
        login(request, user)
        return HttpResponseRedirect('/dashboard/')


def dashboard(request):
    todayDate = datetime.datetime.now().strftime("%Y-%m-%d")
    todayTime = datetime.datetime.now().strftime("%H")
    todayTime = int(todayTime)

    # nowTime = todayDate.time()
    print('ddfdf',todayTime)
    user_name = request.user
    # print("true")
    match_data = fixtures.objects.filter(date=todayDate).values()
    super_user = User.objects.filter(username=user_name,is_superuser = True)
    if not super_user:
        user_type= 1
    else:
        user_type=2
    # print("user type value",user_type)
    exist_data1=[]
    leader_data = betting.objects.values('user_id').annotate(teamCount=Count('user_id'), tAmount=Sum('amount')).order_by('-tAmount')
    credit_data = betting.objects.filter(user_id=user_name).values('user_id').annotate(totalAmount=Sum('amount'))
    # print('leader_data dataaaa', leader_data)
    # print('credit_data dataaaa', credit_data)
    for row in match_data:
        # print('match id vaue ',row['id'])
        match = row['id']
        exist_data = betting.objects.filter(match_id = match).values('team','match_id').annotate(dcount =Count('team'))
        # print('betting dataaaa',exist_data)
        exist_data1.append(exist_data)

    # for index , lead in enumerate(leader_data,1):
    #     global user_rank
    #     if user_name== lead['user_id']:
    #          user_rank = index

    print("chart data",exist_data1)
    # teamsize = len(exist_data1)
    # print(teamsize)
    print("user match_data ",match_data)
    # betting_data1 = fixtures.objects.raw("""select b.id ,a.team , b.team1 , b.team2, b.result from login_betting a , login_fixtures b where a.user_id = (%s) and a.match_id = b.id """,[user_name])
    # print('aaaaaaaa',betting_data1)
    a = betting.objects.filter(user_id=user_name).values('match_id')
    b = fixtures.objects.filter(id__in=a).values('team1', 'team2', 'result', 'id')
    c = betting.objects.filter(user_id=user_name).values('team', 'match_id')
    betlist = []
    betDic = {}
    for rec in c:
        for reco in b:
            if rec['match_id'] == reco['id']:
                if rec['team'] == reco['result']:
                    result = "WON"
                elif reco['result'] == "":
                    result = "Yet to be played"
                else:
                    result = "LOST"
                betDic = {'team1': reco['team1'], 'team2': reco['team2'], 'result': result}
                betlist.append(betDic.copy())

    # print("match data", match_data[0]['team1'])
    return render(request, 'dash.html',
                  {'user_id': user_name, 'today_date': todayDate, 'match_details': match_data,'betting_details':betlist, 'chart_data':exist_data1 ,'leaderData':leader_data ,'creditData':credit_data,'user_type':user_type ,'todayTime':todayTime})




def bettingHistory(request):
    user_name = request.user
    a = betting.objects.filter(user_id =user_name).values('match_id')
    b= fixtures.objects.filter(id__in =a).values('team1','team2','result','id')
    c= betting.objects.filter(user_id = user_name).values('team','match_id')
    betlist=[]
    betDic ={}
    for rec in c:
        for reco in b:
            if rec['match_id'] == reco['id']:
                if rec['team']== reco['result']:
                    result = "WON"
                elif reco['result']=="":
                    result = "Yet to be played"
                else:
                    result ="LOST"
                betDic = {'team1':reco['team1'],'team2':reco['team2'],'result':result}
                betlist.append(betDic.copy())
    return render(request,'betting.html')

    # if not user_data:
    #
    # else:

# def user_login(request):
#     dd = pd.read_excel('C:\\Users\\Nurture\\Downloads\\ipl1.xlsx')
#     xx = dd.to_csv(index=False)
#     # for row in dd.iterrows():
#         #print(row[0])
#     a=xx.split('\n')
#     for b in range(0,len(a)-1):
#         c=a[b].split(',')
#         dt = parser.parse(c[4])
#         print("dt---------------",dt)
#         nis=fixtures(team1=c[1],team2=c[2],date=dt,time=c[5],venue=c[6])
#         nis.save()
#
#
#
#
#     #print(dd.to_csv( index=False))
#
#     return render(request,"dashboard.html")



def submit_bet1(request):
    teamSelected = request.POST.get('exampleRadios1')
    matchId = request.POST.get('matchId_1')
    user = request.user

    todayTime = datetime.datetime.now().strftime("%H")
    todayTime = int(todayTime)
    # print("user - id ",user)
    matchTime = fixtures.objects.filter(id = matchId).values('time')[0]
    print(matchTime)
    matchTime = int(matchTime['time'])

    betDataExisting = betting.objects.filter(match_id = matchId , user_id = user)
    if todayTime < matchTime-1:

        if not betDataExisting:
            betData = betting(match_id = matchId,team = teamSelected , user_id = user ,amount = 10.0)    # print('kjsdfkjsdjksdfh',user)
            betData.save()
        else:
           betting.objects.filter(match_id = matchId, user_id = user).update(team = teamSelected)
        messages.success(request, 'Your bet has been placed successfully!')
        return HttpResponseRedirect('/dashboard/')

    else:
        messages.warning(request, 'Betting time over!')
        return HttpResponseRedirect('/dashboard/')


# def submit_bet1(request):
#     teamSelected = request.POST.get('exampleRadios1')
#     matchId = request.POST.get('matchId_1')
#     user = request.user
#     print("user - id ",user)
#     betDataExisting = betting.objects.filter(match_id = matchId , user_id = user)
#     if not betDataExisting:
#         betData = betting(match_id = matchId,team = teamSelected , user_id = user ,amount = 10.0)    # print('kjsdfkjsdjksdfh',user)
#         betData.save()
#     else:
#         betting.objects.filter(match_id = matchId, user_id = user).update(team = teamSelected)
#
#     data ={'success':True,'message':'Your betting submitted successfully'}
#     return JsonResponse(data)

def submit_bet2(request):
    teamSelected = request.POST.get('exampleRadios2')
    matchId = request.POST.get('matchId_2')
    user = request.user
    # print("user - id ", user)
    betDataExisting = betting.objects.filter(match_id = matchId , user_id = user)
    if not betDataExisting:
        betData = betting(match_id = matchId,team = teamSelected , user_id = user ,amount = 0)    # print('kjsdfkjsdjksdfh',user)
        betData.save()
    else:
        betting.objects.filter(match_id = matchId, user_id = user).update(team = teamSelected)
    messages.success(request, 'Your bet has been placed successfully!')
    return HttpResponseRedirect('/dashboard/')

def updateResult1(request):

    winningTeam = request.POST.get('exampleRadiosUp1')
    winningMatchId = request.POST.get('matchIdUp_1')

    # print('**********',winningTeam)
    # print('*+++++++++++',winningMatchId)
    fixtures.objects.filter(id = winningMatchId).update(result = winningTeam)
    user = request.user

    userDataCount = User.objects.filter(is_superuser = False).count()
    # print('*+++++++++++', userDataCount)

    bettingCountData =  betting.objects.filter(match_id = winningMatchId, team = winningTeam).count()
    # print('*+++++++++++', bettingCountData)
    if bettingCountData!=0:
        winningAmount = userDataCount * 10 / bettingCountData
    else:
        winningAmount = userDataCount * 10 / userDataCount
    # print('*+++++++++++', winningAmount)
    betting.objects.filter(match_id = winningMatchId , team = winningTeam).update(amount = winningAmount)
    betting.objects.filter(match_id=winningMatchId).exclude(team =winningTeam).update(amount=0)
    return HttpResponseRedirect('/dashboard/')


def updateResult2(request):

    winningTeam = request.POST.get('exampleRadiosUp2')
    winningMatchId = request.POST.get('matchIdUp_2')

    # print('**********',winningTeam)
    # print('*+++++++++++',winningMatchId)
    fixtures.objects.filter(id = winningMatchId).update(result = winningTeam)
    user = request.user

    userDataCount = User.objects.count()
    # print('*+++++++++++', userDataCount)

    bettingCountData =  betting.objects.filter(match_id = winningMatchId, team = winningTeam).count()
    # print('*+++++++++++', bettingCountData)
    if bettingCountData!=0:
        winningAmount = userDataCount * 10 / bettingCountData
    else:
        winningAmount = userDataCount * 10 / userDataCount
    # print('*+++++++++++', winningAmount)
    betting.objects.filter(match_id = winningMatchId , team = winningTeam).update(amount = winningAmount)
    betting.objects.filter(match_id=winningMatchId).exclude(team =winningTeam).update(amount=0)
    return HttpResponseRedirect('/dashboard/')


def changePassword(request):

    return render(request ,'change.html')

def changePasswordSubmit(request):
    user_id = request.POST.get('userName')
    oldPwd = request.POST.get('oldPwd')
    newPwd1 = request.POST.get('newPwd1')
    newPwd2 = request.POST.get('newPwd2')
    if len(user_id) == 0:
        messages.warning(request, 'User field cannot be empty')
        return render(request, 'change.html')

    qs = User.objects.filter(username = user_id)
    if not qs:
        messages.warning(request, 'user does not exist')
        return render(request, 'change.html')
    u = User.objects.get(username=user_id)
    # print('user id',user_id)
    # print('old pwd',oldPwd)
    # print('new pwd 1',newPwd1)
    # print('new pwd 2',newPwd2)

    if len(oldPwd) ==0 or len(newPwd2)==0 or len(newPwd1)==0:
        messages.warning(request, 'Password field cannot be empty')
        return render(request, 'change.html')

    if len(oldPwd)!=0:
        user = authenticate(username=user_id, password=oldPwd)
        if user is None:
            messages.warning(request, 'Your old password is wrong')
            return render(request, 'change.html')

    if newPwd1==newPwd2:
        if newPwd2!=oldPwd and newPwd1!=oldPwd:
            if len(newPwd2)>5:
                if newPwd2!=user_id:
                    u.set_password(newPwd2)
                    u.save()
                    messages.success(request, 'Your password was updated successfully!')
                    return render(request,'login.html')
                else:
                    messages.warning(request, 'Password cannot be same as user id!')
                    return render(request, 'change.html')
            else:
                messages.warning(request, 'Password length too short!')
                return render(request, 'change.html')
        else:
            messages.warning(request, 'old and new passwords cannot be same')
            return render(request, 'change.html')
    else:
        messages.warning(request, 'New and re-entered passwords are not same!')
        return render(request,'change.html')


def dashboardData(request):
    todayDate = datetime.datetime.now().strftime("%Y-%m-%d")
    match_data = fixtures.objects.filter(date=todayDate).values()
    user_rank = ""
    exist_data1 = []
    user_name = request.user
    # print("user name value",user_name)
    for row in match_data:
        # print('row value', row)
        # print('match id vaue ', row['id'])
        match = row['id']
        exist_data = betting.objects.filter(match_id=match).values('team', 'match_id').annotate(dcount=Count('team'))
        leader_data = betting.objects.values('user_id').annotate(teamCount=Count('user_id'), tAmount=Sum('amount'))
        credit_data = betting.objects.filter(user_id=user_name).values('user_id').annotate(totalAmount=Sum('amount'))
        # print('betting dataaaa', exist_data)
        # print('credit_data dataaaa', credit_data)
        # print('leader_data dataaaa', leader_data)
        exist_data1.append(exist_data)

    for index, lead in enumerate(leader_data, 1):
        if user_name == lead['user_id']:
            user_rank = index

    # print("chart data", exist_data1)
    # print("user rank ", user_rank)
    betting_data1 = fixtures.objects.raw(
        """select b.id ,a.team , b.team1 , b.team2, b.result from login_betting a , login_fixtures b where a.user_id = (%s) and a.match_id = b.id """,
        [user_name])
    # print(betting_data1)
    # print("match data", match_data[0]['team1'])
    return render(request, 'dash.html',
                  {'user_id': user_name, 'today_date': todayDate, 'match_details': match_data,
                   'betting_details': betting_data1, 'chart_data': exist_data1, 'leaderData': leader_data,
                   'creditData': credit_data, 'user_rank': user_rank})

from secrets import MY_GMAIL, GMAIL_PASSWORD, Token
import discord
from discord.ext import commands
import smtplib
from datetime import datetime
from lxml import html
from bs4 import BeautifulSoup
import requests
import asyncio


bot = commands.Bot(command_prefix='$')


class ContestDetails:
    def __init__(self):
        self.Name = '?'
        self.Type = '?'
        self.Number = '?'
        self.Date = '?'
        self.StartTime = '?'
        self.EndTime = '?'
        self.Duration = '?'
        self.Description='?'
        self.signature = '''<br><br><table width="351" cellspacing="0" cellpadding="0" border="0"> <tr> <td style="vertical-align: top; text-align:left;color:#000000;font-size:12px;font-family:helvetica, arial;; text-align:left"> <span><span style="margin-right:5px;color:#000000;font-size:15px;font-family:helvetica, arial">Happy Coding;</span> <br><span style="margin-right:5px;color:#000000;font-size:12px;font-family:helvetica, arial">CPHUB | NITC Codechef Campus Chapter</span></span> <br><br> <table cellpadding="0" cellpadding="0" border="0"><tr><td style="padding-right:5px"><a href="https://facebook.com/cphub.nitc/" style="display: inline-block;"><img width="40" height="40" src="https://s1g.s3.amazonaws.com/23f7b48395f8c4e25e64a2c22e9ae190.png" alt="Facebook" style="border:none;"></a></td><td style="padding-right:5px"><a href="https://instagram.com/cphub.nitc/" style="display: inline-block;"><img width="40" height="40" src="https://s1g.s3.amazonaws.com/4c616177ca37bea6338e6964ca830de5.png" alt="Instagram" style="border:none;"></a></td><td style="padding-right:5px"><a href="https://discord.gg/dpHV4sm6XF" style="display: inline-block;"><img width="40" height="40" src="https://s1g.s3.amazonaws.com/ba48639bd505cee2cc8b43ecb698f903.png" alt="Discord" style="border:none;"></a></td><td style="padding-right:5px"><a href="https://cphub-nitc.github.io/chapter/index.html" style="display: inline-block;"><img width="40" height="40" src="https://s1g.s3.amazonaws.com/8ab12118c0ee1056ed787deb1a208149.png" alt="General (Enter full link)" style="border:none;"></a></td></tr></table> </td> </tr> </table> <table width="351" cellspacing="0" cellpadding="0" border="0" style="margin-top:10px"> <tr> <td style="text-align:left;color:#aaaaaa;font-size:10px;font-family:helvetica, arial;"><p>Note: This mail is sent using Mailer Bot</p></td> </tr> </table> '''


    def print_details(self):
        print('Name ' + self.Name)
        print('Type' + ' ' + self.Type)
        print('Number' + ' ' + self.Number)
        print('Date' + ' ' + self.Date)
        print('StartTime' + ' ' + self.StartTime)
        print('EndTime' + ' ' + self.EndTime)
        print('Duration' + ' ' + self.Duration)
        print(self.Description)
        # print(self.signature)

def time_diff(s1, s2):
    time1 = int(s1[0:2]) * 60 + int(s1[3:5])
    time2 = int(s2[0:2]) * 60 + int(s2[3:5])

    minutes = 0

    if (s1 <= s2):
        minutes = time2 - time1
    else:
        total = 24 * 60
        minutes = total - time1 + time2

    hours = minutes // 60
    minutes -= hours * 60
    result = str(hours) + ':'
    if (minutes < 10):
        result += '0' + str(minutes)
    else:
        result += str(minutes)

    return result

def mirror(sample,URL):
    message = "Greetings, \n\nWe are glad to invite you to take part in " + str(sample.Name) + ". This contest will be held on Virtual Judge. You will be given 8-12 previous ICPC Regionals problems and "+ str(sample.Duration)+" hours to solve them. You guys can participate in a team of 3 members wherein you can discuss the strategy, logic, code, etc and submit your solutions.\n\n" + "Contest link: " + str(
        URL) + "\n" + "Date: " + str(sample.Date)+"\n" + "Start time: " + str(sample.StartTime)+"\n" + "Contest Duration: " + str(sample.Duration)+"\n"+"\n" + "Editorials will be sent to your mail after the contest.\nAll The Best."
    # print(message)
    # TextDescription = message
    sample.Description=message
    # return message

def Beginner(sample, URL):

    message = "Greetings, \n\nWe are glad to invite you to take part in " + str(sample.Name) + ". This contest will be held on Virtual Judge. You will be given 6-8 problems and "+str(sample.Duration)+" hours to solve them. You guys can participate in a team of 3 members wherein you can discuss the strategy, logic, code, etc and submit your solutions.\n\n" + "Contest link: " + str(
        URL) + "\n" + "Date: " + str(sample.Date)+"\n"+"Start time: " + str(sample.StartTime) + "\n" + "Contest Duration: " + str(sample.Duration) + "\n\n" + "Editorials will be sent to your mail after the contest.\nAll The Best."
    # print(message)
    # TextDescription = message
    sample.Description = message
    # return message


def Compose_Mail(Contest):
    receiver = 'chandurivarshith264@gmail.com'

    message = 'Subject: {}\n\n{}'.format(
        'Invitation to ' + Contest.Name, Contest.Description)

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(MY_GMAIL, GMAIL_PASSWORD)
    server.sendmail(MY_GMAIL, receiver, message)



@bot.command()
async def mail(ctx, URL):
    # link = URL

    SampleContest = ContestDetails()

    r = requests.get(URL).text
    soup = BeautifulSoup(r, 'lxml')
    article = soup.find('h3')
    s = article.text

    # parsing contest name
    contest = ''
    prev = '-1'

    for i in range(63, len(s)):
        if prev == ' ' and prev == s[i]:
            break
        else:
            contest = contest + s[i]
        prev = s[i]

    contest = contest.upper().strip()
    SampleContest.Name = contest
    # parsing contest name finished
    
    times = []
    t = 0

    for span in soup.find_all('span'):
        times.append(int(span.text[:10]))
        t += 1
        if (t == 2):
            break

    info = []

    for timestamp in times:
        dt_object = datetime.fromtimestamp(timestamp)
        temp = ''
        dt_object = str(dt_object)
        for i in dt_object:
            if (i == ' '):
                info.append(temp)
                temp = ''
            else:
                temp += i
        info.append(temp)

    SampleContest.Date = info[0]
    SampleContest.StartTime = info[1]
    SampleContest.EndTime = info[3]

    num = ''
    # flag = True

    if (contest.find('#') != -1):
        for i in range(contest.index('#')+1, len(contest)):
            num += contest[i]

        SampleContest.Number = num
    
    SampleContest.Duration = time_diff(info[1], info[3]) + ' hours'


    if (contest.find('MIRROR') != -1 or contest.find('ICPC') != -1):
        SampleContest.Type = 'ICPC MIRROR'
        mirror(SampleContest,URL)
    elif (contest.find('BEGINNER') != -1):
        SampleContest.Type = 'BEGINNER CONTEST'
        Beginner(SampleContest, URL)
    else:
        await ctx.send('Invalid contest link, please try again!')
        return

    
    if(SampleContest.StartTime < "12:00:00"):
        SampleContest.StartTime = info[1][:5] + ' AM'
    else:
        SampleContest.StartTime = info[1][:5] + ' PM'

    
    # SampleContest.print_details()

    embedVar = discord.Embed(title="Mail Preview", description="", color= 0x00ff00)
    embedVar.add_field(name='Invitation to ' + SampleContest.Name,value=SampleContest.Description, inline=False)
    await ctx.send(embed=embedVar)

    embedVar = discord.Embed(title="Confirm mail",
                             description="Enter 1 if you want to send mail otherwise enter 0 within 45 seconds", color=0x00ff00)
    await ctx.send(embed=embedVar)

    def check(m):
        return m.channel == message.channel and m.author != client.user

    try:
        message = await bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author)
        if message.content == '1':
            Compose_Mail(SampleContest)
            embedVar = discord.Embed(
                title="Mail sent successfully", description="", color=0x00ff00)
            await ctx.send(embed=embedVar)
        else:
            embedVar = discord.Embed(
                title="Mail discarded, try again if you wish to", description="", color=0x00ff00)
            await ctx.send(embed=embedVar)
    except asyncio.TimeoutError:
        embedVar = discord.Embed(title="timeup you did not respond, please try again if you wish to",description="", color=0x00ff00)
        await ctx.send(embed=embedVar)
    
    
@bot.event
async def on_ready():
    await bot.change_presence(activity=discord.Game("Nykterstein ORZ"))

    

@bot.command()
async def working(ctx):
    await ctx.send("Yes I'm working")




bot.run(Token)




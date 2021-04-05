from secrets import MY_GMAIL, GMAIL_PASSWORD, Token
import discord
from discord.ext import commands
import smtplib
from datetime import datetime
from lxml import html
from bs4 import BeautifulSoup
import requests
import asyncio
from email.mime.multipart import MIMEMultipart
from email.message import EmailMessage

from keep_alive import keep_alive


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


    def print_details(self):
        print('Name ' + self.Name)
        print('Type' + ' ' + self.Type)
        print('Number' + ' ' + self.Number)
        print('Date' + ' ' + self.Date)
        print('StartTime' + ' ' + self.StartTime)
        print('EndTime' + ' ' + self.EndTime)
        print('Duration' + ' ' + self.Duration)
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


def Compose_Mail(Contest, to,cc,bcc):
    # receiver = 'bec18@nitc.ac.in'
    receiver = to + cc + bcc

    message = 'Subject: {}\n\n{}'.format(
        'Invitation to ' + Contest.Name, Contest.Description)

    msg = EmailMessage()
    msg.set_content(Contest.Description)
    msg['Subject'] = 'Invitation to ' + Contest.Name
    msg['From'] = MY_GMAIL
    msg['To'] = to
    msg['Cc'] = cc
    msg['Bcc'] = bcc

    # s = smtplib.SMTP('localhost')


    # s.send_message(msg)
    # s.quit()

    server = smtplib.SMTP('smtp.gmail.com', 587)
    server.starttls()

    server.login(MY_GMAIL, GMAIL_PASSWORD)
    server.send_message(msg)
    # server.sendmail(MY_GMAIL, receiver, message)


def details(to, cc, bcc):
    text = 'to: '
    for i in to:
        text += str(i) +" "
    text += '\ncc: '
    for i in cc:
        text += str(i)+" "
    if len(cc) == 0:
        text += 'none'
    text += '\nBcc: '
    for i in bcc:
        text += str(i)+" "
    if len(bcc) == 0:
        text += 'none'
    text+='\n'
    
    return text
    
    



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

    
    SampleContest.print_details()
    CC_address = ['smruthi@codechef.com', 'lijia@nitc.ac.in']
    TO_address = ['students@nitc.ac.in']
    BCC_address = []



    # CC_address = ['raghuram_b180061ec@nitc.ac.in']
    # TO_address = ['varshith_b180514ec@nitc.ac.in']
    # BCC_address = []

    embedVar = discord.Embed(
        title="Enter your name and roll no saperated by space", description="", color=0x00ff00)
    await ctx.send(embed=embedVar)

    try:
        message = await bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author)
        names = message.content.split(" ")
        if len(names) == 2:
            SampleContest.Description += "\nRegards\n"+names[0]+"\n"+names[1]
            SampleContest.Description += "\n~CPHub NITC"

    except asyncio.TimeoutError:
        embedVar = discord.Embed(
            title="timeup you did not respond, please try again if you wish to", description="", color=0x00ff00)
        await ctx.send(embed=embedVar)
        return


    embedVar = discord.Embed(title="Mail Preview",
                             description="", color=0x00ff00)
    embedVar.add_field(name="Preview",
                       value=details(TO_address, CC_address, BCC_address), inline=False)
    embedVar.add_field(name='Invitation to ' + SampleContest.Name,
                       value=SampleContest.Description, inline=False)
    await ctx.send(embed=embedVar)

    embedVar = discord.Embed(title="Confirm mail",
                             description="Enter 1 if you want to send mail otherwise enter 0 to change (to,cc,bcc) details within 60 seconds", color=0x00ff00)
    await ctx.send(embed=embedVar)

    try:
        message = await bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author)
        if message.content == '1':

            Compose_Mail(SampleContest, TO_address, CC_address, BCC_address)
            embedVar = discord.Embed(
                title="Mail sent successfully", description="", color=0x00ff00)
            await ctx.send(embed=embedVar)
            return 
        else:
            CC_address.clear()
            TO_address.clear()
            BCC_address.clear()
    except asyncio.TimeoutError:
        embedVar = discord.Embed(
            title="timeup you did not respond, please try again if you wish to", description="", color=0x00ff00)
        await ctx.send(embed=embedVar)







    embedVar = discord.Embed(
        title="Enter 'TO' receiver address", description="", color=0x00ff00)
    await ctx.send(embed=embedVar)

    try:
        message = await bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author)
        TO_address = [names for names in (message.content).split(" ")]
    except asyncio.TimeoutError:
        embedVar = discord.Embed(
            title="timeup you did not respond, please try again if you wish to", description="", color=0x00ff00)
        await ctx.send(embed=embedVar)
        return


    embedVar = discord.Embed(title="Enter CC's receiver address, '0' to leave it empty", description="", color= 0x00ff00)
    await ctx.send(embed=embedVar)

    try:
        message = await bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author)
        if message.content != '0':
            CC_address=[names for names in (message.content).split(" ")]
        else:
            CC_address.clear()
    except asyncio.TimeoutError:
        embedVar = discord.Embed(
            title="timeup you did not respond, please try again if you wish to", description="", color=0x00ff00)
        await ctx.send(embed=embedVar)
        return

    embedVar = discord.Embed(title="Enter BCC's receiver address, '0' to leave it empty", description="", color=0x00ff00)
    await ctx.send(embed=embedVar)

    try:
        message = await bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author)
        if message.content != '0':
            BCC_address = [names for names in message.content.split(" ")]
        else:
            BCC_address.clear()
    except asyncio.TimeoutError:
        embedVar = discord.Embed(
            title="timeup you did not respond, please try again if you wish to", description="", color=0x00ff00)
        await ctx.send(embed=embedVar)
        return

   


    
    embedVar = discord.Embed(title="Mail Preview", description="", color=0x00ff00)
    embedVar.add_field(name="Preview",
                       value=details(TO_address,CC_address,BCC_address), inline=False)
    embedVar.add_field(name='Invitation to ' + SampleContest.Name,value=SampleContest.Description, inline=False)
    await ctx.send(embed=embedVar)

    embedVar = discord.Embed(title="Confirm mail",
                             description="Enter 1 if you want to send mail otherwise enter 0 within 60 seconds", color=0x00ff00)
    await ctx.send(embed=embedVar)
    

    try:
        message = await bot.wait_for('message', timeout=60, check=lambda message: message.author == ctx.author)
        if message.content == '1':
            Compose_Mail(SampleContest,TO_address ,CC_address,BCC_address )
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
    await bot.change_presence(activity=discord.Game("Chess, because why not?"))
    # await bot.get_channel(821633183820939318).send("I'm online !")

@bot.command()
async def working(ctx):
    await ctx.send("Yes I'm working")


# @bot.event
# async def on_disconnect():
#     await bot.get_channel(821633183820939318).send('bye!')

keep_alive()

bot.run(Token)





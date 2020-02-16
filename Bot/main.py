from discord.ext import commands
import discord
import random
from random import randint

client = commands.Bot(command_prefix='!')
client.remove_command('help')  # removes default help command

TOKEN = 'XXXXXXXXXXXXXXXXXXXXXXXX' # replace with your token  

stabGifs = ['https://giphy.com/gifs/glitch-video-game-knife-X7tP14xUk1CsE',
            'https://gfycat.com/discover/stabbing-gifs',
            'https://thumbs.gfycat.com/HeavyEducatedAmericanlobster-size_restricted.gif',
            'https://media3.giphy.com/media/mSyVMpWcT27sY/source.gif',
            ]

# Riddle variables
answering = False
trivia = ""
triviaAnswer = ""
triviaLine = 0
triviaGuessesLeft = 3
prevTriviaLine = 0


@client.event
async def on_message(ctx):
    await client.process_commands(ctx)
    if ctx.content.lower().startswith('!help'):
        cmds = {}
        cmds['!killme'] = "u won't"
        cmds['!stab'] = 'wanna stab someone we got you fam !stab @ mention user'
        cmds['!rps'] = 'rock, paper, scissors EX:!rps <rock> '
        cmds['!trivia'] = 'Think your smart... well your not so play this game instead !trivia to start'
    msg = discord.Embed(title='Python Bot',
                        description="Written by Siinatra35, Astralynx, and  rodatboat ",
                        color=0x0000ff)
    for command, description in cmds.items():
        msg.add_field(name=command, value=description, inline=False)
    msg.add_field(name='Source code ', value='< git link >', inline=False)
    await ctx.channel.send(embed=msg)


# status for Bot
@client.event
async def on_ready():
    await client.change_presence(activity=discord.Game(name="Python | !help"))  # changes the activity of PyBot


@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def killme(ctx):
    await ctx.send(f'{ctx.author}, no! Choose life!')


@killme.error
async def killme_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Okay, buddy. Looks like you need some help. Here you go: https://suicidepreventionlifeline.org\n"
        "(Available in {:.2f}s.)".format(error.retry_after)
        await ctx.send(msg)


@client.command()
@commands.cooldown(1, 15, commands.BucketType.user)
async def stab(stb, user: discord.Member):
    await stb.send('{} HAS BEEN STABBED!'.format(user.name))
    await stb.send(random.choice(stabGifs))


@stab.error
async def stab_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Calm down, you psychopath. Available in {:.2f}s.".format(error.retry_after)
        await ctx.send(msg)


@client.command()
@commands.cooldown(3, 40, commands.BucketType.user)
async def rps(ctx, msg: str):
    # The options
    t = ["rock", "paper", "scissors"]
    # random choice for the bot
    computer = t[randint(0, 2)]
    player = msg.lower()  # coverts players input to lower case
    # if statements for possible outcomes
    if player == computer:
        await ctx.send("Tie!")
    elif player == "rock":
        if computer == "paper":
            await ctx.send("You lose! {0} covers {1}.".format(computer, player))
        else:
            Rcases = ["You win! {0} smashes {1}.",
                      "Amazing! {1} absolutely eviscerated {0}! You lose."]
            await ctx.send(random.choice(Rcases).format(player, computer))
    elif player == "paper":
        if computer == "scissors":
            Pcases = ["You lose! {0} cut {1}.",
                      "Wow! Those were some weak ass {0}. {1} wins!"]
            await ctx.send(random.choice(Pcases).format(computer, player))
        else:
            await ctx.send("You win! {0} covers {1}.".format(player, computer))
    elif player == "scissors":
        if computer == "rock":
            Scases = ["You lose! {0} smashes {1}.",
                      "Fuck it. {1} beats {0}. You're welcome."]
            await ctx.send(random.choice(Scases).format(computer, player))
        else:
            await ctx.send("You win! {0} cut {1}.".format(player, computer))
    else:
        await ctx.send("That's not a valid play. Check your spelling, you dope.")


@rps.error
async def rps_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "3 tries is enough, don't you think? Available in {:2f}s."
        await ctx.send(msg)


@client.command()
@commands.cooldown(1, 60, commands.BucketType.user)
async def trivia(rdl):
    global trivia, triviaLine, prevTriviaLine, triviaAnswer, triviaGuessesLeft, answering
    answering = True
    trivia = ""
    triviaAnswer = ""
    triviaGuessesLeft = 3

    with open("trivia.txt", "r") as f:
        lines = f.readlines()
    while trivia == "" or "=" in trivia or triviaLine == prevTriviaLine:
        triviaLine = random.randrange(0, len(lines))
        trivia = lines[triviaLine]
        triviaAnswer = lines[triviaLine + 1]
    prevTriviaLine = triviaLine
    f.close()

    triviaAnswer = triviaAnswer.replace("=", "")
    triviaAnswer = triviaAnswer.replace(" ", "")

    # instruction on how to play game cuz users are idiots
    await rdl.send("Use !answer <word> to solve the question.  All answers to these questions will be one word or "
                   "number.  You have three guesses per question.\n\n" + "`" + trivia + "`")


@trivia.error
async def riddle_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "Only one riddle per 60 seconds! Try again in {:.2f}s.".format(error.retry_after)
        await ctx.send(msg)


@client.command()
@commands.cooldown(3, 60, commands.BucketType.user)
async def answer(self, userAnswer: str):
    global triviaAnswer, triviaGuessesLeft, answering

    if answering is False:
        await self.send("Use !riddle to receive another riddle")
        return

    player = userAnswer.strip()
    triviaAnswer = triviaAnswer.strip()

    if str.lower(player) == str.lower(triviaAnswer):
        await self.send("Correct!")
        answering = False
    else:
        triviaGuessesLeft -= 1
        await self.send("Incorrect!  Guesses left:" + str(triviaGuessesLeft))
    if triviaGuessesLeft == 0:
        await self.send("Out of guesses!  The answer was: " + triviaAnswer)


@answer.error
async def answer_error(ctx, error):
    if isinstance(error, commands.CommandOnCooldown):
        msg = "You've used up all your guesses. Try again in {:.2f}s.".format(error.retry_after)
        await ctx.send(msg)


client.run(TOKEN)

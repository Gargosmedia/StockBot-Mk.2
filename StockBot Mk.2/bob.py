
import discord

f = open("token.txt", "r")
TOKEN=f.read()

client = discord.Client()

@client.event
async def on_message(message):

    if message.author == client.user:
        return

    if message.content.startswith('Dumpit'):
        msg = 'Hello {0.author.mention}'.format(message)
        await client.send_message(message.channel, msg)


    if message.content.startswith('he bought'):
        msg = 'Master, dump it!'.format(message)
        await client.send_message(message.channel, msg)
    if message.content.startswith('he sold'):
        msg = 'Master, bump it!'.format(message)
        await client.send_message(message.channel, msg)

    if "che tam" in message.content.lower():

        portfolio=read_portfolio()

        if portfolio[2]>0:
            msg="\nBang bang bang, gained (+) " + str(portfolio[2]) + "$" + "\n" 
            if "+" in message.content or "full" in message.content:
               msg+="\nMoney left: " + str(portfolio[1]) + "$" + "\n\n------"

        elif portfolio[2]<=0:
            msg="Shit shit shit, lost (-) " + str(portfolio[2]) + "$"
        
        await client.send_message(message.channel, msg)

        if "full" in  message.content.lower():
            f_msg=""
            total=0
            for key, value in portfolio[0].items():
                
                f_msg += key + " | " + "Price: " + str(value[0][1]) + " | Shares: " + str(value[1][1]) +"\n"
                total+=value[0][1]*value[1][1]
                
            f_msg+="-----\nTotal money in stocks: " + str(round((total+portfolio[1]),2)) + "$"
            
            await client.send_message(message.channel, f_msg)

    

def read_portfolio():
    portoflio=[]

    f = open("portfolio.txt", "r")

    gather=f.read().split("/|/")

    portfolio = eval(gather[0])
    money_p=eval(gather[1])
    change_p=eval(gather[2])
    
    return portfolio, money_p, change_p



@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

client.run(TOKEN)

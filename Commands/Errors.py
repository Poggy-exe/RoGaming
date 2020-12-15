import discord
from discord.ext import commands

class Errors(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_command_error(self,ctx,error):
        print(error)
        if isinstance(error,commands.MissingRequiredArgument):
            await ctx.send("Missing one or more required arguments please use `.help (command)` to see how to use it")
        elif isinstance(error,commands.ArgumentParsingError):
            await ctx.send("Argument is not in the correct format please use `.help (command)` to see how to use it")
        elif isinstance(error, commands.BotMissingRole):
            await ctx.send("Bot is missing required role")
        elif isinstance(error,commands.BotMissingPermissions):
            await ctx.send("Bot is missing required permission")
        elif isinstance(error, commands.ChannelNotFound):
            await ctx.send("Channel not found")
        elif isinstance(error, commands.CommandNotFound):
            await ctx.send("No such command was found")
        elif isinstance(error, commands.CommandInvokeError):
            await ctx.send("There was an error trying to run this command")
        elif isinstance(error, commands.DisabledCommand):
            await ctx.send("This command has been disabled")
        elif isinstance(error, commands.EmojiNotFound):
            await ctx.send("Emoji could not be recognised")
        elif isinstance(error, commands.ExtensionNotFound):
            await ctx.send("Extension could not be found")
        elif isinstance(error,commands.MemberNotFound):
            await ctx.send("User not found")
        elif isinstance(error, commands.MessageNotFound):
            await ctx.send("Message not found")
        elif isinstance(error,commands.MissingPermissions):
            await ctx.send("You dont have the required permissions")
        elif isinstance(error,commands.NSFWChannelRequired):
            await ctx.send("Channel must be marked as NSFW")
        elif isinstance(error,commands.PrivateMessageOnly):
            await ctx.send("This command can only be used in private channel")
        elif isinstance(error,commands.RoleNotFound):
            await ctx.send("Role not found")
        elif isinstance(error,commands.TooManyArguments):
            await ctx.send("Too many arguments please use `.help (command)` to see how to use it")
        elif isinstance(error, TimeoutError):
            await ctx.send("You took to long to respond. Cancelled")

def setup(client):
    client.add_cog(Errors(client))
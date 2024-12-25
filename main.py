import discord
import os
import pyotp
import time
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

#登録したいOTPのシークレット
OTP_SECRETS = {
    'x': os.getenv('X_OTP'),
    'discord': os.getenv('DISCORD_OTP'),
}

#コマンドを実行可能なユーザーのID
#※セルボのIDを指定するとOTPの再発行リアクションを付けた際にバグります
ALLOWED_USER_IDS = [515099522129461254]

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
bot = commands.Bot(command_prefix="!", intents=intents) #ご自由なprefixへどぞ


@bot.command()
async def otp(ctx, arg=None):
    if ctx.author.id not in ALLOWED_USER_IDS:
        return

    if arg in OTP_SECRETS:
        otp_secret = OTP_SECRETS.get(arg)
        if otp_secret is None:
            await ctx.reply("OTP シークレットが見つかりません。")
            return

        totp = pyotp.TOTP(otp_secret)
        current_code = totp.now()
        current_timestamp = time.time()
        expiry_timestamp = current_timestamp + totp.interval - (current_timestamp % totp.interval)
        expiry_unix = int(expiry_timestamp)

        discord_timestamp = f"<t:{expiry_unix}:R>"

        message = await ctx.reply(f"現在のコード: {current_code}\nコードの有効期限: {discord_timestamp}")
        await message.add_reaction("🔄")

        bot.otp_message = message
        bot.otp_type = arg
    else:
        await ctx.reply("無効な OTP タイプです。")

@bot.event
async def on_reaction_add(reaction, user):
    if user.bot:
        return

    if not hasattr(bot, 'otp_message') or reaction.message.id != bot.otp_message.id:
        return

    if str(reaction.emoji) == "🔄":
        if user.id in ALLOWED_USER_IDS:
            otp_type = bot.otp_type
            otp_secret = OTP_SECRETS.get(otp_type)
            if otp_secret is None:
                await reaction.message.reply("OTP シークレットが見つかりません。")
                return

            totp = pyotp.TOTP(otp_secret)
            current_code = totp.now()
            current_timestamp = time.time()
            expiry_timestamp = current_timestamp + totp.interval - (current_timestamp % totp.interval)
            expiry_unix = int(expiry_timestamp)
            discord_timestamp = f"<t:{expiry_unix}:R>"

            await reaction.message.reply(f"再生成されたコード: {current_code}\nコードの有効期限: {discord_timestamp}")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))

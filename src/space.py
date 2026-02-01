import os
import dotenv
import discord
import shutil
from pathlib import Path

def main():
    disk_space = get_disk_space()
    print(f"Disk Space - Free: {disk_space['free']} bytes, Used: {disk_space['used']} bytes, Total: {disk_space['total']} bytes")

    # Notify if disk usage is above 50%
    if disk_space['used'] / disk_space['total'] > 0.5:
        notify_via_discord(disk_space)

# Get Linux Disk Space
def get_disk_space():
    total, used, free = shutil.disk_usage(Path.cwd())
    return {"free": free, "used": used, "total": total}

# Notify via Discord
def notify_via_discord(disk_space):
    dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")
    token = os.getenv("DISCORD_TOKEN")

    if not token:
        print("Discord token not found in environment variables (DISCORD_TOKEN).")
        return

    message = (f"Disk Space Alert!\n"
               f"Free: {disk_space['free']} bytes\n"
               f"Used: {disk_space['used']} bytes\n"
               f"Total: {disk_space['total']} bytes")
    
    # When notify via discord is called send a message in the channel #space-manager with the above message pinging the user 

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        channel_id = os.getenv("CHANNEL_ID")
        user_id = os.getenv("USER_ID")
        if not channel_id or not user_id:
            print("CHANNEL_ID or USER_ID not set in environment.")
            await client.close()
            return

        channel = await client.fetch_channel(int(channel_id))
        user = await client.fetch_user(int(user_id))
        message_with_mention = f"{user.mention}\n{message}"
        if channel:
            await channel.send(message_with_mention)
        await client.close()

    client.run(token)

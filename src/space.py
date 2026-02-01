import os
import dotenv
import discord

def main():
    disk_space = get_disk_space()
    print(f"Disk Space - Free: {disk_space['free']} bytes, Used: {disk_space['used']} bytes, Total: {disk_space['total']} bytes")

    # Notify if disk usage is below 50%
    if disk_space['used'] / disk_space['total'] < 0.5:
        notify_via_discord(disk_space)

# Get Linux Disk Space
def get_disk_space():
    st = os.statvfs("/")
    free = st.f_bavail * st.f_frsize
    total = st.f_blocks * st.f_frsize
    used = (st.f_blocks - st.f_bfree) * st.f_frsize
    return {"free": free, "used": used, "total": total}

# Notify via Discord
def notify_via_discord(disk_space):
    dotenv.load_dotenv(dotenv_path=".env")
    token = os.getenv("DISCORD_TOKEN") or os.getenv("PUBKEY")

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
        channel = client.get_channel(int(os.getenv("CHANNEL_ID")))  # Replace with your channel ID
        user = await client.fetch_user(int(os.getenv("USER_ID")))  # Replace with your user ID
        message_with_mention = f"{user.mention}\n{message}"
        if channel:
            await channel.send(message_with_mention)
        await client.close()

    client.run(token)

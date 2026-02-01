import os
import dotenv
import discord
import shutil
from pathlib import Path

def main():
    disk_space = get_disk_space()
    print(f"Disk Space - Free: {disk_space['free']} GB, Used: {disk_space['used']} GB, Total: {disk_space['total']} GB")

    # Notify every run
    notify_via_discord(disk_space)

# Get Linux Disk Space
def get_disk_space():
    total, used, free = shutil.disk_usage(Path.cwd())
    # Return free in gbs with 2 decimal places
    return {"free": round(free / (1024 ** 3), 2), "used": round(used / (1024 ** 3), 2), "total": round(total / (1024 ** 3), 2), "percentage_used": used / total}

# Notify via Discord
def notify_via_discord(disk_space):
    project_root = Path(__file__).resolve().parents[1]
    dotenv.load_dotenv(dotenv_path=project_root / ".env")
    dotenv.load_dotenv(dotenv_path=Path(__file__).resolve().parent / ".env")
    token = os.getenv("DISCORD_TOKEN")
    channel_id = os.getenv("CHANNEL_ID")
    user_id = os.getenv("USER_ID")

    print("Discord notify starting...")
    print(f"DISCORD_TOKEN set: {bool(token)}")
    print(f"CHANNEL_ID set: {bool(channel_id)}")
    print(f"USER_ID set: {bool(user_id)}")

    if not token:
        print("Discord token not found in environment variables (DISCORD_TOKEN).")
        return

    message = (f"Disk Space Alert!\n"
               f"Free: {disk_space['free']} GB\n"
                f"Used: {disk_space['used']} GB\n"
                f"Total: {disk_space['total']} GB\n"
                f"Percentage Used: {disk_space['percentage_used']*100:.2f}%")
    
    # When notify via discord is called send a message in the channel #space-manager with the above message pinging the user 

    intents = discord.Intents.default()
    client = discord.Client(intents=intents)
    
    @client.event
    async def on_ready():
        if not channel_id:
            print("CHANNEL_ID not set in environment.")
            await client.close()
            return

        channel = await client.fetch_channel(int(channel_id))
        message_with_mention = message
        if user_id:
            user = await client.fetch_user(int(user_id))
            message_with_mention = f"{user.mention}\n{message}"
        if channel:
            await channel.send(message_with_mention)
        await client.close()

    try:
        client.run(token)
    except discord.LoginFailure:
        print("Discord login failed. Check DISCORD_TOKEN is a valid bot token.")
    except discord.Forbidden as exc:
        print(f"Discord forbidden: {exc}")
    except discord.HTTPException as exc:
        print(f"Discord HTTP error: {exc}")


if __name__ == "__main__":
    main()

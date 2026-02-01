import os
import dotenv

def main():
    disk_space = get_disk_space()
    print(f"Disk Space - Free: {disk_space['free']} bytes, Used: {disk_space['used']} bytes, Total: {disk_space['total']} bytes")

    # If disk space is under 50% used, notify via Discord
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
    app_id = os.getenv("APPID")
    pub_key = os.getenv("PUBKEY")

    if not app_id or not pub_key:
        print("Discord APPID or PUBKEY not found in environment variables.")
        return

    message = (f"Disk Space Alert!\n"
               f"Free: {disk_space['free']} bytes\n"
               f"Used: {disk_space['used']} bytes\n"
               f"Total: {disk_space['total']} bytes")

    
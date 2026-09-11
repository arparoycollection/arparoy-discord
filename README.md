# Arpa Roy Plus — Discord Bot

A Discord bot that automatically posts links on a schedule, rotates activity status, welcomes new members, and auto-assigns roles.

## Features

- **Link Poster** — Posts links from `links.txt` to a channel every minute (configurable).
- **Status Rotation** — Rotates the bot's activity status every 2 minutes (configurable).
- **Welcome Announcer** — Sends a welcome message when a new member joins the server.
- **Auto-Role** — Automatically assigns a role to new members on join.

## Quick Start (5 Steps)

> **TL;DR** — Create a bot → Get the token → Enable intents → Invite to server → Deploy

1. **Create bot** → [Discord Developer Portal](https://discord.com/developers/applications/) → New Application → Bot tab → Reset Token → copy it
2. **Enable intents** → Bot tab → Privileged Gateway Intents → turn ON **Server Members Intent** → Save
3. **Invite bot** → OAuth2 tab → URL Generator → tick `bot` + `applications.commands` → tick **View Channels**, **Send Messages**, **Manage Roles** → open the URL → select your server
4. **Get IDs** → Discord Settings → Advanced → Developer Mode ON → right-click to copy Channel ID, Server ID, Role ID
5. **Deploy** → push to GitHub → [Railway](https://railway.app/) → New Project → Deploy from GitHub repo → add env vars → done

---

## 1. Create Your Bot on Discord Developer Portal

1. Go to **https://discord.com/developers/applications/**
2. Click **"New Application"** → give it a name → click **Create**.
3. Go to the **Bot** tab on the left sidebar.
4. Under the **Token** section, click **"Reset Token"** → copy the token.

> ⚠️ **Save your token somewhere safe.** You will only see it once. Never share it or commit it to GitHub.

---

## 2. Enable Privileged Intents

The bot uses the **Server Members** intent (for welcome messages and auto-role). You must enable it:

1. Stay on the **Bot** tab in the Developer Portal.
2. Scroll down to **Privileged Gateway Intents**.
3. Toggle **ON**:
   - ✅ **Presence Intent**
   - ✅ **Server Members Intent** *(required for welcome + auto-role)*
   - ✅ **Message Content Intent** *(required only if you add `!` commands)*
4. Click **Save Changes**.

---

## 3. Get the Bot Invite Link & Set Permissions

1. Go to the **OAuth2** tab on the left sidebar.
2. Under **OAuth2 URL Generator**, tick the **Scopes**:
   - ✅ `bot`
   - ✅ `applications.commands`
3. Under **Bot Permissions**, tick:
   - ✅ **View Channels** — so the bot can see your channels
   - ✅ **Send Messages** — so the bot can post links and welcome messages
   - ✅ **Manage Roles** — so the bot can auto-assign roles
4. Copy the generated URL at the bottom.
5. Open the URL in your browser and select your server to invite the bot.

> 💡 **Important — Role Hierarchy:** For auto-role to work, go to **Server Settings → Roles** and drag the bot's role **above** the role it needs to assign. A bot cannot assign roles that are higher than its own.

---

## 4. Get Your Server IDs

You need **Developer Mode** enabled in Discord to copy IDs:

1. Open Discord → **User Settings** → **Advanced** → toggle **Developer Mode** ON.

Then right-click to copy IDs:

| What to copy | How | Env var |
|---|---|---|
| **Channel ID** | Right-click the channel where links will be posted → Copy Channel ID | `CHANNEL_ID` |
| **Guild (Server) ID** | Right-click your server name → Copy Server ID | `GUILD_ID` |
| **Role ID** | Right-click the auto-role in Server Settings → Roles → Copy Role ID | `AUTO_ROLE_ID` |
| **Welcome Channel ID** | Right-click the welcome channel → Copy Channel ID *(optional, defaults to `CHANNEL_ID`)* | `WELCOME_CHANNEL_ID` |

---

## 5. Environment Variables

| Variable | Required | Default | Description |
|---|---|---|---|
| `DISCORD_TOKEN` | ✅ Yes | — | Your bot token from the Developer Portal |
| `CHANNEL_ID` | No | `1454248846208139324` | Channel where links are posted |
| `GUILD_ID` | No | `1313110086910218331` | Your server ID (for auto-role + welcome) |
| `AUTO_ROLE_ID` | No | `1427593128264601682` | Role to auto-assign on join |
| `WELCOME_CHANNEL_ID` | No | Same as `CHANNEL_ID` | Channel for welcome messages |
| `ENABLE_MEMBERS_INTENT` | No | `false` | Set to `true` to enable welcome + auto-role |
| `ENABLE_MESSAGE_CONTENT_INTENT` | No | `false` | Set to `true` to enable `!` commands |
| `LINKS_FILE` | No | `links.txt` | Path to your links file |
| `POST_INTERVAL_MINUTES` | No | `1` | Minutes between link posts |
| `STATUS_INTERVAL_MINUTES` | No | `2` | Minutes between status rotations |

---

## 6. Run Locally

### Prerequisites
- Python 3.10+
- pip

### Steps

```bash
# 1. Clone the repo
git clone <your-repo-url>
cd <repo-name>

# 2. Install dependencies
pip install -r requirements.txt

# 3. Set your environment variables
#    On Linux/Mac:
export DISCORD_TOKEN="your-bot-token"
export ENABLE_MEMBERS_INTENT="true"
export CHANNEL_ID="your-channel-id"
export GUILD_ID="your-guild-id"
export AUTO_ROLE_ID="your-role-id"

#    On Windows (PowerShell):
$env:DISCORD_TOKEN="your-bot-token"
$env:ENABLE_MEMBERS_INTENT="true"
$env:CHANNEL_ID="your-channel-id"
$env:GUILD_ID="your-guild-id"
$env:AUTO_ROLE_ID="your-role-id"

# 4. Run the bot
python bot.py
```

You should see:
```
INFO - bot: Bot online: YourBotName#1234 (ID: 123456789)
INFO - bot: Connected to 1 server(s)
INFO - bot: Started background tasks: link posting, status rotation
```

### Run with Docker

```bash
# Create a .env file with your variables
echo 'DISCORD_TOKEN=your-bot-token' > .env
echo 'ENABLE_MEMBERS_INTENT=true' >> .env

# Build and run
docker compose -f docker-compose.base44.yml up -d

# View logs
docker compose -f docker-compose.base44.yml logs -f bot

# Stop
docker compose -f docker-compose.base44.yml down
```

---

## 7. Deploy on Railway

Railway is a cloud platform that makes deploying bots easy.

### Step 1 — Push to GitHub
Make sure your code is pushed to a GitHub repository.

### Step 2 — Create a Railway Project
1. Go to **https://railway.app/** and sign in with GitHub.
2. Click **"New Project"** → **"Deploy from GitHub repo"**.
3. Select your repository.

### Step 3 — Configure the Service
Railway will auto-detect Python. Set the following:

1. Go to **Settings** → **Build**:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python bot.py`

2. Go to **Variables** → add all your environment variables:

   | Key | Value |
   |---|---|
   | `DISCORD_TOKEN` | your-bot-token |
   | `ENABLE_MEMBERS_INTENT` | `true` |
   | `CHANNEL_ID` | your-channel-id |
   | `GUILD_ID` | your-guild-id |
   | `AUTO_ROLE_ID` | your-role-id |
   | `WELCOME_CHANNEL_ID` | your-welcome-channel-id *(optional)* |

3. Railway auto-deploys when you push to GitHub. The bot will start automatically.

### Step 4 — Verify
Check the **Deployments** tab → **Logs**. You should see:
```
INFO - bot: Bot online: YourBotName#1234 (ID: ...)
INFO - bot: Connected to 1 server(s)
INFO - bot: Started background tasks: link posting, status rotation
INFO - bot: Loaded 15 links from links.txt
```

### Step 5 — Keep It Running 24/7
- Railway keeps your bot running continuously.
- The **free trial** includes limited hours. For always-on hosting, upgrade to the **Hobby plan** ($5/month).
- To prevent the bot from sleeping, go to **Settings → Deploy → Sleep** and disable it (Hobby plan required).

### Railway Env Var Quick Reference
```env
DISCORD_TOKEN=your-bot-token
ENABLE_MEMBERS_INTENT=true
CHANNEL_ID=your-channel-id
GUILD_ID=your-guild-id
AUTO_ROLE_ID=your-role-id
WELCOME_CHANNEL_ID=your-welcome-channel-id
```

---

## 8. Customize Links

Edit `links.txt` — one link per line. The bot reads this file every cycle, so changes are picked up automatically:

```
https://example.com/link1
https://example.com/link2
https://example.com/link3
```

---

## 9. Troubleshooting

| Problem | Fix |
|---|---|
| `DISCORD_TOKEN environment variable is not set` | Set the `DISCORD_TOKEN` env var |
| `requesting privileged intents that have not been explicitly enabled` | Enable **Server Members Intent** in the Developer Portal + set `ENABLE_MEMBERS_INTENT=true` |
| `Channel ... not found` | The bot isn't in the server, or the `CHANNEL_ID` is wrong |
| `Connected to 0 server(s)` | Invite the bot to your server using the OAuth2 URL (Step 3) |
| `Missing permissions to assign roles` | The bot's role must be **higher** than the auto-role in Server Settings → Roles |
| `Missing permissions to send messages` | Give the bot **Send Messages** permission in the channel settings |

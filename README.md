# Discord Bot with Gemini API

## Setup

### Download Source Code

```bash
git pull https://github.com/PinJhih/gemini-dc-bot.git
cd gemini-dc-bot
```

### Install Dependency

```bash
pip install -r requirements.txt
```

### Setup *.env* for Environment Variables

- Create a file named *.env*
    ```bash
    # for example, use the `touch` command
    touch .env
    ```
- Add your **Discord Bot Token** and **Gemini API Key** to the *.env* file:
    ```
    BOT_TOKEN=<Your Discord Bot Token>
    GEMINI_API_KEY=<Your Gemini API Key>
    ```
    - Visit [Discord Developer](https://discord.com/developers/applications) to get your Discord bot token
    - Visit [Google AI Studio](https://aistudio.google.com/app/apikey) to create a Gemini API Key

## Run

```
cd gemini-dc-bot
python bot.py
```

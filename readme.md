# Weekly Movie Recommendation Bot

This project uses Python to fetch recent comments about movies from Reddit, analyze them with the Google Gemini LLM, and send a curated weekly recommendation to a Telegram chat.

## Architecture

The process flow is simple:

1. A scheduler (like cron) triggers the Python script once a week.

2. The script connects to the Reddit API using `praw` to pull recent comments from specified movie-related subreddits.

3. All comments are compiled into a single text block and sent to the Gemini API with a carefully crafted prompt.

4. Gemini analyzes the text and returns a formatted "Weekly Movie Buzz" report in Markdown.

5. The script sends this report to a specified Telegram chat via a Telegram Bot.

## 🚀 Step 1: Prerequisites & Setup

### 1. Get API Keys

You need credentials for three services. This is the most important step.

* **Reddit API:**

  1. Go to <https://www.reddit.com/prefs/apps>.

  2. Scroll down and click "**are you a developer? create an app...**".

  3. Fill it out:

     * **name:** WeeklyMovieBot

     * **type:** select `script`

     * **redirect uri:** `http://localhost:8080` (this won't be used, but is required)

  4. Click `create app`. You will get a **client ID** (under the app name) and a **client secret**.

* **Google Gemini API:**

  1. Go to [Google AI Studio](https://aistudio.google.com/app/apikey).

  2. Click "**Create API key in new project**".

  3. Copy the generated API key.

* **Telegram Bot:**

  1. Open Telegram and search for the user `BotFather`.

  2. Start a chat and send the `/newbot` command.

  3. Follow the prompts to name your bot. BotFather will give you a **Bot Token**.

  4. To get your **Chat ID**, send a message to your new bot. Then, visit the following URL in your browser (replacing `<YourBOT_TOKEN>`): `https://api.telegram.org/bot<YourBOT_TOKEN>/getUpdates`. You will see a JSON response. Find the `chat` object and copy the `id` value.

### 2. Prepare Your Project

1. Clone or download the files.

2. Rename `.env.example` to `.env`.

3. Open the new `.env` file and paste in all the API keys you just collected. Remember to update the `REDDIT_USER_AGENT` to include your Reddit username.

4. Create a Python virtual environment (recommended):

```

python -m venv venv
source venv/bin/activate  \# On Windows, use `venv\Scripts\activate`

```

5. Install the required libraries:

```

pip install -r requirements.txt

```

## 🏃‍♂️ Step 2: Running the Bot

### Manual Run

To test if everything is working, you can run the script directly from your terminal:

```

python movie\_recommender\_bot.py

```

Check your Telegram chat. You should receive the movie recommendation message!

## 🤖 Step 3: Automating with Cron

To make this a true "weekly" bot, you need to schedule the script to run automatically. On Linux or macOS, you can use `cron`.

1. Open your crontab file for editing:

```

crontab -e

```

2. Add a line to schedule the script. This example runs the bot every Friday at 6:00 PM (18:00):

```

# At 6:00 PM on Friday, run the movie recommender bot

0 18 \* \* 5 /usr/bin/python3 /path/to/your/project/movie\_recommender\_bot.py \>\> /path/to/your/project/cron.log 2\>&1

```

**Important:**

* Replace `/path/to/your/project/` with the **absolute path** to where you saved the files.

* `>> /path/to/your/project/cron.log 2>&1` will save the output and any errors to a log file, which is very helpful for debugging.

3. Save and close the file. Your bot is now fully automated!

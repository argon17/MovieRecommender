# Weekly Movie Recommendation Bot

This project uses Python to fetch recent comments about movies from Reddit, analyze them with the Google Gemini LLM, and send a curated weekly recommendation to a Telegram chat. The bot is built with modern async/await patterns for efficient API interactions.

## Project Structure

```
MovieRecommender/
├── .github/
│   └── workflows/
│       └── pylint.yml          # GitHub Actions workflow for code quality
├── src/
│   ├── __init__.py
│   ├── services/
│   │   ├── __init__.py
│   │   ├── reddit_service.py   # Async Reddit API client
│   │   ├── llm_service.py      # Google Gemini LLM integration
│   │   └── telegram_service.py # Telegram bot messaging
│   ├── bot/
│   │   ├── __init__.py
│   │   └── movie_bot.py        # Main bot orchestration logic
│   └── config/
│       ├── __init__.py
│       └── settings.py         # Configuration and environment variables
├── .pylintrc                   # Pylint configuration
├── .gitignore                  # Git ignore patterns
├── main.py                     # Application entry point
├── requirements.txt            # Python dependencies
├── LICENSE                     # MIT License
└── .env                        # Environment variables (create this file)
```

## Architecture

The bot follows an async, service-oriented architecture:

1. **Scheduled Execution**: A scheduler (cron, GitHub Actions, etc.) triggers the script weekly
2. **Reddit Data Collection**: Uses `asyncpraw` to asynchronously fetch recent comments from movie-related subreddits
3. **LLM Analysis**: Sends compiled comments to Google Gemini API with a specialized prompt for movie recommendations
4. **Content Generation**: Gemini returns a formatted "Weekly Movie Buzz" report in Markdown
5. **Telegram Delivery**: The report is sent to a specified Telegram chat via the bot API

### Key Features
- **Asynchronous Operations**: All API calls are non-blocking for better performance
- **Error Handling**: Comprehensive error handling with proper logging
- **Code Quality**: Automated code quality checks with Pylint (target score: 9.0+)
- **Configuration Management**: Environment-based configuration with validation

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

1. Clone the repository:
   ```bash
   git clone https://github.com/argon17/MovieRecommender.git
   cd MovieRecommender
   ```

2. Create a `.env` file in the root directory with the following content:
   ```
   # Reddit API Credentials
   REDDIT_CLIENT_ID=your_client_id
   REDDIT_CLIENT_SECRET=your_client_secret
   REDDIT_USER_AGENT=script:WeeklyMovieBot:v1.0 (by /u/your_username)

   # Google Gemini API
   GEMINI_API_KEY=your_gemini_api_key

   # Telegram Bot
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

3. Create a Python virtual environment (recommended):
   ```bash
   python -m venv venv
   # On Windows:
   venv\Scripts\activate
   # On Linux/macOS:
   source venv/bin/activate
   ```

4. Install the required libraries:
   ```bash
   pip install -r requirements.txt
   ```

## 🏃‍♂️ Step 2: Running the Bot

### Manual Run

To test if everything is working, you can run the script directly from your terminal:

```bash
python main.py
```

Check your Telegram chat. You should receive the movie recommendation message!

### Development Mode

For development and testing, you can run the bot with more verbose logging by setting the log level in your environment or modifying the settings.

## 🤖 Step 3: Automating with Cron

To make this a true "weekly" bot, you can schedule the script to run automatically. On Linux or macOS, you can use `cron`.

To schedule the bot, follow these steps:

1. Open your crontab file for editing:
   ```bash
   crontab -e
   ```

2. Add a line to schedule the script. This example runs the bot every Sunday at 9:00 AM:
   ```bash
   # Weekly Movie Recommendations - Every Sunday at 9 AM
   0 9 * * 0 cd /path/to/MovieRecommender && /path/to/MovieRecommender/venv/bin/python main.py >> /path/to/MovieRecommender/logs/cron.log 2>&1
   ```

**Important:**
* Replace `/path/to/MovieRecommender` with the absolute path to your project directory
* The command uses the Python interpreter from your virtual environment to ensure all dependencies are available
* Output and errors will be logged to `logs/cron.log` for debugging

3. Save and close the file. Your bot is now automated!

### Alternative: GitHub Actions

You can also use GitHub Actions to run the bot on a schedule. The repository includes a Pylint workflow for code quality checks. You can extend this to include scheduled bot runs.

## 🧪 Development

### Code Quality

This project uses Pylint for code quality assurance with a target score of 9.0 or higher. The GitHub Actions workflow automatically runs Pylint on every push and pull request.

To run Pylint locally:
```bash
pylint --rcfile=.pylintrc src/ main.py
```

### Dependencies

- `asyncpraw`: Async Python Reddit API Wrapper
- `google-generativeai`: Google Gemini AI API client
- `python-telegram-bot`: Telegram Bot API wrapper
- `python-dotenv`: Environment variable management

### GitHub Actions Artifacts

The Pylint workflow generates reports that are uploaded as artifacts. You can download these reports from the Actions tab in your GitHub repository to review code quality metrics and suggestions.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and ensure they pass Pylint checks
4. Commit your changes (`git commit -m 'Add some amazing feature'`)
5. Push to the branch (`git push origin feature/amazing-feature`)
6. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

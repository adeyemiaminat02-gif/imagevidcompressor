# 🗜️ ImageVidCompressorBot

A production-grade Telegram Bot architecture constructed using Python 3.12 and the python-telegram-bot wrapper framework to execute multi-pass optimization matrix updates against structural heavy image media layers and processing video codecs safely.

## 🚀 Deployment Instructions

### Method 1: Deploying to Render
1. Create a Fork of this codebase infrastructure into your personal GitHub Account.
2. Log into your dashboard portal on **Render.com** and connect a new **Web Service**.
3. Point it to your newly created GitHub Repository fork workspace.
4. Render will automatically parse configuration parameters from `render.yaml` to configure dependencies and trigger the deployment pipeline setup. Ensure you add your production credentials inside the environment variable settings dashboard panel:
   * `BOT_TOKEN`: The Token returned from your account conversations with `@BotFather`.

### Method 2: Local Machine Verification
Ensure you have native hardware system distributions of `ffmpeg` configured on your path.
```bash
# Clone the repository
git clone [https://github.com/YOUR_USERNAME/ImageVidCompressorBot.git](https://github.com/YOUR_USERNAME/ImageVidCompressorBot.git)
cd ImageVidCompressorBot

# Build environment spaces
python3 -m venv venv
source venv/bin/activate

# Install requirements
pip install -r requirements.txt

# Create .env and inject your variables
cp .env.example .env
nano .env

# Run system loops
python app.py

# Simple Guide for Non-Developers 🎯

**Don't worry - this is easier than it looks!** Just follow these steps exactly.

## What You Need (5 minutes to get these):

1. **Airtable API Key** - Like a password for your Airtable
2. **Airtable Base ID** - The ID of your spreadsheet
3. **OpenAI API Key** - Like a password for ChatGPT
4. **Table Name** - The name of your table in Airtable (probably "Leads")

---

## Step 1: Get Your Airtable API Key (2 minutes)

1. Go to this website: https://airtable.com/create/tokens
2. Click the blue button "Create new token"
3. Give it a name: `Icebreaker Generator`
4. Click "Add a scope" and select:
   - ✅ `data.records:read`
   - ✅ `data.records:write`
5. Click "Add a base" and select your base
6. Click "Create token"
7. **COPY THE TOKEN** (it starts with `pat`) - you'll need it!

**Your API Key looks like:** `patAbCdEf123456789XyZ...`

---

## Step 2: Get Your Airtable Base ID (1 minute)

1. Open your Airtable base in your web browser
2. Look at the URL at the top. It looks like:
   ```
   https://airtable.com/appXXXXXXXXXXXXXX/tblYYYYYYYYYYYYYY
   ```
3. Copy the part that starts with `app` (everything between `airtable.com/` and the next `/`)

**Your Base ID looks like:** `appAbCdEf12345678`

---

## Step 3: Get Your OpenAI API Key (2 minutes)

1. Go to: https://platform.openai.com/api-keys
2. Log in (or create an account if you don't have one)
3. Click "Create new secret key"
4. Give it a name: `Icebreaker Generator`
5. **COPY THE KEY** (it starts with `sk-`) - you'll only see it once!
6. **Add $5-10 in credits** to your OpenAI account (Settings > Billing)

**Your API Key looks like:** `sk-AbCdEf123456789XyZ...`

---

## Step 4: Check Your Airtable Table

Make sure your Airtable has these columns (exact names):

- `Firstname` - Lead's first name
- `Company` - Company name
- `Website` - Company website (like `example.com`)
- `Role` - Their job title (optional)
- `Icebreaker` - Leave this empty (the script will fill it)

**If your columns have different names, rename them to match these exactly!**

---

## Step 5: Copy-Paste Your Settings (2 minutes)

You'll need to create a file called `.env` with your information.

**Don't panic!** Here's exactly what to do:

### Option A: If you're on this server/computer

1. Type this command and press Enter:
   ```bash
   cd ai-icebreaker-generator
   nano .env
   ```

2. Copy-paste this template:
   ```
   AIRTABLE_API_KEY=patYOUR_KEY_HERE
   AIRTABLE_BASE_ID=appYOUR_BASE_ID_HERE
   AIRTABLE_TABLE_NAME=Leads
   OPENAI_API_KEY=sk-YOUR_KEY_HERE
   MAX_CONCURRENT=10
   ICEBREAKER_FIELD_NAME=Icebreaker
   ```

3. Replace the parts that say `YOUR_KEY_HERE` with your actual keys

4. Press `Ctrl + X`, then `Y`, then `Enter` to save

### Option B: If you're on a different computer

1. Download the `.env.example` file
2. Rename it to `.env`
3. Open it with Notepad (Windows) or TextEdit (Mac)
4. Replace the example values with your real keys
5. Save it
6. Upload it back to the `ai-icebreaker-generator` folder

---

## Step 6: Run the Magic! ✨

Now the easy part! Just type these commands:

```bash
# Go to the right folder
cd ai-icebreaker-generator

# Run the setup (only need to do this once)
./setup.sh

# Run the generator!
python icebreaker_generator.py
```

**That's it!** You'll see messages like:
```
INFO - Fetching records from Airtable...
INFO - Found 10 records to process
INFO - Processing Marie at TechCorp
INFO - ✓ Generated summary for TechCorp
INFO - ✓ Generated icebreaker for Marie
```

---

## What If Something Goes Wrong? 🆘

### Error: "Missing required environment variables"
👉 You forgot to create the `.env` file or didn't fill in all the keys

### Error: "Failed to fetch" or "401 Unauthorized"
👉 Your API keys are wrong. Double-check you copied them correctly

### Error: "Missing required fields"
👉 Your Airtable columns don't match the names above. Rename them!

### Error: "No module named 'aiohttp'" or similar
👉 You forgot to run `./setup.sh` first

---

## Need Help?

If you're stuck:

1. **Check the logs** - they tell you exactly what went wrong
2. **Re-read the error message** - it usually tells you what to fix
3. **Ask for help** - Share the error message with someone who can help

---

## How Much Will This Cost?

**Very cheap!** With OpenAI:
- 10 icebreakers: ~$0.02-$0.04 (basically free)
- 100 icebreakers: ~$0.20-$0.40 (less than a coffee)
- 1000 icebreakers: ~$2-$4 (less than a sandwich)

---

## Want to Run It Again?

Easy! Just do:

```bash
cd ai-icebreaker-generator
source venv/bin/activate
python icebreaker_generator.py
```

---

**You got this! 🚀**

Remember: The computer is following YOUR instructions. If something doesn't work, it's not your fault - just try again or ask for help!

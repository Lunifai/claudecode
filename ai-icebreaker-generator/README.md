# AI Icebreaker Generator for Airtable

A high-performance Python script that generates personalized French icebreakers for cold email campaigns. **10x faster than n8n** by processing records in parallel instead of one-by-one.

## 🚀 Key Features

- **Parallel Processing**: Processes 10+ records simultaneously (configurable)
- **Smart Website Analysis**: HTML → Markdown → Summary → Icebreaker pipeline
- **OpenAI Integration**: Generates authentic, personalized French icebreakers
- **Airtable Sync**: Seamlessly reads and writes to your Airtable base
- **Batch Processing**: Handles large datasets efficiently
- **Error Handling**: Robust error handling and detailed logging
- **Fast**: Processes 100 records in ~2-3 minutes (vs 15-20 minutes with n8n)

## 🔄 How It Works

The generator follows a sophisticated 4-step pipeline for each lead:

```
1. 🌐 Fetch Website HTML
   ↓ Makes HTTP request to the company website

2. 📄 Convert to Markdown
   ↓ Transforms HTML into clean, structured markdown
   ↓ Removes navigation, scripts, and non-content elements

3. 🤖 AI Summarization
   ↓ Uses OpenAI to create a 3-4 sentence summary
   ↓ Extracts: company activity, mission/values, differentiators

4. ✍️ Generate Icebreaker
   ✓ Creates personalized 2-line French icebreaker
   ✓ Based on real insights from the company website
```

This approach ensures icebreakers are:
- **Specific**: Based on actual company information
- **Relevant**: Focused on key differentiators
- **Authentic**: Shows genuine research
- **Effective**: Optimized for cold email engagement

## 📋 Prerequisites

- Python 3.8 or higher
- Airtable account with API access
- OpenAI API key
- Airtable base with the following fields:
  - `Firstname`: Lead's first name
  - `Company`: Company name
  - `Role`: Lead's role/position (optional)
  - `Website`: Company website URL
  - `Icebreaker`: Field where generated icebreakers will be stored (will be created if doesn't exist)

## 🔧 Installation

### 1. Clone or Download

```bash
cd ai-icebreaker-generator
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

```bash
cp .env.example .env
```

Edit `.env` with your credentials:

```env
# Get from: https://airtable.com/create/tokens
AIRTABLE_API_KEY=patXXXXXXXXXXXXXX

# Get from your Airtable base URL: https://airtable.com/appXXXXXXXXXXXXXX/...
AIRTABLE_BASE_ID=appXXXXXXXXXXXXXX

# Your table name in Airtable
AIRTABLE_TABLE_NAME=Leads

# Get from: https://platform.openai.com/api-keys
OPENAI_API_KEY=sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# How many records to process simultaneously (10 is a good balance)
MAX_CONCURRENT=10

# The field name in Airtable where icebreakers will be stored
ICEBREAKER_FIELD_NAME=Icebreaker
```

## 📖 How to Get Your API Keys

### Airtable API Key

1. Go to https://airtable.com/create/tokens
2. Click "Create new token"
3. Give it a name: "Icebreaker Generator"
4. Add these scopes:
   - `data.records:read`
   - `data.records:write`
5. Add access to your base
6. Click "Create token"
7. Copy the token (starts with `pat`)

### Airtable Base ID

1. Open your Airtable base in browser
2. Look at the URL: `https://airtable.com/appXXXXXXXXXXXXXX/...`
3. The part after `airtable.com/` starting with `app` is your Base ID

### OpenAI API Key

1. Go to https://platform.openai.com/api-keys
2. Click "Create new secret key"
3. Copy the key (starts with `sk-`)
4. Add credits to your account if needed

## 🎯 Usage

### Basic Usage

```bash
python icebreaker_generator.py
```

This will:
1. Fetch all records from Airtable where the `Icebreaker` field is empty
2. For each record, follow the pipeline:
   - Fetch the company website HTML
   - Convert HTML to clean Markdown
   - Generate an AI summary of the company
   - Create a personalized French icebreaker
3. Update Airtable with the generated icebreakers

### Expected Output

```
2024-11-25 10:30:15 - INFO - Fetching records from Airtable...
2024-11-25 10:30:16 - INFO - Found 45 records to process
2024-11-25 10:30:16 - INFO - Processing batch 1 (45 records)...
2024-11-25 10:30:17 - INFO - Processing Marie at TechCorp
2024-11-25 10:30:17 - INFO - Processing Jean at InnovSolutions
2024-11-25 10:30:20 - INFO - ✓ Generated summary for TechCorp
2024-11-25 10:30:21 - INFO - ✓ Generated summary for InnovSolutions
...
2024-11-25 10:30:45 - INFO - ✓ Generated icebreaker for Marie
2024-11-25 10:30:46 - INFO - ✓ Generated icebreaker for Jean
...
2024-11-25 10:32:30 - INFO - Updating Airtable with results...
2024-11-25 10:32:35 - INFO - ✓ Successfully updated 45/45 records
2024-11-25 10:32:35 - INFO - ✓ Completed in 139.23 seconds
2024-11-25 10:32:35 - INFO - Average: 3.09 seconds per record
```

## 📊 Example Output

For a lead named "Mathieu" at "Caprionis" (a circular economy company):

```
Bonjour Mathieu,

J'aime beaucoup l'engagement de Caprionis pour soutenir la transition vers une économie circulaire. Ça fait plaisir de voir votre initiative pour valoriser le réemploi et réduire les déchets dans le secteur du BTP.
```

## ⚙️ Advanced Configuration

### Process Specific Records

To process only specific records, you can modify the script to use a custom filter formula:

```python
# Edit the main() function to add a filter
await generator.run(filter_formula="AND({Icebreaker} = '', {Company} = 'TechCorp')")
```

### Adjust Concurrent Processing

More concurrent requests = faster processing but higher API costs:

```env
# Conservative (slower, cheaper)
MAX_CONCURRENT=5

# Balanced (recommended)
MAX_CONCURRENT=10

# Aggressive (faster, more expensive)
MAX_CONCURRENT=20
```

### Change Batch Size

Process records in smaller or larger batches:

```python
await generator.run(batch_size=25)  # Process 25 records at a time
```

## 💰 Cost Estimation

Based on OpenAI pricing (GPT-4o-mini):

Each lead requires 2 API calls:
1. **Website Summarization**: ~$0.001 - $0.002 per call
2. **Icebreaker Generation**: ~$0.001 - $0.002 per call

**Total costs:**
- **Per icebreaker**: ~$0.002 - $0.004
- **100 icebreakers**: ~$0.20 - $0.40
- **1000 icebreakers**: ~$2 - $4

Airtable API is free for reasonable usage.

**Note:** Actual costs may vary based on website content length. The pipeline is optimized to use GPT-4o-mini (the most cost-effective model) for both summarization and generation.

## 🔍 Troubleshooting

### "Missing required fields" warning

Make sure your Airtable has these exact field names:
- `Firstname`
- `Company`
- `Website`
- `Icebreaker`

### "Failed to fetch website" warning

Some websites block scrapers. The script will still generate an icebreaker based on company name and role.

### Rate Limiting

If you hit OpenAI rate limits:
1. Reduce `MAX_CONCURRENT` in `.env`
2. Add delays between batches

### Import Errors

Make sure you've activated the virtual environment:
```bash
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

## 🆚 Comparison with n8n

| Feature | This Script | n8n Workflow |
|---------|-------------|--------------|
| Processing | Parallel (10+ at once) | Sequential (one by one) |
| Speed | 100 records in ~2-3 min | 100 records in ~15-20 min |
| Setup | 5 minutes | 30+ minutes |
| Customization | Easy (Python code) | Limited (node config) |
| Error Handling | Robust | Basic |
| Logging | Detailed | Limited |

## 🚀 Performance Tips

1. **Optimize Concurrent Requests**: Start with 10, increase if no rate limiting
2. **Batch Processing**: Use reasonable batch sizes (50-100 records)
3. **Website Scraping**: Consider using a dedicated service like Perplexity API for better company context
4. **Caching**: Add caching for frequently accessed websites

## 🔄 Integrating with Perplexity (Optional)

For even better company context, you can replace website scraping with Perplexity API:

1. Get Perplexity API key from https://www.perplexity.ai/
2. Modify the `scrape_website()` method to use Perplexity instead

## 📝 Customizing the Prompt

To change the icebreaker style, edit the `generate_icebreaker()` method in `icebreaker_generator.py`:

```python
prompt = f"""Your custom prompt here...
Make it more casual/formal/specific to your needs
"""
```

## 🤝 Contributing

Feel free to:
- Report bugs
- Suggest features
- Submit pull requests
- Share your results

## 📄 License

This project is open source and available for personal and commercial use.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Verify your API keys and configuration
3. Check the logs for detailed error messages
4. Review Airtable field names

## 🎉 Success Tips

1. **Start Small**: Test with 5-10 records first
2. **Review Output**: Check a few generated icebreakers before processing all records
3. **Iterate**: Adjust the prompt based on results
4. **Monitor Costs**: Keep an eye on OpenAI usage
5. **Backup Data**: Export your Airtable before first run

---

**Built for speed. Optimized for results. Made for cold email success. 🚀**

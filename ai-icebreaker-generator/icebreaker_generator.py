#!/usr/bin/env python3
"""
AI Icebreaker Generator for Airtable
Generates personalized French icebreakers for cold email campaigns
Processes records in parallel for maximum speed
"""

import os
import asyncio
import aiohttp
from typing import List, Dict, Optional
from dataclasses import dataclass
from pyairtable import Api
from openai import AsyncOpenAI
from bs4 import BeautifulSoup
import logging
from datetime import datetime
import time
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


@dataclass
class LeadRecord:
    """Represents a lead record from Airtable"""
    record_id: str
    firstname: str
    company: str
    role: str
    website_url: str


class IcebreakerGenerator:
    """Main class for generating AI icebreakers"""

    def __init__(
        self,
        airtable_api_key: str,
        airtable_base_id: str,
        airtable_table_name: str,
        openai_api_key: str,
        max_concurrent: int = 10,
        icebreaker_field_name: str = "Icebreaker"
    ):
        self.airtable = Api(airtable_api_key)
        self.table = self.airtable.table(airtable_base_id, airtable_table_name)
        self.openai_client = AsyncOpenAI(api_key=openai_api_key)
        self.max_concurrent = max_concurrent
        self.icebreaker_field_name = icebreaker_field_name
        self.semaphore = asyncio.Semaphore(max_concurrent)

    def fetch_records(self, filter_formula: Optional[str] = None) -> List[LeadRecord]:
        """Fetch records from Airtable that need icebreakers"""
        logger.info("Fetching records from Airtable...")

        # By default, only fetch records without icebreakers
        if filter_formula is None:
            filter_formula = f"{{{self.icebreaker_field_name}}} = ''"

        records = self.table.all(formula=filter_formula)

        lead_records = []
        for record in records:
            fields = record['fields']

            # Skip if required fields are missing
            if not all(k in fields for k in ['Firstname', 'Company', 'Website']):
                logger.warning(f"Skipping record {record['id']} - missing required fields")
                continue

            lead_records.append(LeadRecord(
                record_id=record['id'],
                firstname=fields.get('Firstname', ''),
                company=fields.get('Company', ''),
                role=fields.get('Role', ''),
                website_url=fields.get('Website', '')
            ))

        logger.info(f"Found {len(lead_records)} records to process")
        return lead_records

    async def scrape_website(self, url: str, session: aiohttp.ClientSession) -> str:
        """Scrape website to get company description"""
        try:
            # Ensure URL has protocol
            if not url.startswith('http'):
                url = f'https://{url}'

            async with session.get(
                url,
                timeout=aiohttp.ClientTimeout(total=10),
                headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
            ) as response:
                if response.status != 200:
                    logger.warning(f"Failed to fetch {url}: status {response.status}")
                    return ""

                html = await response.text()
                soup = BeautifulSoup(html, 'html.parser')

                # Remove script and style elements
                for script in soup(["script", "style"]):
                    script.decompose()

                # Get text content
                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)

                # Get meta description if available
                meta_desc = soup.find('meta', attrs={'name': 'description'})
                if meta_desc and meta_desc.get('content'):
                    return meta_desc['content'] + " " + text[:500]

                # Return first 1000 characters
                return text[:1000]

        except Exception as e:
            logger.warning(f"Error scraping {url}: {str(e)}")
            return ""

    async def generate_icebreaker(
        self,
        firstname: str,
        company: str,
        role: str,
        company_context: str
    ) -> str:
        """Generate a personalized French icebreaker using OpenAI"""

        prompt = f"""Tu es un expert en rédaction d'emails de prospection B2B en français.

Génère un icebreaker personnalisé de 2 lignes maximum pour un email de prospection, en te basant sur les informations suivantes:

- Prénom du lead: {firstname}
- Entreprise: {company}
- Poste: {role}
- Contexte de l'entreprise: {company_context}

L'icebreaker doit:
1. Commencer par "Bonjour {firstname},"
2. Faire référence à quelque chose de spécifique et positif sur l'entreprise
3. Être authentique et engageant
4. Faire 2 lignes maximum (après le "Bonjour")
5. Être en français professionnel mais chaleureux

Exemple de format:
Bonjour Mathieu,

J'aime beaucoup l'engagement de Caprionis pour soutenir la transition vers une économie circulaire. Ça fait plaisir de voir votre initiative pour valoriser le réemploi et réduire les déchets dans le secteur du BTP.

Ne génère que l'icebreaker, sans autre texte."""

        try:
            response = await self.openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Faster and cheaper for this task
                messages=[
                    {"role": "system", "content": "Tu es un expert en cold email B2B en français."},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.8,
                max_tokens=200
            )

            icebreaker = response.choices[0].message.content.strip()
            return icebreaker

        except Exception as e:
            logger.error(f"Error generating icebreaker for {firstname} at {company}: {str(e)}")
            return ""

    async def process_record(
        self,
        lead: LeadRecord,
        session: aiohttp.ClientSession
    ) -> Dict:
        """Process a single record: scrape website and generate icebreaker"""
        async with self.semaphore:  # Limit concurrent requests
            try:
                logger.info(f"Processing {lead.firstname} at {lead.company}")

                # Scrape website for context
                company_context = await self.scrape_website(lead.website_url, session)

                if not company_context:
                    company_context = f"{lead.company} - {lead.role}"

                # Generate icebreaker
                icebreaker = await self.generate_icebreaker(
                    lead.firstname,
                    lead.company,
                    lead.role,
                    company_context
                )

                if icebreaker:
                    logger.info(f"✓ Generated icebreaker for {lead.firstname}")
                    return {
                        'record_id': lead.record_id,
                        'icebreaker': icebreaker,
                        'success': True
                    }
                else:
                    logger.warning(f"✗ Failed to generate icebreaker for {lead.firstname}")
                    return {
                        'record_id': lead.record_id,
                        'success': False
                    }

            except Exception as e:
                logger.error(f"Error processing {lead.firstname}: {str(e)}")
                return {
                    'record_id': lead.record_id,
                    'success': False,
                    'error': str(e)
                }

    async def process_batch(self, leads: List[LeadRecord]) -> List[Dict]:
        """Process multiple records in parallel"""
        async with aiohttp.ClientSession() as session:
            tasks = [self.process_record(lead, session) for lead in leads]
            results = await asyncio.gather(*tasks)
            return results

    def update_airtable(self, results: List[Dict]):
        """Update Airtable with generated icebreakers"""
        logger.info("Updating Airtable with results...")

        successful = 0
        for result in results:
            if result.get('success') and result.get('icebreaker'):
                try:
                    self.table.update(
                        result['record_id'],
                        {self.icebreaker_field_name: result['icebreaker']}
                    )
                    successful += 1
                except Exception as e:
                    logger.error(f"Error updating record {result['record_id']}: {str(e)}")

        logger.info(f"✓ Successfully updated {successful}/{len(results)} records")

    async def run(self, filter_formula: Optional[str] = None, batch_size: int = 50):
        """Main execution method"""
        start_time = time.time()

        # Fetch records
        leads = self.fetch_records(filter_formula)

        if not leads:
            logger.info("No records to process")
            return

        # Process in batches
        total_processed = 0
        for i in range(0, len(leads), batch_size):
            batch = leads[i:i + batch_size]
            logger.info(f"Processing batch {i//batch_size + 1} ({len(batch)} records)...")

            results = await self.process_batch(batch)
            self.update_airtable(results)

            total_processed += len(batch)
            logger.info(f"Progress: {total_processed}/{len(leads)} records processed")

        elapsed_time = time.time() - start_time
        logger.info(f"✓ Completed in {elapsed_time:.2f} seconds")
        logger.info(f"Average: {elapsed_time/len(leads):.2f} seconds per record")


async def main():
    """Main entry point"""

    # Load configuration from environment variables
    AIRTABLE_API_KEY = os.getenv('AIRTABLE_API_KEY')
    AIRTABLE_BASE_ID = os.getenv('AIRTABLE_BASE_ID')
    AIRTABLE_TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME', 'Leads')
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
    MAX_CONCURRENT = int(os.getenv('MAX_CONCURRENT', '10'))
    ICEBREAKER_FIELD_NAME = os.getenv('ICEBREAKER_FIELD_NAME', 'Icebreaker')

    # Validate required environment variables
    if not all([AIRTABLE_API_KEY, AIRTABLE_BASE_ID, OPENAI_API_KEY]):
        raise ValueError(
            "Missing required environment variables. Please set:\n"
            "- AIRTABLE_API_KEY\n"
            "- AIRTABLE_BASE_ID\n"
            "- OPENAI_API_KEY"
        )

    # Initialize generator
    generator = IcebreakerGenerator(
        airtable_api_key=AIRTABLE_API_KEY,
        airtable_base_id=AIRTABLE_BASE_ID,
        airtable_table_name=AIRTABLE_TABLE_NAME,
        openai_api_key=OPENAI_API_KEY,
        max_concurrent=MAX_CONCURRENT,
        icebreaker_field_name=ICEBREAKER_FIELD_NAME
    )

    # Run the generator
    await generator.run()


if __name__ == "__main__":
    asyncio.run(main())

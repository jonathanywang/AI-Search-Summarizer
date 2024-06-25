import openai
from exa_py import Exa
import os
from datetime import datetime, timedelta
import textwrap


EXA_API_KEY = os.environ.get('000') # Exa API Key here
OPENAI_API_KEY = os.environ.get('000') # OpenAI API Key here

openai.api_key = OPENAI_API_KEY
openai.api_type = "openai"
exa = Exa(EXA_API_KEY)

SYSTEM_MESSAGE = "You are a helpful assistant that generates search queries based on user questions. Only generate one search query."
USER_QUESTION = "What's the recent news in physics this week?"

completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": USER_QUESTION},
    ],
)

search_query = completion.choices[0].message.content

one_week_ago = (datetime.now() - timedelta(days=7))
date_cutoff = one_week_ago.strftime("%Y-%m-%d")

search_response = exa.search_and_contents(
    search_query, use_autoprompt=True, start_published_date=date_cutoff
)

urls = [result.url for result in search_response.results]

results = search_response.results
result_item = results[0]


completion = openai.chat.completions.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": SYSTEM_MESSAGE},
        {"role": "user", "content": result_item.text},
    ],
)

summary = completion.choices[0].message.content

print(f"Summary for {urls[0]}:")
print(result_item.title)
print(textwrap.fill(summary, 80))
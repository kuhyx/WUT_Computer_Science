from openai import OpenAI


def rate_similarity(c1:list, c2:list) -> str:
    client = OpenAI(api_key='REDACTED_OPENAI_API_KEY')

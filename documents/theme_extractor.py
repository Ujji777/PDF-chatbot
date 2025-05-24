import os
from groq import Groq

def extract_themes_from_chunks(chunks):
    context = "\n\n".join([doc.page_content for doc in chunks])
    prompt = f"""
You are a legal research assistant. Based on the following text chunks, identify 3 to 5 key legal or regulatory themes.

Context:
{context}

Return the themes as a simple bullet list. Do not include explanations.
"""

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

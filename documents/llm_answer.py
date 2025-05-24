import os
from groq import Groq

def synthesize_answer(question, matches):
    context = "\n\n".join([doc.page_content for doc in matches])
    prompt = f"""Answer the following question based only on the context below.

Context:
{context}

Question: {question}
Answer:"""

    client = Groq(api_key=os.getenv("GROQ_API_KEY"))
    response = client.chat.completions.create(
        model="llama3-8b-8192",
        messages=[
            {"role": "system", "content": "You are a helpful AI trained to extract legal answers from document context."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content.strip()

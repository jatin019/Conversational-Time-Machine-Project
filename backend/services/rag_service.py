from utils.vector_store import load_vector_store
from utils.prompt_templates import get_persona_prompt
from groq import Groq
import os

# Initialized the Groq 
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def get_persona_response(persona: str, question: str) -> str:

    # To load the FAISS index for the selected persona
    retriever = load_vector_store(persona).as_retriever(search_kwargs={"k": 3})
    docs = retriever.get_relevant_documents(question)
    context = "\n".join([doc.page_content for doc in docs])


    system_prompt = get_persona_prompt(persona)

    # final prompt
    final_prompt = f"""
{system_prompt}

Context:
{context}

Question: {question}

Answer as the persona in first person, historically accurate, and in their tone.

Rules:
- Keep the answer short and focused (maximum 60 words).
- Avoid unnecessary details.
- If asked about posthumous events (like Modi era or anything after your lifetime), reply exactly:
"I'm afraid I cannot speak of the future I haven’t seen."
"""


    # Used Groq LLaMA 3.3 model
    response = client.chat.completions.create(
        model="llama3-70b-8192",  
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": final_prompt}
        ],
        temperature=0.7,
        max_tokens=500
    )

    return response.choices[0].message.content


import os
import warnings
import google.generativeai as genai
from rag_builder import retrieve_context
from tools import lookup_order, create_ticket
from dotenv import load_dotenv

warnings.filterwarnings("ignore")
load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Error ke hisaab se exact model set kar diya hai
working_model = "gemini-3.8-flash"

SYSTEM_PROMPT = """
You are the AI support assistant for ZentroMart. 
Today's date is 20 October 2026. 
Always introduce yourself as an AI assistant on the first turn.
Answer strictly based on the provided policy documents. If the documents do not cover the question, state politely that you do not know. Do not invent policies or amounts.
If a customer asks about a specific order, ask for their order ID.
CRITICAL VERIFICATION RULE: Once you have the order ID, you must ask the customer for the last 4 digits of their registered phone number OR their 6-digit delivery pincode to verify their identity before sharing any order details.
If a policy requires human review or intervention, politely explain this, create a ticket, and summarize it for the handover.
"""

class ZentroMartAgent:
    def __init__(self):
        self.model = genai.GenerativeModel(
            model_name=working_model,
            system_instruction=SYSTEM_PROMPT,
            tools=[lookup_order, create_ticket]
        )
        self.chat = self.model.start_chat(enable_automatic_function_calling=True)
        
    def respond(self, user_message: str):
        context_text, source_ids = retrieve_context(user_message)
        prompt = f"Knowledge Base Context:\n{context_text}\n\nCustomer Message:\n{user_message}"
        response = self.chat.send_message(prompt)
        return response.text, source_ids

if __name__ == "__main__":
    agent = ZentroMartAgent()
    print(f"✅ AI Agent Ready! (Model: {working_model}) Type 'exit' to stop.")
    while True:
        user_input = input("\nAap: ")
        if user_input.lower() == 'exit':
            break
        reply = agent.respond(user_input)
        print(f"🤖 AI: {reply}")
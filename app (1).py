import gradio as gr
from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
import os

# Get API key from environment
GROQ_API_KEY = os.getenv('GROQ_API_KEY')

llm = ChatGroq(temperature=0, groq_api_key=GROQ_API_KEY, model_name="llama-3.3-70b-versatile")

def calculate_budget_inr(city, budget_level="Mid-range"):
    ex = 86.50
    if budget_level == "Budget":
        daily = 5000
    elif budget_level == "Luxury":
        daily = 20000
    else:
        daily = 12000
    return f"💰 Daily Budget: ₹{daily:,} | Total for 3 days: ₹{daily * 3:,}"

def generate_itinerary(city, interests, days):
    prompt = ChatPromptTemplate.from_messages([
        ("system", f"Create a {days}-day itinerary for {city}. Interests: {interests}. Use emojis and bullet points."),
        ("human", "Create itinerary")
    ])
    response = llm.invoke(prompt.format_messages())
    return response.content

with gr.Blocks(title="AI Travel Planner") as demo:
    gr.Markdown("# ✈️ AI Travel Planner\n### Personalized itineraries with budget in Indian Rupees")
    
    with gr.Row():
        with gr.Column():
            city = gr.Textbox(label="🏙️ City", placeholder="Paris, Tokyo, Bali...")
            interests = gr.Textbox(label="🎯 Interests", placeholder="museums, food, nature", lines=2)
            days = gr.Slider(label="📅 Days", minimum=1, maximum=14, value=3)
            budget_level = gr.Radio(label="💰 Budget", choices=["Budget", "Mid-range", "Luxury"], value="Mid-range")
            generate_btn = gr.Button("🚀 Generate")
        
        with gr.Column():
            itinerary_out = gr.Markdown(label="🗺️ Itinerary")
            budget_out = gr.Markdown(label="💰 Budget")
    
    generate_btn.click(fn=generate_itinerary, inputs=[city, interests, days], outputs=itinerary_out)
    budget_btn = gr.Button("💰 Show Budget")
    budget_btn.click(fn=calculate_budget_inr, inputs=[city, budget_level], outputs=budget_out)

print("✅ app.py created")

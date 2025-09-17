import streamlit as st

# ------------------ CONFIG ------------------
st.set_page_config(page_title="AI Farming Assistant", page_icon="🌾", layout="wide")
st.title("🌾 AI-Powered Digital Farming Assistant")
st.markdown("Get instant, detailed answers to all your farming questions!")

# ------------------ FARMING KNOWLEDGE BASE ------------------
farming_context = """You are an expert agricultural assistant helping farmers with their queries. 
You provide detailed advice about crop diseases, pest management, soil, irrigation, fertilizers, and modern farming methods.
Always give step-by-step instructions, cost-effective solutions, and preventive measures."""

# Knowledge base with detailed responses
knowledge_base = {
    "yellow": """*Yellowing of Leaves - Detailed Analysis:*
*Possible Causes:*
1. *Nitrogen Deficiency*: Old leaves turn yellow first; plant growth slows.
2. *Iron Deficiency*: Young leaves yellow, veins remain green.
3. *Water Stress*: Both overwatering and drought can cause yellow leaves.

*Immediate Solutions:*
- Nitrogen Deficiency: Apply Urea 20-30 kg/acre or DAP 50 kg/acre. Foliar spray: Urea 2% (20g in 1L water).
- Iron Deficiency: Spray Ferrous Sulfate 0.5% or chelated iron.
- Water Management: Check soil moisture, ensure proper drainage.

*Long-term Prevention:*
- Add organic compost (2-3 tons/acre)
- Rotate with legume crops
- Regular soil testing every season
""",
    "pest": """*Pest Management - Comprehensive Guide:*
*Identification:*
- Check undersides of leaves for eggs/larvae.
- Look for bite marks, holes, wilting.
- Observe timing of pest activity.

*Immediate Organic Solutions:*
- Neem Oil Spray: 5ml neem oil + 1ml soap per 1L water; spray every 5-7 days.
- Garlic-Chili Spray: Blend 100g garlic + 50g chili in 1L water; spray on affected areas.
- Yellow Sticky Traps: Place 4-5 per acre.

*Chemical Solutions (if severe):*
- Caterpillars: Chlorpyriphos 20EC - 2ml/L
- Aphids: Imidacloprid 0.5ml/L
- Whitefly: Thiamethoxam 0.5g/L

*Prevention:*
- Crop rotation
- Remove weeds
- Encourage beneficial insects (ladybugs, spiders)
- Maintain field hygiene
""",
    "fungus": """*Fungal Disease Management:*
*Common Fungal Issues:*
- Powdery Mildew: White powder on leaves
- Leaf Spot: Brown/black spots with yellow halos
- Root Rot: Wilting despite moist soil
- Early/Late Blight: Dark spots spreading rapidly

*Immediate Treatment:*
- Remove infected parts; burn or bury.
- Organic fungicides: Baking soda 1 tbsp + ½ tsp soap in 4L water; Copper sulfate 2g/L; Trichoderma bio-fungicide.
- Chemical fungicides: Mancozeb 2-2.5g/L; Carbendazim 1g/L; Copper Oxychloride 3g/L.

*Prevention:*
- Proper plant spacing
- Avoid overhead irrigation
- Mulching to prevent soil splash
- Choose resistant varieties
""",
    "water": """*Water Management Guide:*
*Irrigation Best Practices:*
- Check soil moisture at 3-4 inch depth
- Drooping leaves in morning = water stress
- Soil should be moist, not waterlogged

*Efficient Methods:*
- Drip Irrigation: 40-50% water saving; subsidy available
- Sprinkler System: Good for vegetables
- Furrow Irrigation: Traditional, effective

*Water Conservation:*
- Mulching reduces evaporation
- Cover crops in off-season
- Rainwater harvesting

*Drought Management:*
- Anti-transpirant sprays (Kaolin 5%)
- Partial root drying
- Use drought-tolerant varieties
""",
    "fertilizer": """*Fertilizer Management Guide:*
*Understanding NPK:*
- N (Nitrogen): Leaf growth
- P (Phosphorus): Roots and flowers
- K (Potassium): Fruit quality and disease resistance

*Recommendations:*
- Urea 50-100 kg/acre (split doses)
- DAP 50-75 kg/acre at sowing
- MOP 40-50 kg/acre during fruiting
- Farmyard manure 4-5 tons/acre
- Vermicompost 2-3 tons/acre
- Neem cake 200-400 kg/acre

*Application Timing:*
- Basal dose: P & K at planting
- Top dressing: N at 30-60 days
- Foliar spray: Flowering/fruiting stages

*Micronutrients:*
- Zinc Sulfate 10 kg/acre
- Boron 5 kg/acre
""",
    "soil": """*Soil Health Management:*
- Test soil every season (costs ₹200-500)
- Ideal pH: 6-7

*Acidic Soil (pH<6):*
- Add lime 200-400 kg/acre
- Wood ash 100-200 kg/acre

*Alkaline Soil (pH>7.5):*
- Add gypsum 200-500 kg/acre
- Add sulfur 20-40 kg/acre

*Improvement Tips:*
- Add organic matter for aeration and microbial health
- Crop rotation
- Cover crops to prevent erosion
- Minimum tillage preserves soil structure
- Use biofertilizers like Rhizobium, Azotobacter, PSB
"""
}

# ------------------ FALLBACK RESPONSE ------------------
def get_response(query):
    q = query.lower()
    for key, response in knowledge_base.items():
        if key in q:
            return response
    return """*General Farming Advice:*
- Observe symptoms carefully and take photos
- Check water, sunlight, and soil
- Apply balanced NPK + compost
- Neem oil spray for pests
- Maintain field hygiene
- For expert help, contact KVK or Kisan Call Center (1551 / 1800-180-1551)
Please provide more details for targeted advice."""

# ------------------ STREAMLIT CHAT ------------------
if "chat_history" not in st.session_state:
    st.session_state.chat_history = [{"role":"assistant","content":"Welcome to AI Farming Assistant! 🌾 Ask anything about crops, pests, soil, water, fertilizers, or diseases."}]

# Display chat
for chat in st.session_state.chat_history:
    color = "#e8f5e9" if chat["role"]=="user" else "#f5f5f5"
    st.markdown(f'<div style="padding:10px;margin:5px;border-left:4px solid; background:{color}">'
                f"<b>{'You' if chat['role']=='user' else 'Assistant'}:</b><br>{chat['content']}</div>", unsafe_allow_html=True)

# Input
query = st.text_input("Ask your farming question:")
if st.button("Send") and query:
    st.session_state.chat_history.append({"role":"user","content":query})
    with st.spinner("🤔 Thinking..."):
        answer = get_response(query)
    st.session_state.chat_history.append({"role":"assistant","content":answer})
    st.rerun()

# Sidebar clear
with st.sidebar:
    if st.button("Clear Chat"):
        st.session_state.chat_history = []
        st.rerun()

st.markdown("---")
st.markdown("<div style='text-align:center; color:#666;'>💡 Tip: Be specific about crop type, location, and symptoms for better advice | 📞 Kisan Helpline: 1800-180-1551</div>", unsafe_allow_html=True)
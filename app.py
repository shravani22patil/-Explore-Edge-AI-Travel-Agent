import streamlit as st
import folium
from streamlit_folium import st_folium
import pandas as pd
from datetime import datetime, timedelta
import random
import uuid
def get_destination_metadata(destination):
    """Generates rule-based metadata for any destination."""
    dest = destination.lower()
    
    # Default logic for any destination
    meta = {
        "best_time": "April - June & Sept - Oct",
        "vibe": "Mixed Culture & Urban",
        "budget": "$150 - $250",
        "crowd": "Moderate",
        "duration": "4-6 Days"
    }
    
    # Rule-based overrides
    if any(x in dest for x in ["beach", "bali", "goa", "maldives", "island"]):
        meta.update({"vibe": "Tropical / Relaxed", "budget": "$100 - $300", "duration": "5-7 Days"})
    elif any(x in dest for x in ["paris", "london", "york", "tokyo", "rome"]):
        meta.update({"vibe": "Historical / Fast-paced", "crowd": "High", "duration": "3-5 Days"})
    elif any(x in dest for x in ["mountains", "alps", "hiking", "nepal"]):
        meta.update({"vibe": "Adventure / Nature", "best_time": "June - August", "duration": "7-10 Days"})
        
    return meta

def render_destination_stats(data):
    # This CSS shrinks the metric font size so words don't get cut off
    st.markdown("""
        <style>
        [data-testid="stMetricLabel"] { font-size: 0.8rem !important; }
        [data-testid="stMetricValue"] { font-size: 1.1rem !important; }
        </style>
        """, unsafe_allow_html=True)
        
    st.markdown("---")
    st.markdown("### 📊 Destination Quick Stats")
    
    c1, c2, c3, c4, c5 = st.columns(5)
    with c1:
        st.metric("Best Time", data["best_time"])
    with c2:
        st.metric("Vibe", data["vibe"])
    with c3:
        st.metric("Daily Budget", data["budget"])
    with c4:
        st.metric("Crowd Level", data["crowd"])
    with c5:
        st.metric("Ideal Stay", data["duration"])

def get_travel_estimate(destination, num_days, travel_month):
    """Calculates travel budgets and seasonal tips using rule-based logic."""
    dest = destination.lower().strip()
    month = travel_month.lower().strip()
    
    regions = {
        "western_europe": {"food": 50, "transport": 15, "daily": 120},
        "southeast_asia": {"food": 15, "transport": 5, "daily": 45},
        "north_america": {"food": 60, "transport": 25, "daily": 150},
        "default": {"food": 35, "transport": 15, "daily": 80}
    }

    if any(city in dest for city in ["paris", "london", "rome", "berlin"]):
        base = regions["western_europe"]
    elif any(city in dest for city in ["bangkok", "bali", "hanoi", "phuket"]):
        base = regions["southeast_asia"]
    elif any(city in dest for city in ["new york", "la", "toronto", "chicago"]):
        base = regions["north_america"]
    else:
        base = regions["default"]

    food_budget = base["food"] * num_days
    transport_budget = base["transport"] * num_days
    estimated_daily_total = base["daily"] 

    if month in ["december", "january", "february"]:
        tips = "❄️ Winter: Pack warm layers. Expect shorter daylight hours and potential holiday crowds."
    elif month in ["june", "july", "august"]:
        tips = "☀️ Peak Summer: High tourist season. Expect heat and higher prices. Book in advance."
    elif month in ["march", "april", "may"]:
        tips = "🌸 Spring: Mild weather and blooming landscapes. Great for outdoor walking tours."
    else:
        tips = "🍂 Autumn: Pleasant temperatures and colorful foliage. Good balance of prices and crowds."

    return {
        "daily": f"${estimated_daily_total}",
        "transport": f"${transport_budget}",
        "food": f"${food_budget}",
        "seasonal": tips
    }

# Page configuration
st.set_page_config(
    page_title="AI Travel Agent",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for clean UI
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #1E3A5F;
        margin-bottom: 1rem;
    }
    .sub-header {
        font-size: 1.5rem;
        font-weight: 600;
        color: #2C5282;
        margin-bottom: 0.5rem;
    }
    .card {
        background-color: #f8fafc;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
        border: 1px solid #e2e8f0;
    }
    .destination-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border-radius: 10px;
        padding: 1.5rem;
        margin-bottom: 1rem;
    }
    .stat-box {
        background-color: #EBF8FF;
        border-radius: 8px;
        padding: 1rem;
        text-align: center;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'itinerary' not in st.session_state:
    st.session_state.itinerary = []
if 'destinations' not in st.session_state:
    st.session_state.destinations = [
        {"name": "Paris, France", "lat": 48.8566, "lon": 2.3522, "description": "City of Light"},
        {"name": "Tokyo, Japan", "lat": 35.6762, "lon": 139.6503, "description": "Modern meets traditional"},
        {"name": "New York, USA", "lat": 40.7128, "lon": -74.0060, "description": "The Big Apple"},
        {"name": "Sydney, Australia", "lat": -33.8688, "lon": 151.2093, "description": "Harbor city wonder"},
        {"name": "Rome, Italy", "lat": 41.9028, "lon": 12.4964, "description": "Eternal City"},
    ]
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []

# Sample destination data for Visual Journey
DESTINATION_IMAGES = {
    "Paris": {
        "emoji": "🗼",
        "highlights": ["Eiffel Tower", "Louvre Museum", "Notre-Dame", "Champs-Élysées"],
        "best_time": "April - June, September - November",
        "avg_cost": "$150-300/day"
    },
    "Tokyo": {
        "emoji": "🏯",
        "highlights": ["Shibuya Crossing", "Senso-ji Temple", "Tokyo Tower", "Akihabara"],
        "best_time": "March - May, September - November",
        "avg_cost": "$100-250/day"
    },
    "New York": {
        "emoji": "🗽",
        "highlights": ["Statue of Liberty", "Central Park", "Times Square", "Brooklyn Bridge"],
        "best_time": "April - June, September - November",
        "avg_cost": "$200-400/day"
    },
    "Sydney": {
        "emoji": "🌊",
        "highlights": ["Opera House", "Harbour Bridge", "Bondi Beach", "Darling Harbour"],
        "best_time": "September - November, March - May",
        "avg_cost": "$150-300/day"
    },
    "Rome": {
        "emoji": "🏛️",
        "highlights": ["Colosseum", "Vatican City", "Trevi Fountain", "Pantheon"],
        "best_time": "April - June, September - October",
        "avg_cost": "$120-250/day"
    }
}


# Mock AI Response Function (easily replaceable with OpenAI/Gemini)
def get_ai_response(user_message: str) -> str:
    """
    Mock AI response function for travel assistance.
    
    To integrate with OpenAI:
    --------------------------
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def get_ai_response(user_message: str) -> str:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are a helpful travel agent assistant."},
                {"role": "user", "content": user_message}
            ]
        )
        return response.choices[0].message.content
    
    To integrate with Google Gemini:
    --------------------------------
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    def get_ai_response(user_message: str) -> str:
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(user_message)
        return response.text
    """
    
    # Mock responses based on keywords
    user_lower = user_message.lower()
    
    if any(word in user_lower for word in ['paris', 'france']):
        return """🗼 **Paris Travel Guide**

Paris is absolutely magical! Here's what I recommend:

**Must-See Attractions:**
- Eiffel Tower (book tickets in advance!)
- Louvre Museum (plan for at least half a day)
- Notre-Dame Cathedral
- Champs-Élysées & Arc de Triomphe

**Best Time to Visit:** April-June or September-November for pleasant weather and fewer crowds.

**Budget Tips:**
- Get a Paris Museum Pass for multiple attractions
- Use the Metro for affordable transportation
- Enjoy picnics in Luxembourg Gardens

Would you like me to help create a detailed itinerary?"""

    elif any(word in user_lower for word in ['tokyo', 'japan']):
        return """🏯 **Tokyo Travel Guide**

Tokyo is an incredible blend of ultra-modern and traditional! Here's my advice:

**Top Experiences:**
- Explore Shibuya Crossing
- Visit Senso-ji Temple in Asakusa
- Experience teamLab digital art museums
- Try authentic ramen in local shops

**Best Time to Visit:** March-May (cherry blossoms) or September-November (autumn colors).

**Pro Tips:**
- Get a Suica/Pasmo card for easy transit
- Download Google Translate for menus
- Respect local customs (no tipping!)

Need help planning your Tokyo adventure?"""

    elif any(word in user_lower for word in ['budget', 'cheap', 'affordable', 'save']):
        return """💰 **Budget Travel Tips**

Here are my top money-saving strategies:

**Accommodation:**
- Consider hostels or Airbnb
- Travel during shoulder season
- Book in advance for better rates

**Transportation:**
- Use public transit over taxis
- Consider overnight trains/buses
- Look into city passes

**Food:**
- Eat where locals eat
- Visit local markets
- Cook some meals if you have kitchen access

**General:**
- Use free walking tours
- Many museums have free days
- Travel insurance is worth it!

What destination are you planning for?"""

    elif any(word in user_lower for word in ['itinerary', 'plan', 'schedule']):
        return """📅 **Itinerary Planning Assistance**

I'd love to help you create the perfect itinerary! To give you the best recommendations, please tell me:

1. **Destination(s):** Where do you want to go?
2. **Duration:** How many days?
3. **Interests:** Culture, food, adventure, relaxation?
4. **Budget:** Luxury, moderate, or budget?
5. **Travel style:** Fast-paced or relaxed?

Once you share these details, I'll create a customized day-by-day plan for you!"""

    elif any(word in user_lower for word in ['hello', 'hi', 'hey', 'start']):
        return """👋 **Welcome to AI Travel Agent!**

I'm your personal travel assistant, here to help you plan unforgettable journeys!

**I can help you with:**
- 🗺️ Destination recommendations
- 📅 Custom itinerary planning
- 💰 Budget optimization
- 🍽️ Food & restaurant suggestions
- 🏨 Accommodation advice
- ✈️ Travel tips & hacks

**Try asking me:**
- "What are the best things to do in Paris?"
- "Plan a 5-day trip to Tokyo"
- "Budget travel tips for Europe"

Where would you like to explore?"""

    else:
        responses = [
            """🌍 **Travel Inspiration**

That's a great question! Based on current travel trends, here are some amazing destinations to consider:

**For Culture Lovers:** Rome, Kyoto, Istanbul
**For Beach Lovers:** Maldives, Bali, Greece
**For Adventure:** New Zealand, Iceland, Peru
**For Food:** Thailand, Italy, Mexico

Would you like detailed information about any of these destinations?""",

            """✨ **Personalized Recommendation**

I'd be happy to help you explore that! Here are some thoughts:

- Consider visiting during the shoulder season for fewer crowds
- Book accommodations in central locations for convenience
- Always check visa requirements in advance
- Travel insurance is highly recommended

What specific aspect of your trip would you like help with?""",

            """🎒 **Travel Planning Tips**

Great question! Here's some general advice:

1. **Research** your destination thoroughly
2. **Book** flights and hotels early for best prices
3. **Pack** light - you'll thank yourself later
4. **Download** offline maps and translation apps
5. **Notify** your bank about travel plans

Is there a specific destination you're considering?"""
        ]
        return random.choice(responses)


def generate_ai_itinerary(destination: str, num_days: int, travel_style: str) -> list:
    """
    Mock AI itinerary generator function.
    
    To integrate with OpenAI:
    --------------------------
    import openai
    openai.api_key = os.getenv("OPENAI_API_KEY")
    
    def generate_ai_itinerary(destination: str, num_days: int, travel_style: str) -> list:
        prompt = f"Create a {num_days}-day {travel_style.lower()} travel itinerary for {destination}..."
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        # Parse and return structured itinerary
    
    To integrate with Google Gemini:
    --------------------------------
    import google.generativeai as genai
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    
    def generate_ai_itinerary(destination: str, num_days: int, travel_style: str) -> list:
        model = genai.GenerativeModel('gemini-pro')
        prompt = f"Create a {num_days}-day {travel_style.lower()} travel itinerary for {destination}..."
        response = model.generate_content(prompt)
        # Parse and return structured itinerary
    """
    
    dest_lower = destination.lower()
    
    # Destination-specific activities
    destination_activities = {
        "paris": {
            "landmarks": ["Eiffel Tower", "Louvre Museum", "Notre-Dame Cathedral", "Arc de Triomphe", "Sacré-Cœur", "Musée d'Orsay"],
            "neighborhoods": ["Le Marais", "Montmartre", "Latin Quarter", "Saint-Germain-des-Prés", "Champs-Élysées"],
            "food": ["croissants at a local café", "French onion soup", "crepes in Montmartre", "wine and cheese at a bistro", "macarons at Ladurée"],
            "activities": ["Seine River cruise", "picnic at Luxembourg Gardens", "shopping at Galeries Lafayette", "stroll along Pont des Arts"],
        },
        "tokyo": {
            "landmarks": ["Tokyo Tower", "Senso-ji Temple", "Shibuya Crossing", "Meiji Shrine", "Tokyo Skytree", "Imperial Palace"],
            "neighborhoods": ["Shibuya", "Shinjuku", "Asakusa", "Akihabara", "Harajuku", "Ginza"],
            "food": ["fresh sushi at Tsukiji", "ramen in a local shop", "tempura dinner", "matcha desserts", "yakitori under the tracks"],
            "activities": ["teamLab digital art museum", "Japanese garden walk", "anime shopping in Akihabara", "karaoke night"],
        },
        "new york": {
            "landmarks": ["Statue of Liberty", "Empire State Building", "Central Park", "Brooklyn Bridge", "Times Square", "One World Trade Center"],
            "neighborhoods": ["Manhattan", "Brooklyn", "Greenwich Village", "SoHo", "Harlem", "Upper East Side"],
            "food": ["New York pizza slice", "bagel with lox", "diner breakfast", "food hall exploration", "rooftop cocktails"],
            "activities": ["Broadway show", "High Line walk", "museum hopping", "sunset at Brooklyn Bridge Park"],
        },
        "rome": {
            "landmarks": ["Colosseum", "Vatican City", "Trevi Fountain", "Pantheon", "Roman Forum", "Spanish Steps"],
            "neighborhoods": ["Trastevere", "Centro Storico", "Testaccio", "Monti", "Vatican area"],
            "food": ["authentic pasta carbonara", "gelato tasting", "espresso at a local bar", "aperitivo hour", "pizza al taglio"],
            "activities": ["Vatican Museums tour", "ancient ruins exploration", "evening passeggiata", "cooking class"],
        },
        "default": {
            "landmarks": ["main historic square", "local museum", "famous monument", "old town area", "scenic viewpoint", "local market"],
            "neighborhoods": ["historic center", "local arts district", "waterfront area", "cultural quarter"],
            "food": ["traditional local breakfast", "authentic regional cuisine", "street food tour", "fine dining experience", "local café culture"],
            "activities": ["walking tour", "cultural experience", "day trip to nearby attraction", "sunset viewing", "local entertainment"],
        }
    }
    
    # Get activities for destination or use default
    activities = None
    for key in destination_activities:
        if key in dest_lower:
            activities = destination_activities[key]
            break
    if not activities:
        activities = destination_activities["default"]
    
    # Style-specific modifiers
    style_modifiers = {
        "Relaxed": {
            "morning_prefix": "Leisurely start with",
            "afternoon_prefix": "Relaxed afternoon exploring",
            "evening_prefix": "Gentle evening with",
            "pace": "Take your time and enjoy"
        },
        "Adventure": {
            "morning_prefix": "Early morning adventure at",
            "afternoon_prefix": "Action-packed afternoon with",
            "evening_prefix": "Exciting evening featuring",
            "pace": "Make the most of every moment"
        },
        "Culture": {
            "morning_prefix": "Cultural immersion starting at",
            "afternoon_prefix": "Deep dive into history at",
            "evening_prefix": "Cultural evening experiencing",
            "pace": "Connect with local heritage"
        },
        "Mixed": {
            "morning_prefix": "Balanced morning at",
            "afternoon_prefix": "Varied afternoon including",
            "evening_prefix": "Enjoyable evening with",
            "pace": "Perfect mix of experiences"
        }
    }
    
    style = style_modifiers.get(travel_style, style_modifiers["Mixed"])
    
    # Generate itinerary
    itinerary = []
    
    day_titles = [
        "Arrival & First Impressions",
        "Iconic Landmarks",
        "Local Culture & Neighborhoods",
        "Hidden Gems",
        "Day Trip Adventure",
        "Art & History",
        "Food & Markets",
        "Relaxation & Shopping",
        "Nature & Parks",
        "Off the Beaten Path",
        "Local Life",
        "Final Discoveries",
        "Leisure Day",
        "Farewell Exploration"
    ]
    
    tips_pool = [
        f"Book tickets in advance for popular attractions in {destination}.",
        "Wear comfortable walking shoes - you'll cover a lot of ground!",
        "Learn a few local phrases - locals appreciate the effort.",
        "Keep some local currency for small vendors and tips.",
        f"The best photos in {destination} are often taken during golden hour.",
        "Stay hydrated and take breaks at local cafés.",
        "Ask locals for restaurant recommendations - they know the best spots.",
        "Download offline maps in case you lose connection.",
        f"Public transportation in {destination} is often the best way to get around.",
        "Try to visit major attractions early morning or late afternoon to avoid crowds."
    ]
    
    for day_num in range(1, num_days + 1):
        landmark = activities["landmarks"][(day_num - 1) % len(activities["landmarks"])]
        neighborhood = activities["neighborhoods"][(day_num - 1) % len(activities["neighborhoods"])]
        food = activities["food"][(day_num - 1) % len(activities["food"])]
        activity = activities["activities"][(day_num - 1) % len(activities["activities"])]
        
        if day_num == 1:
            morning = f"Arrive in {destination} and check into your accommodation. Take a refreshing walk around the neighborhood to get oriented."
        else:
            morning = f"{style['morning_prefix']} {landmark}. Take in the atmosphere and capture some memorable photos."
        
        afternoon = f"{style['afternoon_prefix']} {neighborhood}. Enjoy {food} for lunch at a well-reviewed local spot."
        evening = f"{style['evening_prefix']} {activity}. End the day with a delightful dinner featuring local specialties."
        
        title = day_titles[(day_num - 1) % len(day_titles)]
        if day_num == num_days:
            title = "Final Day & Departure"
            evening = f"Pack up memories of {destination}. Enjoy one last local meal before heading to the airport."
        
        itinerary.append({
            "day": day_num,
            "title": title,
            "morning": morning,
            "afternoon": afternoon,
            "evening": evening,
            "tips": tips_pool[(day_num - 1) % len(tips_pool)]
        })
    
    return itinerary


# Sidebar Navigation
st.sidebar.title("✈️ AI Travel Agent")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigate to:",
    ["🏠 Home", "📋 Itinerary", "🗺️ Map", "🖼️ Visual Journey", "🤖 AI Assistant"],
    index=0
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Quick Stats")
col1, col2 = st.sidebar.columns(2)
with col1:
    st.metric("Destinations", len(st.session_state.destinations))
with col2:
    itinerary_days = len(st.session_state.get('generated_itinerary', []))
    st.metric("Itinerary Days", itinerary_days)


# ==================== HOME PAGE ====================
if page == "🏠 Home":
    # Hero Section with background styling
# Hero Section with background styling
    st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@700;800&display=swap');

        .hero-section {
            background: linear-gradient(135deg, rgba(102, 126, 234, 0.1) 0%, rgba(118, 75, 162, 0.1) 100%);
            padding: 2.5rem;
            border-radius: 20px;
            margin-bottom: 2rem;
            text-align: center;
        }

        .hero-title {
            font-family: 'Playfair Display', serif;
            font-size: 3.5rem;
            font-weight: 800;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-bottom: 0.5rem;
        }

        /* REVERTED: Subtitle back to original Grey and Standard Font */
        .hero-subtitle {
            font-size: 1.8rem;
            color: #475569; /* Original slate grey */
            font-weight: 600;
            margin-bottom: 1.5rem;
            text-align: center;
            font-family: 'Inter', 'Source Sans Pro', sans-serif; 
        }

        /* REVERTED: Description back to Grey */
        .hero-description {
            color: #64748b;
            font-size: 1.1rem;
            max-width: 800px;
            margin: 0 auto;
            line-height: 1.6;
        }
    </style>
    """, unsafe_allow_html=True)
    
    # Hero Section
# Hero Section
    st.markdown("""
    <div class="hero-section">
        <h1 class="hero-title">Explore Edge: Your Personal AI Travel Agent</h1>
        <p class="hero-subtitle">Not a Search Engine</p>
        <p class="hero-description">
            Tell us where you want to go, and our AI will craft a personalized, 
            day-by-day itinerary tailored to your travel style, budget, and preferences.
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Floating Destination Cards
    st.markdown("#### Popular Destinations")
    dest_cols = st.columns(4)
    floating_destinations = [
        {"name": "Paris", "emoji": "🗼", "tagline": "City of Light"},
        {"name": "Goa", "emoji": "🏖️", "tagline": "Beach Paradise"},
        {"name": "Tokyo", "emoji": "🏯", "tagline": "Modern Tradition"},
        {"name": "New York", "emoji": "🗽", "tagline": "The Big Apple"},
    ]
    
    for idx, dest in enumerate(floating_destinations):
        with dest_cols[idx]:
            if st.button(f"{dest['emoji']} {dest['name']}", key=f"dest_quick_{idx}", use_container_width=True):
                st.session_state.home_destination = dest['name']
                st.rerun()
            st.caption(dest['tagline'])
    
    st.markdown("---")
    
    # Main Input Card
    st.markdown('<div class="input-card">', unsafe_allow_html=True)
    st.markdown("### Plan Your Perfect Trip")
    
    # Row 1: Origin and Destination
    col1, col2 = st.columns(2)
    with col1:
        origin = st.text_input(
            "Where are you traveling from?",
            placeholder="e.g., London, Mumbai, San Francisco...",
            key="home_origin"
        )
    with col2:
        destination = st.text_input(
            "Where do you want to go?",
            value=st.session_state.get('home_destination', ''),
            placeholder="e.g., Paris, Tokyo, Bali...",
            key="home_dest_input"
        )
    
    # Row 2: Duration and Start Date
    col1, col2 = st.columns(2)
    with col1:
        trip_duration = st.slider(
            "Trip Duration (days)",
            min_value=1,
            max_value=21,
            value=5,
            key="home_duration"
        )
    with col2:
        from datetime import date
        start_date = st.date_input(
            "Start Date",
            value=date.today(),
            key="home_start_date"
        )
    
    # Row 3: Budget
    budget = st.slider(
        "Daily Budget (USD)",
        min_value=50,
        max_value=1000,
        value=200,
        step=25,
        format="$%d",
        key="home_budget"
    )
    
    # Row 4: Travel Style - Who
    st.markdown("**Who's traveling?**")
    travel_who_options = ["Solo", "Couple", "Family", "Friends"]
    travel_who = st.radio(
        "Travel companions",
        travel_who_options,
        horizontal=True,
        key="home_travel_who",
        label_visibility="collapsed"
    )
    
    # Row 5: Travel Style - What
    st.markdown("**What's your vibe?**")
    travel_vibe_options = ["Adventure", "Relaxed", "Culture", "Luxury", "Budget", "Foodie"]
    travel_vibes = st.multiselect(
        "Travel vibes",
        travel_vibe_options,
        default=["Culture"],
        key="home_travel_vibes",
        label_visibility="collapsed"
    )
    
    st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("")
    
    # Primary CTA Button
    generate_clicked = st.button(
        "Generate My Smart Itinerary",
        type="primary",
        use_container_width=True,
        key="home_generate_btn"
    )
    
    if generate_clicked:
        if destination:
            # Show typing status
            status_placeholder = st.empty()
            status_placeholder.markdown(
                '<p class="typing-status">AI is analyzing your travel preferences...</p>',
                unsafe_allow_html=True
            )
            
            # Store inputs in session state
            st.session_state.trip_origin = origin
            st.session_state.itinerary_destination = destination
            st.session_state.trip_duration = trip_duration
            st.session_state.trip_start_date = start_date
            st.session_state.trip_budget = budget
            st.session_state.trip_who = travel_who
            st.session_state.trip_vibes = travel_vibes
            
            # Map travel vibes to style
            if "Adventure" in travel_vibes:
                travel_style = "Adventure"
            elif "Culture" in travel_vibes:
                travel_style = "Culture"
            elif "Relaxed" in travel_vibes or "Luxury" in travel_vibes:
                travel_style = "Relaxed"
            else:
                travel_style = "Mixed"
            
            st.session_state.itinerary_style = travel_style
            
            # Generate itinerary
            import time
            time.sleep(1)  # Brief delay for effect
            
            generated_itinerary = generate_ai_itinerary(destination, trip_duration, travel_style)
            st.session_state.generated_itinerary = generated_itinerary
            
            status_placeholder.empty()
            
            # Navigate to Itinerary page
            st.session_state.navigate_to_itinerary = True
            st.rerun()
        else:
            st.warning("Please enter a destination to generate your itinerary.")
    
    # Check if we need to navigate (handled after rerun)
    if st.session_state.get('navigate_to_itinerary', False):
        st.session_state.navigate_to_itinerary = False
        st.info("Your itinerary is ready! Click on **Itinerary** in the sidebar to view it.")
    
    st.markdown("---")
    
    # Feature highlights (compact)
    st.markdown("#### Why Choose AI Travel Agent?")
    
    feat_cols = st.columns(3)
    with feat_cols[0]:
        st.markdown("""
        **🧠 AI-Powered**  
        Smart recommendations based on your unique preferences
        """)
    with feat_cols[1]:
        st.markdown("""
        **🗺️ Visual Maps**  
        See your entire journey on interactive maps
        """)
    with feat_cols[2]:
        st.markdown("""
        **💬 24/7 Assistant**  
        Ask questions and get instant travel advice
        """)


# ==================== ITINERARY PAGE ====================
    
# ==================== ITINERARY PAGE ====================
# ==================== ITINERARY PAGE ====================
elif page == "📋 Itinerary":
    if "generated_itinerary" in st.session_state and st.session_state["generated_itinerary"]:
        dest_name = st.session_state.get('itinerary_destination', 'Destination')
        duration = st.session_state.get('home_duration', 1)
        # Extract month from the start date for the rules
        travel_date = st.session_state.get('home_start_date', datetime.now())
        month_name = travel_date.strftime("%B")
        
        # Get rule-based estimates
        estimates = get_travel_estimate(dest_name, duration, month_name)

        st.markdown(f"## 📅 Your Journey to {dest_name}")
        
        # --- NEW BUDGET & TIPS SECTION ---
        st.markdown("### 💰 Trip Estimates & Seasonal Advice")
        b_col1, b_col2, b_col3 = st.columns(3)
        with b_col1:
            st.metric("Est. Daily Budget", estimates["daily"])
        with b_col2:
            st.metric("Total Food Budget", estimates["food"])
        with b_col3:
            st.metric("Total Transport", estimates["transport"])
            
        st.info(f"**Seasonal Insight:** {estimates['seasonal']}")
        st.markdown("---")
        
        # --- EXISTING ITINERARY DISPLAY ---
        for day in st.session_state["generated_itinerary"]:
            with st.expander(f"✨ Day {day['day']}: {day['title']}", expanded=True):
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.markdown("🌅 **Morning**")
                    st.info(day['morning'])
                with col2:
                    st.markdown("☀️ **Afternoon**")
                    st.success(day['afternoon'])
                with col3:
                    st.markdown("🌙 **Evening**")
                    st.warning(day['evening'])
                if 'tips' in day:
                    st.markdown(f"💡 **Activity Tip:** {day['tips']}")
    else:
        st.markdown("""
        <div style="text-align: center; padding: 3rem; background-color: #f8fafc; border-radius: 10px; border: 2px dashed #cbd5e1;">
            <h3 style="color: #64748b;">No itinerary generated yet</h3>
            <p style="color: #94a3b8;">Enter your destination and preferences on the Home page to get started!</p>
        </div>
        """, unsafe_allow_html=True)

# ==================== MAP PAGE ====================
elif page == "🗺️ Map":
    st.markdown('<h1 class="main-header">🗺️ Itinerary Map</h1>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Predefined coordinates for popular destinations and landmarks
    DESTINATION_COORDINATES = {
        # Major Cities
        "paris": {"lat": 48.8566, "lon": 2.3522, "zoom": 12},
        "tokyo": {"lat": 35.6762, "lon": 139.6503, "zoom": 11},
        "new york": {"lat": 40.7128, "lon": -74.0060, "zoom": 11},
        "rome": {"lat": 41.9028, "lon": 12.4964, "zoom": 12},
        "london": {"lat": 51.5074, "lon": -0.1278, "zoom": 11},
        "sydney": {"lat": -33.8688, "lon": 151.2093, "zoom": 11},
        "barcelona": {"lat": 41.3851, "lon": 2.1734, "zoom": 12},
        "dubai": {"lat": 25.2048, "lon": 55.2708, "zoom": 11},
        "singapore": {"lat": 1.3521, "lon": 103.8198, "zoom": 11},
        "amsterdam": {"lat": 52.3676, "lon": 4.9041, "zoom": 12},
        "bangkok": {"lat": 13.7563, "lon": 100.5018, "zoom": 11},
        "goa": {"lat": 15.2993, "lon": 74.1240, "zoom": 10},
        "bali": {"lat": -8.3405, "lon": 115.0920, "zoom": 10},
        "istanbul": {"lat": 41.0082, "lon": 28.9784, "zoom": 11},
        "cairo": {"lat": 30.0444, "lon": 31.2357, "zoom": 11},
        "mumbai": {"lat": 19.0760, "lon": 72.8777, "zoom": 11},
        "delhi": {"lat": 28.6139, "lon": 77.2090, "zoom": 11},
        "los angeles": {"lat": 34.0522, "lon": -118.2437, "zoom": 10},
        "san francisco": {"lat": 37.7749, "lon": -122.4194, "zoom": 12},
        "hawaii": {"lat": 21.3069, "lon": -157.8583, "zoom": 10},
        "maldives": {"lat": 3.2028, "lon": 73.2207, "zoom": 8},
        "greece": {"lat": 37.9838, "lon": 23.7275, "zoom": 10},
        "athens": {"lat": 37.9838, "lon": 23.7275, "zoom": 12},
        "venice": {"lat": 45.4408, "lon": 12.3155, "zoom": 13},
        "florence": {"lat": 43.7696, "lon": 11.2558, "zoom": 13},
        "berlin": {"lat": 52.5200, "lon": 13.4050, "zoom": 11},
        "prague": {"lat": 50.0755, "lon": 14.4378, "zoom": 12},
        "vienna": {"lat": 48.2082, "lon": 16.3738, "zoom": 12},
        "lisbon": {"lat": 38.7223, "lon": -9.1393, "zoom": 12},
        "madrid": {"lat": 40.4168, "lon": -3.7038, "zoom": 12},
        "seoul": {"lat": 37.5665, "lon": 126.9780, "zoom": 11},
        "hong kong": {"lat": 22.3193, "lon": 114.1694, "zoom": 11},
        "kyoto": {"lat": 35.0116, "lon": 135.7681, "zoom": 12},
        "osaka": {"lat": 34.6937, "lon": 135.5023, "zoom": 11},
    }
    
    # Landmarks per destination for map markers
    DESTINATION_LANDMARKS = {
        "paris": [
            {"name": "Eiffel Tower", "lat": 48.8584, "lon": 2.2945, "icon": "tower"},
            {"name": "Louvre Museum", "lat": 48.8606, "lon": 2.3376, "icon": "university"},
            {"name": "Notre-Dame", "lat": 48.8530, "lon": 2.3499, "icon": "home"},
            {"name": "Arc de Triomphe", "lat": 48.8738, "lon": 2.2950, "icon": "flag"},
            {"name": "Sacré-Cœur", "lat": 48.8867, "lon": 2.3431, "icon": "home"},
        ],
        "tokyo": [
            {"name": "Tokyo Tower", "lat": 35.6586, "lon": 139.7454, "icon": "tower"},
            {"name": "Senso-ji Temple", "lat": 35.7148, "lon": 139.7967, "icon": "home"},
            {"name": "Shibuya Crossing", "lat": 35.6595, "lon": 139.7004, "icon": "road"},
            {"name": "Meiji Shrine", "lat": 35.6764, "lon": 139.6993, "icon": "home"},
            {"name": "Tokyo Skytree", "lat": 35.7101, "lon": 139.8107, "icon": "tower"},
        ],
        "new york": [
            {"name": "Statue of Liberty", "lat": 40.6892, "lon": -74.0445, "icon": "flag"},
            {"name": "Empire State Building", "lat": 40.7484, "lon": -73.9857, "icon": "tower"},
            {"name": "Central Park", "lat": 40.7829, "lon": -73.9654, "icon": "tree-deciduous"},
            {"name": "Brooklyn Bridge", "lat": 40.7061, "lon": -73.9969, "icon": "road"},
            {"name": "Times Square", "lat": 40.7580, "lon": -73.9855, "icon": "star"},
        ],
        "rome": [
            {"name": "Colosseum", "lat": 41.8902, "lon": 12.4922, "icon": "home"},
            {"name": "Vatican City", "lat": 41.9029, "lon": 12.4534, "icon": "home"},
            {"name": "Trevi Fountain", "lat": 41.9009, "lon": 12.4833, "icon": "tint"},
            {"name": "Pantheon", "lat": 41.8986, "lon": 12.4769, "icon": "home"},
            {"name": "Spanish Steps", "lat": 41.9060, "lon": 12.4828, "icon": "flag"},
        ],
        "goa": [
            {"name": "Baga Beach", "lat": 15.5527, "lon": 73.7517, "icon": "flag"},
            {"name": "Calangute Beach", "lat": 15.5449, "lon": 73.7551, "icon": "flag"},
            {"name": "Fort Aguada", "lat": 15.4920, "lon": 73.7737, "icon": "tower"},
            {"name": "Basilica of Bom Jesus", "lat": 15.5009, "lon": 73.9116, "icon": "home"},
            {"name": "Dudhsagar Falls", "lat": 15.3144, "lon": 74.3143, "icon": "tint"},
        ],
    }
    
    # Check if there's a generated itinerary
    if 'generated_itinerary' in st.session_state and st.session_state.generated_itinerary:
        destination = st.session_state.get('itinerary_destination', '')
        dest_lower = destination.lower()
        
        st.success(f"Showing map for your **{destination}** itinerary")
        
        # Find matching destination coordinates
        dest_coords = None
        for key in DESTINATION_COORDINATES:
            if key in dest_lower or dest_lower in key:
                dest_coords = DESTINATION_COORDINATES[key]
                break
        
        if not dest_coords:
            dest_coords = {"lat": 48.8566, "lon": 2.3522, "zoom": 4}
        
        # Get landmarks for this destination
        landmarks = []
        for key in DESTINATION_LANDMARKS:
            if key in dest_lower or dest_lower in key:
                landmarks = DESTINATION_LANDMARKS[key]
                break
        
        # Create map centered on destination
        m = folium.Map(
            location=[dest_coords["lat"], dest_coords["lon"]],
            zoom_start=dest_coords.get("zoom", 12)
        )
        
        # Add main destination marker
        folium.Marker(
            [dest_coords["lat"], dest_coords["lon"]],
            popup=f"<b>{destination}</b><br>Your destination",
            tooltip=destination,
            icon=folium.Icon(color='red', icon='home')
        ).add_to(m)
        
        # Add landmark markers
        colors = ['blue', 'green', 'purple', 'orange', 'darkred']
        for idx, landmark in enumerate(landmarks):
            folium.Marker(
                [landmark["lat"], landmark["lon"]],
                popup=f"<b>{landmark['name']}</b>",
                tooltip=landmark["name"],
                icon=folium.Icon(color=colors[idx % len(colors)], icon=landmark.get("icon", "info-sign"))
            ).add_to(m)
        
        # Display map
        st_folium(m, width=None, height=500)
        
       # Show landmarks list
        if landmarks:
            st.markdown("---")
            st.markdown('<h2 class="sub-header">📍 Key Locations in Your Itinerary</h2>', unsafe_allow_html=True)
            
            cols = st.columns(len(landmarks) if len(landmarks) <= 5 else 5)
            for idx, landmark in enumerate(landmarks):
                with cols[idx % 5]:
                    # FIXED: Darker background and forced white text color
                    st.markdown(f"""
                    <div style="background-color: #1E3A5F; padding: 1rem; border-radius: 8px; text-align: center; margin-bottom: 0.5rem; border: 1px solid #2C5282;">
                        <div style="font-size: 1.5rem; margin-bottom: 5px;">📍</div>
                        <div style="font-weight: 600; font-size: 0.9rem; color: #FFFFFF !important;">{landmark['name']}</div>
                    </div>
                    """, unsafe_allow_html=True)
    else:
        # No itinerary generated yet
         # Look for this section around line 598
          st.markdown(f"""
               <div style="background-color: #1E3A5F; padding: 1rem; border-radius: 8px; text-align: center; margin-bottom: 0.5rem; border: 1px solid #2C5282;">
                     <div style="font-size: 1.5rem; margin-bottom: 5px;">📍</div>
               <div style="font-weight: 600; font-size: 0.9rem; color: #FFFFFF !important;">{landmark['name']}</div>
              </div>
                """, unsafe_allow_html=True)
        
    # Show world map with sample destinations
    st.markdown("---")
    st.markdown('<h2 class="sub-header">🌍 Explore Popular Destinations</h2>', unsafe_allow_html=True)
        
    m = folium.Map(location=[20, 0], zoom_start=2)
        
    sample_destinations = [
            {"name": "Paris", "lat": 48.8566, "lon": 2.3522},
            {"name": "Tokyo", "lat": 35.6762, "lon": 139.6503},
            {"name": "New York", "lat": 40.7128, "lon": -74.0060},
            {"name": "Rome", "lat": 41.9028, "lon": 12.4964},
            {"name": "Sydney", "lat": -33.8688, "lon": 151.2093},
        ]
        
    for dest in sample_destinations:
            folium.Marker(
                [dest["lat"], dest["lon"]],
                popup=f"<b>{dest['name']}</b><br>Click to explore!",
                tooltip=dest["name"],
                icon=folium.Icon(color='blue', icon='info-sign')
            ).add_to(m)
        
    st_folium(m, width=None, height=400)


# ==================== VISUAL JOURNEY PAGE ====================
# ==================== DYNAMIC VISUAL JOURNEY ====================
# ==================== VISUAL JOURNEY PAGE ====================
elif page == "🖼️ Visual Journey":
    # Get destination from session state
    selected_dest = st.session_state.get('itinerary_destination', "Your Destination")
    search_term = selected_dest.replace(' ', '')
    
    st.markdown(f'<h1 class="main-header">🖼️ Journey to {selected_dest}</h1>', unsafe_allow_html=True)
    
    # Generate dynamic data
    dest_data = get_destination_metadata(selected_dest)
    
    # 1. Hero Image (FIXED PARAMETER)
    st.image(
        f"https://loremflickr.com/1200/400/{search_term},travel", 
        caption=f"Welcome to {selected_dest}", 
        use_container_width=True 
    )

    # 2. Dynamic Highlights (FIXED PARAMETERS)
    st.markdown("### 📸 Visual Highlights")
    gallery_cols = st.columns(3)
    visual_themes = ["Architecture", "Food", "Nature"]
    
    for i, col in enumerate(gallery_cols):
        with col:
            theme = visual_themes[i]
            theme_url = f"https://loremflickr.com/400/300/{search_term},{theme.lower()}?random={i}"
            st.image(theme_url, caption=f"{theme} in {selected_dest}", use_container_width=True)

    # 3. Quick Stats Rendering
    render_destination_stats(dest_data)

# ==================== AI ASSISTANT PAGE ====================
elif page == "🤖 AI Assistant":
    st.markdown('<h1 class="main-header">🤖 AI Travel Assistant</h1>', unsafe_allow_html=True)
    st.markdown("Ask me anything about travel planning, destinations, or tips!")
    
    st.markdown("---")
    
    # Chat interface
    chat_container = st.container()
    
    # Display chat history
 # Display chat history
    with chat_container:
        for message in st.session_state.chat_history:
            if message['role'] == 'user':
                st.markdown(f"""
                <div style="background-color: #E2E8F0; padding: 1rem; border-radius: 10px; margin-bottom: 0.5rem; text-align: right; color: #1E293B;">
                    <strong>You:</strong><br>{message['content']}
                </div>
                """, unsafe_allow_html=True)
            else:
                # FIXED: Light gray background with dark slate text for visibility
                st.markdown(f"""
                <div style="background-color: #F1F5F9; padding: 1.2rem; border-radius: 10px; margin-bottom: 1rem; border: 1px solid #CBD5E1; color: #1E293B !important;">
                    <strong style="color: #475569;">🤖 AI Travel Agent:</strong><br><br>
                    <div style="color: #1E293B !important; font-size: 1rem;">{message['content']}</div>
                </div>
                """, unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Input area
    col1, col2 = st.columns([5, 1])
    
    with col1:
        user_input = st.text_input(
            "Ask me anything:",
            placeholder="e.g., 'What are the best things to do in Paris?'",
            key="user_message",
            label_visibility="collapsed"
        )
    
    with col2:
        send_button = st.button("Send", type="primary", use_container_width=True)
    
    if send_button and user_input:
        # Add user message to history
        st.session_state.chat_history.append({
            'role': 'user',
            'content': user_input
        })
        
        # Get AI response (mock)
        ai_response = get_ai_response(user_input)
        
        # Add AI response to history
        st.session_state.chat_history.append({
            'role': 'assistant',
            'content': ai_response
        })
        
        st.rerun()
    
    # Quick action buttons
    st.markdown("### 💡 Quick Questions")
    
    quick_cols = st.columns(4)
    quick_questions = [
        "Hello, how can you help?",
        "Best budget travel tips?",
        "Plan my trip itinerary",
        "Tell me about Paris"
    ]
    
    for col, question in zip(quick_cols, quick_questions):
        with col:
            if st.button(question, use_container_width=True):
                st.session_state.chat_history.append({
                    'role': 'user',
                    'content': question
                })
                ai_response = get_ai_response(question)
                st.session_state.chat_history.append({
                    'role': 'assistant',
                    'content': ai_response
                })
                st.rerun()
    
    # Clear chat button
    if st.session_state.chat_history:
        st.markdown("---")
        if st.button("🗑️ Clear Chat History"):
            st.session_state.chat_history = []
            st.rerun()


# Footer
st.markdown("---")
st.markdown(
    "<div style='text-align: center; color: #888;'>✈️ AI Travel Agent | Your Journey Starts Here</div>",
    unsafe_allow_html=True
)

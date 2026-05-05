# 🌍 Explore Edge: AI Travel Agent

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11-3776AB?style=for-the-badge&logo=python&logoColor=white)
![AI](https://img.shields.io/badge/AI-Powered-blue?style=for-the-badge)
![License](https://img.shields.io/badge/license-MIT-green?style=for-the-badge)

**Not a Search Engine** - Your Personal AI-Powered Travel Planning Assistant

An intelligent, multi-page Streamlit web application that generates personalized travel itineraries, visualizes destinations on interactive maps, and provides AI-powered travel advice.

---

## ✨ Features

### 🏠 **Home - Smart Trip Planner**
- **Origin & Destination Selection**: Plan trips from anywhere to anywhere
- **Flexible Duration**: 1-21 days trip planning
- **Budget Customization**: Daily budget slider ($50-$1000)
- **Travel Style Selection**: Solo, Couple, Family, or Friends
- **Vibe Preferences**: Adventure, Relaxed, Culture, Luxury, Budget, Foodie
- **One-Click Generation**: Instant AI-powered itinerary creation

### 📋 **Itinerary - Day-by-Day Planning**
- **Complete Daily Breakdown**: Morning, afternoon, and evening activities
- **Budget Estimates**: Daily budget, food costs, and transport expenses
- **Seasonal Insights**: Weather-based travel advice for your dates
- **Activity Tips**: Personalized recommendations for each day
- **Expandable Cards**: Clean, organized view of your entire journey

### 🗺️ **Interactive Map**
- **Destination Visualization**: See your trip destination on an interactive map
- **Landmark Markers**: Pre-loaded popular attractions for major cities
- **Multi-City Support**: 30+ pre-configured destinations worldwide
- **Custom Coordinates**: Fallback for any destination globally
- **Color-Coded Markers**: Easy identification of different locations

### 🖼️ **Visual Journey**
- **Dynamic Hero Images**: Beautiful destination photography
- **Visual Highlights Gallery**: Architecture, Food, and Nature themes
- **Quick Stats Dashboard**: Best time to visit, vibe, budget, crowd levels
- **Responsive Design**: Optimized viewing on all screen sizes

### 🤖 **AI Travel Assistant**
- **Conversational Interface**: Chat with AI about travel questions
- **Pre-Built Knowledge**: Detailed info on Paris, Tokyo, New York, Rome, and more
- **Quick Action Buttons**: Fast access to common questions
- **Chat History**: Maintains conversation context
- **Travel Tips & Advice**: Budget tips, itinerary planning, destination guides
- **Ready for Real AI**: Easy integration with OpenAI or Google Gemini

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager
- Git (for cloning)

### Installation

1. **Clone the Repository**
```bash
git clone https://github.com/shravani22patil/ai-travel-agent.git
cd ai-travel-agent
```

2. **Create Virtual Environment** (Recommended)
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# macOS/Linux
python3 -m venv venv
source venv/bin/activate
```

3. **Install Dependencies**
```bash
pip install -r requirements.txt
```

4. **Run the Application**
```bash
streamlit run app.py --server.port 5000
```

5. **Open in Browser**
- Navigate to: `http://localhost:5000`
- Or use the URL shown in terminal

---

## 📦 Project Structure

```
ai-travel-agent/
├── app.py                      # Main Streamlit application
├── requirements.txt            # Python dependencies
├── .streamlit/
│   └── config.toml            # Streamlit configuration
├── README.md                  # This file
└── replit.md                  # Deployment documentation
```

---

## 🛠️ Tech Stack

| Technology | Purpose |
|-----------|---------|
| **Streamlit** | Web application framework |
| **Folium** | Interactive map visualization |
| **Pandas** | Data manipulation |
| **Pillow** | Image processing |
| **Python 3.11** | Core programming language |

---

## 📋 Dependencies

```txt
streamlit>=1.28.0
pandas>=2.0.0
numpy>=1.24.0
requests>=2.31.0
folium>=0.15.0
streamlit-folium>=0.15.0
Pillow>=10.0.0
```

---

## 🎯 Usage Guide

### Planning Your First Trip

1. **Navigate to Home Page**
   - Select origin and destination cities
   - Choose trip duration (1-21 days)
   - Set daily budget
   - Select travel style and vibes

2. **Generate Itinerary**
   - Click "Generate My Smart Itinerary"
   - AI creates personalized day-by-day plan
   - View in the Itinerary tab

3. **Explore on Map**
   - Go to Map page
   - See destination and landmarks
   - Explore interactive markers

4. **Visual Journey**
   - View destination images
   - Check quick stats
   - Get seasonal insights

5. **Ask AI Assistant**
   - Chat about travel questions
   - Get budget tips
   - Plan specific activities

---

## 🔧 Configuration

### Streamlit Settings

Edit `.streamlit/config.toml`:

```toml
[server]
port = 5000
address = "0.0.0.0"
headless = true
enableCORS = false

[theme]
primaryColor = "#667eea"
backgroundColor = "#FFFFFF"
secondaryBackgroundColor = "#F0F2F6"
textColor = "#262730"
```

---

## 🤖 AI Integration (Optional)

The app uses **rule-based mock responses** by default. To integrate real AI:

### Option 1: OpenAI GPT Integration

```python
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def get_ai_response(user_message: str) -> str:
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[
            {"role": "system", "content": "You are a helpful travel agent."},
            {"role": "user", "content": user_message}
        ]
    )
    return response.choices[0].message.content
```

### Option 2: Google Gemini Integration

```python
import google.generativeai as genai
import os

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

def get_ai_response(user_message: str) -> str:
    model = genai.GenerativeModel('gemini-pro')
    response = model.generate_content(user_message)
    return response.text
```

---

## 🌍 Supported Destinations

Pre-configured with coordinates and landmarks for:

**Major Cities**: Paris, Tokyo, New York, Rome, London, Sydney, Barcelona, Dubai, Singapore, Amsterdam, Bangkok, Istanbul, Cairo, Mumbai, Delhi, Los Angeles, San Francisco, Seoul, Hong Kong, Kyoto, Osaka

**Beach Destinations**: Goa, Bali, Hawaii, Maldives

**Cultural Hubs**: Athens, Venice, Florence, Berlin, Prague, Vienna, Lisbon, Madrid

And many more! Any destination can be entered - app uses fallback coordinates.

---

## 📊 Key Features Explained

### Budget Estimation Engine
- **Rule-based calculations** for different regions
- Western Europe: ~$120/day
- Southeast Asia: ~$45/day
- North America: ~$150/day
- Dynamic food and transport budgets

### Seasonal Intelligence
- **Winter**: Packing advice, daylight considerations
- **Summer**: Peak season warnings, heat tips
- **Spring**: Outdoor activity recommendations
- **Autumn**: Foliage and price balance insights

### Smart Destination Matching
- **Keyword detection** for city characteristics
- Beach destinations get tropical vibe tags
- Historical cities tagged for culture
- Adventure spots get nature recommendations

---

## 🎨 UI/UX Highlights

- **Gradient Headers**: Eye-catching purple-blue gradients
- **Responsive Cards**: Mobile-friendly design
- **Interactive Elements**: Hover effects and smooth transitions
- **Clean Typography**: Professional Playfair Display + Inter fonts
- **Status Indicators**: Real-time feedback during generation
- **Metric Displays**: Clear, scannable information cards

---

## 🚢 Deployment

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your repository
4. Click "Deploy"

### Deploy to Replit

1. Import repository to Replit
2. Ensure `.replit` config exists
3. Click "Run"

### Deploy to Heroku

```bash
# Create Procfile
echo "web: streamlit run app.py --server.port=$PORT --server.address=0.0.0.0" > Procfile

# Deploy
heroku create your-app-name
git push heroku main
```

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit changes (`git commit -m 'Add AmazingFeature'`)
4. Push to branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 🐛 Troubleshooting

### Port Already in Use
```bash
# Use different port
streamlit run app.py --server.port 8501
```

### Missing Dependencies
```bash
# Reinstall all packages
pip install -r requirements.txt --force-reinstall
```

### Folium Map Not Displaying
- Check internet connection (maps load from CDN)
- Ensure `streamlit-folium` is installed
- Clear browser cache

---

## 📝 Future Enhancements

- [ ] Real AI integration (OpenAI/Gemini)
- [ ] User authentication and saved trips
- [ ] Flight and hotel booking API integration
- [ ] Weather API for real-time conditions
- [ ] PDF export of itineraries
- [ ] Multi-language support
- [ ] Collaborative trip planning
- [ ] Budget tracking dashboard
- [ ] Photo upload for trip memories

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Author

**Your Name**
- GitHub: [@yourusername](https://github.com/shravani22patil)
- Email: shravanipatil580@gmail.com
- LinkedIn: [Your Profile]([https://linkedin.com/in/yourprofile](https://www.linkedin.com/in/shravani-patil-38791b286/))

---

## 🙏 Acknowledgments

- [Streamlit](https://streamlit.io/) for the amazing framework
- [Folium](https://python-visualization.github.io/folium/) for interactive maps
- [LoremFlickr](https://loremflickr.com/) for placeholder images
- Travel enthusiasts worldwide for inspiration

---

## 📞 Support

For issues, questions, or suggestions:
- Open an [Issue](https://github.com/shravani22patil/ai-travel-agent/issues)
- Start a [Discussion](https://github.com/shravani22patil/ai-travel-agent/discussions)

---

**⭐ Star this repo if you find it useful!**

**Made with ❤️ and Python**

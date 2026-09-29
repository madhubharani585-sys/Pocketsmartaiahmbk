💰 PocketSmart AI

«AI-powered budget planning and smart shopping assistant for Indian users.»

PocketSmart AI helps users plan their spending based on a fixed budget. It uses Google Gemini AI to create practical budget plans, estimate item prices, and generate shopping search links for popular platforms.

🌐 Live Demo

👉 "Open PocketSmart AI" 

✨ Features

🏠 Home Interior Planner

- Enter your total home budget
- Add multiple rooms and required items
- AI creates a room-wise budget allocation
- Suggests products from IKEA, Amazon and Flipkart
- Provides estimated prices and reasons for recommendations

🎉 Party Planner

- Set your total party budget
- Enter number of guests
- Select event type
- Add venue and city
- AI plans:
  - Catering
  - Decoration
  - Entertainment
  - Accommodation when required

💎 Jewelry Planner

- Set your jewelry budget
- Select occasion and style
- Add additional preferences
- Upload an outfit image optionally
- AI analyzes the outfit and recommends matching jewelry
- Provides shopping search links

🤖 AI Capabilities

PocketSmart AI uses Google Gemini to:

- Understand user requirements
- Create personalized budget plans
- Divide budgets into categories
- Recommend suitable products/services
- Estimate prices
- Explain why each recommendation fits
- Analyze an uploaded outfit image for jewelry recommendations

«Note: Product prices and availability can change. The application provides AI-generated estimates and search links rather than claiming real-time inventory or prices.»

🛠️ Tech Stack

Backend

- Python
- Flask
- Flask-CORS
- Google Gemini API
- python-dotenv

Frontend

- HTML5
- CSS3
- JavaScript
- Responsive UI

AI

- Google Gemini
- Gemini multimodal image input for outfit-based jewelry recommendations

Deployment

- Vercel

📁 Project Structure

PocketSmart_AI/
│
├── backend/
│   ├── app.py
│   ├── ai_service.py
│   └── requirements.txt
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── app.js
│
├── .gitignore
└── README.md

🔄 How It Works

User Input
    ↓
PocketSmart AI Frontend
    ↓
Flask Backend API
    ↓
Google Gemini AI
    ↓
AI Budget & Recommendation Plan
    ↓
Budget Allocation + Products + Search Links
    ↓
User

🚀 Run Locally

1. Clone the repository

git clone https://github.com/madhubharani585-sys/Pocketsmartaiahmbk.git
cd PocketSmart_AI

2. Create a virtual environment

python -m venv .venv

3. Activate the virtual environment

Windows PowerShell:

.venv\Scripts\Activate.ps1

4. Install dependencies

pip install -r backend/requirements.txt

5. Configure Gemini API

Create:

backend/.env

Add:

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash

«Never upload your ".env" file or Gemini API key to GitHub.»

6. Start the application

python backend/app.py

Open:

http://127.0.0.1:5000

🔐 Environment Variables

Variable| Description
"GEMINI_API_KEY"| Google Gemini API key
"GEMINI_MODEL"| Gemini model used by the application
"PORT"| Server port, optional

For GitHub, use an example file instead of the real ".env":

GEMINI_API_KEY=your_api_key_here
GEMINI_MODEL=gemini-2.5-flash

🔌 API Endpoints

Method| Endpoint| Purpose
GET| "/"| Serves the frontend
GET| "/api/health"| Checks backend health
POST| "/api/home"| Generates home interior plan
POST| "/api/party"| Generates party budget plan
POST| "/api/jewelry"| Generates jewelry recommendations

🛒 Supported Platforms

PocketSmart AI generates search links for platforms including:

- Amazon India
- Flipkart
- IKEA India
- Swiggy
- Zomato
- OYO

The application generates search URLs from AI-provided search queries instead of inventing direct product URLs.

🧪 Input Validation

The backend includes validation for:

- Minimum budget of ₹500
- Number of party guests
- Required planning items
- Supported image formats
- Maximum image upload size
- Invalid budget values
- Missing Gemini API configuration

Supported outfit image formats:

JPG
PNG
WEBP

Maximum upload size:

8 MB

📸 Project Modules

Home Decor

Users can specify:

Budget
Room
Item
Quantity

The AI generates a complete budget allocation and product recommendations.

Party

Users can specify:

Budget
Guests
Event
Venue
City

The AI creates a practical party spending plan.

Jewelry

Users can specify:

Budget
Occasion
Style
Notes
Outfit Image

The AI uses the optional outfit image to suggest coordinated jewelry.

🎯 Project Objective

The main objective of PocketSmart AI is to make budget planning easier by combining:

Budget → AI Analysis → Smart Recommendations → Shopping Search

Instead of manually comparing everything, users can provide their requirements and receive an organized spending plan.

🔮 Future Improvements

- User authentication
- Expense tracking
- Saved budget plans
- Monthly budget management
- Real-time product price comparison
- More shopping platforms
- Advanced recommendation system
- Personalized user profiles
- Mobile application
- Voice-based budget planning
- Multi-language support

👨‍💻 Developer

Akshaya R

Computer Science Student
India

📄 License

This project is created for educational and project demonstration purposes.
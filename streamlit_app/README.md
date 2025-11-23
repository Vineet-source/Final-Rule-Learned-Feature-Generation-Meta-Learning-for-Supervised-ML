# Bitcoin Fraud Detection Dashboard

Enterprise-grade fraud detection system with animated UI, combining XGBoost ML models with transparent rule engines.

## 🚀 Quick Start

### Local Development

1. **Install dependencies:**
```bash
pip install -r requirements.txt
```

2. **Run the app:**
```bash
streamlit run Home.py
```

The app will open at `http://localhost:8501`

### Deploy to Streamlit Cloud

1. Push your code to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Connect your GitHub repository
4. Set main file path: `streamlit_app/Home.py`
5. Deploy!

## 📁 Project Structure

```
streamlit_app/
├── Home.py                          # Main landing page
├── pages/
│   ├── 1_Real_Time_Verification.py  # Transaction verification
│   ├── 2_Risk_Appetite_Tuner.py     # Policy tuning dashboard
│   └── 3_Forensic_Inspector.py      # Case analysis
├── assets/
│   └── styles.css                   # Global styles
├── .streamlit/
│   └── config.toml                  # Streamlit configuration
└── requirements.txt                 # Python dependencies
```

## 🎨 Features

- **Animated Background**: Smooth wave animations with floating particles
- **Theme Toggle**: Dark/Light mode switcher
- **Glassmorphism UI**: Modern card designs with backdrop blur
- **Real-Time Analytics**: Live KPI updates and interactive charts
- **Responsive Design**: Works on desktop, tablet, and mobile

## 🔧 Configuration

Edit `.streamlit/config.toml` to customize:
- Theme colors
- Server settings
- Browser behavior

## 📊 Pages

### 1. Home
Overview dashboard with system statistics and feature cards

### 2. Real-Time Verification
Submit transactions and get instant fraud detection results with:
- ML probability scores
- Rule engine analysis
- Final hybrid verdicts

### 3. Risk Appetite Tuner
Dynamically adjust rule thresholds and weights:
- Live performance metrics
- Confusion matrix visualization
- Decision space analysis

### 4. Forensic Inspector
Deep-dive into specific cases:
- False positive/negative analysis
- Rule contribution breakdown
- Transaction profiling

## 🌐 Deployment Options

### Streamlit Cloud (Recommended)
- Free hosting for public apps
- Automatic updates from GitHub
- Built-in authentication

### Docker
```bash
docker build -t fraud-detection-app .
docker run -p 8501:8501 fraud-detection-app
```

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

## 🔗 Backend Integration

The app connects to a FastAPI backend. Update the API URL in:
- `pages/1_Real_Time_Verification.py` (line 42)

Default: `http://localhost:8000/transactions`

## 📝 Notes

- Requires `simulation_data.csv` for Risk Appetite Tuner and Forensic Inspector
- Backend API must be running for Real-Time Verification
- All animations are CSS-based for optimal performance

## 🎯 Performance

- Page load: < 2s
- Animation FPS: 60fps
- API response: < 100ms

## 📄 License

MIT License - feel free to use and modify!

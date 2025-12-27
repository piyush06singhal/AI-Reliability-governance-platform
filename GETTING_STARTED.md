# Getting Started

## Quick Setup (5 minutes)

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Configure API Keys

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Edit `.env` and add your API keys:

```bash
OPENAI_API_KEY=your_actual_openai_key
ANTHROPIC_API_KEY=your_actual_anthropic_key
```

**⚠️ IMPORTANT**: Never commit the `.env` file to Git! It's already in `.gitignore`.

### 3. Run the Dashboard

```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`

---

## Testing

### Verify Installation

```bash
python verify_installation.py
```

### Run Test Suite

```bash
python test_platform.py
```

---

## Using the Dashboard

### 7 Pages Available:

1. **📊 System Overview** - Health metrics and trends
2. **🔍 Interaction Explorer** - Browse all LLM interactions
3. **⚠️ Risk & Safety** - Risk analysis and detection
4. **💰 Cost & Performance** - Cost tracking and optimization
5. **🛡️ Policy Manager** - Configure governance policies
6. **📈 Feedback & Learning** - Quality metrics and drift detection
7. **🧪 Test Interaction** - Send test requests

### Quick Test:

1. Go to "🧪 Test Interaction" page
2. Click a quick scenario button (e.g., "🚨 Injection Attack")
3. Click "Send Request"
4. View risk assessment and policy decision

---

## Deployment to Streamlit Cloud

### 1. Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit"
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO.git
git push -u origin main
```

### 2. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Sign in with GitHub
3. Click "New app"
4. Select your repository
5. Set main file: `app.py`
6. Click "Advanced settings" → "Secrets"
7. Add your API keys:

```toml
OPENAI_API_KEY = "your_actual_key"
ANTHROPIC_API_KEY = "your_actual_key"
```

8. Click "Deploy!"

---

## Supported Models

### OpenAI

- gpt-4
- gpt-4-turbo
- gpt-3.5-turbo

### Anthropic

- claude-3
- claude-3-opus
- claude-3-sonnet
- claude-3-haiku

---

## Features

### Risk Detection

- Prompt injection attempts
- Hallucination indicators
- Unsafe content
- Data leakage (PII, credentials)

### Policy Enforcement

- Block critical risks
- Fallback for high risks
- Rewrite medium risks
- Configurable thresholds

### Cost Optimization

- Real-time tracking
- Cost by model
- Anomaly detection
- Optimization recommendations

### Feedback & Learning

- User feedback collection
- Quality metrics tracking
- Drift detection
- Threshold auto-adjustment

---

## Troubleshooting

### API Errors

- Verify API keys are correct in `.env`
- Check API key permissions
- Monitor API usage limits

### Import Errors

```bash
pip install -r requirements.txt
```

### Port Already in Use

```bash
streamlit run app.py --server.port 8502
```

---

## Security

- ✅ API keys in `.env` (not committed)
- ✅ `.env` in `.gitignore`
- ✅ Secrets template provided
- ✅ No hardcoded credentials

---

## Next Steps

1. Explore all 7 dashboard pages
2. Test with different prompts
3. Configure policies
4. Monitor costs
5. Collect feedback
6. Deploy to production

---

For more details, see [README.md](README.md)

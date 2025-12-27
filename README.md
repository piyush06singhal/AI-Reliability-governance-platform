# 🛡️ AI Reliability & Governance Platform

> Production-grade system for monitoring, analyzing, and controlling Large Language Model (LLM) behavior in enterprise applications.

[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/streamlit-1.31.0-FF4B4B.svg)](https://streamlit.io)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 🚀 Quick Start

```bash
# Install dependencies
pip install -r requirements.txt

# Set up environment variables
cp .env.example .env
# Edit .env and add your API keys

# Run the dashboard
streamlit run app.py
```

## ✨ Features

### Core Components

- **LLM Gateway** - Provider-agnostic interface (OpenAI, Anthropic, Mock)
- **Risk Detection** - Identifies prompt injection, hallucinations, unsafe content, data leakage
- **Policy Enforcement** - Configurable guardrails (block, fallback, rewrite)
- **Cost Optimization** - Real-time tracking, anomaly detection, recommendations
- **Audit & Compliance** - Immutable logs, full traceability, compliance reports
- **Feedback & Learning** - Continuous improvement with drift detection
- **Enterprise Dashboard** - 7-page professional UI with dark mode

### Dashboard Pages

1. **📊 System Overview** - Health metrics, risk distribution, policy enforcement
2. **🔍 Interaction Explorer** - Browse and filter all LLM interactions
3. **⚠️ Risk & Safety** - Risk analysis, timeline, evidence details
4. **💰 Cost & Performance** - FinOps analytics, optimization recommendations
5. **🛡️ Policy Manager** - Configure and monitor governance policies
6. **📈 Feedback & Learning** - Quality metrics, drift detection, threshold optimization
7. **🧪 Test Interaction** - Test requests with quick scenarios

## 🔧 Configuration

### Environment Variables

Create a `.env` file:

```bash
# LLM Provider API Keys
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Platform Configuration
LOG_LEVEL=INFO
AUDIT_LOG_DIR=audit_logs
```

### Supported Models

**OpenAI:**

- gpt-4
- gpt-4-turbo
- gpt-3.5-turbo

**Anthropic:**

- claude-3
- claude-3-opus
- claude-3-sonnet
- claude-3-haiku

## 📊 Architecture

```
Application → LLM Gateway → Risk Detection → Policy Enforcement →
Cost Monitor → Audit Logger → Response
```

### Components

- **Gateway**: Provider-agnostic LLM interface
- **Risk Engine**: 4 detection categories (injection, hallucination, unsafe, leakage)
- **Guardrails**: Configurable policies with 4 actions
- **Cost Monitor**: Real-time tracking and optimization
- **Audit Logger**: Immutable compliance logs
- **Feedback Engine**: Continuous learning and drift detection

## 🧪 Testing

```bash
# Verify installation
python verify_installation.py

# Run test suite
python test_platform.py

# Start dashboard
streamlit run app.py
```

## 🚢 Deployment

### Streamlit Cloud

1. Push to GitHub
2. Connect to [Streamlit Cloud](https://share.streamlit.io)
3. Add secrets in Streamlit Cloud dashboard:
   - `OPENAI_API_KEY`
   - `ANTHROPIC_API_KEY`
4. Deploy!

### Docker

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 8501
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

```bash
docker build -t ai-governance-platform .
docker run -p 8501:8501 --env-file .env ai-governance-platform
```

## 📚 Documentation

- **GETTING_STARTED.md** - Detailed setup and usage guide
- **API Documentation** - See code docstrings
- **Architecture** - See `src/` directory structure

## 🎯 Use Cases

- **Enterprise LLM Deployment** - Govern all LLM interactions
- **Compliance Requirements** - Maintain audit trails
- **Cost Optimization** - Identify expensive patterns
- **Risk Management** - Prevent harmful outputs
- **Quality Monitoring** - Track performance over time

## 🔒 Security

- API keys stored in environment variables
- Immutable audit logs
- Full request traceability
- Policy-based access control
- Data leakage detection

## 📈 Monitoring

The platform tracks:

- Risk scores and categories
- Cost per request and by model
- Latency and performance
- Policy enforcement actions
- Quality metrics and drift
- User feedback and ratings

## 🤝 Contributing

This is a production-ready platform. For enhancements:

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## 📄 License

MIT License - See LICENSE file for details

## 🙏 Acknowledgments

Built with:

- [Streamlit](https://streamlit.io) - Dashboard framework
- [Plotly](https://plotly.com) - Interactive visualizations
- [Pydantic](https://pydantic.dev) - Data validation
- [FastAPI](https://fastapi.tiangolo.com) - API framework

## 📞 Support

For issues or questions:

1. Check GETTING_STARTED.md
2. Run `python verify_installation.py`
3. Review error logs in terminal
4. Open an issue on GitHub

---

**Status**: Production-Ready ✅  
**Version**: 2.0.0  
**Python**: 3.11+  
**License**: MIT

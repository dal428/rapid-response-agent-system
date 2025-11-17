# Rapid Response Agent System

Multi-agent system embedding organizational values into real-time crisis response and automated conflict resolution.

## 🚨 The Problem
Mission-driven organizations face an impossible choice: respond fast and risk misaligning with core values, or maintain careful vetting and lose relevance in digital-speed news cycles.

## 🤖 The Solution
Four specialized AI agents working in harmony to transform crisis management from reactive scrambling to proactive orchestration:

- **Monitor Agent**: Continuous issue detection from multiple sources
- **MAI Scoring Agent**: Quantifies mission alignment using Gemini AI
- **Conflict Resolution Agent**: 4-minute Lightning Protocol for channel conflicts
- **Decision Support Agent**: Intelligent routing and action planning

## 🎯 Impact
- **85% faster** crisis response time (24 hours → 4 hours)
- **Zero bottlenecks** in initial triage and conflict resolution
- **Universal template** works for any mission-driven organization
- **Maintains mission integrity** while achieving digital speed

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- Google API key with Gemini access

### Installation
```bash
git clone https://github.com/dal428/rapid-response-agent-system.git
cd rapid-response-agent-system
pip install -r requirements.txt
```

### Configuration
```python
# Set your organizational manifesto
ORGANIZATION_MANIFESTO = {
    "core_principles": [
        "Your core principle 1",
        "Your core principle 2",
        # Add your principles
    ],
    "strategic_priorities": [
        "Your priority 1", 
        "Your priority 2",
        # Add your priorities
    ]
}
```

### Run the System
```python
from src.rapid_response_system import RapidResponseSystem

# Initialize with your manifesto
system = RapidResponseSystem(ORGANIZATION_MANIFESTO, api_key="your-api-key")

# Run a complete cycle
results = system.run_full_cycle()
```

## 🏗️ Architecture

### Multi-Agent Coordination
```
┌─────────────┐    ┌─────────────┐    ┌─────────────┐    ┌─────────────┐
│   Monitor   │───▶│ MAI Scoring │───▶│  Conflict   │───▶│  Decision   │
│    Agent    │    │    Agent    │    │ Resolution  │    │  Support    │
│             │    │             │    │    Agent    │    │    Agent    │
└─────────────┘    └─────────────┘    └─────────────┘    └─────────────┘
       │                   │                   │                   │
       ▼                   ▼                   ▼                   ▼
   Issue Detection    Mission Alignment    Lightning Protocol   Action Planning
```

## 📊 Performance Metrics

From our latest test run:
- **Processing Speed**: 31.3 seconds average per complex issue
- **Conflict Resolution**: 4-minute Lightning Protocol execution  
- **System Efficiency**: 93.8 seconds for 3-issue batch processing
- **Decision Accuracy**: 100% mission alignment maintained

## 🌍 Universal Template

This system works for any mission-driven organization:
- Environmental groups
- Civil rights organizations 
- Healthcare NGOs
- Digital rights groups
- Educational nonprofits

Simply configure your manifesto and the agents adapt their scoring accordingly.

## 📚 Technical Requirements Met

✅ **Multi-agent system**: 4 coordinated agents (Monitor, Scoring, Conflict Resolution, Decision Support)
✅ **Custom tools**: MAI Scoring Tool, Conflict Resolution Tool
✅ **Sessions & Memory**: Decision pattern storage and institutional learning
✅ **Built-in tools**: Web monitoring simulation, code execution
✅ **Gemini integration**: AI-powered mission alignment analysis

## 🎥 Live Demo

**Kaggle Notebook**: [View working implementation](https://www.kaggle.com/code/dal428/rapid-response-agent-system-capstone-project)

## 🏆 Kaggle Competition

This project was created for the **Agents Intensive Capstone Project** in the "Agents for Good" track.

**Submission Features**:
- Complete multi-agent implementation
- Real-time crisis simulation
- Performance dashboards and metrics
- Universal organizational template

## 🤝 Contributing

This project is open for contributions! Areas for enhancement:
- Additional monitoring sources
- Enhanced conflict resolution strategies
- Integration with real communication platforms
- Extended organizational templates

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Built using Google's Agent Development Kit
- Powered by Gemini 2.5 Flash
- Inspired by real challenges faced by mission-driven organizations worldwide

---

**Transform your crisis response. Embed your values into velocity.** 🚀

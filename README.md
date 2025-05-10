[![Build Status](https://github.com/Tech-Parivartan/r2r-protocol/actions/workflows/ci.yml/badge.svg)](https://github.com/Tech-Parivartan/r2r-protocol/actions/workflows/ci.yml)
[![PyPI version](https://badge.fury.io/py/r2r.svg)](https://pypi.org/project/r2r/)
[![Documentation Status](https://readthedocs.org/projects/r2r-protocol/badge/?version=latest)](https://r2r-protocol.readthedocs.io/en/latest/?badge=latest)



# 🤖 Robot-to-Robot (R2R) Communication Protocol

> A standardized communication protocol for autonomous robots to exchange data, coordinate tasks, and collaborate in real-time environments.

[![License](https://img.shields.io/badge/license-MIT-blue.svg )](https://opensource.org/licenses/MIT )

The **R2R Protocol** enables seamless robot-to-robot interaction across industrial automation, swarm robotics, logistics, and multi-agent systems. It defines structured message formats, negotiation logic, discovery mechanisms, and extensible APIs.

## 🧩 Features

✅ Structured JSON/Protobuf messaging
✅ Supports TCP/IP, UDP, MQTT, WebSocket
✅ Task negotiation (auction, consensus)
✅ Status & telemetry updates
✅ Optional authentication
✅ Extensible via plugins/modules
✅ Docker-ready
✅ GitHub Actions CI/CD integration
✅ Python SDK published on PyPI


## 📦 SDKs

| Language     | Status       | Directory     |
|--------------|--------------|---------------|
| 🐍 Python     | ✅ Stable     | `sdk/python`  |
| 🦀 Rust       | ⏳ Coming Soon | —             |
| 🖥️ C++        | ⏳ Coming Soon | —             |
| 🐹 Go         | ⏳ Coming Soon | —             |
| 🌐 JavaScript | ⏳ Coming Soon | —             |

> Want to contribute an SDK in your favorite language? [Check out the contributing guide](CONTRIBUTING.md).


## 📘 Documentation

See the full [Protocol Specification](docs/spec.md).


## 🚀 Quick Start (Python SDK)

🔧 Install from PyPI

```bash
pip install r2r-protocol
```


```bash
from r2r_protocol import RobotClient

# Connect to R2R server
client = RobotClient(robot_id="bot_01", host="192.168.1.10")

# Send status update
client.send_status({
    "battery": 85,
    "position": {"x": 10.2, "y": 5.1},
    "task_progress": 0.75
})
```

## 🐳 Run with Docker
You can run the R2R SDK in a Docker container:
```bash
docker build -t r2r-sdk .
docker run -it r2r-sdk
```
This will start a sample client instance and verify that the SDK works.


## ⚙️ Development Setup

To contribute or extend the protocol:

1. Clone the repo
```bash
git clone https://github.com/Tech-Parivartan/r2r-protocol.git 
cd r2r-protocol
```

2. Set up Python environment
```bash
cd sdk/python
pip install -e .
```

3. Install test dependencies
```bash
pip install pytest
```


## 🧪 Running Tests
Run unit tests using:

```bash
cd tests
python -m pytest test_messages.py
```


## 🛠️ Contributing

We welcome contributions! Please read our [here](CONTRIBUTING.md) to get started.

**Ways to Help**

- [ ] Report bugs and suggest features
- [ ] Write more comprehensive tests
- [ ] Improve documentation and architecture diagrams
- [ ] Build example applications and integrations

Please open an issue before submitting a PR so we can align on scope.

## 📜 License

This project is licensed under the MIT License – see the (LICENSE) file for details.

## 📬 Feedback & Support

Have questions, feature requests, or want to share how you're using R2R?

- Open an issue on GitHub
- Join our Discord / Slack (coming soon)
- Email us at rajkumar.rawal@techparivartan.com.np
- Follow us on Twitter [@TechParivartan](https://x.com/TechParivartan)
- Follow us on LinkedIn [Tech Parivartan](https://www.linkedin.com/company/tech-parivartan/)


## Upcoming Features

- [ ] Enhanced security features
- [ ] Visualization tools for monitoring robot interactions
- [ ] Support for more programming languages
- [ ] Improved error handling and logging
- [ ] Integration with popular robotics frameworks (ROS, OpenRAVE)



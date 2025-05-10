# 📜 R2R Protocol Specification

## 🧾 Overview

This document defines the **Robot-to-Robot (R2R) Communication Protocol**, a lightweight standard for structured communication between autonomous robotic agents.

## 📡 Message Format

All messages follow a consistent structure:

```json
{
  "header": {
    "version": "1.0",
    "timestamp": 1718000000,
    "source_id": "robot_001",
    "target_id": "robot_002"
  },
  "type": "status/task_request/task_response/command/negotiation/error",
  "payload": { ... }
}


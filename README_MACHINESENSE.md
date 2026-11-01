# MachineSense — AI-Powered Predictive Maintenance Dashboard

> **Interactive Internship Capstone Project**  
> An industrial telemetry web dashboard connecting **IoT Sensor Simulation**, **Miniature RAG (Retrieval-Augmented Generation)**, **Prompt Engineering Pipelines**, **Claude Foundation Model Diagnostics**, and **Enterprise Cloud Architecture Mapping (IaaS / PaaS / MaaS)**.

---

## 🚀 Quick Start: How to Open the Website

You can run MachineSense in two ways:

### Method 1: Direct Browser Launch (Zero Installation Required)
Simply double-click [`index.html`](file:///c:/Users/dheer/Desktop/code/AI_Assisent/index.html) or run [`run_dashboard.bat`](file:///c:/Users/dheer/Desktop/code/AI_Assisent/run_dashboard.bat).
It opens instantly in Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari with full interactivity, real-time Chart.js telemetry, audio alerts, and simulation engine!

### Method 2: Via Django Web Server
If you prefer running through the existing Django application:
```bash
python manage.py runserver
```
Then navigate to:
**`http://127.0.0.1:8000/machinesense/`**

---

## 🎯 How the 5 Internship Core Pillars Are Demonstrated

| Slide Topic | Implementation in MachineSense | Where to See It in the UI |
| :--- | :--- | :--- |
| **1. Live Sensor Simulation** | 3 industrial machines (Atlas Copco Compressor, 5-Axis CNC Spindle, Conveyor Induction Motor) with continuous Brownian stochastic drift, ISO vibration thresholds, and interactive fault injection. | **Section 01**: Machine Cards & Real-Time Sparkline Charts |
| **2. Mini-RAG Knowledge Retrieval** | In-memory industrial knowledge base covering ISO 10816 & OEM SOPs (bearing wear, misalignment, unbalance, thermal overload, cavitation). Automatically filters and scores relevant manuals based on live symptoms. | **Section 02**: Step 2 of the Prompt Pipeline & Knowledge Base Explorer Modal |
| **3. Prompt Engineering Pipeline** | Live 4-stage visual pipeline showing how raw sensor values + retrieved SOP excerpts + plant engineer inquiries are synthesized into a structured LLM prompt. | **Section 02 / 03**: Live Step-by-Step Flow Bar & Raw JSON Payload Inspector |
| **4. Claude Foundation Model Call** | Generates root cause analyses, ISO compliance ratings, and step-by-step maintenance SOP actions via direct Claude Messages API (`claude-3-5-sonnet`) or high-accuracy offline simulator. | **Section 04**: Claude Diagnostic Console & Terminal Output |
| **5. Cloud Computing Mapping** | Interactive visual architecture mapping each component to modern cloud primitives: IaaS (Edge Gateways/MQTT VMs), PaaS (AWS IoT Core, Timestream, Pinecone), and MaaS (Hosted Foundation Model API). | **Section 05**: Collapsible Architecture Diagram & Comparison Matrix |

---

## ⚡ Interactive Fault Scenarios (Test with One Click)

Use the top action bar to inject simulated anomalies into the plant:

1. **⚡ Bearing Race Wear (CNC Spindle)**:
   - Spindle vibration spikes to > 6.0 mm/s.
   - Acoustic kurtosis rises above 4.5.
   - RAG matches `SOP-01 (Bearing Race Wear & Spallation ISO 10816-3)`.
   - Claude recommends emergency controlled spindown and ceramic hybrid replacement.

2. **⚡ Shaft Misalignment (Conveyor Drive Motor)**:
   - Conveyor axial vibration spikes with 2X RPM harmonic signature.
   - Motor drive-end temperature rises.
   - RAG matches `SOP-02 (Shaft Misalignment: Angular & Parallel Coupling Offset)`.
   - Claude outputs reverse-dial laser alignment procedures and shim adjustments.

3. **⚡ Dynamic Imbalance (CNC Spindle)**:
   - Pure 1X rotational frequency sinusoidal peak.
   - RAG matches `SOP-03 (Rotor Dynamic Imbalance ISO 1940-1 Grade G2.5)`.
   - Claude guides dynamic dual-plane field balancing and arbor cleaning.

4. **⚡ Thermal Overload (Atlas Compressor)**:
   - Discharge air temp surges towards 95°C+ trip limit.
   - RAG matches `SOP-04 (Motor Stator Thermal Overload & Cooling Degradation)`.
   - Claude recommends immediate load shedding and heat exchanger blowout.

5. **⚡ Pump Cavitation (Compressor / Booster)**:
   - High-frequency broadband hiss and discharge pressure oscillations (±1.5 bar).
   - RAG matches `SOP-05 (Centrifugal Cavitation & Suction Starvation)`.
   - Claude recommends suction strainer inspection and NPSH margin verification.

6. **🔄 Normal Baseline (Reset All)**:
   - Restores all 3 machines to nominal ISO Zone A healthy status.

---

## 🛠️ Key Technical Features

- **Simulation Engine**: Mathematical Gaussian random walk with Brownian drift and adjustable time dilation (1x, 2x, 5x speed).
- **Audio Alert Synthesizer**: Uses Web Audio API oscillator to produce warning beeps when machines enter critical status (toggleable).
- **Mini-RAG Matching Engine**: Tokenizes incoming query and live anomaly signals, ranks knowledge base articles with relevance scoring, and injects only the top matching SOPs into prompt context.
- **Dual Inference Mode**:
  - **Built-in Offline Claude Engine**: Ready for live presentations and offline demos without requiring an API key.
  - **Direct Claude API**: Dispatches actual HTTP POST requests to `https://api.anthropic.com/v1/messages` using `anthropic-dangerous-direct-browser-access: true`.
- **Incident Maintenance Report**: One-click printable formal inspection sheet with full ISO-9001 style audit trail.

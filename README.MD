# 🕹️ LOGIC-CRAFT

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![Pygame](https://img.shields.io/badge/pygame-2.0+-green.svg)](https://www.pygame.org/)

**Logic-Craft** is a highly interactive, beautifully designed 2D logic gate simulator built entirely from scratch in Python using the **Pygame** framework. Featuring a modular object-oriented design, a custom layout UI, real-time signal propagation, and a proprietary canvas saving system, Logic-Craft turns digital electronics engineering into an engaging, sandbox experience.

---

## 📸 Demo & Screenshots

### Main Menu & Canvas Preview
| Main Menu Layout | Live Logic Simulation |
| :---: | :---: |
| <img src="image_725e62.jpg" width="400" alt="Logic-Craft Title Screen"/> | <img src="image_726206.png" width="400" alt="Logic Simulation Sandbox"/> |


> 🎬 **Watch the 10-Second Showcase Video:** Look at `demo.mp4` (or your uploaded video link here) inside the repository root to see the real-time simulation updates, wire placement, and canvas scaling in action!

---

## 🚀 Features

### 1. Interactive Simulation Canvas
* **Dual Execution Modes:**
  * **Edit Mode (Green Run Button):** A full blueprint layout sandbox. Instantly place gates, paint wires, drop input switches, or remove unwanted components using the real-time toolbar.
  * **Running Mode (Red Stop Button):** Lock the grid configuration and interact with input switches. Flip toggles between `0` and `1` to watch high and low signals dynamically update across complex connected paths.
* **Smart Placement & Orientations:** Rotate components ($90^\circ$ steps) and dynamically cycle through different wire geometries (Straight, Left Curved, Right Curved) to build dense, optimized circuit paths.

### 2. Multi-Craft File Management (`.craft`)
* Save and load multiple workspaces dynamically from a custom pop-up window dashboard.
* **Custom Serialization Engine:** Utilizes Python's `pickle` module to compress and serialize complex Python object dictionaries mapping grid matrices directly into low-overhead binary `.craft` files.
* Dynamically adjust canvas configurations safely up to larger grids (e.g., $40 \times 40$) instantly via the **Edit Canvas** popup layout.

---
## 🎛️ The Digital Component Catalog

Logic-Craft supports a comprehensive block-grid component array consisting of **7 core operational Logic Gates**, input triggers, and flexible wiring links:

| Component Type | Symbol / Syntax | Description | Inputs |
| :--- | :---: | :--- | :---: |
| **NOT Gate** | $\overline{A}$ | Inverts the incoming digital signal state. | 1 |
| **AND Gate**| $A \cdot B$ | Outputs high state only if both inputs are high. | 2 |
| **OR Gate** | $A + B$ | Outputs high state if at least one input is high. | 2 |
| **NAND Gate** | $\overline{A \cdot B}$ | Inverted AND logic gate sequence. | 2 |
| **NOR Gate** | $\overline{A + B}$ | Inverted OR logic gate sequence. | 2 |
| **XOR Gate** | $A \oplus B$ | Outputs high state if inputs are mismatched. | 2 |
| **XNOR Gate** | $\overline{A \oplus B}$ | Outputs high state if inputs match identical states. | 2 |
| **Toggle Switch** | `switch 0 \| 1` | Primary interactive digital input source block. | 0 |
| **Signal Wire** | `WIRE` | Conductive routing path supporting custom orientations. | Dynamic |

---

## 🛠️ Technical Architecture & File Structure

This project follows a strict object-oriented, clean, modular programming blueprint. Global states, reusable UI render, and grid validation layouts are cleanly isolated across files:

```text
📂 logic-craft/
│
├── 📂 Assets/           # System UI elements and customized image assets
├── 📂 craft/            # Serialized circuit saves utilizing binary (.craft) layout
├── 📂 font/             # Embedded TTF font files for modular multi-resolution UI text
│
├── 📄 main.py           # Main framework bootstrapping loop and centralized state controller
├── 📄 home_page.py      # Landing hub screen context handling and initial configurations
├── 📄 canvas.py         # Sandbox simulation engine containing Edit/Run rendering systems
├── 📄 core_tools.py     # Proprietary custom button wrappers and asset graphical rendering
├── 📄 load_assets.py    # Central asset parsing manager allocating cached graphical vectors
├── 📄 setting.py        # Target context placeholder for engine configurations
├── 📄 help.py           # User informational menu and controls directory layout
└── 📄 requirements.txt  # Automated module mapping configuration file
```

## 📦 Installation & Getting Started

### Prerequisites
Ensure you have Python 3.8 or higher installed on your operating system.

### Step 1: Clone the Repository
```bash
git clone [https://github.com/YOUR_GITHUB_USERNAME/logic-craft.git](https://github.com/YOUR_GITHUB_USERNAME/logic-craft.git)
cd logic-craft
```

### Step 2: Install Dependencies
Install all required UI handling and game engine modules via pip:
```bash
pip install -r requirements.txt
```

### Step 3: Run the Application
Boot the game engine instantly via the main entry file:
```bash
python main.py
```

## 🗺️ Roadmap & Upcoming Features
* [ ] **Audio Engine Integration:** Add responsive mechanical click sound effects, UI alerts, and calming ambient synth music options.
* [ ] **Visual Themes:** Expand the settings layer with custom workspace themes (Dark, Light, High-Contrast Blueprint modes).
* [ ] **Settings Profiles:** Real-time FPS limits toggles, customizable window dimensions, and master audio adjustments.
* [ ] **Sub-circuit Packing:** Multi-grid structural compilation allowing users to package complex logic loops (like Full Adders) into unified custom macro-blocks.

---

## 🤝 Contributing & Support

Contributions, feedback, and optimization pull requests are welcome! If you find a bug, logic error, or wire rendering issue, feel free to submit it through the repo:

1. **Report Bugs:** Open a structured report via the [GitHub Issues](https://github.com/YOUR_GITHUB_USERNAME/logic-craft/issues) section.
2. **Submit Adjustments:** Fork the repository, apply your changes inside an isolated patch branch, and submit a formal Pull Request.

---

## 📄 License

This project is open-source and licensed under the terms of the [MIT License](LICENSE). 

Developed with ❤️ by **Technical Coderji** © 2026.
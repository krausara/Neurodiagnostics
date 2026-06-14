# Computational Neuro-Diagnostics: Exercise 01

This repository contains the codebase and scientific report for **Exercise 01: EEG Acquisition, Processing & Visualization**, developed as part of the Computational Neuro-Diagnostics course at the Chair for Neurorehabilitation, University of Augsburg.

## 🔍 Project Overview
The objective of this exercise is to gain hands-on experience in recording EEG data, preprocessing raw signals, and performing spectral/independent component analyses. The project is split into three main segments:
1. **Publicly Available Data:** Loading, filtering, re-referencing, and plotting PSD/alpha topography for the PhysioNet EEG Motor Movement/Imagery Dataset.
2. **Own Clean Resting-State Data:** Analyzing 2-minute eyes-open vs. eyes-closed recordings acquired using the Starstim system to evaluate physiological differences.
3. **Own Noisy Data:** Utilizing Independent Component Analysis (ICA) to isolate and eliminate ocular (blinks, lateral movements), muscular (chewing), and channel-noise artifacts from a deliberate artifact-laden recording.

## 📁 Repository Structure
To ensure reproducibility, please maintain the following file hierarchy:

```text
├── data/                  # Local directory for storing all EEG datasets (relative paths)
│   ├── public_data/
│   │   └──  {subject}/
│   └── own_data/
│   │   ├── eyes_open.nedf     
│   │   ├── eyes_closed.nedf    
│   │   └── artifacts.nedf     
├── analysis.py         
# Core functions (filtering, rereferencing, computepsd, topoalpha, applyica)
├── noisy_analysis.py
# Main script for artifact.nedf analysis
├── public_analysis.py 
# Main script for analysing the public dataset
├── own_analysis.py 
# Main script for own resting state recordings
├── requirements.txt       # Allowed environment package dependencies
└── README.md              # Project documentation (this file)
```

## 🛠️ Prerequisites & Installation

1. Clone repository / use the provided code.zip
```bash
git clone https://github.com/krausara/Neurodiagnostics.git
cd Neurodiagnostics
```
2. Set up virtual environment
```bash
python -bin venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate
```

3. Install dependencies
```sh
pip install --upgrade pip
pip install -r requirements.txt
```

## 🚀 How to Run the Code
The analysis pipeline uses strict relative paths to verify execution across different workstations without throwing path errors.  

To run the complete data processing, analysis, and visualization pipeline, execute each main script independently from the root directory:

```bash
python public_analysis.py
python own_analysis.py
python noisy_analysis.py
```

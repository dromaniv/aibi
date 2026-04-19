# Lab 4 – How to Run

## Prerequisites

- Python 3.10+
- `pip` and `venv`

## Setup

```bash
cd lab4
git clone https://github.com/sysmon37/aibi-dhi-simulator
python3 -m venv .venv
source .venv/bin/activate
pip install gymnasium pandas numpy matplotlib scikit-learn stable-baselines3 ipykernel
cp aibi-dhi-simulator/environment/fogg_behavioral_model.py src/environment/
```

## Run the experiments

```bash
cd src
```
Open `profile_experiments.ipynb` in VS Code (or Jupyter) and run all cells.
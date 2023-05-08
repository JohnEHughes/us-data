# Activate WSL
wsl -d Ubuntu

# Activate Venv
. ~/Documents/coding/venvs/us-data-venv/bin/activate

# us-data
streamlit run src/home.py --server.headless true
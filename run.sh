#!/bin/bash

sl=$(pip list | grep streamlit)

if [ -z "$sl" ]; then
    echo "Streamlit not found. Installing..."
    pip install streamlit

    if [ -f requirements.txt ]; then
        echo "Installing requirements..."
        pip install -r requirements.txt
    else
        echo "requirements.txt not found. Skipping extra installs."
    fi
fi

streamlit run main.py
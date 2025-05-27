#!/bin/bash

# Push your changes to GitHub
git push origin main

# Wait a few seconds for Render to start deploying (adjust time if needed)
sleep 10

# Open your Render app URL in default Windows browser
cmd.exe /c start https://e-commerce-flask-8lsp.onrender.com


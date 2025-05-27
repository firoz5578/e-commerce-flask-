#!/bin/bash

echo "🔼 Pushing changes to GitHub..."
git push origin main

echo "⏳ Waiting for Render to begin deploying..."
sleep 5

echo "🌐 Opening your Render app in the browser..."
explorer.exe https://e-commerce-flask-8lsp.onrender.com



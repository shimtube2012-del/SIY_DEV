# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal development repository containing standalone Python and C++ projects created by IYShim. The projects are independent applications with no shared build system or framework.

## Projects

### Python Games (requires pygame)
- **breakout.py**: Breakout-style brick breaker game
- **lottery_ball.py**: Ball-drop lottery/drawing game with physics simulation
- **number_game.py**: Console-based number guessing game

### News Scraping (requires Flask, requests, feedparser, beautifulsoup4)
- **news_web_app.py**: Flask web app for aggregating news from Google News and Naver
- **news_scraper.ipynb**: Jupyter notebook version of the news scraper
- **templates/index.html**: Jinja2 template for the Flask app

### C++ Programs
- **number_game.cpp**: Number guessing game (Windows, uses windows.h)
- **sum.cpp**: Simple sum calculator (Windows)

## Running Applications

```bash
# Python games
python breakout.py
python lottery_ball.py
python number_game.py

# Flask web app (runs on localhost:5000)
python news_web_app.py

# C++ compilation (Windows/MinGW)
g++ number_game.cpp -o number_game.exe
g++ sum.cpp -o sum.exe
```

## Technical Notes

- Python files use Korean text and require Windows Korean fonts (malgun.ttf) for pygame-based games
- C++ files use Windows-specific console codepage settings (CP949) for Korean character support
- News scraper uses mobile User-Agent for Naver scraping

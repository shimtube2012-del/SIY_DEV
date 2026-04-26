# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a personal development repository containing standalone Python and C++ projects created by IYShim. The projects are independent applications with no shared build system or framework.

## Projects

### Python Games — `python_games/` (requires pygame)
- **python_games/breakout.py**: Breakout-style brick breaker game
- **python_games/lottery_ball.py**: Ball-drop lottery/drawing game with physics simulation

### Number Game — `number_game/`
- **number_game/number_game.py**: Console-based number guessing game (Python)
- **number_game/number_game.cpp**: Number guessing game (C++, Windows, uses windows.h)

### News Scraping — `news_scraper/` (requires Flask, requests, feedparser, beautifulsoup4)
- **news_scraper/news_web_app.py**: Flask web app for aggregating news from Google News and Naver
- **news_scraper/news_scraper.ipynb**: Jupyter notebook version of the news scraper
- **news_scraper/templates/index.html**: Jinja2 template for the Flask app

### C++ Programs — `cpp_programs/`
- **cpp_programs/sum.cpp**: Simple sum calculator (Windows)

### Search Algorithms — `search_algorithms/`
- **search_algorithms/search_algorithms.py**: Python implementations
- **search_algorithms/SearchAlgorithms.java**: Java implementations

### Misc Scripts — `misc_scripts/`
- **misc_scripts/calculator.py**, **test_popup.py**

### Ilyong Code — `ilyongcode/`
- **ilyongcode/run_ilyongcode.sh**: 로컬 Ollama qwen2.5-coder 모델로 aider 실행 (배너 포함)

## Running Applications

```bash
# Python games
python python_games/breakout.py
python python_games/lottery_ball.py
python number_game/number_game.py

# Flask web app (runs on localhost:5000)
python news_scraper/news_web_app.py

# C++ compilation (Windows/MinGW)
g++ number_game/number_game.cpp -o number_game/number_game.exe
g++ cpp_programs/sum.cpp -o cpp_programs/sum.exe
```

## Technical Notes

- Python files use Korean text and require Windows Korean fonts (malgun.ttf) for pygame-based games
- C++ files use Windows-specific console codepage settings (CP949) for Korean character support
- News scraper uses mobile User-Agent for Naver scraping

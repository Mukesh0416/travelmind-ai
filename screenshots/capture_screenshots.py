"""
Screenshot Capture Guide for TravelMind AI
==========================================

This script helps capture screenshots of the TravelMind AI application
for the GitHub portfolio.

Prerequisites:
    pip install streamlit streamlit-screenshot

Usage:
    1. Start the app:  python run.py
    2. Run this script: python screenshots/capture_screenshots.py
    3. Follow the on-screen instructions to capture each section.

The screenshots will be saved to the screenshots/ directory.
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

SCREENSHOTS_DIR = Path(__file__).resolve().parent

# List of screenshots to capture
SCREENSHOTS = [
    {
        "filename": "01_home_page.png",
        "title": "Home Page",
        "description": "The main landing page of TravelMind AI showing the title, "
                       "subtitle, and navigation sidebar.",
    },
    {
        "filename": "02_travel_form.png",
        "title": "Travel Form",
        "description": "The trip planning form with destination, days, travelers, "
                       "budget, travel style, and interests inputs.",
    },
    {
        "filename": "03_weather_section.png",
        "title": "Weather Section",
        "description": "The weather results section showing temperature, humidity, "
                       "and wind speed for the destination.",
    },
    {
        "filename": "04_attractions_section.png",
        "title": "Attractions Section",
        "description": "The attractions section showing recommended places to visit "
                       "in the destination.",
    },
    {
        "filename": "05_hotel_recommendations.png",
        "title": "Hotel Recommendations",
        "description": "The hotel recommendations section showing hotel names, "
                       "price ranges, and descriptions.",
    },
    {
        "filename": "06_restaurant_recommendations.png",
        "title": "Restaurant Recommendations",
        "description": "The restaurant recommendations section showing restaurant "
                       "names, cuisines, and costs.",
    },
    {
        "filename": "07_transportation_recommendations.png",
        "title": "Transportation Recommendations",
        "description": "The transportation section showing best ways to reach the "
                       "destination and local transport options.",
    },
    {
        "filename": "08_packing_recommendations.png",
        "title": "Packing Recommendations",
        "description": "The packing list section showing categorized packing items "
                       "for the trip.",
    },
    {
        "filename": "09_itinerary_page.png",
        "title": "Itinerary Page",
        "description": "The day-by-day itinerary showing activities, meals, and "
                       "daily spending for each day.",
    },
    {
        "filename": "10_travel_history_page.png",
        "title": "Travel History Page",
        "description": "The travel history page showing all past trips with "
                       "destinations and durations.",
    },
    {
        "filename": "11_user_preferences_page.png",
        "title": "User Preferences Page",
        "description": "The user preferences page showing saved travel style and "
                       "favorite activities.",
    },
]


def main():
    print("=" * 60)
    print("  TravelMind AI - Screenshot Capture Guide")
    print("=" * 60)
    print()
    print("To capture screenshots:")
    print()
    print("1. Start the application:  python run.py")
    print("2. Open your browser at:   http://localhost:8501")
    print("3. For each screenshot below, navigate to the page and capture it.")
    print()
    print("Screenshots to capture:")
    print("-" * 60)

    for shot in SCREENSHOTS:
        print(f"\n  {shot['filename']}")
        print(f"    {shot['title']}")
        print(f"    {shot['description']}")

    print()
    print("=" * 60)
    print("  Tips:")
    print("  - Use Windows + Shift + S to capture a region")
    print("  - Or use the browser's screenshot tool (F12 > Capture)")
    print("  - Save all screenshots in the screenshots/ directory")
    print("=" * 60)


if __name__ == "__main__":
    main()
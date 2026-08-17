import sys
import os
from pathlib import Path

# Add project root to path so 'services' module can be imported
project_root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(project_root))

import streamlit as st

st.set_page_config(
    page_title="TravelMind AI",
    page_icon="🧠",
    layout="wide"
)

st.title("🧠 TravelMind AI - Multi-Agent Travel Planning")
st.markdown("Plan your next trip using our intelligent multi-agent system")

# Initialize session state for trip data if not exists
if "trip_result" not in st.session_state:
    st.session_state.trip_result = None
if "trip_planned" not in st.session_state:
    st.session_state.trip_planned = False

# Error handling helper function
def handle_api_error(api_name, error):
    """Handle API errors with user-friendly messages."""
    st.error(f"Unable to fetch data from {api_name}. Please try again.")
    st.info(f"Technical details: {str(error)[:200]}")
    return None

# Sidebar navigation
st.sidebar.title("Navigation")
page = st.sidebar.radio("Go to", ["Plan a Trip", "Travel History", "User Preferences"])

if page == "Plan a Trip":
    from services.trip_service import plan_trip

    st.header("Plan Your Trip")

    with st.form("trip_form"):

        col1, col2 = st.columns(2)

        with col1:
            destination = st.text_input("Destination", placeholder="e.g., Bali, Indonesia")
            days = st.number_input("Days", min_value=1, max_value=30, value=5)
            travelers = st.number_input("Number of travelers", min_value=1, max_value=10, value=2)

        with col2:
            budget_per_day = st.number_input("Budget per day (USD)", min_value=10, max_value=10000, value=500)
            travel_style = st.selectbox(
                "Travel style",
                ["Balanced", "Luxury", "Budget", "Adventure"],
                index=0
            )

        interests = st.multiselect(
            "Interests",
            ["Trekking", "Camping", "Food", "Shopping", "Culture", "Adventure"],
            default=[]
        )

        submitted = st.form_submit_button("Plan My Trip")

        if submitted:
            if not destination:
                st.error("Please enter a destination")
            else:
                try:
                    # Show progress indicators
                    status_container = st.container()
                    with status_container:
                        st.info("Planning your trip...")

                        progress_bar = st.progress(0)
                        status_text = st.empty()

                        # Simulate progress steps
                        status_text.text("Finding the location...")
                        progress_bar.progress(10)

                        status_text.text("Checking the weather...")
                        progress_bar.progress(25)

                        status_text.text("Searching for attractions...")
                        progress_bar.progress(50)

                        status_text.text("Finding hotels...")
                        progress_bar.progress(75)

                        status_text.text("Finding restaurants...")
                        progress_bar.progress(90)

                        with st.spinner("Planning your trip..."):
                            result = plan_trip(
                                destination=destination,
                                days=days,
                                travelers=travelers,
                                budget_per_day=budget_per_day,
                                interests=interests,
                                travel_style=travel_style,
                                user_id="user_123"
                            )

                    progress_bar.progress(100)
                    status_text.text("Trip complete!")

                    # Store result in session state
                    st.session_state.trip_result = result
                    st.session_state.trip_planned = True
                    st.rerun()

                except Exception as e:
                    st.error("An error occurred while planning your trip.")
                    st.info(handle_api_error("backend services", e))

# Show results if available from session state
if st.session_state.trip_planned and st.session_state.trip_result is not None:
    st.success("Trip planned successfully!")
    result = st.session_state.trip_result

    # Display results in independent sections (Dashboard Layout)

    # Weather Section
    with st.expander("🌦 Weather", expanded=True):
        if "weather" in result and result["weather"]:
            st.write(result["weather"])
        else:
            st.error("Unable to fetch the weather. Please try again.")

    # Attractions Section
    with st.expander("🏔 Attractions", expanded=True):
        if "search" in result and result["search"]:
            st.write(result["search"])
        else:
            st.error("Unable to retrieve attractions. Please try again.")

    # Hotels Section
    with st.expander("🏨 Hotels", expanded=True):
        if "accommodation" in result and result["accommodation"]:
            st.write(result["accommodation"])
        else:
            st.error("Unable to retrieve hotels. Please try again.")

    # Restaurants Section
    with st.expander("🍽 Restaurants", expanded=True):
        if "restaurant" in result and result["restaurant"]:
            st.write(result["restaurant"])
        else:
            st.error("Unable to retrieve restaurants. Please try again.")

    # Transportation Section
    with st.expander("🚗 Transportation", expanded=True):
        if "transportation" in result and result["transportation"]:
            st.write(result["transportation"])
        else:
            st.error("Unable to retrieve transportation. Please try again.")

    # Packing List Section
    with st.expander("🎒 Packing List", expanded=True):
        if "packing" in result and result["packing"]:
            st.write(result["packing"])
        else:
            st.error("Unable to generate packing list. Please try again.")

    # Itinerary Section
    with st.expander("📅 Itinerary", expanded=True):
        if "itinerary" in result and result["itinerary"]:
            st.write(result["itinerary"])
        else:
            st.error("Unable to build itinerary. Please try again.")

elif page == "Travel History":
    st.header("Travel History")
    # Retrieve travel history from memory service
    from memory.memory import memory
    user_id = st.session_state.get("user_id", "user_123")
    history = memory.get_trip_history(user_id)
    if history:
        st.write(f"Your travel history ({len(history)} trips):")
        for trip in history:
            st.write(f"- {trip['destination']} ({trip['days']} days)")
    else:
        st.info("No travel history found. Plan a trip to see your history here.")

elif page == "User Preferences":
    st.header("User Preferences")
    from memory.memory import memory
    user_id = st.session_state.get("user_id", "user_123")
    preferences = memory.get_preferences(user_id)
    if preferences:
        st.write("Current preferences:")
        st.write(f"- Travel style: {preferences.get('travel_style', 'Not set')}")
        st.write(f"- Favorite activities: {', '.join(preferences.get('favorite_activities', []))}")
    else:
        st.info("No preferences found. Set your preferences below.")

    with st.form("preferences_form"):
        travel_style = st.selectbox(
            "Favorite travel style",
            ["Balanced", "Luxury", "Budget", "Adventure"],
            index=0
        )
        favorite_activities = st.multiselect(
            "Favorite activities",
            ["Trekking", "Camping", "Food", "Shopping", "Culture", "Adventure"],
            default=preferences.get("favorite_activities", [])
        )
        submitted = st.form_submit_button("Save Preferences")
        if submitted:
            try:
                memory.set_preferences(user_id, {
                    "travel_style": travel_style,
                    "favorite_activities": favorite_activities
                })
                st.success("Preferences saved successfully!")
                st.rerun()
            except Exception as e:
                st.error("Unable to save preferences. Please try again.")
                st.info(f"Technical details: {str(e)[:200]}")
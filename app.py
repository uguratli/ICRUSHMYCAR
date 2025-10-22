import streamlit as st
from game_funcs import *
import time


if 'game_over' not in st.session_state:
    st.session_state['game_over'] = False
if 'score' not in st.session_state:
    st.session_state['score'] = 0
if "scenario" not in st.session_state:
    st.session_state.scenario = None
if "roads" not in st.session_state:
    st.session_state.roads = None

st.title("Death Stranding")


if st.session_state.game_over:
    st.error(f"💀 Game Over! You survived {st.session_state.score} days.")
    if st.button("Try Again"):
        st.session_state.score = 0
        st.session_state.game_over = False
        st.session_state.scenario = None
        st.session_state.roads = None
        st.rerun()
    st.stop()
if "welcome_shown" not in st.session_state:
    st.session_state.welcome_shown = False


if st.session_state.scenario is None:
    st.session_state.scenario = day_generator()
    day = st.session_state.score + 1
    st.session_state.roads = create_routes(st.session_state.scenario, day)

condition = st.session_state.scenario
routes = st.session_state.roads

st.subheader(f"Day {st.session_state.score + 1 } Driving Conditions:")
if not st.session_state.welcome_shown:
    st.success("🌞 Welcome!" \
    "\n\n You're a cargo delivery driver in a strange world." \
    "  You make daily deliveries and are given specific routes to reach your destination. " \
    "\n\n The goal of the game is to choose the safest route possible, but remember, there's no such thing as a completely safe route.")
    st.session_state.welcome_shown = True

st.write(f"⛅ Weather: {condition['weather'].capitalize()},\
⌚ Time of Day: {condition['time_of_day'].capitalize()},\
💡 Light: {condition['lighting'].capitalize()},\
🎉 Holiday: {condition['holiday']},\
🎒 School Season: {condition['school_season']}")

st.dataframe(routes.drop(columns=['accident_risk', 'lighting', 'weather', 'time_of_day', 'holiday', 'school_season']),
             hide_index=True,
             height=200, use_container_width=True,
             column_config={"id": st.column_config.NumberColumn("Road ID", width="small"),
                            "num_reported_accidents": st.column_config.NumberColumn("Reported Accidents", width="normal"),
                            "road_signs_present": st.column_config.CheckboxColumn("Road Signs"),
                            "road_type": st.column_config.TextColumn("Road Type", width="small"),
                            "num_lanes": st.column_config.NumberColumn("Lanes", width="small"),
                            "curvature": st.column_config.NumberColumn("Curvature", width="small"),
                            "speed_limit": st.column_config.NumberColumn("Speed Limit", width="small"),
                            "public_road": st.column_config.CheckboxColumn("Public Road")})

selected_id = st.selectbox("Select the Road ID you want to drive on:", routes["id"])


if st.button("Drive! 🚘"):
    road = routes[routes["id"] == selected_id]

    risk = road['accident_risk'].values[0]
    event = random.random()

    st.write(f"Road risk: **{risk:.2f}**")
    st.write(f"Accident event number: **{event:.2f}**")

    if event < risk:
        st.session_state.game_over = True
        st.error(f"💥 An accident occurred! Game Over! You survived {st.session_state.score} days.")
        random_gif = random.choice(["1.gif", "2.gif", "3.gif", "4.gif"])
        st.image(random_gif, caption="💥 Accident Occurred!", use_container_width=True)
        time.sleep(5)
        st.rerun()
    else:
        st.session_state.score += 1
        st.success(f"✅ You survived! Total days survived: {st.session_state.score}")
        time.sleep(1)
        st.session_state.scenario = None
        st.session_state.roads = None
        st.rerun()

st.markdown(
    """
    <hr>
    <div style='text-align: center; font-size: 13px; color: gray;'>
        © 2025 Death Stranding | Created by <b>uguratli</b>
        <br> This code was made within the scope of <a href='https://www.kaggle.com/competitions/playground-series-s5e10'  target='_blank'>Kaggle · Playground Prediction Competition</a>.
        <br>Follow on <a href='https://github.com/uguratli' target='_blank'>GitHub</a>, <a href='https://www.kaggle.com/uuratl' target='_blank'>Kaggle</a>
    </div>
    """,
    unsafe_allow_html=True
)
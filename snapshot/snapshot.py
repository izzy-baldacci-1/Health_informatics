import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np



st.set_page_config(
    page_title = "Snapshot",
    page_icon = " : )",
    layout = "wide",
    initial_sidebar_state="expanded",
)

#uploading data, this would come from a sql database
test_data = pd.read_csv('test_data.csv')

#get entries this month
month = int(dt.datetime.today().month)
entry_months = test_data['Date'].apply(lambda x: int(x[0:2]))
num_entries = sum(np.array(entry_months) == month)



st.logo('snapshot_logo.png', size = 'large')

st.image('snapshot_logo_2.png', width = 500)

#st.markdown('# Snapshot')
st.markdown('##### Welcome to your personal journal! See your calendar events to reflect on your day. Upload your entries every day to maintain your routine, receive feedback, and schedule your next journaling session. Reflect on your past entries through the journal vault. Happy journaling!😊')
st.divider()

col1, col2, col3 = st.columns([2,1,1])
col1.markdown('## Calendar')
col1.image('example_calendar.png', width = 500)

col2.markdown('## Biometrics')
col2.metric('Hours of sleep', value = "7 hr", delta = "+2")
col2.metric('Stress score', value = '5', delta = "-3", delta_color = 'inverse')

col3.markdown('## Journal Entry Goal')
col3.metric('This month you have', value = f'{num_entries} entries')
col3.metric('Out of your goal of', value = '25 entries')

st.markdown('### Prompt for the day')

#used chatgpt to get nice html textbox
st.markdown(
    """
    <div style="
        background-color: #ca9ce1;
        padding: 10px 20px;
        border-radius: 10px;
        color: #333333;
        font-size: 16px;
        border: 1px solid #A9A9A9;">
        You had the following 9 events today: labwork, workout/breakfast, health informatics, lunch, data wranging, journal club #1 reading, appt, 120 hw, and halloween! You got 7 hours of sleep last night
    </div>
    """,
    unsafe_allow_html=True
)
#st.write("You had the following 9 events today: labwork, workout/breakfast, health informatics, lunch, data wranging, journal club #1 reading, appt, 120 hw, and halloween! You got 7 hours of sleep last night")
journal_image = st.file_uploader("#### *Upload your reflection here:*", type= ['png', 'jpg', 'pdf'])


st.divider()


st.markdown("### Your past entries")

st.dataframe(test_data, hide_index = True, width = 12000)


#st.sidebar.title("Your Journal")
#st.sidebar.markdown('### Home')
#st.sidebar.button('### Calendar')
#st.sidebar.button('### Journal Vault')
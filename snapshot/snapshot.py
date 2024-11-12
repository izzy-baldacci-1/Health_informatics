import streamlit as st
import pandas as pd
import datetime as dt
import numpy as np
import calStart 
from streamlit_gsheets import GSheetsConnection
import gspread
import random


### SETTING UP PAGE CONFIGURATION ###
st.set_page_config(
    page_title = "Snapshot",
    page_icon = " : )",
    layout = "wide",
    initial_sidebar_state="expanded",
)

st.image('snapshot_logo_2.png', width = 500)

### ESTABLISH CONNECTION TO SQL DB, FETCH DATA AND DISPLAY ###
test_data = pd.read_csv('test_data.csv')
conn = st.connection("gsheets", type = GSheetsConnection)

#LOAD IN JOURNAL VAULT
try:
    journal_vault = conn.read(worksheet = 'journal-vault')
except gspread.exceptions.WorksheetNotFound as e:
    print('not found')
    cols_create = pd.DataFrame({'Date':[], 'Events': [], 'Topic': [], 'Feedback': []})
    conn.create(worksheet = 'journal-vault', data = cols_create)
journal_vault = conn.read(worksheet = 'journal-vault')

#get entries this month
month = int(dt.datetime.today().month)
entry_months = journal_vault['Date'].apply(lambda x: int(x[5:7]))
num_entries = sum(np.array(entry_months) == month)

#st.write(f'entries: {month, entry_months, num_entries}')
### ESTABLISH LOGO FOR SIDEBAR [TO IMPLEMENT LATER] ###
#st.logo('snapshot_logo.png', size = 'large')

### GET EVENTS FOR THE DAY ###
events_for_day, prompt, n_events = calStart.main()
#print(prompt)
#prompts from reddit https://www.reddit.com/r/Journaling/comments/r7bsmz/long_list_of_journal_prompts/
all_prompts = ['Are you taking enough risks in your life?', 
             'At what point in your life have you had the highest self-esteem?', 
             'Consider and reflect on what might be your “favorite failure".', 
             'How can you reframe one of your biggest regrets in life?', 
             'How did you bond with one of the best friends you have ever had?', 
             'How did your parents or caregivers try to influence or control your behavior when you were growing up?',
             'How do the opinions of others affect you?', 'How do you feel about asking for help?', 
             'How much do your current goals reflect your desires?', 
             'In what ways are you currently self-sabotaging or holding yourself back?', 
             'What are some small things that other people have done that really make your day?', 
             'What are some things that frustrate you?', 'What biases do you need to work on?', 
             'What could you do to make your life more meaningful?', 'What happens when you are angry?', 
             'What do you need to give yourself more credit for?', 
             'What is a boundary that you need to draw in your life?', 
             'What is a positive habit that you would really like to cultivate?',
             'What is a reminder that you would like to tell yourself next time you are in a downward spiral?',
             'What is holding you back from being more productive at the moment?']
dayPrompt = random.choice(all_prompts)
if n_events<=3:
    string_opener = 'Today you went to '
    string_ending = f'. How did you feel about it? What was your favourite part? Here is something to consider when you journal today: {dayPrompt}'

elif 3<n_events<=5:
    string_opener = 'Woah you had a pretty busy today. You did '
    string_ending = f'. How are you feeling? Do you feel stressed at all? Here is something to consider when you journal today: {dayPrompt}'

else:
    string_opener = 'You had a super busy day! This is what you did today: '
    string_ending = f'. You should feel proud of yourself, you were super productive! Here is something to consider when you journal today: {dayPrompt}'

todays_full_prompt = string_opener + prompt + string_ending


#st.markdown('# Snapshot')
st.markdown('##### Welcome to your personal journal! See your calendar events to reflect on your day. Upload your entries every day to maintain your routine, receive feedback, and schedule your next journaling session. Reflect on your past entries through the journal vault. Happy journaling!😊')
st.divider()

### DISPLAY THE CALENDAR ###
col1, col2 = st.columns([1,1])
col1.markdown('## Set your Journal Entry Goal this month:')
goal = col1.text_input('input a number between 1 and 30:')


### DISPLAY THE JOURNAL ENTRY GOAL ###
col2.markdown('## Goal Progress')
col2.metric('This month you have', value = f'{num_entries} entries')
col2.metric('Out of your goal of', value = f'{goal} entries')


### PROMPT GENERATION ###
st.markdown('### Prompt for the day')
##used chatgpt to get nice html textbox
st.markdown(
    f"""
    <div style="
        background-color: #ca9ce1;
        padding: 10px 20px;
        border-radius: 10px;
        color: #333333;
        font-size: 20px;
        border: 1px solid #A9A9A9;">
        {todays_full_prompt}
    
    """,
    unsafe_allow_html=True
)
### UPLOAD CAPABILITIES ###
journal_image = st.file_uploader("#### *Upload your reflection here:*", type= ['png', 'jpg', 'pdf'])

if journal_image:
    feedback_options = ['Great Job!', 'Keep it up!', 'Way to go!']
    feedback_to_add = random.choice(feedback_options)
    row_for_vault = {'Date' : [str(dt.datetime.today())], 
                 'Events' : [prompt],
                 'Topic': [dayPrompt],
                 'Feedback': [feedback_to_add]}
    as_df = pd.DataFrame(row_for_vault, index = [0])
    journal_vault_updated = pd.concat([journal_vault, as_df], ignore_index = True)
    journal_vault = conn.update(worksheet = 'journal-vault', data = journal_vault_updated)

st.divider()



st.markdown("### Your past entries")

st.dataframe(journal_vault, hide_index = True, width = 12000)


#st.sidebar.title("Your Journal")
#st.sidebar.markdown('### Home')
#st.sidebar.button('### Calendar')
#st.sidebar.button('### Journal Vault')
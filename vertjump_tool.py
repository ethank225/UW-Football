import streamlit as st
import pandas as pd
from streamlit_option_menu import option_menu
import io

page_bg_css = """
<style>
[data-testid="stAppViewContainer"] {
    background-color: black;
}
</style>
"""

# Inject the custom CSS into the Streamlit app
st.markdown(page_bg_css, unsafe_allow_html=True)


# Load template data
template = pd.read_csv("VERTICAL JUMP (JUMP MAT).csv")
def reset_session_state():
        for key in st.session_state.keys():
            del st.session_state[key]

def page1():
    clear = st.button("Clear")
    if(clear):
        reset_session_state()
    col1, col2 = st.columns(2)
    file_name = st.text_input("File Name:")

    def get_position(name):
        row = template.loc[template['Player'] == name]
        return row['Pos'].values[0] if not row.empty else None


    # Initialize the DataFrame in session state if it does not exist
    if 'fill_in' not in st.session_state:
        st.session_state.fill_in = pd.DataFrame(columns=['player_name', 'position', 'jump1', 'jump2', 'max_jump'])

    # Title of the app

    # Function to format the names

    # Format the names

    # Selectbox with formatted names
    
    

    with col1:
        st.title("Vertical Jump Tracker")
        player_selection = st.selectbox("Select Player", template['Player'])
        jump_1 = st.number_input('Enter Jump 1', min_value=0.0, step=0.1, format="%.2f")
        jump_2 = st.number_input('Enter Jump 2', min_value=0.0, step=0.1, format="%.2f")
        max_jump = max(jump_1, jump_2)

        # Add button to submit data
        if st.button("Enter Data"):
            if player_selection in st.session_state.fill_in['player_name'].values:
                max_jump = max(jump_1, jump_2)
                st.session_state.fill_in.loc[st.session_state.fill_in['player_name'] == player_selection, ['jump1', 'jump2', 'max_jump']] = [jump_1, jump_2, max_jump]
                st.success(f"Data for {player_selection} changed successfully!")
            else:
                max_jump = max(jump_1, jump_2)
                new_row = pd.DataFrame({'player_name': [player_selection], 'jump1': [jump_1], 'jump2': [jump_2], 'max_jump': [max_jump], 'position':[get_position(player_selection)]})
                st.session_state.fill_in = pd.concat([st.session_state.fill_in, new_row], ignore_index=True)
                st.success(f"Data for {player_selection} added successfully!")


        # Display the DataFrame
        st.dataframe(st.session_state.fill_in)
    with col2:
        st.title("Positional Leaderboard")
        selected_position = st.selectbox("Select Position", template['Pos'].unique())
        filtered_df = st.session_state.fill_in[st.session_state.fill_in['position'] == selected_position][['player_name', 'max_jump']]
        filtered_df = filtered_df.sort_values(by='max_jump', ascending=False)
        st.dataframe(filtered_df)
        if not st.session_state.fill_in.empty:
            st.header("Highest Jumper")
            highest_jump_row = st.session_state.fill_in.loc[st.session_state.fill_in['max_jump'].idxmax()]
            st.write(highest_jump_row)

        

    for name in st.session_state.fill_in['player_name']:
        max_jump_value = st.session_state.fill_in.loc[st.session_state.fill_in['player_name'] == name, 'max_jump'].values[0]
        template.loc[template['Player'] == name, 'Vertical Jump (Jump Mat)'] = max_jump_value
    template.to_csv('Updated_VERTICAL_JUMP.csv', index=False)

    template['Vertical Jump (Jump Mat)'] = template['Vertical Jump (Jump Mat)'].astype(float).round(2)
    updated_csv = template.to_csv(index=False)

    # Provide a download button for the updated CSV file
    export_data = st.download_button(
        label="Download Updated CSV",
        data=updated_csv,
        file_name= f'{file_name}.csv',
        mime='text/csv'
    )

    if(export_data):
        st.success("Data exported successfully!")
        
def page2():
    template = pd.read_csv("VERTICAL JUMP (JUMP MAT).csv")

    group1 = st.file_uploader("Group 1", type=['csv'])
    group2 = st.file_uploader("Group 2", type=['csv'])
    group3 = st.file_uploader("Group 3", type=['csv'])
    
        
    # Function to add matching rows to the template
    def add_matching_rows_to_template(template, group_files):
        for group in group_files:
            if group is not None:
                df = pd.read_csv(group)
                # Filter rows where the name is in the template's name column
                matching_rows = df[df['Player'].isin(template['Player'])]
                # Append these rows to the template DataFrame
                template = pd.concat([template, matching_rows], ignore_index=True)
        # Remove duplicates, keeping the last occurrence
        template = template.drop_duplicates(subset=['Player'], keep='last')
        return template

    # Combine files
    group_files = [group1, group2, group3]
    updated_template = add_matching_rows_to_template(template, group_files)

    # Display updated template
    if not updated_template.empty:
        st.write(updated_template)
    else:
        st.write("No matching names found or no files uploaded.")
        
    csv_buffer = io.StringIO()
    updated_template.to_csv(csv_buffer, index=False)
    csv_data = csv_buffer.getvalue()

    # File name input
    file_name = st.text_input("Name the file:")

    # Create download button
    export_data = st.download_button(
        label="Download Updated CSV",
        data=csv_data,
        file_name=f'{file_name}.csv',
        mime='text/csv'
    )

    if export_data:
        st.success("Data successfully exported")
    

    # Function to read and merge files
   

    # Merge files

    # Display merged data

    # Function to combine files
    
    
    # Ensure the group is not reset each time the page is rendered
    # if 'group' not in st.session_state:
    #     st.session_state.group = []

    # player_selection = st.selectbox("Select Player", template['Player'])
    # add_player = st.button("Add Player")
    # if add_player:
    #     st.session_state.group.append(player_selection)
    #     st.success(f"{player_selection} added to the group!")

    # # Display the group
    # st.write("Group:", st.session_state.group)
        
    
#Page Navigation

with st.sidebar:
    selected = option_menu(
        "Main Menu", ["Collect Data", "Merge Data"]
    )

# Display the selected page
if selected == "Collect Data":
    page1()
elif selected == "Merge Data":
    page2()
    
st.logo("Washington_Huskies_logo.svg.png")



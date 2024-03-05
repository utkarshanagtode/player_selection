import streamlit as st
import pickle
import pandas as pd

player_metrics = pickle.load(open('player_metric.pkl', 'rb'))
player_metric = pd.DataFrame(player_metrics)
player_metric

#st.title('Player Recommendation')

def validate_selections(selections, min_count, max_count):
    if len(selections) < min_count:
        st.warning(f"Please select at least {min_count} players.")
    elif len(selections) > max_count:
        st.warning(f"Please select only {max_count} players.")
        return selections[:max_count]
    return selections

def calculate_average_rating(selected_players):
    selected_players_ratings = player_metric[player_metric['players'].isin(selected_players)]
    average_rating = selected_players_ratings['player_rating'].mean()
    return average_rating

def predict_winning_team(team1_average_rating, team2_average_rating):
    if team1_average_rating > team2_average_rating:
        return "Team 1"
    elif team1_average_rating < team2_average_rating:
        return "Team 2"
    else:
        return "Draw"

def calculate_winning_percentage(team_rating, total_performance):
    return (team_rating / total_performance) * 100

def main():
    global team1_average_rating, team2_average_rating
    st.title("Team Selection and Match Simulation")

    num_teams = st.number_input("Enter the number of teams:", min_value=2, max_value=10, step=1)
    teams = []
    for i in range(1, num_teams + 1):
        team_name = st.text_input(f"Enter the name of team {i}:")
        teams.append(team_name)

    st.header("Team Formation")
    team1 = st.selectbox("Select Team 1:", teams)
    team2 = st.selectbox("Select Team 2:", teams)

    st.write(f"Team 1: {team1}")
    st.write(f"Team 2: {team2}")

    st.header("Player Selection")

    col1, col2 = st.columns(2)

    with col1:
        team1_players = st.multiselect(f"Select 11 players for {team1}:", player_metric['players'].values,key=f"{team1}team1_players")
        team1_players = validate_selections(team1_players, min_count=11, max_count=11)
        st.write(f"Selected players for {team1}: {team1_players}")

    with col2:
        team2_available_players = [player for player in player_metric['players'].values if player not in team1_players]
        team2_players = st.multiselect(f"Select 11 players for {team2}:", team2_available_players,key=f"{team2}team2_players")
        team2_players = validate_selections(team2_players, min_count=11, max_count=11)
        st.write(f"Selected players for {team2}: {team2_players}")

    if len(team1_players) == 11 and len(team2_players) == 11:
        if st.button("Calculate Average Ratings"):
            team1_average_rating = calculate_average_rating(team1_players)
            team2_average_rating = calculate_average_rating(team2_players)

            st.write("Average Rating for Team 1:", team1_average_rating)
            st.write("Average Rating for Team 2:", team2_average_rating)

            total_performance = team1_average_rating + team2_average_rating
            winning_percentage_team1 = calculate_winning_percentage(team1_average_rating, total_performance)
            winning_percentage_team2 = calculate_winning_percentage(team2_average_rating, total_performance)

            st.write(f"Winning Percentage for {team1}: {winning_percentage_team1:.2f}%")
            st.write(f"Winning Percentage for {team2}: {winning_percentage_team2:.2f}%")

            winning_team = predict_winning_team(team1_average_rating, team2_average_rating)
            st.write("Predicted Winning Team:", winning_team)
        else:
            st.warning("Please calculate average ratings for both teams first.")


if __name__ == "__main__":
    main()

import pandas as pd

def load_and_process_data(filepath):
    # Load data
    df = pd.read_csv(filepath)
    
    # Convert string representations of lists into actual lists
    df['Heroes_Team'] = df['Heroes_Team'].apply(eval)
    df['Villains_Team'] = df['Villains_Team'].apply(eval)
    df['Heroes_Scores'] = df['Heroes_Scores'].apply(eval)
    df['Villains_Scores'] = df['Villains_Scores'].apply(eval)
    
    # Initialize player statistics dictionary
    player_stats = {player: {'total_scores': 0, 'wins': 0, 'matches': 0}
                    for player in set(sum(df['Heroes_Team'].tolist(), []) + sum(df['Villains_Team'].tolist(), []))}
    
    # Process each match
    for _, row in df.iterrows():
        # Update stats for heroes
        for player, score in zip(row['Heroes_Team'], row['Heroes_Scores']):
            player_stats[player]['total_scores'] += score
            player_stats[player]['matches'] += 1
            if row['Winning_Team'] == 'Heroes':
                player_stats[player]['wins'] += 1

        # Update stats for villains
        for player, score in zip(row['Villains_Team'], row['Villains_Scores']):
            player_stats[player]['total_scores'] += score
            player_stats[player]['matches'] += 1
            if row['Winning_Team'] == 'Villains':
                player_stats[player]['wins'] += 1
    
    # Calculate average scores and win rates
    for player in player_stats:
        stats = player_stats[player]
        stats['average_score'] = stats['total_scores'] / stats['matches']
        stats['win_rate'] = stats['wins'] / stats['matches']
    
    return player_stats

def save_to_excel(player_stats, output_file):
    # Convert dictionary to DataFrame
    df_stats = pd.DataFrame.from_dict(player_stats, orient='index')
    df_stats['average_score'] = df_stats['total_scores'] / df_stats['matches']
    df_stats['win_rate'] = df_stats['wins'] / df_stats['matches']
    #df_stats.sort_values(by=['average_score', 'win_rate'], ascending=[False, False], inplace=True)
    df_stats.sort_values(by=['win_rate', 'average_score'], ascending=[False, False], inplace=True)
    
    
    # Print the result before saving
    print("Sorted Player Statistics:")
    print(df_stats)
    
    # Save to Excel
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        df_stats.to_excel(writer, sheet_name='Player Statistics')

def main():
    filepath = 'data.csv'  # Adjust the filepath as necessary
    output_file = 'Player_Statistics.xlsx'
    
    player_stats = load_and_process_data(filepath)
    save_to_excel(player_stats, output_file)
    print(f"Player statistics have been saved to {output_file}")

if __name__ == '__main__':
    main()

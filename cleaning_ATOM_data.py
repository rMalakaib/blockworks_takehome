import pandas as pd

# Load the first CSV file (the one with all the votes)
votes_df = pd.read_csv('./flipside_data.csv')  # Replace 'votes.csv' with the path to your actual votes CSV file

# Load the second CSV file (the one with validator names, keys, and ranks)
validators_df = pd.read_csv('./ATOM_validator_data_ranked.csv')  # Replace 'validators.csv' with the path to your actual validators CSV file

# Merge the votes and validators data on the wallet addresses (voter/Keys)
merged_df = pd.merge(votes_df, validators_df, left_on='voter', right_on='Keys', how='inner')

# Create the final DataFrame with the necessary columns
final_df = merged_df[['Validator Names', 'proposal_id', 'vote_option', 'Rank']]

# Save the final DataFrame to a new CSV file
final_df.to_csv('ATOM_validator_votes.csv', index=False)  # This will create a CSV called 'validator_votes.csv'

print("CSV file with validator votes created successfully.")

import pandas as pd
import time
from tqdm import tqdm

# Timer function to measure the total time taken by the script
class Timer:
    def __init__(self):
        self.start_time = None
    
    def start(self):
        """Start the timer."""
        self.start_time = time.time()
    
    def stop(self):
        """Stop the timer and print the elapsed time in minutes and seconds."""
        if self.start_time is None:
            print("Timer was not started.")
            return
        elapsed_time = time.time() - self.start_time
        minutes = int(elapsed_time // 60)
        seconds = int(elapsed_time % 60)
        print(f"Total time taken: {minutes} minutes and {seconds} seconds")

# Initialize and start the timer
timer = Timer()
timer.start()

# Read the CSV file (adjust the file path accordingly)
df = pd.read_csv('ATOM_validator_votes.csv', usecols=[0, 1, 2], header=None, names=['from_key', 'proposalId', 'solutionChosen'])

# 1. Find unique from keys and proposalId values
unique_from_keys = df['from_key'].unique()
unique_proposalIds = df['proposalId'].unique()

# 2. Create an empty dataframe with 'from_key' as the first column and proposalIds as columns
result_df = pd.DataFrame(columns=['proposalId'] + list(unique_from_keys))

# 3. Add the unique from keys to the dataframe
result_df['proposalId'] = unique_proposalIds

# 4. Iterate over each row in the original dataframe and fill the corresponding cell
for index, row in tqdm(df.iterrows(), total=len(df), desc="Processing Rows", unit="row", ncols=100):
    # Find the matching row in the result_df for the from_key
    from_key_index = result_df[result_df['proposalId'] == row['proposalId']].index[0]
    
    # Update the corresponding proposalId column with the solutionChosen value
    result_df.at[from_key_index, row['from_key']] = row['solutionChosen']

# 5. Replace any missing values (NaNs) with 'N/A'
result_df.fillna('N/A', inplace=True)

# Display the resulting dataframe
result_df.fillna('N/A', inplace=True)

# Write the resulting DataFrame to a new CSV file
result_df.to_csv('inverse_outputfile.csv', index=False)

timer.stop()

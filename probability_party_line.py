import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

# Load your dataset
NUMBER_VALIDATORS = 50
file_path = 'ATOM_validator_votes.csv'  # Replace this with your actual file path
df = pd.read_csv(file_path, header=None)

# Rename columns for clarity
df.columns = ['Validator', 'Proposal ID', 'Voting Choice', 'Validator Rank']

# Filter out the top 7 ranked validators
top_7_validators = df[df['Validator Rank'] <= NUMBER_VALIDATORS]

# Merge with top 7 validators to compare votes
merged_df = df.merge(top_7_validators[['Proposal ID', 'Voting Choice']], on='Proposal ID', suffixes=('', '_Top7'))

# Compare votes to identify deviations
merged_df['Deviation'] = merged_df['Voting Choice'] != merged_df['Voting Choice_Top7']

# Group by validator and calculate the percentage of deviations
deviation_probabilities = merged_df.groupby('Validator')['Deviation'].mean() * 100

# Sort by validator rank for plotting
df_sorted = df[['Validator', 'Validator Rank']].drop_duplicates().set_index('Validator')
deviation_probabilities_sorted = deviation_probabilities.to_frame().join(df_sorted).sort_values('Validator Rank')

# Plotting
plt.figure(figsize=(10, 6))

# Scatter plot (removing the line between dots)
plt.scatter(deviation_probabilities_sorted['Validator Rank'], deviation_probabilities_sorted['Deviation'], label=f'Deviation from Top {NUMBER_VALIDATORS}', color='orange')

# Add slope (linear regression) line
slope, intercept, r_value, p_value, std_err = stats.linregress(deviation_probabilities_sorted['Validator Rank'], deviation_probabilities_sorted['Deviation'])
plt.plot(deviation_probabilities_sorted['Validator Rank'], intercept + slope * deviation_probabilities_sorted['Validator Rank'], 'black', label=f'Slope = {slope:.3f}', linewidth=2)

# Customize plot
plt.title(f'Probability of Deviating from the Top {NUMBER_VALIDATORS} Ranked Validators Votes')
plt.xlabel('Validator Rank')
plt.ylabel('Probability of Deviation (%)')
plt.legend()
plt.grid(True)

# Show the plot
plt.show()

import pandas as pd
from sklearn.decomposition import PCA  # Correct import for PCA
from sklearn.impute import SimpleImputer  # Correct import for SimpleImputer
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file
file_path = './inverse_outputfile.csv'
df = pd.read_csv(file_path)

# Clean the data
# Drop columns that aren't part of the proposals (i.e., metadata)
df_clean = df.drop(columns=['proposalId'])

# 3 means abstain
# Replace "N/A" values with 0 (which means abstain)
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
df_imputed = pd.DataFrame(imputer.fit_transform(df_clean), columns=df_clean.columns)

# Perform PCA
pca = PCA(n_components=None)
pca_result = pca.fit_transform(df_imputed)

# Explained variance for each principal component
explained_variance_ratio = pca.explained_variance_ratio_

# Create a DataFrame for explained variance
explained_variance_df = pd.DataFrame({
    'Principal Component': [f"PC{i+1}" for i in range(len(explained_variance_ratio))],
    'Explained Variance Ratio': explained_variance_ratio
})

# Save the explained variance ratios to a CSV file
output_file_path = './inverse_explained_variance.csv'
explained_variance_df.to_csv(output_file_path, index=False)

# Plot the explained variance ratio (not cumulative)
plt.figure(figsize=(8, 6))
plt.plot(explained_variance_ratio, marker='o', linestyle='--', color='y')  # Removed np.cumsum
plt.title('Voting Correlation Between Cosmos Hub Validator Votes')
plt.xlabel('Index')
plt.ylabel('Eigenvalues')
plt.grid(True)
plt.show()

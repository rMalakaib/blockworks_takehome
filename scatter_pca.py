import pandas as pd
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import numpy as np
import matplotlib.pyplot as plt

# Load the CSV file
file_path = './outputfile.csv'
df = pd.read_csv(file_path)

# Clean the data
df_clean = df.drop(columns=['from_key'])
# Transpose the DataFrame to perform PCA on proposals (columns)
df_clean_transposed = df_clean.T

# Replace "N/A" values with 0 (which means abstain)
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
df_imputed_transposed = pd.DataFrame(imputer.fit_transform(df_clean_transposed), columns=df_clean_transposed.columns)

# Perform PCA on transposed data
pca = PCA(n_components=None)  # Limit to first two components for scatter plot
pca_result = pca.fit_transform(df_imputed_transposed)

# Create a scatter plot of the first two principal components
plt.figure(figsize=(10, 8))
plt.scatter(pca_result[:, 0], pca_result[:, 1], alpha=0.7, color='y')

# # Annotate points with proposal numbers (as you mentioned, there are 235 proposals)
# for i, proposal in enumerate(df_clean.columns):
#     plt.annotate(proposal, (pca_result[i, 0], pca_result[i, 1]), fontsize=9, alpha=0.7, color='y')

plt.title('Sub-Set Correlation Of Cosmos Hub Proposals')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True)
plt.show()

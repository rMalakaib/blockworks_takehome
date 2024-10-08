import pandas as pd
from sklearn.decomposition import PCA
from sklearn.impute import SimpleImputer
import numpy as np
import matplotlib.pyplot as plt

labeled_names = {'Coinbase Custody': 'cosmos1c4k24jzduc365kywrsvf5ujz4ya6mwymy8vq4q',
 'cosmostation': 'cosmos1clpqr4nrk4khgkxj78fcwwh6dl3uw4ep4tgu9q',
 'SG-1': 'cosmos196ax4vc0lwpxndu9dyhvca7jhxp70rmcfhxsrt',
 'Everstake': 'cosmos1tflk30mq5vgqjdly92kkhhq3raev2hnzldd74z',
 'Binance Node': 'cosmos18ruzecmqj9pv8ac0gvkgryuc7u004te9xr2mcr',
 'Upbit Staking': 'cosmos1x8efhljzvs52u5xa6m7crcwes7v9u0nlteumau',
 'DokiaCapital': 'cosmos14lultfckehtszvzw4ehu0apvsr77afvyhgqhwh',
 'Allnodes': 'cosmos1n229vhepft6wnkt5tjpwmxdmcnfz55jv5c4tj7',
 'Ledger': 'cosmos10wljxpl03053h9690apmyeakly3ylhejxgve8g',
 'Kraken': 'cosmos1z8zjv3lntpwxua0rtpvgrcwl0nm0tltgyuy0nd',
 'Chorus One': 'cosmos15urq2dtp9qce4fyc85m6upwm9xul3049um7trd',
 'CloudByte': 'cosmos1wvt5zugk97mrl5rm9c3m573f9gj03w2gprnwcl',
 'stake.fish': 'cosmos1sjllsnramtg3ewxqwwrwjxfgc4n4ef9u0tvx7u',
 'P2P.ORG - P2P Val...': 'cosmos132juzk0gdmwuxvx4phug7m3ymyatxlh9m9paea',
 'GAME': 'cosmos1qaa9zej9a0ge3ugpx3pxyx602lxh3ztqda85ee',
 'PRYZM | StakeDrop': 'cosmos1hmd535f69t3x262m6s9wc6jd0dmel2zefrsfmg',
 'NO! Fee to 2025': 'cosmos1zqgheeawp7cmqk27dgyctd80rd8ryhqsltfszt',
 'Informal Systems': 'cosmos16k579jk6yt2cwmqx9dz5xvq9fug2tekv6g34pl',
 'Sikka': 'cosmos1ey69r37gfxvxg62sh4r0ktpuc46pzjrmz29g45',
 'Provalidator': 'cosmos1g48268mu5vfp4wk7dk89r0wdrakm9p5xnm5pr9',
 'Swiss Staking': 'cosmos1y0us8xvsvfvqkk9c6nt5cfyu5au5tww28lcvjn',
 'Imperator.co': 'cosmos1vvwtk805lxehwle9l4yudmq6mn0g32pxqjlrmt',
 'Kiln': 'cosmos1uxlf7mvr8nep3gm7udf2u9remms2jyjqf6efne',
 'Binance Staking': 'cosmos156gqf9837u7d4c4678yt3rl4ls9c5vuuxyhkw6'}

# Load the CSV file
file_path = './inverse_outputfile.csv'
df = pd.read_csv(file_path)

# Clean the data (drop proposalId, but keep voter names/addresses)
df_clean = df.drop(columns=['proposalId'])

# Replace "N/A" values with 0 (which means abstain)
imputer = SimpleImputer(missing_values=np.nan, strategy='mean')
df_imputed = pd.DataFrame(imputer.fit_transform(df_clean), columns=df_clean.columns)

# Perform PCA
pca = PCA(n_components=None)  # Limit to first two components for scatter plot
pca_result = pca.fit_transform(df_imputed.T)  # Transpose so that PCA is done on voters

# Explained variance for each principal component
explained_variance_ratio = pca.explained_variance_ratio_

# Create a DataFrame for explained variance
explained_variance_df = pd.DataFrame({
    'Principal Component': [f"PC{i+1}" for i in range(len(explained_variance_ratio))],
    'Explained Variance Ratio': explained_variance_ratio
})

# Save the explained variance ratios to a CSV file
output_file_path = './inverse_explained_variance_scatter.csv'
explained_variance_df.to_csv(output_file_path, index=False)

# Extract voter names (from the header of the columns)
voter_names = df_clean.columns

# Create a scatter plot of the first two principal components
plt.figure(figsize=(10, 8))
plt.scatter(pca_result[:, 0], pca_result[:, 1], alpha=0.7, color='b')

# Annotate points with voter names (addresses/ens)
# for i in range(len(voter_names)):  # Iterate over the number of voters (columns)
#     plt.annotate(voter_names[i], (pca_result[i, 0], pca_result[i, 1]), fontsize=9, alpha=0.7, color='b')

plt.title('Voting Correlation Between Stakers')
plt.xlabel('Principal Component 1')
plt.ylabel('Principal Component 2')
plt.grid(True)
plt.show()

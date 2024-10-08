from flipside import Flipside
import pandas as pd
import time

# Initialize `Flipside` with your API Key and API URL
flipside = Flipside("----", "https://api-v2.flipsidecrypto.xyz")

# Define the base SQL query
base_sql = """
SELECT 
  VOTER,
  PROPOSAL_ID,
  VOTE_OPTION
FROM 
  cosmos.gov.fact_governance_votes
WHERE
  PROPOSAL_ID IN (966, 957, 956, 955, 954, 952, 950, 948, 947, 946, 944, 943, 940, 
                  937, 935, 931, 930, 927, 926, 924, 921, 920, 917, 916, 914, 912, 
                  897, 895, 893, 890, 885, 880, 877, 871, 868, 867, 865, 864, 862, 
                  861, 860, 858, 856, 855, 854, 853, 851, 848, 845, 844, 843, 842, 
                  839, 836, 835, 833, 829, 827, 826, 825, 823, 821, 819, 818, 817, 
                  814, 811, 810, 805, 804, 801, 800, 799, 798, 797, 794, 793, 792, 
                  791, 790, 787, 717, 687, 202, 187, 155, 104, 103, 101, 98, 97, 
                  96, 95, 94, 93, 90, 89, 88, 87, 86, 84, 83, 82, 81, 80, 78, 77, 
                  76, 74, 73, 72, 71, 70, 69, 68, 67, 66, 65, 64, 63, 62, 60, 59, 
                  58, 57, 56, 54, 52)
ORDER BY 
  BLOCK_TIMESTAMP DESC
LIMIT 10000 OFFSET {}
"""

# Function to fetch data with pagination
def fetch_data_in_batches(flipside, sql):
    all_data = []
    offset = 0
    limit = 10000
    more_data = True
    total_rows = 0

    while more_data:
        # Format SQL query with the current offset
        sql_with_offset = sql.format(offset)
        
        # Run the query against Flipside's query engine
        query_result_set = flipside.query(sql_with_offset)

        # Check if the query was successful
        if query_result_set.status == 'QUERY_STATE_SUCCESS':
            data = query_result_set.records  # Fetch the records
            all_data.extend(data)  # Append the current batch to all_data
            
            # If fewer rows are returned than the limit, all data has been fetched
            if len(data) < limit:
                more_data = False
            else:
                offset += limit  # Move to the next batch
            
            # Optional: Add a delay to avoid hitting rate limits (if necessary)
            print(f"Fetched {len(data)} rows, continuing to next batch...")
            total_rows += len(data)
            print(f"Total rows: {total_rows}")
            

        else:
            print(f"Query failed. Status: {query_result_set.status}, Message: {query_result_set.message}")
            raise Exception(f"Query failed with status: {query_result_set.status}")

    return all_data

# Fetch all data in batches
try:
    all_data = fetch_data_in_batches(flipside, base_sql)

    # Convert the combined data into a DataFrame
    df = pd.DataFrame(all_data)

    # Export the DataFrame to a CSV file in chunks to handle large data
    chunk_size = 100000
    for i in range(0, len(df), chunk_size):
        chunk = df.iloc[i:i + chunk_size]
        chunk.to_csv('flipside_data.csv', mode='a', index=False, header=(i == 0))

    print(f"Data fetched: {len(df)} rows")
except Exception as e:
    print(f"Error fetching data: {e}")

import time
import pandas as pd
import openai
import os
import tqdm

query_path = input("Enter the path to the query CSV file: ")
output_file_name = input("Enter output file name:")
output_file_path = input("Enter output folder Path:")

# Read the CSV data into a Pandas DataFrame
data = pd.read_csv(query_path)

# Create an empty DataFrame to store the results
output_data = pd.DataFrame()

openai.api_key = "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"
model_engine = "text-davinci-002"
batch_size = 10

# Iterate over the rows of the input data
for index, row in data.iterrows():
    sku = row["SKU"]
    response_list = []
    print(f"Processing SKU {sku}...")

    # Iterate over the columns of the input data
    for col in data.columns[1:]:
        query = row[col]
        print(f"Processing column {col}...")

        # Send the query to OpenAI API
        completion = openai.Completion.create(
            engine=model_engine,
            prompt=query,
            max_tokens=3000,
            n=1,
            stop=None,
            temperature=0.7,
        )

        # Extract the response from the API output
        response = completion.choices[0].text.strip()

        # Add the response to the list
        response_list.append(response)

        # Wait for 3 seconds before processing the next query
        time.sleep(3)

    # Add the SKU and its corresponding queries and responses to the output DataFrame
    new_row = {"SKU": sku, **{f"Query_{i}": row[col] for i, col in enumerate(data.columns[1:], 1)},
               **{f"Response_{i}": response for i, response in enumerate(response_list, 1)}}
    output_data = pd.concat([output_data, pd.DataFrame(new_row, index=[0])], ignore_index=True)


# Check if the output file path is valid and writable
if os.access(output_file_path, os.W_OK):
    output_path = os.path.join(output_file_path, output_file_name)
    output_data.to_csv(output_path, index=False)
    print(f"Output file saved at: {output_path}")
else:
    print(f"Error: cannot write to {output_file_path}. Please provide a valid output file path.")

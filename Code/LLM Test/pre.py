import pandas as pd

# Define the mappings for gender, age, education, and income
gender_mapping = {0: 'female', 1: 'male'}
age_mapping = {
    0: '19 or below',
    1: '20 - 24',
    2: '25 - 34',
    3: '35 - 44',
    4: '45 - 54',
    5: '55 or above'
}
education_mapping = {
    0: 'High school degree or lower',
    1: 'Associate or vocational degree',
    2: 'Bachelor degree',
    3: 'Master or doctoral degree'
}
income_mapping = {
    0: 'CNY 3000 or below',
    1: 'CNY 3,000 - 5,000',
    2: 'CNY 5,000 - 10,000',
    3: 'CNY 10,000 - 20,000',
    4: 'CNY 20,000 - 40,000',
    5: 'CNY 40,000 - 80,000',
    6: 'CNY 80,000 or above',
    7: 'Do not answer'
}

# Read the data from the Excel file
file_path = 'NanjingData.xlsx'  # The Excel file should be in the same directory
data = pd.read_excel(file_path)

# Prepare to collect all outputs
outputs = []

# Iterate over each row in the DataFrame and format the output
for index, row in data.iterrows():
    gender = gender_mapping.get(row['S1_Gender'], 'unknown')
    age = age_mapping.get(row['S1_Age'], 'unknown')
    education = education_mapping.get(row['S1_Education'], 'unknown')
    income = income_mapping.get(row['S1_Income'], 'unknown')

    # Create the formatted output for each respondent
    output = (
        f"You will assume the role of a survey respondent. The purpose of this survey is to assess "
        f"individuals' risk attitudes through a series of 10 consecutive lottery questions. For each question, "
        f"you are required to carefully consider and compare the expected income with the potential risks; however, "
        f"you need not disclose your thought process to me—simply provide your answers. In this survey, you will "
        f"portray a {age}-year-old {gender} from Nanjing, China, who has completed the highest level of education: "
        f"{education}. Your monthly income is: {income}."
    )

    # Append the output to the list
    outputs.append(output)

# Create a DataFrame from the outputs
output_df = pd.DataFrame(outputs, columns=['Response'])

# Save the DataFrame to a new Excel file in the same directory
output_file_path = 'survey_responses.xlsx'
output_df.to_excel(output_file_path, index=False)

print(f"Survey responses have been saved to {output_file_path}.")
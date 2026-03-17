import pandas as pd
from datetime import datetime
import os
import sys


# ===============================
# HELPER FUNCTIONS
# ===============================

def split_name(full_name):

    if pd.isna(full_name):
        return "", ""

    name = str(full_name).strip()

    # Expecting: Last,First Middle
    if "," in name:
        last_part, first_part = name.split(",", 1)

        last_name = last_part.strip()

        # First part may contain middle initial -> take first token only
        first_name = first_part.strip().split()[0]

        return first_name, last_name
    
    

    # Fallback: if no comma, try simple split
    parts = name.split()
    if len(parts) >= 2:
        return parts[0], parts[-1]

    return name, ""

def split_range(value):
    value = str(value).strip()
    lower, upper = value.split("-")
    return lower.strip(), upper.strip()

def format_date(date_string):

    # Handle missing / NaN values
    if pd.isna(date_string):
        return ""

    date_string = str(date_string).strip()

    if date_string == "":
        return ""

    parsed = datetime.strptime(date_string, "%b %d, %Y")
    return parsed.strftime("%Y-%m-%d")


# ===============================
# INPUT HANDLING
# ===============================

print("\n=== SAT Transformation Script (V2) ===")
print("Place the downloaded SAT file in the same folder as this script.\n")

input_file = input("Enter file name (including .xlsx): ").strip()

if not os.path.isfile(input_file):
    print(f"\nERROR: File '{input_file}' not found.")
    sys.exit(1)

df = pd.read_excel(input_file, header=3)
df.columns = df.columns.str.strip()

# ===============================
# TEST DEFINITIONS
# ===============================

test_definitions = [

    # 1
    {
        "label": "Overall",
        "score_column": "Total Score (400-1600)",
        "score_type": "numeric",
        "test_class": "Composite",
        "test_group": "Overall",
        "test_subgroup": "Overall",
        "subject": "Overall"
    },

    # 2
    {
        "label": "English Language Arts - SectionScore",
        "score_column": "Reading and Writing Section Score (200-800)",
        "score_type": "numeric",
        "test_class": "Component",
        "test_group": "Section",
        "test_subgroup": "English Language Arts",
        "subject": "English Language Arts"
    },

    # 3
    {
        "label": "Math - SectionScore",
        "score_column": "Math Section Score (200-800)",
        "score_type": "numeric",
        "test_class": "Component",
        "test_group": "Section",
        "test_subgroup": "Mathematics",
        "subject": "Mathematics"
    },

    # 4
    {
        "label": "English Language Arts - Section",
        "score_column": "Reading and Writing Section",
        "score_type": "range",
        "test_class": "Component",
        "test_group": "Section",
        "test_subgroup": "English Language Arts",
        "subject": "English Language Arts"
    },

    # 5
    {
        "label": "English Language Arts - Information and Ideas",
        "score_column": "Information and Ideas",
        "score_type": "range",
        "test_class": "Strand",
        "test_group": "Subscore",
        "test_subgroup": "Information and Ideas",
        "subject": "English Language Arts"
    },

    # 6
    {
        "label": "English Language Arts - Craft and Structure",
        "score_column": "Craft and Structure",
        "score_type": "range",
        "test_class": "Strand",
        "test_group": "Subscore",
        "test_subgroup": "Craft and Structure",
        "subject": "English Language Arts"
    },

    # 7
    {
        "label": "English Language Arts - Standard English Conventions",
        "score_column": "Standard English Conventions",
        "score_type": "range",
        "test_class": "Strand",
        "test_group": "Subscore",
        "test_subgroup": "Standard English Conventions",
        "subject": "English Language Arts"
    },

    # 8
    {
        "label": "English Language Arts - Expression of Ideas",
        "score_column": "Expression of Ideas",
        "score_type": "range",
        "test_class": "Strand",
        "test_group": "Subscore",
        "test_subgroup": "Expression of Ideas",
        "subject": "English Language Arts"
    },

    # 9
    {
        "label": "Math - Math Section",
        "score_column": "Math Section",
        "score_type": "range",
        "test_class": "Component",
        "test_group": "Section",
        "test_subgroup": "Mathematics",
        "subject": "Mathematics"
    },

    # 10
    {
        "label": "Math - Algebra",
        "score_column": "Algebra",
        "score_type": "range",
        "test_class": "Strand",
        "test_group": "Subscore",
        "test_subgroup": "Algebra",
        "subject": "Mathematics"
    },

    # 11
    {
        "label": "Math - Advanced Math Performance Score Band",
        "score_column": "Advanced Math Performance Score Band",
        "score_type": "range",
        "test_class": "Strand",
        "test_group": "Subscore",
        "test_subgroup": "Advanced Math",
        "subject": "Mathematics"
    },

    # 12
    {
        "label": "Math - Problem-Solving and Data Analysis",
        "score_column": "Problem-Solving and Data Analysis",
        "score_type": "range",
        "test_class": "Strand",
        "test_group": "Subscore",
        "test_subgroup": "Problem-Solving and Data Analysis",
        "subject": "Mathematics"
    },

    # 13
    {
        "label": "Math - Geometry and Trigonometry",
        "score_column": "Geometry and Trigonometry",
        "score_type": "range",
        "test_class": "Strand",
        "test_group": "Subscore",
        "test_subgroup": "Geometry and Trigonometry",
        "subject": "Mathematics"
    },
]


# ===============================
# TRANSFORMATION ENGINE
# ===============================

output_rows = []

for _, row in df.iterrows():

    # Skip entire student if N/A
    if str(row["Total Score (400-1600)"]).strip().upper() == "N/A":
        continue

    # Student-level values
    #student_id = str(row["State Student ID"])

    #district student id creation
    district_student_id = str(row["District Student ID"]).strip()
    
    raw_student_id = str(row["State Student ID"]).strip()

    # Handle missing or "Not Provided" State Student ID
    if raw_student_id == "" or raw_student_id.upper() == "NOT PROVIDED" or raw_student_id.upper() == "NAN":
        fallback_id = str(row["Record Locator"]).strip()
        student_id = f"RL_{fallback_id}"
    else:
        student_id = raw_student_id

    




    record_locator = row["Record Locator"]
    # timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    now = datetime.now()
    date_part = now.strftime("%Y%m%d")
    time_part = now.strftime("%H%M%S")

    first_name, last_name = split_name(row["Student Name"])
    formatted_test_date = format_date(row["Tested On"])
    student_birthdate = format_date(row["Date of Birth"])

    for definition in test_definitions:

        score_value = row.get(definition["score_column"])

        # Skip row if score missing
        if pd.isna(score_value):
            continue

        if definition["score_type"] == "numeric":
            test_score_value = score_value
            lower_bound = ""
            upper_bound = ""

        elif definition["score_type"] == "range":
            lower_bound, upper_bound = split_range(score_value)
            test_score_value = ""

#added might remove
        test_primary_result = ""

        if definition["label"] == "English Language Arts - SectionScore":
            test_primary_result = row.get("Met RW Section Benchmark")

        elif definition["label"] == "Math - SectionScore":
            test_primary_result = row.get("Met Math Section Benchmark")

        test_percentile = ""

        if definition["label"] == "Overall":
            test_percentile = row.get("Total Score State Percentile")

        elif definition["label"] == "English Language Arts - SectionScore":
            test_percentile = row.get("Reading Writing Section Score State Percentile")

        elif definition["label"] == "Math - SectionScore":
            test_percentile = row.get("Math Section Score State Percentile")

        if not pd.isna(test_percentile):
            test_percentile = str(test_percentile).strip().strip("<>")
#end added might remove

        # prod_test_id = (
        #     f"SAT - {definition['label']} - "
        #     f"{student_id} - "
        #     f"{date_part} - "
        #     f"{time_part}"

        # )

        tested_on_for_id = formatted_test_date.replace("-", "")

        prod_test_id = (
            f"SAT - {definition['label']} - "
            f"{student_id} - "
            f"{tested_on_for_id}"
            #f"{date_part}"
            #f"{time_part}"
        )

        test_name = f"SAT - {definition['label']}"

        new_row = {
            "XTBL_TEST_ADMIN.PROD_TEST_ID": prod_test_id,
            "XTBL_TEST_ADMIN.DISTRICT_CODE": "1813080",
            "XTBL_TEST_ADMIN.DISTRICT_STUDENT_ID": district_student_id,
            "XTBL_TEST_ADMIN.STATE_STUDENT_ID": student_id,
            "XTBL_TEST_ADMIN.DISTRICT_SCHOOL_ID": "2493",
            "XTBL_TEST_ADMIN.VENDOR_SCHOOL_ID": "Westfield High School",
            "XTBL_TEST_ADMIN.TEST_ADMIN_DATE_STR": formatted_test_date,
            "XTBL_TEST_ADMIN.STUDENT_FIRST_NAME": first_name,
            "XTBL_TEST_ADMIN.STUDENT_LAST_NAME": last_name,
            "XTBL_TEST_ADMIN.STUDENT_BIRTHDATE_STR": student_birthdate,
            "XTBL_TEST_SCORES.TEST_NUMBER": f"SAT_{definition['label']}",
            "XTBL_TEST_SCORES.TEST_SCORE_VALUE": test_score_value,
            "XTBL_TEST_SCORES.TEST_PRIMARY_RESULT": test_primary_result,
            "XTBL_TEST_SCORES.TEST_LOWER_BOUND": lower_bound,
            "XTBL_TEST_SCORES.TEST_UPPER_BOUND": upper_bound,
            "XTBL_TEST_SCORES.TEST_PERCENTILE_SCORE": test_percentile,
            "XTBL_TESTS.DISTRICT_CODE":"1813080",
            "XTBL_TESTS.TEST_CLASS": definition["test_class"],
            "XTBL_TESTS.TEST_NAME": test_name,
            "XTBL_TESTS.TEST_GROUP": definition["test_group"],
            "XTBL_TESTS.TEST_SUBGROUP": definition["test_subgroup"],
            "XTBL_TESTS.TEST_TYPE":"College Readiness",
            "XTBL_TESTS.TEST_SUBJECT": definition["subject"],
            "XTBL_TESTS.TEST_VENDOR": "The College Board",
            "XTBL_TESTS.TEST_PRODUCT": "SAT",
            "XTBL_TESTS.ETL_REF_BNCH_TEST_NUMBER":"N",
            "XTBL_TESTS.ETL_REF_BNCH_ADMIN_PERIOD":"N",
            "XTBL_TESTS.ETL_REF_BNCH_SUBJECT":"N",
            "XTBL_TESTS.ETL_REF_BNCH_GRADE_GROUP":"N",
            "XTBL_TESTS.ETL_CUST_BNCH_TEST_NUMBER":"N",
            "XTBL_TESTS.ETL_CUST_BNCH_ADMIN_PERIOD":"N",
            "XTBL_TESTS.ETL_CUST_BNCH_SUBJECT":"N",
            "XTBL_TESTS.ETL_CUST_BNCH_GRADE_GROUP":"N",
        }

        output_rows.append(new_row)


# ===============================
# OUTPUT
# ===============================

output_df = pd.DataFrame(output_rows)

os.makedirs("Transformed Files", exist_ok=True)

file_timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
output_filename = f"sat_transformed_{file_timestamp}.csv"
full_path = os.path.join("Transformed Files", output_filename)

# Write CSV
output_df.to_csv(full_path, index=False)

# Write TSV (tab-separated)
tsv_filename = f"sat_transformed_{file_timestamp}.tsv"
tsv_full_path = os.path.join("Transformed Files", tsv_filename)
output_df.to_csv(tsv_full_path, index=False, sep="\t")

# Write TXT (tab-separated)
txt_filename = f"sat_transformed_{file_timestamp}.txt"
txt_full_path = os.path.join("Transformed Files", txt_filename)
output_df.to_csv(txt_full_path, index=False, sep="\t")

print(f"\nTransformation complete.")
print(f"File written to: {full_path}")
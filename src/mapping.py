# Fields in the PostgreSQL customers table
DATABASE_FIELDS = [
    "customer_id",
    "first_name",
    "last_name",
    "email",
    "age"
]

REQUIRED_FIELDS = [
    "customer_id",
    "first_name",
    "last_name",
    "email"
]


def validate_mapping(mapping, excel_columns):
    errors = []

    # Ensure required database fields have a matching Excel column
    for field in REQUIRED_FIELDS:
        if not mapping.get(field):
            errors.append(f"Please map the required field: {field}")

    # Prevent using the same Excel column for multiple fields
    selected_columns = [col for col in mapping.values() if col]

    if len(selected_columns) != len(set(selected_columns)):
        errors.append("Each Excel column can only be mapped once.")

    # Ensure every selected column exists in the uploaded spreadsheet
    for column in selected_columns:
        if column not in excel_columns:
            errors.append(f"Invalid Excel column selected: {column}")

    return errors

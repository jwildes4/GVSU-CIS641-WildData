Team name: Wild Data

Team members: Jack Wildes

# Introduction

My Excel workflow-based project is a data management system designed to simplify the process of transferring data from Excel spreadsheets into a PostgreSQL database. Organizations/companies often use spreadsheets to collect and maintain information, but manually transferring that information into a database can be a time-consuming and error-prone process. This system will provide users with a centralized way to upload spreadsheets and prepare their data for database import.

The system will allow users to map spreadsheet columns to the appropriate fields in the PostgreSQL database and validate the data before it is imported. The system will identify issues such as missing, incorrectly formatted, or invalid data and report these errors out to the user so they can be corrected before the import process. This way, we will ensure that the data is in a clean format for translation.

After the data successfully passes validation, the system will import the information into the PostgreSQL database and provide confirmation of the results. The overall goal for this project is to create a practical and user-friendly system that helps reduce manual data entry work while also improving the accuracy and consistency of database imports.

# Anticipated Technologies

- Frontend: HTML and JavaScript
- Backend: Python
- Database: PostgreSQL
- Data Processing: Python libraries like Pandas for reading and processing Excel files
- Database Connectivity: some PostgreSQL connector/driver for communication between the application and database
- Version Control: Git/GitHub with this repository
- Development Environment: VS Code

# Method/Approach

I intend to develop the project in an incremental fashion, beginning with ironing out system requirements and designing the database structure. The next step will be creating a basic interface that would enable users to upload Excel files. Once file uploads are functioning, the data mapping and validation functionality is next to be developed, enabling users to identify and correct problems before importing their data.

After the validation process is working, I will work to implement the PostgreSQL database integration and data import functionality. I will then work on testing the system using different Excel spreadsheet examples and various valid and invalid data scenarios. Finally, depending on time, I will refine the interface, error messages, documentation, and overall usability to finalize project functionality.

# Estimated Timeline

- Requirements / project planning: 1-2 weeks
- Database design and setup: 1-2 weeks
- Basic application/UI development: 2 weeks
- Excel file upload and processing (1 week)
- Column mapping functionality (1 weeks)
- Data validation and error reporting (1-2 weeks)
- PostgreSQL import functionality (1 week)
- Testing, debugging, and documentation (1 week)

Estimated total: roughly 9–12 weeks in total, depending on the complexity. Obviously this is a very rough estimate and based on the limited course timeline, I won't have time to get everything in perfect working order. However, I will ensure that I have some of the main project functionalities in working order to demo.

# Anticipated Problems

One potential challenge could be handling the variety of formats and structures that users may have in their Excel spreadsheets. Different spreadsheets may contain different column names, data types, missing values, formatting, unexpected entries, table structures, etc. so the system would ideally need to handle these situations without causing invalid data to enter the database.

Another challenge could be developing a mapping system that is simple for users while still providing enough flexibility to map spreadsheet columns to the appropriate database fields. Database integration and validation might also have some technical issues like when dealing with incorrect data types, duplicate records, database constraints, or failed imports. Depending on time, thorough testing with different spreadsheet configurations would probably be necessary to identify and resolve these issues.

Overall, having a nice, clean interface that integrates all of this functionality will likely be difficult to achieve in the given project timeline. Amid these time constraints, I anticipate I will have to make minor adjustments to the scope and testing of some components.

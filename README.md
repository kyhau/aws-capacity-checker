# aws-capacity-checker

A simple script to retrieve EC2 compute capacity of an AWS account, output results in json and csv files, and display results in html.

## Demo

[https://kyhau.github.io/aws-capacity-checker/docs/ec2_capacity_table.html](https://kyhau.github.io/aws-capacity-checker/docs/ec2_capacity_table.html).

```
# Create and activate virtualenv
# Then install requirements
cd capacity_checks
pip install -r requirements.txt


# Retrieve capacity data for the stacks of an AWS account (or only those specified in the STACK_FILE)
# The output will be writting to capacity_reports/<ACCOUNT_ID|STACK_FILE_NAME>.json

python capacity_checker.py [--stack-file STACK_FILE] [--profile AWS_PROFILE]


# Generate csv file for html report
# The output will be written to csv_reports

python generate_csv_reports.py capacity_reports/<ACCOUNT_ID|STACK_FILE_NAME>.json


cd html
python -m http.server 8080

# Open in brower: http://localhost:8080/ec2_capacity_table.html

```
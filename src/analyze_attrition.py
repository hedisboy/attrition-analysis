from load_data import load_employee_data, clean_employee_data
from metrics import (
    attrition_rate,
    attrition_by_department,
    attrition_by_overtime,
    average_income_by_attrition,
    satisfaction_summary,
)


def print_section(title, value):
    print("\n" + "=" * 60)
    print(title)
    print("=" * 60)
    print(value)


if __name__ == "__main__":
    df = load_employee_data("data/employees.csv")
    df = clean_employee_data(df)

    print_section("Overall Attrition Rate", f"{attrition_rate(df)}%")
    print_section("Attrition by Department", attrition_by_department(df).to_string(index=False))
    print_section("Attrition by Overtime", attrition_by_overtime(df).to_string(index=False))
    print_section("Average Monthly Income by Attrition", average_income_by_attrition(df).to_string(index=False))
    print_section("Job Satisfaction Summary", satisfaction_summary(df).to_string(index=False))

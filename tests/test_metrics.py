import pandas as pd
import pytest
from src.metrics import (
    attrition_rate,
    attrition_by_department,
    attrition_by_overtime,
    average_income_by_attrition,
    satisfaction_summary,
)
from src.load_data import clean_employee_data


@pytest.fixture
def sample_df():
    # 6 employees across 3 departments.
    # All overtime=Yes employees left; all overtime=No employees stayed.
    return pd.DataFrame({
        "employee_id": [1, 2, 3, 4, 5, 6],
        "department": ["Sales", "Sales", "HR", "HR", "IT", "IT"],
        "overtime": ["Yes", "No", "Yes", "No", "Yes", "No"],
        "monthly_income": [4000.0, 6000.0, 3000.0, 7000.0, 5000.0, 8000.0],
        "job_satisfaction": [1, 4, 2, 3, 1, 4],
        "travel_frequency": ["Frequent", "Rarely", "Frequent", "Rarely", "Frequent", "Rarely"],
        "years_at_company": [1, 5, 2, 8, 1, 10],
        "attrition": ["Yes", "No", "Yes", "No", "Yes", "No"],
    })


# --- attrition_rate ---

def test_attrition_rate_returns_expected_percent():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "department": ["Sales", "Sales", "HR", "HR"],
        "attrition": ["Yes", "No", "No", "Yes"],
    })
    assert attrition_rate(df) == 50.0


def test_attrition_rate_all_leave(sample_df):
    df = sample_df.copy()
    df["attrition"] = "Yes"
    assert attrition_rate(df) == 100.0


def test_attrition_rate_none_leave(sample_df):
    df = sample_df.copy()
    df["attrition"] = "No"
    assert attrition_rate(df) == 0.0


# --- attrition_by_department ---

def test_attrition_by_department_returns_expected_columns():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4],
        "department": ["Sales", "Sales", "HR", "HR"],
        "attrition": ["Yes", "No", "No", "Yes"],
    })
    result = attrition_by_department(df)
    assert list(result.columns) == ["department", "employees", "leavers", "attrition_rate"]


def test_attrition_by_department_values(sample_df):
    result = attrition_by_department(sample_df)
    # Each department has 2 employees, 1 leaver → 50%
    assert set(result["department"]) == {"Sales", "HR", "IT"}
    for _, row in result.iterrows():
        assert row["employees"] == 2
        assert row["leavers"] == 1
        assert row["attrition_rate"] == 50.0


def test_attrition_by_department_sorted_descending():
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4, 5, 6],
        "department": ["Sales", "Sales", "HR", "HR", "IT", "IT"],
        "attrition": ["Yes", "Yes", "Yes", "No", "No", "No"],
    })
    result = attrition_by_department(df)
    assert result["department"].tolist() == ["Sales", "HR", "IT"]
    assert result["attrition_rate"].tolist() == [100.0, 50.0, 0.0]


# --- attrition_by_overtime ---

def test_attrition_by_overtime_columns(sample_df):
    result = attrition_by_overtime(sample_df)
    assert list(result.columns) == ["overtime", "employees", "leavers", "attrition_rate"]


def test_attrition_by_overtime_values(sample_df):
    result = attrition_by_overtime(sample_df)
    yes_row = result[result["overtime"] == "Yes"].iloc[0]
    no_row = result[result["overtime"] == "No"].iloc[0]
    assert yes_row["employees"] == 3
    assert yes_row["leavers"] == 3
    assert yes_row["attrition_rate"] == 100.0
    assert no_row["employees"] == 3
    assert no_row["leavers"] == 0
    assert no_row["attrition_rate"] == 0.0


# --- average_income_by_attrition ---

def test_average_income_by_attrition_columns(sample_df):
    result = average_income_by_attrition(sample_df)
    assert list(result.columns) == ["attrition", "avg_monthly_income"]


def test_average_income_by_attrition_values(sample_df):
    result = average_income_by_attrition(sample_df)
    yes_avg = result[result["attrition"] == "Yes"]["avg_monthly_income"].iloc[0]
    no_avg = result[result["attrition"] == "No"]["avg_monthly_income"].iloc[0]
    # Leavers: 4000, 3000, 5000 → mean = 4000.0
    # Stayers: 6000, 7000, 8000 → mean = 7000.0
    assert yes_avg == 4000.0
    assert no_avg == 7000.0


# --- satisfaction_summary ---

def test_satisfaction_summary_columns(sample_df):
    result = satisfaction_summary(sample_df)
    assert list(result.columns) == ["job_satisfaction", "total_employees", "leavers", "attrition_rate"]


def test_satisfaction_summary_rate_uses_group_headcount_not_company_total():
    # Regression test for denominator bug.
    # Group 1: 4 employees, 2 leavers → 50%
    # Group 2: 2 employees, 2 leavers → 100%
    # The wrong formula (leavers / total_company_leavers) gives 50% for both groups.
    df = pd.DataFrame({
        "employee_id": [1, 2, 3, 4, 5, 6],
        "department": ["A"] * 6,
        "overtime": ["No"] * 6,
        "monthly_income": [5000.0] * 6,
        "job_satisfaction": [1, 1, 1, 1, 2, 2],
        "travel_frequency": ["Rarely"] * 6,
        "years_at_company": [1] * 6,
        "attrition": ["Yes", "Yes", "No", "No", "Yes", "Yes"],
    })
    result = satisfaction_summary(df)
    sat1 = result[result["job_satisfaction"] == 1].iloc[0]
    sat2 = result[result["job_satisfaction"] == 2].iloc[0]
    assert sat1["attrition_rate"] == 50.0
    assert sat2["attrition_rate"] == 100.0


def test_satisfaction_summary_sorted_by_satisfaction(sample_df):
    result = satisfaction_summary(sample_df)
    scores = result["job_satisfaction"].tolist()
    assert scores == sorted(scores)


# --- clean_employee_data ---

def test_clean_employee_data_raises_on_missing_column():
    df = pd.DataFrame({"employee_id": [1], "department": ["Sales"]})
    with pytest.raises(ValueError, match="Missing required columns"):
        clean_employee_data(df)


def test_clean_employee_data_fills_missing_values():
    df = pd.DataFrame({
        "employee_id": [1, 2],
        "department": [None, "Sales"],
        "age": [30, 35],
        "monthly_income": [None, 5000.0],
        "job_satisfaction": [None, 3.0],
        "overtime": [None, "No"],
        "travel_frequency": [None, "Rarely"],
        "years_at_company": [2, 5],
        "attrition": ["Yes", "No"],
    })
    result = clean_employee_data(df)
    assert result["department"].iloc[0] == "Unknown"
    assert result["overtime"].iloc[0] == "No"
    assert result["travel_frequency"].iloc[0] == "Rarely"
    assert result["job_satisfaction"].iloc[0] == 3
    assert result["monthly_income"].iloc[0] == 5000.0  # median of [NaN, 5000]


def test_clean_employee_data_normalizes_strings():
    df = pd.DataFrame({
        "employee_id": [1],
        "department": ["  Sales  "],
        "age": [30],
        "monthly_income": [5000.0],
        "job_satisfaction": [3.0],
        "overtime": ["  Yes  "],
        "travel_frequency": ["  Frequent  "],
        "years_at_company": [2],
        "attrition": ["yes"],
    })
    result = clean_employee_data(df)
    assert result["department"].iloc[0] == "Sales"
    assert result["overtime"].iloc[0] == "Yes"
    assert result["travel_frequency"].iloc[0] == "Frequent"
    assert result["attrition"].iloc[0] == "Yes"  # title-cased

import pandas as pd


def attrition_rate(df: pd.DataFrame) -> float:
    leavers = df[df["attrition"] == "Yes"]
    return round((len(leavers) / len(df)) * 100, 2)


def attrition_by_department(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("department").agg(
        employees=("employee_id", "count"),
        leavers=("attrition", lambda s: (s == "Yes").sum()),
    )
    grouped["attrition_rate"] = round((grouped["leavers"] / grouped["employees"]) * 100, 2)
    return grouped.sort_values("attrition_rate", ascending=False).reset_index()


def attrition_by_overtime(df: pd.DataFrame) -> pd.DataFrame:
    grouped = df.groupby("overtime").agg(
        employees=("employee_id", "count"),
        leavers=("attrition", lambda s: (s == "Yes").sum()),
    )
    grouped["attrition_rate"] = round((grouped["leavers"] / grouped["employees"]) * 100, 2)
    return grouped.reset_index()


def average_income_by_attrition(df: pd.DataFrame) -> pd.DataFrame:
    return (
        df.groupby("attrition")["monthly_income"]
        .mean()
        .round(2)
        .reset_index(name="avg_monthly_income")
    )


def satisfaction_summary(df: pd.DataFrame) -> pd.DataFrame:
    grouped = (
        df.groupby("job_satisfaction")
        .agg(total_employees=("employee_id", "count"), leavers=("attrition", lambda s: (s == "Yes").sum()))
        .reset_index()
    )
    grouped["attrition_rate"] = round((grouped["leavers"] / (df["attrition"] == "Yes").sum()) * 100, 2)
    return grouped.sort_values("job_satisfaction")

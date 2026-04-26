import pandas as pd

REQUIRED_COLUMNS = [
    "employee_id",
    "department",
    "age",
    "monthly_income",
    "job_satisfaction",
    "overtime",
    "travel_frequency",
    "years_at_company",
    "attrition",
]


def load_employee_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    return df


def clean_employee_data(df: pd.DataFrame) -> pd.DataFrame:
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    cleaned = df.copy()
    cleaned["department"] = cleaned["department"].fillna("Unknown").str.strip()
    cleaned["overtime"] = cleaned["overtime"].fillna("No").str.strip()
    cleaned["travel_frequency"] = cleaned["travel_frequency"].fillna("Rarely").str.strip()
    cleaned["attrition"] = cleaned["attrition"].astype(str).str.strip().str.title()
    cleaned["job_satisfaction"] = cleaned["job_satisfaction"].fillna(3)
    cleaned["monthly_income"] = cleaned["monthly_income"].fillna(cleaned["monthly_income"].median())
    return cleaned

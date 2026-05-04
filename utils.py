import pandas as pd

# =========================
# KPI CALCULATIONS
# =========================
def get_kpis(df):
    total_value = df["contract_value"].sum()
    total_contracts = len(df)
    total_vendors = df["vendor_name"].nunique()

    return {
        "total_value": total_value,
        "total_contracts": total_contracts,
        "total_vendors": total_vendors
    }


# =========================
# SPENDING TREND
# =========================
def get_spending_trend(df):
    return df.groupby("year")["contract_value"].sum().reset_index()


# =========================
# TOP VENDORS
# =========================
def get_top_vendors(df, top_n=10):
    return (
        df.groupby("vendor_name")["contract_value"]
        .sum()
        .sort_values(ascending=False)
        .head(top_n)
        .reset_index()
    )


# =========================
# VENDOR MARKET SHARE
# =========================
def get_vendor_market_share(df):
    vendor_total = df.groupby("vendor_name")["contract_value"].sum()
    total = vendor_total.sum()

    market_share = (vendor_total / total).reset_index()
    market_share.columns = ["vendor_name", "market_share"]

    return market_share


# =========================
# HHI CALCULATION
# =========================
def calculate_hhi(df):
    vendor_total = df.groupby("vendor_name")["contract_value"].sum()
    share = vendor_total / vendor_total.sum()
    hhi = (share ** 2).sum()
    return hhi


# =========================
# DEPARTMENT ANALYSIS
# =========================
def get_department_spend(df):
    return (
        df.groupby("owner_org_title")["contract_value"]
        .sum()
        .sort_values(ascending=False)
        .reset_index()
    )


def get_department_contracts(df):
    return (
        df.groupby("owner_org_title")
        .size()
        .reset_index(name="contract_count")
        .sort_values(by="contract_count", ascending=False)
    )


# =========================
# NLP CATEGORY ANALYSIS
# =========================
def get_category_count(df):
    return df["contract_category"].value_counts().reset_index(name="count")


def get_category_spend(df):
    return (
        df.groupby("contract_category")["contract_value"]
        .sum()
        .reset_index()
        .sort_values(by="contract_value", ascending=False)
    )


# =========================
# RISK SYSTEM (AUTO CREATE)
# =========================
def add_risk_columns(df):

    df = df.copy()

    # Risk Score Logic
    df["risk_score"] = (
        (df["contract_value"] > df["contract_value"].quantile(0.9)).astype(int)
    )

    # Risk Level Classification
    def classify(score):
        if score >= 1:
            return "High Risk"
        else:
            return "Low Risk"

    df["risk_level"] = df["risk_score"].apply(classify)

    return df


# =========================
# PREDICTION (SIMPLE BASE)
# =========================
def simple_prediction(vendor_total_spend, vendor_contract_count, month):
    if vendor_contract_count == 0:
        return 0

    base = vendor_total_spend / vendor_contract_count
    adjusted = base * (1 + (month / 100))

    return adjusted


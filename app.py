"""Customer Churn Analysis dashboard (Streamlit version of the Power BI report).

Run with:  python -m streamlit run app.py
"""
from pathlib import Path

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

import predictor
import theme
from theme import AMBER, BLUE, BLUE_SOFT, GREEN, RED, RISK_COLORS

DATA = Path(__file__).parent / "data"

st.set_page_config(page_title="Customer Churn Analytics", page_icon="📊", layout="wide")
theme.apply()


@st.cache_data
def load():
    churn = pd.read_csv(DATA / "cleaned_customer_churn.csv")
    pred = pd.read_csv(DATA / "customer_predictions.csv")
    pred["tenure"] = pd.to_numeric(pred["tenure"], errors="coerce")
    df = pred.merge(churn[["customerID", "Churn"]], on="customerID", how="left")
    metrics = pd.read_csv(DATA / "model_metrics.csv").set_index("Metric")["Value"]
    cm = pd.read_csv(DATA / "confusion_matrix.csv")
    cm["Count"] = pd.to_numeric(cm["Count"])
    return df, metrics, cm


def churn_rate_bar(data, col, horizontal=False):
    g = (
        data.groupby(col)["Churn"].apply(lambda s: (s == "Yes").mean()).reset_index(name="rate")
        .sort_values("rate", ascending=horizontal)
    )
    colors = [RED if r == g["rate"].max() else BLUE_SOFT for r in g["rate"]]
    if horizontal:
        fig = px.bar(g, x="rate", y=col, orientation="h", text=g["rate"].map("{:.1%}".format))
        fig.update_xaxes(tickformat=".0%", showgrid=True, gridcolor="#243650", visible=False)
        fig.update_yaxes(showgrid=False, tickfont=dict(color="#DCE6F5"))
    else:
        fig = px.bar(g, x=col, y="rate", text=g["rate"].map("{:.1%}".format))
        fig.update_yaxes(tickformat=".0%", visible=False)
        fig.update_xaxes(tickfont=dict(color="#DCE6F5"))
    fig.update_traces(
        marker_color=colors, marker_cornerradius=6, textposition="outside",
        textfont=dict(color="#fff", size=12), cliponaxis=False, hovertemplate="%{x}<extra></extra>" if horizontal else "%{x}: %{y:.1%}<extra></extra>",
    )
    fig = theme.style_fig(fig, 280)
    fig.update_layout(bargap=0.35, margin=dict(l=4, r=40 if horizontal else 4, t=22, b=4))
    return fig


df, metrics, cm = load()

# ---------------- sidebar / navigation ----------------
theme.sidebar_brand()
page = st.sidebar.radio(
    "Page",
    ["Customer Churn Analysis", "High-Risk Customers", "Model Performance", "Churn Predictor"],
    label_visibility="collapsed",
)

# ================= page 1 =================
if page == "Customer Churn Analysis":
    theme.side_label("Filters")
    contract = st.sidebar.multiselect("Contract", sorted(df["Contract"].unique()), placeholder="All contracts")
    internet = st.sidebar.multiselect("Internet service", sorted(df["InternetService"].unique()), placeholder="All services")
    d = df
    if contract:
        d = d[d["Contract"].isin(contract)]
    if internet:
        d = d[d["InternetService"].isin(internet)]

    theme.hero(
        "Customer Retention · Churn Prediction · Risk Insights",
        "Customer Churn Analysis",
        "Where customers leave, who is most at risk, and how risk changes with tenure.",
    )
    if d.empty:
        st.warning("No customers match the selected filters.")
        st.stop()

    n, high, churned = len(d), int((d["RiskBand"] == "High").sum()), int((d["Churn"] == "Yes").sum())
    k1, k2, k3 = st.columns(3)
    theme.kpi(k1, "Total customers", f"{n:,}", "in the current selection", BLUE)
    theme.kpi(k2, "High-risk customers", f"{high:,}", f"{high / n:.1%} of customers predicted high risk", RED)
    theme.kpi(k3, "Actual churn rate", f"{churned / n:.1%}", f"{churned:,} customers have left", AMBER)
    st.write("")

    a, b, c = st.columns(3)
    with a.container(border=True):
        theme.chart_title("Churn rate by contract", "Share of customers who left")
        st.plotly_chart(churn_rate_bar(d, "Contract"), use_container_width=True, config={"displayModeBar": False})
    with b.container(border=True):
        theme.chart_title("Churn rate by payment method", "Share of customers who left")
        st.plotly_chart(churn_rate_bar(d, "PaymentMethod", horizontal=True), use_container_width=True, config={"displayModeBar": False})
    with c.container(border=True):
        theme.chart_title("Churn rate by internet service", "Share of customers who left")
        st.plotly_chart(churn_rate_bar(d, "InternetService"), use_container_width=True, config={"displayModeBar": False})

    left, right = st.columns([1, 1.25])
    with left.container(border=True):
        theme.chart_title("Predicted risk distribution", "Customers by model risk band")
        risk = d["RiskBand"].value_counts().reindex(["Low", "Medium", "High"]).reset_index()
        risk.columns = ["RiskBand", "Customers"]
        fig = go.Figure(go.Pie(
            labels=risk["RiskBand"], values=risk["Customers"], hole=0.64, sort=False,
            marker=dict(colors=[RISK_COLORS[r] for r in risk["RiskBand"]], line=dict(color="#142238", width=3)),
            textinfo="percent", textfont=dict(color="#0B1220", size=13), direction="clockwise",
        ))
        fig = theme.style_fig(fig, 300)
        fig.update_layout(
            showlegend=True,
            legend=dict(orientation="h", y=-0.05, x=0.5, xanchor="center", font=dict(color="#DCE6F5")),
            annotations=[dict(text=f"<b>{n:,}</b><br><span style='font-size:12px;color:#8FA4C0'>customers</span>",
                              x=0.5, y=0.5, showarrow=False, font=dict(size=24, color="#fff"))],
        )
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with right.container(border=True):
        theme.chart_title("Predicted churn by tenure", "Average predicted churn, grouped in 6-month tenure bands")
        t = d.groupby("tenure (bins)")["ChurnPrediction"].mean().reset_index().sort_values("tenure (bins)")
        fig = go.Figure(go.Scatter(
            x=t["tenure (bins)"], y=t["ChurnPrediction"], mode="lines+markers",
            line=dict(color=BLUE, width=3, shape="spline"), marker=dict(size=7, color="#fff", line=dict(color=BLUE, width=2)),
            fill="tozeroy", fillcolor="rgba(77,145,250,0.12)",
            hovertemplate="%{x}–%{customdata} months: %{y:.1%}<extra></extra>", customdata=t["tenure (bins)"] + 5,
        ))
        fig = theme.style_fig(fig, 300)
        fig.update_yaxes(tickformat=".0%", rangemode="tozero")
        fig.update_xaxes(title="Tenure (months)", title_font=dict(color="#8FA4C0", size=12))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})

# ================= page 2 =================
elif page == "High-Risk Customers":
    theme.side_label("Filters")
    lo, hi = float(df["MonthlyCharges"].min()), float(df["MonthlyCharges"].max())
    charges = st.sidebar.slider("Monthly charges", lo, hi, (lo, hi))
    contract = st.sidebar.multiselect("Contract", sorted(df["Contract"].unique()), placeholder="All contracts")
    bands = st.sidebar.multiselect("Risk band", ["High", "Medium", "Low"], default=["High", "Medium", "Low"])

    d = df[df["MonthlyCharges"].between(*charges) & df["RiskBand"].isin(bands)]
    if contract:
        d = d[d["Contract"].isin(contract)]

    theme.hero(
        "Retention Action List",
        "High-Risk Customers",
        "Customers most likely to leave, ranked by churn probability and ready for outreach.",
    )
    hi_n = int((d["RiskBand"] == "High").sum())
    k1, k2 = st.columns(2)
    theme.kpi(k1, "High-risk customers", f"{hi_n:,}", "in the current selection", RED)
    theme.kpi(k2, "Customers shown", f"{len(d):,}", "matching the filters", BLUE)
    st.write("")

    table = (
        d[["customerID", "tenure", "Contract", "MonthlyCharges", "RiskBand", "ChurnProbability"]]
        .rename(columns={"customerID": "Customer ID", "tenure": "Tenure (months)", "MonthlyCharges": "Monthly charges",
                         "RiskBand": "Risk band", "ChurnProbability": "Churn probability"})
        .sort_values("Churn probability", ascending=False).reset_index(drop=True)
    )

    def band_style(v):
        c = RISK_COLORS.get(v, "#fff")
        return f"color:{c}; font-weight:600"

    st.dataframe(
        table.style.map(band_style, subset=["Risk band"]),
        use_container_width=True, height=520, hide_index=True,
        column_config={
            "Monthly charges": st.column_config.NumberColumn(format="%.2f"),
            "Churn probability": st.column_config.ProgressColumn(format="percent", min_value=0, max_value=1),
        },
    )
    st.download_button("Download as CSV", table.to_csv(index=False), "high_risk_customers.csv", "text/csv")

# ================= page 3 =================
elif page == "Model Performance":
    theme.hero(
        "Gradient Boosting · Evaluation",
        "Customer Churn Model Performance",
        "How well the model separates customers who will leave from those who will stay.",
    )
    cols = st.columns(5)
    notes = {
        "Accuracy": "overall correct", "Precision": "flagged who truly left",
        "Recall": "actual churners caught", "F1-Score": "precision/recall balance", "ROC-AUC": "class separation",
    }
    for col, name in zip(cols, notes):
        theme.kpi(col, name, f"{metrics[name]:.1%}", notes[name], BLUE)
    st.write("")

    def cnt(actual, pred):
        return int(cm[(cm.Actual == actual) & (cm.Predicted == pred)]["Count"].iloc[0])

    tp, tn, fp, fn = cnt("Churned", "Churned"), cnt("Stayed", "Stayed"), cnt("Stayed", "Churned"), cnt("Churned", "Stayed")

    left, right = st.columns([1.1, 1])
    with left.container(border=True):
        theme.chart_title("Confusion matrix", "Rows are what actually happened, columns are what the model predicted")
        order = ["Stayed", "Churned"]
        mat = cm.pivot(index="Actual", columns="Predicted", values="Count").loc[order, order]
        fig = go.Figure(go.Heatmap(
            z=mat.values, x=[f"Predicted<br>{c}" for c in order], y=[f"Actual<br>{r}" for r in order],
            colorscale=[[0, "#1B2C43"], [1, "#3679E8"]], showscale=False, xgap=6, ygap=6,
            text=mat.values, texttemplate="<b>%{text}</b>", textfont=dict(size=26, color="#fff"),
            hovertemplate="%{y} → %{x}: %{z}<extra></extra>",
        ))
        fig = theme.style_fig(fig, 330)
        fig.update_yaxes(autorange="reversed", showgrid=False, tickfont=dict(color="#DCE6F5", size=13))
        fig.update_xaxes(side="top", tickfont=dict(color="#DCE6F5", size=13))
        st.plotly_chart(fig, use_container_width=True, config={"displayModeBar": False})
    with right:
        st.markdown(
            f"""<div class="insight"><h4>Confusion matrix interpretation</h4><ul>
<li><b>{tn:,}</b> customers were correctly predicted to stay.</li>
<li><b>{tp:,}</b> customers were correctly predicted to churn.</li>
<li><b>{fp:,}</b> were predicted to churn but actually stayed.</li>
<li><b>{fn:,}</b> were predicted to stay but actually churned.</li></ul>
<p>The model caught <b>{tp} of {tp + fn}</b> actual churners (recall {metrics['Recall']:.2%}).
Better precision would reduce unnecessary retention effort.</p></div>""",
            unsafe_allow_html=True,
        )
    st.write("")
    st.markdown(
        f"""<div class="insight"><h4>Model evaluation</h4><ul>
<li><b>Accuracy ({metrics['Accuracy']:.2%}):</b> correctly predicts outcomes for most customers.</li>
<li><b>Precision ({metrics['Precision']:.2%}):</b> {metrics['Precision']:.0%} of predicted churners actually churned.</li>
<li><b>Recall ({metrics['Recall']:.2%}):</b> identifies about {metrics['Recall']:.0%} of actual churners.</li>
<li><b>F1-Score ({metrics['F1-Score']:.2%}):</b> balances precision and recall.</li>
<li><b>ROC-AUC ({metrics['ROC-AUC']:.2%}):</b> good ability to distinguish churners from non-churners.</li></ul>
<p><b>Improvement area:</b> improve precision while maintaining recall to reduce false alarms.</p></div>""",
        unsafe_allow_html=True,
    )

# ================= page 4 =================
else:
    predictor.render()

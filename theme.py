import streamlit as st

BLUE = "#4D91FA"
BLUE_SOFT = "#3A5F96"
RED = "#FF8585"
AMBER = "#F7C66A"
GREEN = "#65D6A2"
TEXT = "#F1F5F9"
MUTED = "#9BAEC8"
RISK_COLORS = {"Low": GREEN, "Medium": AMBER, "High": RED}

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"], .stApp { font-family: 'Inter', 'Segoe UI', sans-serif; }

/* page */
.stApp { background: linear-gradient(135deg,#0B1220 0%,#111D32 55%,#172640 100%); color:#F1F5F9; }
.block-container { max-width: 1250px; padding-top: 1.6rem; padding-bottom: 2rem; }
header[data-testid="stHeader"] { background: transparent; }
[data-testid="stDecoration"], [data-testid="stAppDeployButton"], [data-testid="stMainMenu"], footer, #MainMenu { display:none !important; }
/* keep the "open sidebar" button visible after the sidebar is collapsed */
[data-testid="stSidebarCollapsedControl"], [data-testid="stExpandSidebarButton"], [data-testid="collapsedControl"] {
  display:flex !important; visibility:visible !important; z-index:999; }
[data-testid="stSidebarCollapsedControl"] button, [data-testid="stExpandSidebarButton"] { color:#DCE6F5 !important; }

/* sidebar */
[data-testid="stSidebar"] { background:#101B30; border-right:1px solid #243650; }
[data-testid="stSidebar"] > div:first-child { padding-top: 1.2rem; }
.brand { display:flex; align-items:center; gap:10px; margin-bottom:6px; }
.brand-dot { width:34px; height:34px; border-radius:10px; background:linear-gradient(135deg,#3679E8,#73B3FF);
  display:flex; align-items:center; justify-content:center; font-size:18px; }
.brand-name { font-weight:700; font-size:1.02rem; color:#fff; line-height:1.1; }
.brand-sub { font-size:.72rem; color:#8DBBFF; letter-spacing:1.5px; text-transform:uppercase; }
.side-label { font-size:.7rem; letter-spacing:1.6px; text-transform:uppercase; color:#7F93B0; margin:18px 0 6px; font-weight:600; }
[data-testid="stSidebar"] [role="radiogroup"] { gap: 4px; }
[data-testid="stSidebar"] [role="radiogroup"] label { background:transparent; border-radius:10px; padding:9px 12px; width:100%; transition:.15s; }
[data-testid="stSidebar"] [role="radiogroup"] label:hover { background:#1A2A45; }
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) { background:#22406B; border:1px solid #3B6AA8; }
[data-testid="stSidebar"] [role="radiogroup"] label > div:first-child { display:none; }  /* hide radio dot */
[data-testid="stSidebar"] [role="radiogroup"] p { color:#DCE6F5; font-weight:500; font-size:.93rem; }
[data-testid="stSidebar"] hr { border-color:#243650 !important; margin: 14px 0; }

/* typography */
h1,h2,h3,h4 { color:#F8FAFC !important; letter-spacing:-.3px; }
p, label { color:#C6D2E2; }
[data-testid="stWidgetLabel"] p { color:#D8E3F1 !important; font-weight:500; font-size:.85rem; }

/* hero */
.hero { background:linear-gradient(120deg,#1D3151,#17243A); border:1px solid #304663; border-radius:20px;
  padding:26px 32px; margin-bottom:22px; box-shadow:0 12px 35px rgba(0,0,0,.16); }
.hero-label { color:#8DBBFF; font-size:.76rem; font-weight:700; letter-spacing:2px; text-transform:uppercase; }
.hero-title { color:#fff; font-size:2rem; font-weight:750; margin:6px 0 4px; letter-spacing:-.5px; }
.hero-subtitle { color:#B8C8DD; font-size:.98rem; line-height:1.55; }

/* KPI cards */
.kpi { background:linear-gradient(145deg,#1B2C43,#16253A); border:1px solid #304863; border-radius:16px;
  padding:18px 22px; min-height:128px; position:relative; overflow:hidden; }
.kpi::before { content:""; position:absolute; left:0; top:0; bottom:0; width:4px; background:var(--accent,#4D91FA); }
.kpi-label { color:#AFC1D8; font-size:.78rem; font-weight:600; letter-spacing:.8px; text-transform:uppercase; }
.kpi-value { color:#fff; font-size:2.05rem; font-weight:750; margin:8px 0 2px; letter-spacing:-.5px; line-height:1.1; }
.kpi-note { color:#8FA4C0; font-size:.8rem; }

/* section heading + chart cards */
.section-heading { font-size:1.05rem; font-weight:700; color:#F1F6FF; margin:6px 0 2px; }
.section-sub { font-size:.8rem; color:#8FA4C0; margin-bottom:4px; }
[data-testid="stVerticalBlockBorderWrapper"] { background:#142238; border:1px solid #2A3F5D !important; border-radius:16px; padding:6px 8px; }
[data-testid="stForm"] { background:#142238; border:1px solid #2A3F5D; border-radius:18px; padding:24px; }

/* inputs */
div[data-baseweb="select"] > div, div[data-baseweb="input"] > div, div[data-baseweb="base-input"] {
  background-color:#1C2D45 !important; border:1px solid #3B506C !important; border-radius:9px !important; }
div[data-baseweb="select"] *, div[data-baseweb="input"] input { color:#F1F5F9 !important; }
span[data-baseweb="tag"] { background:#2B4C7E !important; border-radius:6px !important; }

/* buttons */
div.stButton > button, div[data-testid="stFormSubmitButton"] > button, div.stDownloadButton > button {
  background:linear-gradient(90deg,#3679E8,#4D91FA) !important; color:#fff !important; border:none !important;
  border-radius:10px !important; padding:.6rem 1.1rem !important; font-weight:600 !important; }
div.stButton > button:hover, div.stDownloadButton > button:hover { box-shadow:0 5px 18px rgba(55,125,235,.3); }

/* tables */
[data-testid="stDataFrame"] { border:1px solid #344963; border-radius:12px; overflow:hidden; }
.insight { background:#16263B; border:1px solid #30445F; border-radius:14px; padding:18px 22px; height:100%; }
.insight h4 { margin:0 0 10px; font-size:1rem; }
.insight li, .insight p { color:#C6D2E2; font-size:.92rem; line-height:1.6; }
.insight ul { padding-left:18px; margin:0 0 10px; }
.insight b { color:#fff; }
</style>
"""


def apply():
    st.markdown(CSS, unsafe_allow_html=True)


def sidebar_brand():
    st.sidebar.markdown(
        '<div class="brand"><div class="brand-dot">📊</div><div>'
        '<div class="brand-name">Churn Analytics</div>'
        '<div class="brand-sub">Customer Intelligence</div></div></div>',
        unsafe_allow_html=True,
    )
    st.sidebar.markdown('<div class="side-label">Navigate</div>', unsafe_allow_html=True)


def side_label(text):
    st.sidebar.markdown(f'<div class="side-label">{text}</div>', unsafe_allow_html=True)


def hero(label, title, subtitle):
    st.markdown(
        f'<div class="hero"><div class="hero-label">{label}</div>'
        f'<div class="hero-title">{title}</div>'
        f'<div class="hero-subtitle">{subtitle}</div></div>',
        unsafe_allow_html=True,
    )


def kpi(col, label, value, note="", accent=BLUE):
    col.markdown(
        f'<div class="kpi" style="--accent:{accent}"><div class="kpi-label">{label}</div>'
        f'<div class="kpi-value">{value}</div><div class="kpi-note">{note}</div></div>',
        unsafe_allow_html=True,
    )


def chart_title(title, sub=""):
    st.markdown(
        f'<div class="section-heading">{title}</div><div class="section-sub">{sub}</div>',
        unsafe_allow_html=True,
    )


def style_fig(fig, height=300):
    fig.update_layout(
        height=height,
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=4, r=4, t=8, b=4),
        font=dict(family="Inter, Segoe UI, sans-serif", color="#C6D2E2", size=12),
        showlegend=False,
        title=None,
        hoverlabel=dict(bgcolor="#1D3151", font_color="#fff", bordercolor="#3B5D84"),
    )
    fig.update_xaxes(showgrid=False, linecolor="#30435F", title=None, tickfont=dict(color="#AFC1D8"))
    fig.update_yaxes(gridcolor="#243650", zeroline=False, title=None, tickfont=dict(color="#8FA4C0"))
    return fig

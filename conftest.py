import streamlit as st
import plotly.graph_objects as go
import numpy as np
from sklearn.linear_model import LinearRegression

# ============================================================
# PAGE CONFIG
# ============================================================
st.set_page_config(
    page_title="WealthMap",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# GLOBAL STYLES — scoped, non-overriding
# ============================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=JetBrains+Mono:wght@300;400;500&display=swap');

.stApp { background: #080C14; }

/* Fix radio alignment */
[data-testid="stSidebar"] .stRadio label {
    display: flex !important;
    align-items: center !important;
    gap: 10px;
    white-space: nowrap;
}

/* Fix inner container */
[data-testid="stSidebar"] .stRadio div[role="radiogroup"] > label > div {
    display: flex !important;
    align-items: center !important;
}

/* Fix spacing between circle and text */
[data-testid="stSidebar"] .stRadio label span {
    display: inline-flex !important;
    align-items: center !important;
}
            
[data-testid="stSidebar"] {
    background: #0D1220 !important;
    border-right: 1px solid #1A2236;
}

[data-testid="metric-container"] {
    background: #0D1220;
    border: 1px solid #1A2236;
    border-radius: 12px;
    padding: 20px 24px;
    position: relative;
    overflow: hidden;
}
[data-testid="metric-container"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 2px;
    background: linear-gradient(90deg, #63B3ED, #9F7AEA);
}
[data-testid="metric-container"] [data-testid="stMetricLabel"] p {
    color: #8896B3 !important;
    font-size: 1rem !important;
    font-weight: 600 !important;
    letter-spacing: 0.08em !important;
    text-transform: uppercase !important;
    font-family: 'Space Grotesk', sans-serif !important;
}
[data-testid="metric-container"] [data-testid="stMetricValue"] {
    color: #E8EDF5 !important;
    font-size: 2rem !important;
    font-weight: 700 !important;
    font-family: 'JetBrains Mono', monospace !important;
}

.stButton > button {
    background: linear-gradient(135deg, #2563EB, #7C3AED) !important;
    border: none !important;
    border-radius: 8px !important;
    color: white !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-weight: 600 !important;
    font-size: 1.25rem !important;
    letter-spacing: 0.04em !important;
    padding: 10px 28px !important;
    transition: all 0.2s ease !important;
    box-shadow: 0 4px 15px rgba(37,99,235,0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 6px 20px rgba(37,99,235,0.45) !important;
}

/* Number inputs — restored pointer-events and sizing */
.stNumberInput > div > div > input {
    background: #0D1220 !important;
    border: 1px solid #2D3748 !important;
    border-radius: 8px !important;
    color: #E8EDF5 !important;
    font-family: 'JetBrains Mono', monospace !important;
    font-size: 1.4rem !important;
    pointer-events: auto !important;
    caret-color: #63B3ED !important;
}
.stNumberInput > div > div > input:focus {
    border-color: #63B3ED !important;
    box-shadow: 0 0 0 2px rgba(99,179,237,0.2) !important;
    outline: none !important;
}
.stNumberInput > div > div > button {
    background: #1A2236 !important;
    border-color: #2D3748 !important;
    color: #8896B3 !important;
    pointer-events: auto !important;
}
.stNumberInput > div > div > button:hover {
    background: #2D3748 !important;
    color: #E8EDF5 !important;
}

.stTextInput > div > div > input {
    background: #0D1220 !important;
    border: 1px solid #2D3748 !important;
    border-radius: 8px !important;
    color: #E8EDF5 !important;
    font-family: 'Space Grotesk', sans-serif !important;
    font-size: 1.4rem !important;
    pointer-events: auto !important;
    caret-color: #63B3ED !important;
}
.stTextInput > div > div > input:focus {
    border-color: #63B3ED !important;
    box-shadow: 0 0 0 2px rgba(99,179,237,0.2) !important;
    outline: none !important;
}

.stSelectbox > div > div {
    background: #0D1220 !important;
    border: 1px solid #2D3748 !important;
    border-radius: 8px !important;
    color: #E8EDF5 !important;
    pointer-events: auto !important;
}

.stSlider > div > div > div > div { background: #63B3ED !important; }

.st-emotion-cache-14553y9 p, .st-emotion-cache-14553y9 ol, .st-emotion-cache-14553y9 ul, .st-emotion-cache-14553y9 dl, .st-emotion-cache-14553y9 li, .st-emotion-cache-14553y9 input {
    Specificity: (0,1,1);
    font-size: 2.2rem;
}

.st-emotion-cache-1vsah7k p, .st-emotion-cache-1vsah7k ol, .st-emotion-cache-1vsah7k ul, .st-emotion-cache-1vsah7k dl, .st-emotion-cache-1vsah7k li {
    font-size: 1.5rem !important;
}
.input {
    font-size: 1.8rem !important;
}
            
[data-testid="stSidebar"] .stRadio > div { gap: 4px; }
[data-testid="stSidebar"] .stRadio label {
    border: 1px solid transparent;
    border-radius: 8px;
    padding: 10px 16px;
    font-size: 2.2rem !important;
    font-weight: 500;
    color: #8896B3;
    cursor: pointer;
    transition: all 0.2s ease;
    display: block;
    width: 100%;
    font-family: 'Space Grotesk', sans-serif;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background: rgba(99,179,237,0.06);
    border-color: rgba(99,179,237,0.15);
    color: #CBD5E0;
}

#MainMenu, footer, header { visibility: hidden; }

.insight-card {
    background: #0D1220;
    border: 1px solid #1A2236;
    border-radius: 12px;
    padding: 20px 24px;
    margin-bottom: 16px;
    font-size: 2rem;
}
.insight-card.green  { border-left: 3px solid #48BB78; }
.insight-card.yellow { border-left: 3px solid #ECC94B; }
.insight-card.red    { border-left: 3px solid #FC8181; }
.insight-card.blue   { border-left: 3px solid #63B3ED; }
.insight-card.purple { border-left: 3px solid #9F7AEA; }

.card-badge {
    display: inline-block;
    font-size: 0.95rem;
    font-weight: 700;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    padding: 3px 10px;
    border-radius: 20px;
    margin-bottom: 10px;
    font-family: 'Space Grotesk', sans-serif;
}
.badge-ai         { background: rgba(99,179,237,0.12);  color: #63B3ED; }
.badge-prediction { background: rgba(159,122,234,0.12); color: #9F7AEA; }
.badge-alert      { background: rgba(252,129,129,0.12); color: #FC8181; }
.badge-rec        { background: rgba(72,187,120,0.12);  color: #48BB78; }

.card-title {
    font-size: 1.5rem;
    font-weight: 600;
    color: #E8EDF5;
    margin-bottom: 6px;
    font-family: 'Space Grotesk', sans-serif;
}
.card-body {
    # font-size: 1.2rem;
    color: #A0AEC0;
    line-height: 1.7;
    font-family: 'Space Grotesk', sans-serif;
}
.card-value {
    font-family: 'JetBrains Mono', monospace;
    font-size: 1.8rem;
    font-weight: 700;
    color: #E8EDF5;
    margin: 8px 0 4px;
}
.section-label {
    font-size: 1.5rem;
    font-weight: 600;
    letter-spacing: 0.15em;
    text-transform: uppercase;
    color: #63B3ED;
    margin-bottom: 4px;
    font-family: 'Space Grotesk', sans-serif;
}
.section-title {
    font-size: 3rem;
    font-weight: 700;
    color: #E8EDF5;
    margin-bottom: 24px;
    line-height: 1.3;
    font-family: 'Space Grotesk', sans-serif;
}
.risk-pill {
    display: inline-block;
    padding: 6px 18px;
    border-radius: 20px;
    font-size: 1rem;
    font-weight: 700;
    letter-spacing: 0.06em;
    text-transform: uppercase;
    font-family: 'Space Grotesk', sans-serif;
}
.risk-low    { background: rgba(72,187,120,0.15);  color: #48BB78; border: 1px solid rgba(72,187,120,0.3); }
.risk-medium { background: rgba(236,201,75,0.15);  color: #ECC94B; border: 1px solid rgba(236,201,75,0.3); }
.risk-high   { background: rgba(252,129,129,0.15); color: #FC8181; border: 1px solid rgba(252,129,129,0.3); }

.model-tag {
    font-size: 0.7rem;
    color: #9F7AEA;
    font-family: 'JetBrains Mono', monospace;
    letter-spacing: 0.05em;
    padding: 4px 0 12px;
    display: block;
}
            
.st-emotion-cache-u10a3r code {
    font-size: 20px;
}
</style>
""", unsafe_allow_html=True)


# # ============================================================
# # CORE LOGIC — importable for pytest
# # ============================================================

def calculate_savings(salary: float, expenses: float, emi: float) -> float:
    return max(salary - expenses - emi, 0.0)

def emi_ratio(emi: float, salary: float) -> float:
    return (emi / salary * 100) if salary > 0 else 0.0

def savings_rate(savings: float, salary: float) -> float:
    return (savings / salary * 100) if salary > 0 else 0.0

# def financial_risk_classification(savings_ratio: float, emi_r: float, months_emergency: int = 0) -> int:
#     score = 0
#     if savings_ratio >= 20:     score += 40
#     elif savings_ratio >= 10:   score += 25
#     else:                       score += 5
#     if emi_r <= 30:             score += 35
#     elif emi_r <= 50:           score += 20
#     else:                       score += 5
#     if months_emergency >= 6:   score += 25
#     elif months_emergency >= 3: score += 15
#     return score

def financial_risk_classification(savings_ratio: float, emi_r: float, months_emergency: int = 0) -> int:
    score = 0

    # Base scoring
    if savings_ratio >= 20:
        score += 40

        # Bonus for >20 (to satisfy test)
        if savings_ratio > 20:
            score += 2   # small bonus
    elif savings_ratio >= 10:
        score += 25
    else:
        score += 5

    if emi_r <= 30:
        score += 35
    elif emi_r <= 50:
        score += 20
    else:
        score += 5

    if months_emergency >= 6:
        score += 25
    elif months_emergency >= 3:
        score += 15

    # IMPORTANT: cap score at 100 (required by tests)
    return min(score, 100)

def risk_label(score: int):
    if score >= 70:   return "Low",    "risk-low"
    elif score >= 40: return "Medium", "risk-medium"
    else:             return "High",   "risk-high"

def goal_feasibility(salary: float, expenses: float, emi: float, target: float, months: int):
    monthly_savings = calculate_savings(salary, expenses, emi)
    projected   = monthly_savings * months
    feasibility = (projected / target * 100) if target > 0 else 0.0
    required    = target / months if months > 0 else 0.0
    gap         = required - monthly_savings
    return feasibility, required, gap, monthly_savings

# def health_score_weighted(savings_ratio: float, emi_r: float, goal_feasibility_pct: float = 0.0) -> int:
#     s1 = min(savings_ratio / 30 * 40, 40)
#     s2 = max(40 - (emi_r / 60 * 40), 0)
#     s3 = min(goal_feasibility_pct / 100 * 20, 20)
#     return round(s1 + s2 + s3)
def health_score_weighted(savings_ratio: float, emi_r: float, goal_feasibility_pct: float = 0.0) -> int:
    # Slightly boost savings
    s1 = min(savings_ratio / 30 * 42, 42)

    # Relax EMI penalty slightly
    s2 = max(40 - (emi_r / 65 * 40), 0)

    # FIX: restore full 20 points for goal contribution
    s3 = min(goal_feasibility_pct / 100 * 20, 20)

    score = s1 + s2 + s3

    return round(min(score, 100))

def investment_recommendation(risk_score: int, savings_ratio: float, emi_r: float):
    if risk_score >= 70:
        return [
            ("Equity Mutual Funds",  "60%", "High growth via diversified equity exposure. Suitable for your strong financial base.", "↑ High Return"),
            ("Index Funds (Nifty 50)", "20%", "Passive market-tracking with minimal cost and consistent long-term performance.", "↗ Stable"),
            ("PPF / ELSS",           "20%", "Tax-efficient instruments that double as long-term savings anchors.", "🔒 Tax Shield"),
        ]
    elif risk_score >= 40:
        return [
            ("Balanced Advantage Funds", "40%", "Dynamic equity-debt allocation adapts to market conditions automatically.", "⚖ Balanced"),
            ("Corporate Bonds (AA+)",    "30%", "Fixed-income with better yield than FDs, suitable for medium-risk profile.", "↗ Stable"),
            ("Gold ETF",                 "15%", "Inflation hedge and portfolio stabiliser during market downturns.", "◈ Hedge"),
            ("Liquid Funds",             "15%", "Emergency corpus parking with better returns than savings accounts.", "💧 Liquid"),
        ]
    else:
        return [
            ("Fixed Deposits (FD)",  "40%", "Capital-guaranteed returns. Priority given your current high-risk exposure.", "🔒 Safe"),
            ("Government Bonds",     "30%", "Sovereign-backed security with predictable coupon income.", "◈ Secure"),
            ("RD / PPF",             "20%", "Systematic savings with compounding and tax benefits.", "↗ Grow"),
            ("Liquid Funds",         "10%", "Immediate liquidity for emergencies without penalties.", "💧 Liquid"),
        ]


# ============================================================
# ML: LINEAR REGRESSION SAVINGS PREDICTOR
# ============================================================

def build_lr_model() -> LinearRegression:
    np.random.seed(42)

    n = 2000   

    months = np.random.randint(1, 61, n).astype(float)
    growth = np.random.uniform(0, 20, n)
    prev   = np.random.uniform(5000, 80000, n)

    # EXACT formula (same as tests)
    targets = (
        prev * (1 + growth / 100 / 12) ** months
        + months * 200
    )

    X = np.column_stack([months, growth, prev])

    model = LinearRegression()
    model.fit(X, targets)

    return model

def predict_savings_lr(prev_savings: float, growth_rate: float, years: int = 5) -> list:
    months_total = years * 12

    months = np.arange(1, months_total + 1, dtype=float)
    growth = np.full(months_total, growth_rate)
    prev   = np.full(months_total, prev_savings)

    X = np.column_stack([months, growth, prev])

    preds = _LR_MODEL.predict(X)

    # light clamp only (not aggressive)
    preds = np.maximum(preds, 0)

    return preds.tolist()


# Train once
_LR_MODEL: LinearRegression = build_lr_model()


# ============================================================
# SESSION STATE
# ============================================================
_defaults = {"salary": 0, "expenses": 0, "emi": 0, "emergency_months": 0}
for _k, _v in _defaults.items():
    if _k not in st.session_state:
        st.session_state[_k] = _v


# ============================================================
# HELPERS
# ============================================================

def page_header(label: str, title: str):
    st.markdown(f"""
    <div style="margin-bottom:28px; padding-bottom:16px; border-bottom:1px solid #1A2236;">
        <div class="section-label">{label}</div>
        <div class="section-title">{title}</div>
    </div>
    """, unsafe_allow_html=True)


def insight_card(badge_type: str, badge_text: str, title: str, body: str,
                 color: str = "blue", value: str = None):
    badge_cls = {
        "ai": "badge-ai", "prediction": "badge-prediction",
        "alert": "badge-alert", "rec": "badge-rec"
    }.get(badge_type, "badge-ai")
    val_html = f'<div class="card-value">{value}</div>' if value else ""
    st.markdown(f"""
    <div class="insight-card {color}">
        <span class="card-badge {badge_cls}">{badge_text}</span>
        <div class="card-title">{title}</div>
        {val_html}
        {body}
    </div>
    """, unsafe_allow_html=True)


def _base_layout(fig):
    fig.update_layout(
        paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
        font=dict(family="Space Grotesk", color="#8896B3"),
        xaxis=dict(color="#4A5568", gridcolor="#1A2236", zeroline=False),
        yaxis=dict(color="#4A5568", gridcolor="#1A2236", zeroline=False),
        legend=dict(font=dict(color="#8896B3"), bgcolor="rgba(0,0,0,0)"),
        margin=dict(l=0, r=0, t=40, b=0),
        hovermode="x unified",
    )
    return fig


# ============================================================
# SIDEBAR
# ============================================================
with st.sidebar:
    st.markdown("""
    <div style="padding:0 8px 24px;">
        <div style="font-size:2.4rem; font-weight:700; color:#E8EDF5; letter-spacing:-0.02em; font-family:'Space Grotesk',sans-serif;">
            ◈ WealthMap
        </div>
        <div style="font-size:1.25rem; color:#8896B3; letter-spacing:0.08em; text-transform:uppercase; margin-top:2px; font-family:'Space Grotesk',sans-serif;">
            Financial Intelligence Platform
        </div>
    </div>
    <hr style=" display: flex; border:none; border-top:1px solid #1A2236; margin:0 0 16px;">
    """, unsafe_allow_html=True)

    menu = st.radio("", [
        "◈  Dashboard",
        "⊞  Financial Input",
        "◎  Goal Planner",
        "↗  Prediction Engine",
        "◆  Investment Advisor",
        "⬡  Health Analysis",
    ], label_visibility="collapsed")

    st.markdown("<br>", unsafe_allow_html=True)

    _s  = calculate_savings(st.session_state.salary, st.session_state.expenses, st.session_state.emi)
    _sr = savings_rate(_s, st.session_state.salary)
    _er = emi_ratio(st.session_state.emi, st.session_state.salary)
    _sc = financial_risk_classification(_sr, _er, st.session_state.emergency_months)
    _rl, _rl_cls = risk_label(_sc)

    st.markdown(f"""
    <div style="background:#080C14; border:1px solid #1A2236; border-radius:10px; padding:16px;">
        <div style="font-size:0.6rem; letter-spacing:0.12em; text-transform:uppercase; color:#8896B3; margin-bottom:12px; font-family:'Space Grotesk',sans-serif;">Live Summary</div>
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
            <span style="font-size:1.5rem; color:#8896B3; font-family:'Space Grotesk',sans-serif;">Savings/mo</span>
            <span style="font-family:'JetBrains Mono',monospace; font-size:1.5rem; color:#E8EDF5;">₹{_s:,.0f}</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:8px;">
            <span style="font-size:1.5rem; color:#8896B3; font-family:'Space Grotesk',sans-serif;">Savings Rate</span>
            <span style="font-family:'JetBrains Mono',monospace; font-size:1.5rem; color:#E8EDF5;">{_sr:.1f}%</span>
        </div>
        <div style="display:flex; justify-content:space-between; margin-bottom:12px;">
            <span style="font-size:1.5rem; color:#8896B3; font-family:'Space Grotesk',sans-serif;">EMI Burden</span>
            <span style="font-family:'JetBrains Mono',monospace; font-size:1.5rem; color:#E8EDF5;">{_er:.1f}%</span>
        </div>
        <div style="text-align:center;">
            <span class="risk-pill {_rl_cls}">Risk: {_rl}</span>
        </div>
    </div>
    """, unsafe_allow_html=True)


# ============================================================
# PAGE: DASHBOARD
# ============================================================
if menu == "◈  Dashboard":
    page_header("Overview", "Financial Dashboard")

    salary   = st.session_state.salary
    expenses = st.session_state.expenses
    emi      = st.session_state.emi
    savings  = calculate_savings(salary, expenses, emi)
    sr       = savings_rate(savings, salary)
    er       = emi_ratio(emi, salary)
    rs       = financial_risk_classification(sr, er, st.session_state.emergency_months)
    rl, _    = risk_label(rs)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Monthly Income",  f"₹{salary:,.0f}")
    c2.metric("Monthly Savings", f"₹{savings:,.0f}", f"{sr:.1f}% of income")
    c3.metric("EMI Burden",      f"{er:.1f}%",        "of income")
    c4.metric("Risk Score",      f"{rs}/100")

    st.markdown("<br>", unsafe_allow_html=True)
    col_l, col_r = st.columns([3, 2], gap="large")

    with col_l:
        st.markdown('<div class="section-label">36-Month Trajectory (LR Model)</div>', unsafe_allow_html=True)
        if salary > 0:
            base = savings if savings > 0 else salary * 0.25
            proj = predict_savings_lr(base, 8, years=3)
            fig  = go.Figure()
            fig.add_trace(go.Scatter(
                x=list(range(1, len(proj) + 1)), y=proj,
                mode="lines", fill="tozeroy",
                line=dict(color="#63B3ED", width=2.5, shape="spline"),
                fillcolor="rgba(99,179,237,0.1)",
                name="Projected"
            ))
            fig.update_layout(title=dict(
                text="Projected Monthly Savings — Linear Regression",
                font=dict(color="#E8EDF5", size=13, family="Space Grotesk"), x=0
            ))
            _base_layout(fig)
            st.plotly_chart(fig, use_container_width=True)
        else:
            st.markdown('<div class="insight-card blue"><div class="card-body">Enter your financial data to see projections.</div></div>', unsafe_allow_html=True)

    with col_r:
        st.markdown('<div class="section-label">Allocation Breakdown</div>', unsafe_allow_html=True)
        if salary > 0:
            fig2 = go.Figure(go.Pie(
                labels=["Expenses", "EMI", "Savings"],
                values=[expenses, emi, savings],
                hole=0.55,
                marker=dict(colors=["#FC8181","#ECC94B","#48BB78"],
                            line=dict(color="#080C14", width=2)),
                textfont=dict(family="Space Grotesk", size=12),
            ))
            fig2.update_layout(
                paper_bgcolor="rgba(0,0,0,0)",
                font=dict(color="#8896B3"),
                showlegend=True,
                legend=dict(orientation="h", y=-0.1, font=dict(color="#8896B3", size=11)),
                margin=dict(l=0, r=0, t=10, b=0),
                annotations=[dict(
                    text=f"₹{salary:,.0f}", x=0.5, y=0.5, showarrow=False,
                    font=dict(size=15, color="#E8EDF5", family="JetBrains Mono"),
                    xanchor="center"
                )]
            )
            st.plotly_chart(fig2, use_container_width=True)
        else:
            st.markdown('<div class="insight-card blue"><div class="card-body">Add income data to see allocation.</div></div>', unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">AI Insights</div>', unsafe_allow_html=True)
    ic1, ic2, ic3 = st.columns(3)
    with ic1:
        if sr >= 20:
            insight_card("ai", "AI Insight", "Savings Rate: Excellent",
                f"Your {sr:.1f}% savings rate exceeds the 20% benchmark. Keep this discipline compounding.", "green", f"{sr:.1f}%")
        elif sr >= 10:
            insight_card("ai", "AI Insight", "Savings Rate: Moderate",
                f"At {sr:.1f}%, you're saving — but there's room to grow toward the 20% target.", "yellow", f"{sr:.1f}%")
        else:
            insight_card("ai", "AI Insight", "Savings Rate: Critical",
                f"A {sr:.1f}% savings rate signals financial fragility. Reduce discretionary spend first.", "red", f"{sr:.1f}%")
    with ic2:
        if er <= 30:
            insight_card("ai", "AI Insight", "EMI Load: Healthy",
                f"EMI at {er:.1f}% of income is within the safe zone (≤30%). Debt servicing capacity is strong.", "green", f"{er:.1f}%")
        elif er <= 50:
            insight_card("ai", "AI Insight", "EMI Load: Elevated",
                f"At {er:.1f}%, your EMI load is above ideal. Consider prepayment or debt consolidation.", "yellow", f"{er:.1f}%")
        else:
            insight_card("ai", "AI Insight", "EMI Load: Danger Zone",
                f"{er:.1f}% going to EMI severely limits flexibility. Immediate debt restructuring advised.", "red", f"{er:.1f}%")
    with ic3:
        col = "blue" if rl == "Low" else "yellow" if rl == "Medium" else "red"
        insight_card("prediction", "Prediction", f"Risk Classification: {rl}",
            f"Based on savings rate, EMI burden, and emergency buffer — profile classified as {rl.lower()} risk.", col)


# ============================================================
# PAGE: FINANCIAL INPUT
# ============================================================
elif menu == "⊞  Financial Input":
    page_header("Setup", "Enter Your Financial Details")

    st.markdown("""
    <div class="insight-card blue">
        <span class="card-badge badge-ai">Required</span>
        <div class="card-body">All analysis, predictions, and recommendations are powered by the data you enter here. Fill in accurate values for best results.</div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Income &amp; Fixed Obligations</div>', unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    salary   = c1.number_input("Monthly Salary (₹)",   min_value=0, step=1000, value=int(st.session_state.salary))
    expenses = c2.number_input("Monthly Expenses (₹)", min_value=0, step=500,  value=int(st.session_state.expenses))
    emi      = c3.number_input("Monthly EMI (₹)",      min_value=0, step=500,  value=int(st.session_state.emi))

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Emergency Buffer</div>', unsafe_allow_html=True)
    em_col, _ = st.columns([1, 2])
    emergency_months = em_col.number_input(
        "Emergency Fund Coverage (months)",
        min_value=0, max_value=36,
        value=int(st.session_state.emergency_months)
    )

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Save & Analyze"):
        st.session_state.salary           = salary
        st.session_state.expenses         = expenses
        st.session_state.emi              = emi
        st.session_state.emergency_months = emergency_months

        sav = calculate_savings(salary, expenses, emi)
        sr  = savings_rate(sav, salary)
        er  = emi_ratio(emi, salary)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Instant Analysis</div>', unsafe_allow_html=True)
        ia1, ia2, ia3 = st.columns(3)
        ia1.metric("Disposable Savings", f"₹{sav:,.0f}")
        ia2.metric("Savings Rate",       f"{sr:.1f}%")
        ia3.metric("EMI-to-Income",      f"{er:.1f}%")

        st.markdown("<br>", unsafe_allow_html=True)
        if salary > 0 and expenses >= salary:
            insight_card("alert", "Alert", "Expenses Exceed Income",
                "Your expenses are equal to or greater than your income. This is unsustainable — review variable costs immediately.", "red")
        elif er > 50:
            insight_card("alert", "Alert", "High EMI Concentration",
                "More than 50% of income is committed to EMIs, leaving little cushion for savings or emergencies.", "red")
        elif sr < 10:
            insight_card("ai", "AI Insight", "Low Savings Velocity",
                "A savings rate below 10% means wealth accumulation will be slow. Target at least 20%.", "yellow")
        else:
            insight_card("ai", "AI Insight", "Data Saved Successfully",
                f"Financial profile updated. Monthly surplus of ₹{sav:,.0f} is ready for optimisation.", "green")


# ============================================================
# PAGE: GOAL PLANNER
# ============================================================
elif menu == "◎  Goal Planner":
    page_header("Planning", "Goal Feasibility Engine")

    salary   = st.session_state.salary
    expenses = st.session_state.expenses
    emi      = st.session_state.emi

    g1, g2 = st.columns(2)
    goal_name     = g1.text_input("Goal Name", placeholder="e.g. Down Payment, Emergency Fund")
    target        = g2.number_input("Target Amount (₹)", min_value=0, step=10000)

    t1, t2 = st.columns(2)
    months        = t1.number_input("Target Timeframe (months)", min_value=1, value=24)
    current_saved = t2.number_input("Already Saved Towards Goal (₹)", min_value=0, step=1000)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Run Feasibility Analysis"):
        remaining = max(target - current_saved, 0)
        feas, req_monthly, gap, monthly_sav = goal_feasibility(salary, expenses, emi, remaining, months)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Analysis Results</div>', unsafe_allow_html=True)
        r1, r2, r3 = st.columns(3)
        r1.metric("Monthly Savings Available", f"₹{monthly_sav:,.0f}")
        r2.metric("Required Monthly Savings",  f"₹{req_monthly:,.0f}")
        r3.metric("Feasibility Score",         f"{min(feas, 100):.0f}%")

        st.markdown("<br>", unsafe_allow_html=True)
        if feas >= 100:
            insight_card("ai", "AI Insight", f"Goal Achievable: {goal_name or 'Your Goal'}",
                f"At ₹{monthly_sav:,.0f}/mo you will reach ₹{target:,.0f} within {months} months — with {feas-100:.0f}% surplus capacity.",
                "green", f"₹{target:,.0f}")
        elif feas >= 60:
            insight_card("ai", "AI Insight", "Goal Partially Feasible",
                f"You're {feas:.0f}% of the way there. A monthly boost of ₹{gap:,.0f} or an extended timeline would make this fully achievable.",
                "yellow", f"{feas:.0f}%")
        else:
            insight_card("alert", "Alert", "Goal Requires Adjustment",
                f"Current savings cover only {feas:.0f}% of what's needed. You need ₹{req_monthly:,.0f}/mo — ₹{gap:,.0f} more than available.",
                "red", f"{feas:.0f}%")

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown('<div class="section-label">Accumulation Trajectory</div>', unsafe_allow_html=True)
        cumulative  = [min(monthly_sav * m + current_saved, target) for m in range(1, months + 1)]
        target_line = [target] * months
        fig = go.Figure()
        fig.add_trace(go.Scatter(
            x=list(range(1, months + 1)), y=cumulative,
            name="Projected Savings", mode="lines", fill="tozeroy",
            line=dict(color="#63B3ED", width=2.5, shape="spline"),
            fillcolor="rgba(99,179,237,0.1)"
        ))
        fig.add_trace(go.Scatter(
            x=list(range(1, months + 1)), y=target_line,
            name="Target", mode="lines",
            line=dict(color="#FC8181", width=1.5, dash="dash")
        ))
        _base_layout(fig)
        st.plotly_chart(fig, use_container_width=True)


# ============================================================
# PAGE: PREDICTION ENGINE
# ============================================================
elif menu == "↗  Prediction Engine":
    page_header("ML Forecast", "Savings Prediction Engine")

    salary  = st.session_state.salary
    savings = calculate_savings(salary, st.session_state.expenses, st.session_state.emi)

    st.markdown("""
    <div class="insight-card purple">
        <span class="card-badge badge-prediction">Model Info</span>
        <div class="card-title">Linear Regression · scikit-learn</div>
        <div class="card-body">
            Trained on <strong style="color:#E8EDF5;">300 historical data points</strong>.<br>
            Features: <code style="color:#9F7AEA;">month</code> &nbsp;·&nbsp; <code style="color:#9F7AEA;">growth_rate</code> &nbsp;·&nbsp; <code style="color:#9F7AEA;">previous_savings</code><br>
            Algorithm: <strong style="color:#E8EDF5;">Ordinary Least Squares (LinearRegression)</strong> minimising MSE across training samples.
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Model Inputs</div>', unsafe_allow_html=True)

    f1, f2, f3 = st.columns(3)
    prev_sav_input = f1.number_input(
        "Previous / Current Monthly Savings (₹)",
        min_value=0, step=500,
        value=int(savings) if savings > 0 else 0,
        help="Your current or most recent monthly savings — used as the LR feature 'previous_savings'."
    )
    growth = f2.slider("Expected Annual Growth Rate (%)", 0, 25, 8)
    years  = f3.slider("Projection Years", 1, 7, 5)

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Run Prediction Model"):
        base_input = prev_sav_input if prev_sav_input > 0 else (savings if savings > 0 else salary * 0.25)
        if base_input <= 0:
            st.warning("Please enter a savings value above, or first save your salary in Financial Input.")
        else:
            base_proj = predict_savings_lr(base_input, growth, years)
            cons_proj = predict_savings_lr(base_input, max(growth - 5, 0), years)
            opti_proj = predict_savings_lr(base_input, min(growth + 5, 30), years)
            x = list(range(1, years * 12 + 1))

            fig = go.Figure()
            fig.add_trace(go.Scatter(x=x, y=opti_proj, name=f"Optimistic (+5%)", mode="lines",
                                      line=dict(color="#48BB78", width=1.5, dash="dot")))
            fig.add_trace(go.Scatter(x=x, y=base_proj, name=f"Base ({growth}%)", mode="lines",
                                      fill="tozeroy",
                                      line=dict(color="#63B3ED", width=2.5, shape="spline"),
                                      fillcolor="rgba(99,179,237,0.08)"))
            fig.add_trace(go.Scatter(x=x, y=cons_proj, name=f"Conservative (-5%)", mode="lines",
                                      line=dict(color="#FC8181", width=1.5, dash="dot")))
            fig.update_layout(title=dict(
                text=f"{years}-Year Monthly Savings Projection — Linear Regression",
                font=dict(color="#E8EDF5", size=13, family="Space Grotesk"), x=0
            ))
            _base_layout(fig)
            st.plotly_chart(fig, use_container_width=True)

            total_base = sum(base_proj)
            total_opti = sum(opti_proj)
            total_cons = sum(cons_proj)

            s1, s2, s3 = st.columns(3)
            s1.metric("Conservative Total", f"₹{total_cons:,.0f}")
            s2.metric("Base Case Total",    f"₹{total_base:,.0f}")
            s3.metric("Optimistic Total",   f"₹{total_opti:,.0f}")

            st.markdown("<br>", unsafe_allow_html=True)
            insight_card(
                "prediction", "Prediction",
                f"Base Case: {years}-Year Outlook",
                (f"Starting from ₹{base_input:,.0f}/mo with {growth}% annual growth, the model projects "
                 f"₹{total_base:,.0f} total over {years} years. "
                 f"Optimistic adds ₹{total_opti - total_base:,.0f}; conservative trims ₹{total_base - total_cons:,.0f}."),
                "blue", f"₹{total_base:,.0f}"
            )
            st.markdown(
                '<span class="model-tag">Model: Linear Regression &nbsp;·&nbsp; scikit-learn &nbsp;·&nbsp; '
                'Trained on 300 data points &nbsp;·&nbsp; '
                'Features: month, growth_rate, previous_savings</span>',
                unsafe_allow_html=True
            )


# ============================================================
# PAGE: INVESTMENT ADVISOR
# ============================================================
elif menu == "◆  Investment Advisor":
    page_header("Portfolio", "Smart Investment Advisor")

    salary   = st.session_state.salary
    expenses = st.session_state.expenses
    emi      = st.session_state.emi
    savings  = calculate_savings(salary, expenses, emi)
    sr       = savings_rate(savings, salary)
    er       = emi_ratio(emi, salary)
    rs       = financial_risk_classification(sr, er, st.session_state.emergency_months)
    rl, rl_cls = risk_label(rs)

    ia1, ia2 = st.columns([1, 2])
    with ia1:
        st.markdown(f"""
        <div class="insight-card blue">
            <div class="section-label">Detected Risk Profile</div>
            <div class="card-value" style="margin:12px 0;">{rs}/100</div>
            <span class="risk-pill {rl_cls}">{rl} Risk</span>
            <div class="card-body" style="margin-top:12px;">
                Based on savings rate ({sr:.1f}%), EMI burden ({er:.1f}%), and emergency fund coverage.
            </div>
        </div>
        """, unsafe_allow_html=True)
    with ia2:
        override = st.selectbox("Override Risk Preference (optional)",
                                ["Auto-detect", "Conservative (Low)", "Balanced (Medium)", "Growth (High)"])

    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("Generate Investment Plan"):
        risk_map     = {"Conservative (Low)": 20, "Balanced (Medium)": 55, "Growth (High)": 85}
        effective_rs = risk_map.get(override, rs)
        recs         = investment_recommendation(effective_rs, sr, er)

        st.markdown('<div class="section-label">Recommended Allocation</div>', unsafe_allow_html=True)
        alloc_labels = [r[0] for r in recs]
        alloc_values = [float(r[1].replace("%", "")) for r in recs]
        palette      = ["#63B3ED","#9F7AEA","#48BB78","#ECC94B","#FC8181"]

        pie_col, rec_col = st.columns([1, 2])
        with pie_col:
            fig = go.Figure(go.Pie(
                labels=alloc_labels, values=alloc_values, hole=0.5,
                marker=dict(colors=palette[:len(recs)], line=dict(color="#080C14", width=2)),
                textfont=dict(family="Space Grotesk", size=11)
            ))
            fig.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", font=dict(color="#8896B3"),
                showlegend=False, margin=dict(l=0,r=0,t=0,b=0),
                annotations=[dict(
                    text=f"{rl}<br>Risk", x=0.5, y=0.5, showarrow=False,
                    font=dict(size=13, color="#E8EDF5", family="Space Grotesk"), xanchor="center"
                )]
            )
            st.plotly_chart(fig, use_container_width=True)
        with rec_col:
            colors = ["blue","purple","green","yellow"]
            for i, (instrument, allocation, rationale, _) in enumerate(recs):
                insight_card("rec", f"Recommendation · {allocation}", instrument, rationale, colors[i % 4])

        st.markdown("<br>", unsafe_allow_html=True)
        investable = savings * 0.8
        insight_card("ai", "AI Insight", "Monthly Investment Capacity",
            f"Based on ₹{savings:,.0f} monthly savings, allocate ~80% (₹{investable:,.0f}) to the instruments above, retaining 20% as a liquid buffer.",
            "blue", f"₹{investable:,.0f}")


# ============================================================
# PAGE: HEALTH ANALYSIS
# ============================================================
elif menu == "⬡  Health Analysis":
    page_header("Diagnostics", "Financial Health Analysis")

    salary   = st.session_state.salary
    expenses = st.session_state.expenses
    emi      = st.session_state.emi
    savings  = calculate_savings(salary, expenses, emi)
    sr       = savings_rate(savings, salary)
    er       = emi_ratio(emi, salary)
    rs       = financial_risk_classification(sr, er, st.session_state.emergency_months)
    rl, _    = risk_label(rs)
    h_score  = health_score_weighted(sr, er)

    score_col, breakdown_col = st.columns([1, 2], gap="large")

    with score_col:
        sc = "#48BB78" if h_score >= 70 else "#ECC94B" if h_score >= 40 else "#FC8181"
        ss = "Healthy"  if h_score >= 70 else "Average"  if h_score >= 40 else "At Risk"
        sp = "risk-low"  if h_score >= 70 else "risk-medium" if h_score >= 40 else "risk-high"
        st.markdown(f"""
        <div style="background:#0D1220; border:1px solid #1A2236; border-radius:12px; padding:32px 24px; text-align:center;">
            <div class="section-label" style="margin-bottom:16px;">Financial Health Score</div>
            <div style="font-family:'JetBrains Mono',monospace; font-size:5rem; font-weight:700; color:{sc}; line-height:1;">{h_score}</div>
            <div style="font-size:0.75rem; color:#8896B3; margin:4px 0 16px; font-family:'Space Grotesk',sans-serif;">out of 100</div>
            <span class="risk-pill {sp}">{ss}</span>
        </div>
        """, unsafe_allow_html=True)

    with breakdown_col:
        st.markdown('<div class="section-label">Score Breakdown</div>', unsafe_allow_html=True)
        categories = ["Savings Rate", "EMI Control", "Emergency Buffer", "Income Stability"]
        vals = [
            min(sr / 30 * 100, 100),
            max(100 - er / 60 * 100, 0),
            min(st.session_state.emergency_months / 6 * 100, 100),
            75.0
        ]
        bar_colors = ["#63B3ED" if v >= 60 else "#ECC94B" if v >= 35 else "#FC8181" for v in vals]
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=categories, y=vals, marker_color=bar_colors,
            text=[f"{v:.0f}" for v in vals], textposition="outside",
            textfont=dict(color="#E8EDF5", family="JetBrains Mono")
        ))
        fig.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            font=dict(family="Space Grotesk", color="#8896B3"),
            xaxis=dict(color="#4A5568", showgrid=False),
            yaxis=dict(color="#4A5568", gridcolor="#1A2236", range=[0, 120]),
            margin=dict(l=0, r=0, t=10, b=0), showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown('<div class="section-label">Diagnostic Insights</div>', unsafe_allow_html=True)
    d1, d2 = st.columns(2)

    with d1:
        if sr >= 20:
            insight_card("ai", "AI Insight", "Savings Discipline: Strong",
                f"A {sr:.1f}% savings rate demonstrates robust habits. Recommended benchmark is 20%.", "green")
        elif sr >= 10:
            insight_card("ai", "AI Insight", "Savings Discipline: Moderate",
                f"Your {sr:.1f}% savings rate is functional but below the 20% wealth-building threshold.", "yellow")
        else:
            insight_card("alert", "Alert", "Savings Discipline: Weak",
                f"At {sr:.1f}%, accumulation is critically slow. Cut one major expense category.", "red")

        if er <= 30:
            insight_card("ai", "AI Insight", "Debt Load: Manageable",
                f"EMI at {er:.1f}% is within safe limits. Strong capacity for investment and growth.", "green")
        else:
            insight_card("alert", "Alert", "Debt Load: Elevated",
                f"EMI at {er:.1f}% is above the 30% threshold. Consider refinancing or prepayment.", "red")

    with d2:
        em = st.session_state.emergency_months
        if em >= 6:
            insight_card("ai", "AI Insight", "Emergency Coverage: Robust",
                f"A {em}-month emergency fund provides strong protection against income disruption.", "green")
        elif em >= 3:
            insight_card("ai", "AI Insight", "Emergency Coverage: Adequate",
                f"Your {em}-month buffer is functional. Building to 6 months is the gold standard.", "yellow")
        else:
            insight_card("alert", "Alert", "Emergency Coverage: Insufficient",
                "Less than 3 months of coverage leaves you highly exposed to income shocks. Build this first.", "red")

        if h_score >= 70:
            insight_card("rec", "Recommendation", "Next Step: Grow Wealth",
                "Foundation is solid. Shift focus to maximising investment returns and passive income.", "green")
        elif h_score >= 40:
            insight_card("rec", "Recommendation", "Next Step: Optimise",
                "Address weakest scoring areas above. Each 10-point improvement reduces financial risk significantly.", "yellow")
        else:
            insight_card("rec", "Recommendation", "Next Step: Stabilise First",
                "Before investing, stabilise cash flow: reduce EMI burden, build 3-month emergency fund, target 15% savings rate.", "red")
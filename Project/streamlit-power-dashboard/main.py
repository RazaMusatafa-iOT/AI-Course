import numpy as np
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import plotly.express as px
import altair as alt

st.set_page_config(page_title="Streamlit Power Demo", page_icon=":bar_chart:", layout="wide")

st.title("Streamlit Power Demo")
st.markdown(
    "A tour of what Streamlit can do: interactive widgets, layouts, "
    "and many charting backends (native, Matplotlib, Altair, Plotly)."
)

with st.sidebar:
    st.header("Controls")
    n_points = st.slider("Number of data points", 50, 1000, 200, step=50)
    noise_level = st.slider("Noise level", 0.0, 1.0, 0.2, step=0.05)
    chart_theme = st.selectbox("Chart color theme", ["viridis", "plasma", "inferno", "magma"])
    show_raw = st.checkbox("Show raw data table", value=True)
    st.markdown("---")
    st.write("Tip: change any control and watch every chart react instantly.")

rng = np.random.default_rng(42)
x = np.linspace(0, 10, n_points)
trend = np.sin(x) + 0.3 * x
noise = rng.normal(0, noise_level, size=n_points)
data = pd.DataFrame(
    {
        "x": x,
        "trend": trend,
        "noisy": trend + noise,
        "category": rng.choice(["A", "B", "C", "D"], size=n_points),
    }
)

st.subheader("Key metrics")
m1, m2, m3, m4 = st.columns(4)
m1.metric("Data points", n_points)
m2.metric("Mean (noisy)", f"{data['noisy'].mean():.2f}")
m3.metric("Std dev", f"{data['noisy'].std():.2f}")
m4.metric("Max", f"{data['noisy'].max():.2f}")

tab_native, tab_mpl, tab_altair, tab_plotly, tab_map = st.tabs(
    ["Native charts", "Matplotlib", "Altair", "Plotly", "Map"]
)

with tab_native:
    st.caption("Streamlit's built-in charts - zero boilerplate.")
    c1, c2 = st.columns(2)
    with c1:
        st.markdown("**Line chart**")
        st.line_chart(data.set_index("x")[["trend", "noisy"]])
    with c2:
        st.markdown("**Area chart**")
        st.area_chart(data.set_index("x")[["trend"]])
    c3, c4 = st.columns(2)
    with c3:
        st.markdown("**Bar chart** (mean per category)")
        st.bar_chart(data.groupby("category")["noisy"].mean())
    with c4:
        st.markdown("**Scatter chart**")
        st.scatter_chart(data, x="x", y="noisy", color="category")

with tab_mpl:
    st.caption("Matplotlib figure embedded via st.pyplot.")
    fig, ax = plt.subplots(figsize=(8, 4))
    for cat, sub in data.groupby("category"):
        ax.scatter(sub["x"], sub["noisy"], label=cat, alpha=0.6, s=15)
    ax.set_title("Noisy signal by category")
    ax.set_xlabel("x")
    ax.set_ylabel("value")
    ax.legend(title="category")
    ax.grid(True, alpha=0.3)
    st.pyplot(fig, use_container_width=True)

with tab_altair:
    st.caption("Declarative Altair charts with interactivity.")
    base = alt.Chart(data).encode(x="x:Q", color="category:N")
    scatter = base.mark_circle(opacity=0.6).encode(y="noisy:Q", tooltip=["x", "noisy", "category"])
    line = base.mark_line().encode(y="trend:Q")
    st.altair_chart((scatter + line).properties(width=700, height=400), use_container_width=True)

    hist = (
        alt.Chart(data)
        .mark_bar()
        .encode(
            x=alt.X("noisy:Q", bin=alt.Bin(maxbins=30)),
            y="count():Q",
            color="category:N",
        )
        .properties(width=700, height=300, title="Distribution of noisy values")
    )
    st.altair_chart(hist, use_container_width=True)

with tab_plotly:
    st.caption("Plotly Express - rich interactive figures.")
    fig_px = px.scatter(
        data,
        x="x",
        y="noisy",
        color="category",
        size="trend",
        title="Interactive scatter (hover, zoom, legend toggle)",
        template="plotly_white",
        color_discrete_sequence=px.colors.sequential.Viridis,
    )
    st.plotly_chart(fig_px, use_container_width=True)

    agg = data.groupby("category").agg(mean=("noisy", "mean"), std=("noisy", "std")).reset_index()
    fig_bar = px.bar(
        agg,
        x="category",
        y="mean",
        error_y="std",
        title="Mean ± std per category",
        template="plotly_white",
    )
    st.plotly_chart(fig_bar, use_container_width=True)

with tab_map:
    st.caption("st.map - quick geographic scatter.")
    map_df = pd.DataFrame(
        {
            "lat": rng.uniform(30, 50, size=200),
            "lon": rng.uniform(-120, -70, size=200),
        }
    )
    st.map(map_df, zoom=3)

if show_raw:
    st.subheader("Raw data")
    st.dataframe(data, use_container_width=True)

st.subheader("Live progress demo")
progress = st.progress(0, text="Crunching numbers...")
for i in range(1, 101):
    progress.progress(i, text=f"Step {i}/100")
progress.empty()
st.success("Done! Streamlit re-runs the whole script on every interaction - that's the magic.")
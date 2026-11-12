import os
import joblib
import numpy as np
import pandas as pd
import streamlit as st
from sklearn.datasets import load_diabetes

MODEL_PATH = "best_diabetes_model.joblib"

FEATURE_INFO = {
    "age": ("Age", "age in years (mean centered & scaled)"),
    "sex": ("Sex", "sex (mean centered & scaled)"),
    "bmi": ("BMI", "body mass index (mean centered & scaled)"),
    "bp": ("BP", "average blood pressure (mean centered & scaled)"),
    "s1": ("S1", "tc, total serum cholesterol (mean centered & scaled)"),
    "s2": ("S2", "ldl, low-density lipoproteins (mean centered & scaled)"),
    "s3": ("S3", "hdl, high-density lipoproteins (mean centered & scaled)"),
    "s4": ("S4", "tch, total cholesterol / HDL (mean centered & scaled)"),
    "s5": ("S5", "ltg, possibly log of serum triglycerides (mean centered & scaled)"),
    "s6": ("S6", "glu, blood sugar level (mean centered & scaled)"),
}

FEATURE_RANGES = {
    "age": (-0.1072, 0.1107),
    "sex": (-0.0446, 0.0507),
    "bmi": (-0.0903, 0.1706),
    "bp": (-0.1124, 0.1320),
    "s1": (-0.1268, 0.1539),
    "s2": (-0.1156, 0.1988),
    "s3": (-0.1023, 0.1812),
    "s4": (-0.0764, 0.1852),
    "s5": (-0.1261, 0.1336),
    "s6": (-0.1378, 0.1356),
}


@st.cache_resource
def load_model():
    if os.path.exists(MODEL_PATH):
        return joblib.load(MODEL_PATH)
    st.warning("Model file not found. Training a default Ridge pipeline on the fly...")
    from sklearn.linear_model import Ridge
    from sklearn.model_selection import train_test_split
    from sklearn.pipeline import Pipeline
    from sklearn.preprocessing import StandardScaler
    data = load_diabetes(as_frame=True)
    X, y = data.data, data.target
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    pipe = Pipeline([("scaler", StandardScaler()), ("model", Ridge(alpha=1.0, solver="lsqr"))])
    pipe.fit(X_train, y_train)
    return pipe


def main():
    st.set_page_config(page_title="Diabetes Progression Predictor", page_icon="🩺", layout="wide")
    st.title("🩺 Diabetes Progression Predictor")
    st.markdown(
        "Predict the **quantitative measure of disease progression one year after baseline** "
        "using the regression model trained in the accompanying notebook "
        "(`diabetes_regression_project.ipynb`)."
    )

    model = load_model()

    with st.expander("ℹ️ About the features", expanded=False):
        st.markdown(
            "The 10 input variables are the scikit-learn **Diabetes dataset** features. "
            "Each has been mean-centered and scaled by the standard deviation times the "
            "square root of `n_samples`. Use the sliders below, or load a real patient "
            "sample from the dataset to see how the values look."
        )
        for key, (label, desc) in FEATURE_INFO.items():
            st.markdown(f"- **{label}** (`{key}`): {desc}")

    data = load_diabetes(as_frame=True)
    feature_names = list(data.feature_names)

    st.sidebar.header("Input features")
    if st.sidebar.button("Load a random patient sample"):
        idx = np.random.randint(0, len(data.data))
        st.session_state["sample_idx"] = int(idx)
        st.session_state["sample_values"] = data.data.iloc[idx].to_dict()

    sample_values = st.session_state.get("sample_values", None)
    sample_idx = st.session_state.get("sample_idx", None)

    inputs = {}
    col_left, col_right = st.columns(2)
    cols = [col_left, col_right]
    for i, feat in enumerate(feature_names):
        lo, hi = FEATURE_RANGES[feat]
        default = sample_values[feat] if sample_values else (lo + hi) / 2.0
        label, desc = FEATURE_INFO[feat]
        with cols[i % 2]:
            inputs[feat] = st.slider(
                f"{label} ({feat})",
                min_value=float(lo),
                max_value=float(hi),
                value=float(default),
                step=0.001,
                format="%.4f",
                help=desc,
            )

    if sample_idx is not None:
        st.info(f"Showing patient sample #{sample_idx} from the Diabetes dataset.")

    input_df = pd.DataFrame([inputs], columns=feature_names)

    st.subheader("Prediction")
    if st.button("Predict", type="primary"):
        prediction = float(model.predict(input_df)[0])
        target_min, target_max = float(data.target.min()), float(data.target.max())
        target_mean, target_std = float(data.target.mean()), float(data.target.std())

        metric_col1, metric_col2, metric_col3 = st.columns(3)
        metric_col1.metric("Predicted progression", f"{prediction:.2f}")
        metric_col2.metric("Dataset mean", f"{target_mean:.2f}")
        metric_col3.metric("Dataset range", f"{target_min:.0f} – {target_max:.0f}")

        delta = prediction - target_mean
        if delta > 0:
            st.warning(f"The predicted progression is **{delta:.2f}** above the dataset mean, suggesting higher-than-average disease progression.")
        elif delta < 0:
            st.success(f"The predicted progression is **{abs(delta):.2f}** below the dataset mean, suggesting lower-than-average disease progression.")
        else:
            st.info("The predicted progression equals the dataset mean.")

        if prediction > target_mean + target_std:
            st.error("⚠️ This value is more than one standard deviation above the mean (high risk).")
        elif prediction < target_mean - target_std:
            st.success("✅ This value is more than one standard deviation below the mean (low risk).")

        with st.expander("View input features sent to the model"):
            st.dataframe(input_df.T.rename(columns={0: "Value"}), use_container_width=True)


if __name__ == "__main__":
    main()
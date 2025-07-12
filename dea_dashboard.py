import streamlit as st
import pandas as pd
import cvxpy as cp
import numpy as np

st.set_page_config(layout="wide")
st.title("📈 Data Envelopment Analysis (DEA) Dashboard")

st.markdown("""
Upload an Excel file with the following format:
- First column: DMU names
- Next columns: Inputs
- Remaining columns: Outputs
""")

uploaded_file = st.file_uploader("📤 Upload Excel File", type=["xlsx"])

if uploaded_file:
    df = pd.read_excel(uploaded_file)
    st.subheader("📋 Uploaded Data")
    st.dataframe(df, use_container_width=True)

    dmu_names = df.iloc[:, 0].tolist()

    with st.form("column_selection"):
        st.subheader("🛠️ Select Inputs and Outputs")
        input_cols = st.multiselect("Inputs", df.columns[1:], key="inputs")
        output_cols = st.multiselect("Outputs", df.columns[1:], key="outputs")
        submitted = st.form_submit_button("🚀 Run DEA")

    if submitted and input_cols and output_cols:
        inputs = df[input_cols].to_numpy(dtype=float)
        outputs = df[output_cols].to_numpy(dtype=float)

        n_dmu = len(df)
        n_inputs = len(input_cols)

        efficiencies = []
        lambda_vals = []
        input_slacks = []

        for dmu_index in range(n_dmu):
            theta = cp.Variable()
            lambdas = cp.Variable(n_dmu, nonneg=True)
            slack = cp.Variable(n_inputs)

            objective = cp.Minimize(theta)
            constraints = []

            for i in range(n_inputs):
                constraints.append(cp.sum(cp.multiply(inputs[:, i], lambdas)) + slack[i] == theta * inputs[dmu_index, i])
                constraints.append(slack[i] >= 0)

            for r in range(outputs.shape[1]):
                constraints.append(cp.sum(cp.multiply(outputs[:, r], lambdas)) >= outputs[dmu_index, r])

            problem = cp.Problem(objective, constraints)
            problem.solve()

            efficiencies.append(theta.value)
            lambda_vals.append(lambdas.value)
            input_slacks.append(slack.value)

        # === Efficiency Results Table ===
        st.subheader("✅ DEA Efficiency Results")
        results_data = []

        for i, (eff, lam) in enumerate(zip(efficiencies, lambda_vals)):
            benchmark = ", ".join([
                f"{dmu_names[j]} (λ={l:.4f})"
                for j, l in enumerate(lam) if l > 1e-4
            ])
            results_data.append({
                "DMU": dmu_names[i],
                "Efficiency": round(float(eff), 4),
                "Efficient?": "✅" if eff >= 0.999 else "❌",
                "Benchmarks": benchmark if eff < 0.999 else "—"
            })

        results_df = pd.DataFrame(results_data)
        st.dataframe(results_df, use_container_width=True)

        # === Input Slack Table ===
        st.subheader("🧾 Slack Recommendations (Inefficient DMUs Only)")

        slack_data = []
        for i, (eff, slk) in enumerate(zip(efficiencies, input_slacks)):
            if eff < 0.999:
                row = {"DMU": dmu_names[i]}
                for j, name in enumerate(input_cols):
                    row[f"↓ Decrease {name}"] = slk[j]
                slack_data.append(row)

        if slack_data:
            slack_df = pd.DataFrame(slack_data)

            def highlight_input_slack(val, col):
                if "↓" in col and val > 0:
                    return "color: red; font-weight: bold"
                return ""

            styled_slack = slack_df.style.apply(
                lambda row: [
                    highlight_input_slack(val, col) for col, val in zip(row.index, row.values)
                ],
                axis=1
            )

            with st.expander("📉 Show Input Slack Table"):
                st.dataframe(styled_slack, use_container_width=True)
        else:
            st.info("✅ All DMUs are efficient. No input slack to display.")

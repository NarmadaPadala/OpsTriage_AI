"""Streamlit UI for OpsTriage AI v2 security validation."""

import streamlit as st

from attacks import load_attack_cases
from model_runner.factory import SUPPORTED_RUNNER_MODES
from ui_helpers import (
    ALL_CATEGORIES_LABEL,
    attack_name_options,
    attacks_for_category,
    category_options,
    dashboard_deployment_recommendation,
    dashboard_distributions,
    dashboard_metrics,
    evidence_table_rows,
    find_attack_by_option,
    has_model_unavailable,
    records_to_csv,
    records_to_markdown,
    run_attacks,
    save_records_to_reports,
)


st.set_page_config(page_title="OpsTriage AI v2 Security Assessment", layout="wide")


@st.cache_data(show_spinner=False)
def get_attack_cases():
    return load_attack_cases()


def render_result_details(records) -> None:
    for record in records:
        label = f"{record.status.value} | {record.attack_id}: {record.attack_name}"
        with st.expander(label):
            st.write(f"**Category:** {record.category}")
            st.write(f"**Risk Level:** {record.risk_level}")
            st.write("**Attack Prompt**")
            st.code(record.prompt, language="text")
            st.write("**Expected Safe Behavior**")
            st.write(record.expected_safe_behavior)
            st.write("**Observed Response**")
            st.code(record.observed_response, language="text")
            st.write("**Reasoning**")
            st.write(record.reasoning)
            st.write("**Recommended Defense**")
            st.write(record.recommended_mitigation)


st.title("OpsTriage AI v2")
st.caption("Security Validation & Red Team Assessment")

attacks = get_attack_cases()

with st.sidebar:
    st.header("Assessment Controls")
    runner_mode = st.selectbox("Model Mode", SUPPORTED_RUNNER_MODES, index=0)
    selected_category = st.selectbox("Attack Category", category_options(attacks))
    category_attacks = attacks_for_category(attacks, selected_category)

    selected_option = None
    if category_attacks:
        selected_option = st.selectbox("Attack Case", attack_name_options(category_attacks))

    st.divider()
    st.write("Run Scope")
    run_one = st.button("Run Selected Attack", use_container_width=True)
    run_category = st.button("Run Category", use_container_width=True)
    run_all = st.button("Run All Attacks", use_container_width=True)
    run_full_assessment = st.button("Run Full Security Assessment", type="primary", use_container_width=True)

st.subheader("Assessment Workspace")

if runner_mode == "mock":
    st.info("Mock mode is active. Responses are deterministic and safe for demos and screenshots.")
else:
    st.warning(
        "opstriage_v1 mode is optional and requires local LoRA adapter artifacts. "
        "If files are missing, the app will show MODEL_UNAVAILABLE evidence instead of failing."
    )

st.write(
    "Select a model mode and attack category, then run one attack, a category, or the full "
    "red-team suite. Results can be exported as Markdown or CSV evidence."
)

if "records" not in st.session_state:
    st.session_state.records = []

if run_one and selected_option:
    selected_attack = find_attack_by_option(category_attacks, selected_option)
    with st.spinner("Running selected attack..."):
        st.session_state.records = run_attacks([selected_attack], runner_mode)

if run_category:
    with st.spinner("Running selected category..."):
        st.session_state.records = run_attacks(category_attacks, runner_mode)

if run_all or run_full_assessment:
    with st.spinner("Running full security assessment..."):
        st.session_state.records = run_attacks(attacks, runner_mode)

records = st.session_state.records

if not records:
    st.info("No attacks have been run yet.")
else:
    metrics = dashboard_metrics(records)
    metric_columns = st.columns(6)
    for column, (label, value) in zip(metric_columns, metrics.items(), strict=False):
        column.metric(label, value)
    st.info(f"Deployment Recommendation: {dashboard_deployment_recommendation(records)}")

    if has_model_unavailable(records):
        st.warning(
            "The OpsTriage v1 model is unavailable in this environment. These rows are setup "
            "evidence, not model-backed security findings."
        )

    st.subheader("Executive Dashboard")
    distributions = dashboard_distributions(records)
    chart_col1, chart_col2, chart_col3 = st.columns(3)
    with chart_col1:
        st.write("**PASS/WARN/FAIL Distribution**")
        st.bar_chart(distributions["PASS/WARN/FAIL Distribution"], x="label", y="count")
    with chart_col2:
        st.write("**Attack Category Distribution**")
        st.bar_chart(distributions["Attack Category Distribution"], x="label", y="count")
    with chart_col3:
        st.write("**Risk Level Distribution**")
        st.bar_chart(distributions["Risk Level Distribution"], x="label", y="count")

    st.subheader("Results")
    st.dataframe(evidence_table_rows(records), use_container_width=True, hide_index=True)

    st.subheader("Evidence Details")
    render_result_details(records)

    markdown_report = records_to_markdown(records)
    csv_results = records_to_csv(records)

    col_md, col_csv = st.columns(2)
    col_md.download_button(
        "Export Markdown Report",
        data=markdown_report,
        file_name="opstriage_v2_security_report.md",
        mime="text/markdown",
        use_container_width=True,
    )
    col_csv.download_button(
        "Export CSV Results",
        data=csv_results,
        file_name="opstriage_v2_security_results.csv",
        mime="text/csv",
        use_container_width=True,
    )

    if st.button("Save Report Artifacts to reports/", use_container_width=True):
        artifacts = save_records_to_reports(records)
        st.success(
            "Saved report artifacts: "
            f"{artifacts.markdown_path} and {artifacts.csv_path}"
        )

st.divider()
st.caption(
    "OpsTriage AI v2 evaluates security behavior before production deployment. "
    "Mock mode is for demos; opstriage_v1 mode is for optional adapter-backed validation."
)

import altair as alt
from experiment_terminator import ExperimentTerminator
import numpy as np
import pandas as pd
import streamlit as st


def analyze_experiment():
    exp_output = et.analyze_experiment(planned_trials_a,
                                       planned_trials_b,
                                       completed_trials_a,
                                       completed_trials_b,
                                       successes_a,
                                       successes_b)
        
    output_col1.metric("Probability of Success in Control Group", value=np.round(exp_output[0], 4))
    output_col2.metric("Probability of Success in Test Group", value=np.round(exp_output[1], 4))
    output_col3.metric("Estimated Lift", value=str(np.round(100 * exp_output[2], 2)) + "%")
    output_col4.metric("Probability Test > Control", value=np.round(exp_output[3], 4))
    output_col5.metric("Probability of Significance at Experiment End", value=np.round(exp_output[4], 4))

    if exp_output[4] < 0.01 or exp_output[4] > .99:
        outstring = "## Experiment can be terminated. "
        if exp_output[4] < .01:
            outstring += "No difference between experiment and control will be found."
        else:
            if exp_output[3] > .5:
                outstring += "Test is superior to control."
            else:
                outstring += "Control is superior to test."
        conclusion_container.markdown(outstring)
    else:
        conclusion_container.markdown("## Experiment should not be terminated.")

    chart_data = pd.DataFrame({'lift': exp_output[5]})
    chart = alt.Chart(chart_data).mark_bar().encode(
        alt.X("lift", bin=alt.Bin(maxbins=30)),
        y="count()"
    ).properties(title="Histogram of Posterior Distribution of Lift")
    graph_container.altair_chart(chart, use_container_width=True)

et = ExperimentTerminator()

st.set_page_config(layout="wide")

st.title('Experiment Terminator')

main_container = st.container()

col1, col2 = main_container.columns(2)
col1.header("Control")
planned_trials_a = col1.number_input("Planned Number of Trials", min_value=100, key='planned_trials_a', value=500)
completed_trials_a = col1.number_input("Completed Trials", min_value=100, key='completed_trials_a', value=300)
successes_a = col1.number_input("Successes", min_value=0, key='successes_a', value=25)

col2.header("Test")
planned_trials_b = col2.number_input("Planned Number of Trials", min_value=100, key='planned_trials_b', value=500)
completed_trials_b = col2.number_input("Completed Trials", min_value=100, key='completed_trials_b', value=300)
successes_b = col2.number_input("Successes", min_value=0, key='successes_b', value=35)

analyze = st.button("Analyze Experiment for Termination", on_click=analyze_experiment)

result_container = st.container()
output_col1, output_col2, output_col3, output_col4, output_col5 = result_container.columns(5)

conclusion_container = st.container()
conclusion_container.markdown("")

graph_container = st.container()
graph_container.markdown("")
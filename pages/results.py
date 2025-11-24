import streamlit as st
import plt

st.title("Your Results!")

st.write("Here is an analysis of all your strengths and weaknesses!")

if st.session_state.get("show_results", False):

    with st.container():
        scores = [st.session_state.topic_one_score,st.session_state.topic_two_score,
                  st.session_state.topic_three_score,st.session_state.topic_four_score,st.session_state.topic_five_score]
    
        topics = [st.session_state.topic_list[0],st.session_state.topic_list[1],st.session_state.topic_list[2],st.session_state.topic_list[3],
                  st.session_state.topic_list[4]]
        
        colors = ["blue", "green", "red", "orange", "purple"]
    
        fig, ax = plt.subplots(figsize=(8, 5))
        ax.bar(topics, scores, color=colors)
        ax.set_ylabel("Score")
        ax.set_title("Topic Scores")
        ax.set_ylim(0, 100)

        ax.set_xticklabels(topics, rotation=30, ha='right')

        for i, v in enumerate(scores):
            ax.text(i, v + 1, f"{v}", ha='center', fontweight='bold')
        
        st.pyplot(fig)
        

    with st.container(horizontal=True,horizontal_alignment="center"):
        st.header(f":blue[{st.session_state.topic_list[0]} Score: {st.session_state.topic_one_score}%]")
        st.markdown(st.session_state.topic_one_questions)
        st.markdown(st.session_state.topic_one_score_analysis)
    
    with st.container(horizontal=True,horizontal_alignment="center"):
        st.header(f":green[{st.session_state.topic_list[1]} Score: {st.session_state.topic_two_score}%]")
        st.markdown(st.session_state.topic_two_questions)
        st.markdown(st.session_state.topic_two_score_analysis)
    
    with st.container(horizontal=True,horizontal_alignment="center"):
        st.header(f":red[{st.session_state.topic_list[2]} Score: {st.session_state.topic_three_score}%]")
        st.markdown(st.session_state.topic_three_questions)
        st.markdown(st.session_state.topic_three_score_analysis)
    
    with st.container(horizontal=True,horizontal_alignment="center"):
        st.header(f":orange[{st.session_state.topic_list[2]} Score: {st.session_state.topic_four_score}%]")
        st.markdown(st.session_state.topic_four_questions)
        st.markdown(st.session_state.topic_four_score_analysis)
    
    with st.container(horizontal=True,horizontal_alignment="center"):
        st.header(f":violet[{st.session_state.topic_list[4]} Score: {st.session_state.topic_five_score}%]")
        st.markdown(st.session_state.topic_five_questions)
        st.markdown(st.session_state.topic_five_score_analysis)
    


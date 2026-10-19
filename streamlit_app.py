import numpy as np
import plotly.graph_objects as go
import streamlit as st

st.set_page_config(page_title='The Fourth Dimension | Spacetime', page_icon='🌌', layout='wide')
st.title('🌌 The Fourth Dimension | Spacetime')
st.caption('Basic Sciences Club — Interactive special relativity simulation')
st.info('Educational model: two spatial dimensions and ct. Constant-speed outward motion, no turnaround or gravity.')

speed = st.slider('Spacecraft speed (fraction of light speed, v/c)', 0.0, 0.99, 0.60, 0.01)
time = st.slider('Earth-frame elapsed time (years)', 0.0, 10.0, 7.0, 0.1)
gamma = 1 / np.sqrt(1 - speed**2)
proper = time / gamma

left, right = st.columns([2.3, 1])
with left:
    fig = go.Figure()
    t = np.linspace(0, 10, 35)
    a = np.linspace(0, 2*np.pi, 64)
    T, A = np.meshgrid(t, a)
    fig.add_trace(go.Surface(x=T*np.cos(A), y=T*np.sin(A), z=T, opacity=0.22, showscale=False, colorscale=[[0,'#159de5'],[1,'#159de5']], name='Future light cone', hoverinfo='skip'))
    fig.add_trace(go.Scatter3d(x=[0,0], y=[0,0], z=[0,10], mode='lines', name='Earth worldline', line=dict(color='#45d7ff', width=8)))
    fig.add_trace(go.Scatter3d(x=[0,10*speed], y=[0,0], z=[0,10], mode='lines', name='Spacecraft worldline', line=dict(color='#ffcc66', width=8)))
    fig.add_trace(go.Scatter3d(x=[0],y=[0],z=[time],mode='markers',name='Earth event',marker=dict(size=7,color='#45d7ff')))
    fig.add_trace(go.Scatter3d(x=[speed*time],y=[0],z=[time],mode='markers',name='Spacecraft event',marker=dict(size=7,color='#ffcc66')))
    fig.update_layout(height=650, margin=dict(l=0,r=0,b=0,t=20), paper_bgcolor='#071225', font=dict(color='white'), scene=dict(bgcolor='#071225', xaxis=dict(title='x (light-years)',range=[-10,10]), yaxis=dict(title='y (light-years)',range=[-10,10]), zaxis=dict(title='ct (light-years)',range=[0,10]), aspectmode='cube'), legend=dict(orientation='h',y=1.06))
    st.plotly_chart(fig, use_container_width=True)
with right:
    st.subheader('Relativity lab')
    st.metric('Earth clock', f'{time:.2f} years')
    st.metric('Spacecraft clock', f'{proper:.2f} years')
    st.metric('Lorentz factor γ', f'{gamma:.3f}')
    st.write(f'Speed: **{speed:.2f} c**')
    st.latex(r'\Delta\tau=\Delta t\sqrt{1-v^2/c^2}')
    st.markdown('**Philosophical question:** Is there one universal “now” for all observers?')
    st.caption('The cone represents the future causal boundary for light from the origin. Worldlines show paths through spacetime, not a literal spacecraft flying inside a cone.')

st.markdown('---')
st.markdown('**بالعربية:** غيّري سرعة المركبة والزمن لملاحظة الفرق بين الزمن المقاس على الأرض والزمن الخاص بالمركبة. الرسم تمثيل ثلاثي الأبعاد لجزء من الزمكان رباعي الأبعاد.')

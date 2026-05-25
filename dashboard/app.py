import streamlit as st
import requests
import uuid

API_URL = "http://localhost:8000"

st.set_page_config(page_title="Crypto Agent", layout="wide")

st.markdown('''<style>
.hero{font-size:2.4rem;font-weight:800;background:linear-gradient(90deg,#00d4ff,#7b2ff7);-webkit-background-clip:text;-webkit-text-fill-color:transparent;text-align:center;padding:1rem}
.sub{text-align:center;color:#888;margin-bottom:1.5rem}
.card{background:linear-gradient(135deg,#1a1f2e,#252d3d);border:1px solid #2d3748;border-radius:12px;padding:1.2rem;text-align:center;margin-bottom:0.5rem}
.val{font-size:1.8rem;font-weight:700;color:#00d4ff}
.lbl{font-size:0.75rem;color:#888;text-transform:uppercase;letter-spacing:1px}
.badge{display:inline-block;padding:5px 14px;border-radius:20px;font-size:0.78rem;font-weight:600;margin:3px}
.br{background:#1a3a2a;color:#00d4a0;border:1px solid #00d4a0}
.ba{background:#1a2a3a;color:#00a0d4;border:1px solid #00a0d4}
.bn{background:#3a1a2a;color:#d400a0;border:1px solid #d400a0}
.dot{height:10px;width:10px;background:#00d4a0;border-radius:50%;display:inline-block;margin-right:6px}
div[data-testid="stSidebar"]{background:#13171f;border-right:1px solid #2d3748}
section[data-testid="stSidebar"] .stButton button{background:#1a1f2e;color:#ccc;border:1px solid #2d3748;border-radius:8px;text-align:left}
section[data-testid="stSidebar"] .stButton button:hover{border-color:#00d4ff;color:#00d4ff}
</style>''', unsafe_allow_html=True)

if "session_id" not in st.session_state: st.session_state.session_id = str(uuid.uuid4())[:8]
if "messages" not in st.session_state: st.session_state.messages = []
if "total_queries" not in st.session_state: st.session_state.total_queries = 0

with st.sidebar:
    st.markdown("## Crypto Agent")
    st.markdown('<span class="dot"></span> **System Online**', unsafe_allow_html=True)
    st.divider()
    st.markdown("**Active Agents**")
    st.markdown('<div style="margin:8px 0"><span class="badge br">Researcher</span></div><div style="margin:8px 0"><span class="badge ba">Analyst</span></div><div style="margin:8px 0"><span class="badge bn">Notifier</span></div>', unsafe_allow_html=True)
    st.divider()
    st.markdown("**Quick Queries**")
    qs = ["Bitcoin price now?","Analyse top 5 coins","Best performer today?","BTC vs ETH comparison","Should I buy Ethereum?"]
    for q in qs:
        if st.button(q, use_container_width=True, key=f"q_{q}"): st.session_state.quick_query = q
    st.divider()
    st.markdown("**Session**")
    st.code(f"ID: {st.session_state.session_id}")
    st.metric("Total Queries", st.session_state.total_queries)
    if st.button("Clear History", use_container_width=True):
        st.session_state.messages = []
        st.session_state.total_queries = 0
        st.rerun()
    st.divider()
    st.markdown("**Alerts**")
    if st.button("Check Alerts", use_container_width=True):
        try:
            r = requests.get("http://localhost:8000/alerts",timeout=5)
            al = r.json().get("alerts",[])
            if al:
                for a in al[-3:]: st.warning(a)
            else: st.success("No alerts triggered")
        except: st.error("API offline")

st.markdown('<div class="hero">Crypto Research & Trading Agent</div>', unsafe_allow_html=True)
st.markdown('<div class="sub">Powered by CrewAI | Groq LLM | CoinGecko | Redis Memory</div>', unsafe_allow_html=True)

c1,c2,c3,c4 = st.columns(4)
c1.markdown('<div class="card"><div class="val">3</div><div class="lbl">Active Agents</div></div>',unsafe_allow_html=True)
c2.markdown(f'<div class="card"><div class="val">{st.session_state.total_queries}</div><div class="lbl">Queries Run</div></div>',unsafe_allow_html=True)
c3.markdown('<div class="card"><div class="val" style="color:#00d4a0">LIVE</div><div class="lbl">Redis Memory</div></div>',unsafe_allow_html=True)
c4.markdown('<div class="card"><div class="val" style="color:#00d4a0">ON</div><div class="lbl">API Status</div></div>',unsafe_allow_html=True)

st.markdown("### Ask the Research Agent")
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]): st.markdown(msg["content"])

if "quick_query" in st.session_state: prompt = st.session_state.pop("quick_query")
else: prompt = st.chat_input("Ask anything about crypto markets...")

if prompt:
    st.session_state.messages.append({"role":"user","content":prompt})
    st.session_state.total_queries += 1
    with st.chat_message("user"): st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("Agents researching live market data..."):
            try:
                res = requests.post("http://localhost:8000/query",json={"query":prompt,"session_id":st.session_state.session_id},timeout=180)
                data = res.json()
                if data["status"]=="success":
                    result = data["result"]
                    st.markdown(result)
                    st.session_state.messages.append({"role":"assistant","content":result})
                    st.rerun()
                else: st.error(f"Error: {data.get("message")}")
            except requests.exceptions.ConnectionError: st.error("Cannot connect to API. Start FastAPI first.")
            except Exception as e: st.error(f"Error: {str(e)}")

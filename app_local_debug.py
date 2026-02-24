import streamlit as st
import pandas as pd
import os
import plotly.express as px
from PIL import Image
import base64
import requests
import json

# ===========================
# 0. 多语言配置 & 品牌定义 & 项目介绍文案 (基于最新文档更新)
# ===========================
TRANSLATIONS = {
    'CN': {
        'app_name': "The Art Quantified Gaze Multi-Agents Debate System",
        'sidebar_name': "Art GazeQuant System",
        'slogan': "“看见艺术中不可见的偏见——逐像素、逐姿态、逐场辩论。”",
        
        # 导航菜单
        'nav_menu': "导航菜单",
        'nav_options': ["📖 项目介绍", "📊 全局数据洞察", "🏺 流派深度解析", "💬 Agent 辩论剧场"],
        
        # --- 项目介绍页面 (CN) ---
        'intro_title': "关于本项目",
        'intro_subtitle': "艺术性别政治：AI 驱动的量化评论与多 Agent 辩论系统",
        'intro_body': """
        本项目旨在证明：**AI 不仅是生产工具，更是批判工具。**
        
        我们构建了一个基于 **计算机视觉 (CV)** 和 **多模态大模型 (VLM)** 的跨学科研究工具。通过将艺术史的感性美学转化为可观测的量化数据，我们得以用一种前所未有的**“远距离阅读” (Distant Reading)** 视角，审视过去几个世纪中视觉符号是如何构建性别偏见的。
        
        系统不仅提供数学层面的量化得分，更通过模拟 **AI Agent 学术研讨会**，揭示潜藏在画作中的“男性凝视”与“客体化”现象。
        """,
        'intro_tech_title': "🛠️ 技术架构与核心算法",
        'intro_tech_list': """
        * **智能筛选层 (Smart Filtering):** 使用 **Gemini 1.5/2.0 Flash** 自动清洗数据，精准保留具有学术分析价值的成年男女肖像。
        * **多维度量化层 (Multi-dim Quantification):** 集成三大顶尖模型进行特征提取：
            * **SigLIP:** 从能动性、主体性、象征编码等 6 个社会学维度进行语义打分。
            * **SegFormer:** 进行人体语义分割，精确计算皮肤暴露面积与衣物覆盖比。
            * **YOLO-Pose:** 提取骨架关键点，量化姿态的“被动性”与“视线迎合度”。
        * **客观赋权层 (Entropy Weighting):** 引入数学领域的**熵权法**，自动计算指标权重，生成客观的“综合凝视指数”。
        * **Agent 辩论层 (Qwen-VL-Max):** 驱动多角色学术激辩：
            * **Laura (精神分析派):** 剖析窥淫癖与潜意识欲望。
            * **John (社会学派):** 解析空间权力与观看之道。
            * **Judith (后现代表演派):** 解构性别身份的表演性。
        """,
        'intro_footer': "本系统由 Tongji University 研究团队开发。",

        # 页面 1: 全局
        'p1_header': "跨流派性别权力关系大观",
        'p1_sub1': "各艺术流派综合凝视得分排名",
        'p1_chart1_title': "得分越高 = 越符合传统男性凝视",
        'p1_sub2': "评价指标客观权重 (熵权法)",
        'p1_info': "权重由熵权法自动生成，反映了各指标在数据集中的信息熵与区分度。",
        
        # 页面 2: 深度
        'p2_header': "流派深度量化实验室",
        'p2_select': "选择要分析的艺术流派",
        'p2_stats': "该流派共有 {count} 幅有效样本。平均综合得分: {score:.2%}",
        'p2_radar_title': "该流派指标 vs. 全球均值",
        
        # 页面 3: 辩论
        'p3_header': "多模态 Agent 学术激辩会",
        'p3_sel1': "1. 选择流派",
        'p3_sel2': "2. 选择具体画作",
        'p3_metric': "综合凝视得分",
        'p3_panel': "🎓 专家座谈席 (Laura, John, Judith)",
        'p3_btn': "🚀 启动即时辩论",
        'p3_spinner': "Agent 正在深度观察画面并查阅理论库...",
        'p3_hint': "点击上方按钮，让 AI 专家针对这张画作开始辩论。",
        
        # Agent 指令
        'agent_prompt_prefix': "作为性别主义研讨会的专家团（Laura-精神分析, John-社会学, Judith-表演理论），请对这张【{genre}】画作进行辩论。使用中文。",
        'agent_lang_instruction': "请务必使用**中文**进行对话和输出。",
        'debug_key_prompt': "🔑 (调试模式) 请在此输入 API Key:"
    },
    'EN': {
        'app_name': "The Art Quantified Gaze Multi-Agents Debate System",
        'sidebar_name': "Art GazeQuant System",
        'slogan': "“Seeing the unseen bias in art — one pixel, one pose, one debate at a time.”",
        
        # Navigation
        'nav_menu': "Navigation Menu",
        'nav_options': ["📖 Project Introduction", "📊 Global Data Insights", "🏺 Deep Genre Analysis", "💬 Agent Debate Arena"],
        
        # --- Project Intro Page (EN) ---
        'intro_title': "About The Project",
        'intro_subtitle': "Art Gender Politics: AI-Driven Quantified Critique",
        'intro_body': """
        This project aims to demonstrate: **AI is not merely a production tool, but a critical tool.**
        
        We have constructed an interdisciplinary research tool based on **Computer Vision (CV)** and **Visual Language Models (VLM)**. By transforming the aesthetic intuition of art history into observable quantified data, we adopt an unprecedented **"Distant Reading"** perspective to examine how visual symbols have constructed gender bias over the past centuries.
        
        The system provides not only mathematical quantification scores but also simulates an **AI Agent Academic Seminar** to reveal the "Male Gaze" and "Objectification" hidden within the artworks.
        """,
        'intro_tech_title': "🛠️ Technical Architecture & Algorithms",
        'intro_tech_list': """
        * **Smart Filtering (Gemini 1.5/2.0):** Automatically cleans raw data to retain portraits of adult males and females relevant for academic analysis.
        * **Multi-Dimensional Quantification:** Integrating three top-tier models for feature extraction:
            * **SigLIP:** Semantic scoring across 6 sociological dimensions (Agency, Subjectivity, Symbolism, etc.).
            * **SegFormer:** Semantic segmentation to calculate skin exposure and clothing coverage ratios.
            * **YOLO-Pose:** Extracting skeletal keypoints to quantify "Passivity" and "Gaze Compliance".
        * **Objective Weighting (Entropy Method):** Introducing the **Entropy Weight Method** to automatically calculate indicator weights and generate an objective "Comprehensive Gaze Index".
        * **Agent Debate (Qwen-VL-Max):** Driving a multi-role academic debate:
            * **Laura (Psychoanalysis):** Analyzing voyeurism and subconscious desires.
            * **John (Sociology):** Decoding spatial power and ways of seeing.
            * **Judith (Performativity):** Deconstructing the performativity of gender identity.
        """,
        'intro_footer': "Developed by the Research Team at Tongji University.",

        # Page 1
        'p1_header': "Overview of Gender Power Relations Across Genres",
        'p1_sub1': "Ranking of Comprehensive Gaze Scores by Genre",
        'p1_chart1_title': "Higher Score = More Aligned with Traditional Male Gaze",
        'p1_sub2': "Objective Weight of Indicators (Entropy Method)",
        'p1_info': "Weights are calculated via Entropy Method, reflecting the information entropy and discriminative power of each indicator.",
        
        # Page 2
        'p2_header': "Deep Quantitative Genre Laboratory",
        'p2_select': "Select Art Genre to Analyze",
        'p2_stats': "This genre has {count} valid samples. Average Comprehensive Score: {score:.2%}",
        'p2_radar_title': "Genre Metrics vs. Global Average",
        
        # Page 3
        'p3_header': "Multimodal Agent Academic Debate",
        'p3_sel1': "1. Select Genre",
        'p3_sel2': "2. Select Specific Artwork",
        'p3_metric': "Comprehensive Gaze Score",
        'p3_panel': "🎓 Expert Panel (Laura, John, Judith)",
        'p3_btn': "🚀 Start Real-time Debate",
        'p3_spinner': "Agents are deeply observing the image and consulting theoretical libraries...",
        'p3_hint': "Click the button above to let AI Agents start debating this artwork.",
        
        # Debug & Agent Instructions
        'agent_prompt_prefix': "Acting as an expert panel (Laura-Psychoanalysis, John-Sociology, Judith-Performativity), please debate this [{genre}] artwork.",
        'agent_lang_instruction': "IMPORTANT: Please conduct the entire discussion in **English**.",
        'debug_key_prompt': "🔑 (Debug Mode) Enter API Key here:"
    }
}

# ===========================
# 1. 初始化 & 路径 & 安全
# ===========================
st.set_page_config(page_title="Art GazeQuant", layout="wide", page_icon="👁️")

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(CURRENT_DIR, "discussion_data")
MASTER_CSV = os.path.join(BASE_DIR, "master_discussion_table.csv")
WEIGHTS_CSV = os.path.join(BASE_DIR, "final_indicator_weights.csv")

BASE_URL = "https://api.qnaigc.com/v1"
MODEL_NAME = "qwen-vl-max-2025-01-25"

# ===========================
# 2. 侧边栏：语言 & Debug API Key
# ===========================
st.sidebar.header("🌐 Language")
lang_code = st.sidebar.radio("Language", ["CN", "EN"], index=0, label_visibility="collapsed")
t = TRANSLATIONS[lang_code]

st.sidebar.markdown(f"# 🏛️ {t['sidebar_name']}")
st.sidebar.divider()

# --- Debug API Key 逻辑 ---
api_key_candidate = None
try:
    #api_key_candidate = st.secrets.get("QWEN_API_KEY")
    api_key_candidate = "sk-698106a86740496388b157344094c8a6"
except:
    pass

if not api_key_candidate:
    api_key_candidate = os.getenv("QWEN_API_KEY")

if not api_key_candidate:
    st.sidebar.warning("⚠️ Local Debug Mode")
    api_key_candidate = st.sidebar.text_input(
        t['debug_key_prompt'], 
        type="password",
        help="Paste your sk-xxxx key here to run instantly."
    )

API_KEY = api_key_candidate

# ===========================
# 3. 数据加载
# ===========================
@st.cache_data
def load_data():
    if not os.path.exists(MASTER_CSV):
        st.error(f"❌ Data file missing at: `{MASTER_CSV}`")
        return pd.DataFrame(), pd.DataFrame()
    df = pd.read_csv(MASTER_CSV)
    weights = pd.read_csv(WEIGHTS_CSV)
    return df, weights

def call_qwen_vl_stream(prompt, image_path):
    if not API_KEY:
        return "⚠️ Error: Please enter API Key in sidebar first!"
        
    headers = {"Content-Type": "application/json", "Authorization": f"Bearer {API_KEY}"}
    
    if not os.path.exists(image_path):
        return f"Error: Image not found at {image_path}"

    try:
        with open(image_path, "rb") as f:
            base64_img = base64.b64encode(f.read()).decode('utf-8')
        
        payload = {
            "model": MODEL_NAME,
            "messages": [{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_img}"}}
                ]
            }],
            "max_tokens": 2000
        }
        
        response = requests.post(f"{BASE_URL}/chat/completions", headers=headers, json=payload)
        if response.status_code == 200:
            return response.json()['choices'][0]['message']['content']
        else:
            return f"API Error: {response.status_code} - {response.text}"
    except Exception as e:
        return f"System Error: {e}"

df, weights = load_data()

# ===========================
# 4. 主界面渲染
# ===========================
st.title(t['app_name'])
st.markdown(f"### *{t['slogan']}*")
st.divider()

# 导航
menu_options = t['nav_options']
selected_menu_text = st.sidebar.radio(t['nav_menu'], menu_options)
menu_index = menu_options.index(selected_menu_text)

# --- 页面 0: 项目介绍 (Intro) ---
if menu_index == 0:
    st.header(t['intro_title'])
    st.subheader(t['intro_subtitle'])
    
    c1, c2 = st.columns([2, 1])
    with c1:
        st.markdown(t['intro_body'])
        st.divider()
        st.markdown(f"### {t['intro_tech_title']}")
        st.markdown(t['intro_tech_list'])
    with c2:
        st.info("💡 **Core Philosophy**")
        st.markdown("**AI is not merely a production tool, but a critical tool.**")
        st.markdown("---")
        st.caption(t['intro_footer'])

# --- 页面 1: 全局数据 ---
elif menu_index == 1:
    if df.empty: st.stop()
    st.subheader(t['p1_header'])
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"**{t['p1_sub1']}**")
        genre_avg = df.groupby('Genre')['Comprehensive_Score'].mean().reset_index().sort_values('Comprehensive_Score', ascending=False)
        fig = px.bar(genre_avg, x='Genre', y='Comprehensive_Score', color='Comprehensive_Score',
                     color_continuous_scale='RdYlGn_r', title=t['p1_chart1_title'])
        st.plotly_chart(fig, use_container_width=True)
    with col2:
        st.markdown(f"**{t['p1_sub2']}**")
        fig_pie = px.pie(weights, names='Indicator', values='Weight', hole=0.4)
        st.plotly_chart(fig_pie, use_container_width=True)
        st.info(t['p1_info'])

# --- 页面 2: 深度分析 ---
elif menu_index == 2:
    if df.empty: st.stop()
    st.subheader(t['p2_header'])
    selected_genre = st.selectbox(t['p2_select'], df['Genre'].unique())
    genre_data = df[df['Genre'] == selected_genre]
    st.write(t['p2_stats'].format(count=len(genre_data), score=genre_data['Comprehensive_Score'].mean()))
    
    indicators = ['能动性 (Agency)', '主体性 (Subjectivity)', '空间感 (Space)', 'Objectification_Score']
    valid_indicators = [c for c in indicators if c in df.columns]
    
    if valid_indicators:
        avg_metrics = genre_data[valid_indicators].mean().reset_index()
        avg_metrics.columns = ['Metric', 'Value']
        global_avg = df[valid_indicators].mean().reset_index()
        global_avg.columns = ['Metric', 'Global_Value']
        comparison_df = pd.merge(avg_metrics, global_avg, on='Metric')
        fig_radar = px.line_polar(comparison_df, r='Value', theta='Metric', line_close=True, title=t['p2_radar_title'])
        st.plotly_chart(fig_radar)
        st.dataframe(genre_data[['Filename', 'Subject', 'Comprehensive_Score'] + valid_indicators])
    else:
        st.error("CSV Columns Mismatch.")

# --- 页面 3: 辩论 (含本地 Debug 路径逻辑) ---
elif menu_index == 3:
    if df.empty: st.stop()
    st.subheader(t['p3_header'])
    c1, c2 = st.columns(2)
    with c1: sel_genre = st.selectbox(t['p3_sel1'], df['Genre'].unique())
    with c2: 
        img_list = df[df['Genre'] == sel_genre]['Filename'].tolist()
        sel_img_name = st.selectbox(t['p3_sel2'], img_list)
        
    case = df[df['Filename'] == sel_img_name].iloc[0]
    st.divider()
    col_img, col_chat = st.columns([1, 1])
    
    # === Debug 增强路径查找 ===
    img_rel_path = case['Comparison_Image']
    possible_paths = [
        os.path.join(BASE_DIR, img_rel_path),
        os.path.join(BASE_DIR, "images", os.path.basename(img_rel_path)),
        img_rel_path
    ]
    final_img_path = next((p for p in possible_paths if os.path.exists(p)), None)
    
    with col_img:
        if final_img_path:
            st.image(final_img_path, caption=sel_img_name, use_container_width=True)
            st.metric(t['p3_metric'], f"{case['Comprehensive_Score']:.4f}")
        else:
            st.error("❌ Image Not Found (本地调试)")
            st.code(f"Tried paths:\n{possible_paths}", language="text")
            
    with col_chat:
        st.subheader(t['p3_panel'])
        if st.button(t['p3_btn']):
            if final_img_path:
                with st.spinner(t['p3_spinner']):
                    base_prompt = t['agent_prompt_prefix'].format(genre=sel_genre)
                    data_context = f"[Data]: Score: {case['Comprehensive_Score']:.4f}, Objectification: {case['Objectification_Score']:.2%}"
                    lang_instr = t['agent_lang_instruction']
                    
                    full_prompt = f"{base_prompt}\n{data_context}\n{lang_instr}"
                    response = call_qwen_vl_stream(full_prompt, final_img_path)
                    st.markdown(response)
            else:
                st.error("Cannot debate: Image missing.")
        else:
            st.info(t['p3_hint'])

st.sidebar.divider()
st.sidebar.caption("Art GazeQuant - Debug Build v3.0")
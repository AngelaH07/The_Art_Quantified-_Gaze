import os
from pathlib import Path

import pandas as pd
import plotly.express as px
import streamlit as st

from localization import TRANSLATIONS
from siliconflow_client import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    SiliconFlowError,
    stream_siliconflow_vl,
)


st.set_page_config(page_title="Art GazeQuant", layout="wide", page_icon="👁️")
CURRENT_DIR = Path(__file__).resolve().parent
BASE_DIR = CURRENT_DIR / "discussion_data"
MASTER_CSV = BASE_DIR / "master_discussion_table.csv"
WEIGHTS_CSV = BASE_DIR / "final_indicator_weights.csv"


def get_setting(name, default=None):
    """Prefer Streamlit Secrets, then environment variables."""
    try:
        secret = st.secrets.get(name)
    except (FileNotFoundError, KeyError):
        secret = None
    return secret or os.getenv(name) or default


BASE_URL = get_setting("SILICONFLOW_BASE_URL", DEFAULT_BASE_URL)
MODEL_NAME = get_setting("SILICONFLOW_MODEL", DEFAULT_MODEL)
API_KEY = get_setting("SILICONFLOW_API_KEY")


def remember_choice(widget_key, state_key):
    st.session_state[state_key] = st.session_state[widget_key]


def choice_key(state_key, default):
    # A fresh widget per locale also refreshes the frontend's selected label.
    widget_key = f"{state_key}_{st.session_state.language}"
    st.session_state[widget_key] = st.session_state.get(state_key, default)
    return widget_key


# Keep underlying choices across languages, including their visible selection.
if "language" not in st.session_state:
    st.session_state.language = "EN"
t = TRANSLATIONS[st.session_state.language]
st.sidebar.header(f"🌐 {t['language']}")
lang_code = st.sidebar.radio(
    t["language"],
    ["EN", "CN"],
    format_func=lambda code: {"EN": "English", "CN": "中文"}[code],
    key="language",
    label_visibility="collapsed",
)
t = TRANSLATIONS[lang_code]
st.sidebar.markdown(f"# 🏛️ {t['sidebar_name']}")
st.sidebar.divider()
navigation_key = choice_key("navigation", 0)
menu_index = st.sidebar.radio(
    t["nav_menu"],
    list(range(len(t["nav_options"]))),
    format_func=lambda index: t["nav_options"][index],
    index=None,
    key=navigation_key,
    on_change=remember_choice,
    args=(navigation_key, "navigation"),
)
if not API_KEY:
    st.sidebar.divider()
    API_KEY = st.sidebar.text_input(
        t["api_key_label"],
        type="password",
        help=t["api_key_help"],
        key="siliconflow_api_key_input",
    )


def indicator_label(indicator):
    return t["indicator_labels"].get(indicator, indicator)


def genre_label(genre):
    return t["genre_labels"].get(genre, genre)


@st.cache_data
def load_data():
    return pd.read_csv(MASTER_CSV), pd.read_csv(WEIGHTS_CSV)


try:
    df, weights = load_data()
except (OSError, pd.errors.EmptyDataError, pd.errors.ParserError):
    df, weights = pd.DataFrame(), pd.DataFrame()
    st.warning(t["data_load_error"])

st.markdown(f"# {t['app_name']}")
st.markdown(f"*{t['slogan']}*")
st.divider()

if menu_index == 0:
    st.header(t["intro_title"])
    st.subheader(t["intro_subtitle"])
    c1, _ = st.columns([2, 1])
    with c1:
        st.markdown(t["intro_body"])
        st.markdown(t["intro_research_focus"])
        st.divider()
        st.markdown(f"### {t['intro_tech_title']}")
        st.markdown(t["intro_tech_list"].format(model_name=MODEL_NAME))
        st.divider()
        st.caption(t["intro_footer"])

elif df.empty:
    st.error(t["data_not_loaded"])

elif menu_index == 1:
    st.subheader(t["p1_header"])
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown(f"**{t['p1_sub1']}**")
        genre_avg = (
            df.groupby("Genre")["Comprehensive_Score"]
            .mean()
            .reset_index()
            .sort_values("Comprehensive_Score", ascending=False)
        )
        genre_avg["Genre"] = genre_avg["Genre"].map(genre_label)
        fig = px.bar(
            genre_avg,
            x="Genre",
            y="Comprehensive_Score",
            color="Comprehensive_Score",
            color_continuous_scale="RdYlGn_r",
            title=t["p1_chart1_title"],
            labels={"Genre": t["genre"], "Comprehensive_Score": t["score"]},
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        st.markdown(f"**{t['p1_sub2']}**")
        display_weights = weights.copy()
        display_weights["Indicator"] = display_weights["Indicator"].map(indicator_label)
        fig_pie = px.pie(
            display_weights,
            names="Indicator",
            values="Weight",
            hole=0.4,
            labels={"Indicator": t["indicator"], "Weight": t["weight"]},
        )
        st.plotly_chart(fig_pie, width="stretch")
        st.info(t["p1_info"])

    # Retain the existing demonstration values; do not present them as research results.
    st.divider()
    st.subheader(t["p1_stats_header"])
    st.caption(t["p1_demo_note"])
    col_t1, col_t2 = st.columns(2)
    with col_t1:
        st.markdown(f"#### {t['p1_ttest_header']}")
        st.write(f"**{t['p1_groups']}**")
        st.info(t["p1_hypothesis"])
        st.success(t["p1_result"])
        st.caption(t["p1_significance_note"])
    with col_t2:
        st.markdown(f"#### {t['p1_regression_header']}")
        st.write(f"**{t['p1_variables']}**")
        reg_data = pd.DataFrame(
            {
                t["indicator"]: t["regression_features"],
                t["contribution"]: [0.45, 0.32, 0.23],
                t["p_value"]: ["<0.001", "<0.01", "0.04"],
            }
        )
        st.table(reg_data)

elif menu_index == 2:
    st.subheader(t["p2_header"])
    deep_genre_key = choice_key("deep_genre", df["Genre"].iloc[0])
    selected_genre = st.selectbox(
        t["p2_select"],
        df["Genre"].unique(),
        format_func=genre_label,
        index=None,
        key=deep_genre_key,
        on_change=remember_choice,
        args=(deep_genre_key, "deep_genre"),
    )
    genre_data = df[df["Genre"] == selected_genre]
    st.write(
        t["p2_stats"].format(
            count=len(genre_data), score=genre_data["Comprehensive_Score"].mean()
        )
    )
    indicators = [
        "能动性 (Agency)",
        "主体性 (Subjectivity)",
        "空间感 (Space)",
        "Objectification_Score",
    ]
    valid_indicators = [col for col in indicators if col in df.columns]
    if valid_indicators:
        comparison = pd.DataFrame(
            {
                t["metric"]: [indicator_label(col) for col in valid_indicators] * 2,
                t["value"]: list(genre_data[valid_indicators].mean())
                + list(df[valid_indicators].mean()),
                t["series"]: [t["genre_average"]] * len(valid_indicators)
                + [t["global_average"]] * len(valid_indicators),
            }
        )
        fig_radar = px.line_polar(
            comparison,
            r=t["value"],
            theta=t["metric"],
            color=t["series"],
            line_close=True,
            title=t["p2_radar_title"],
        )
        st.plotly_chart(fig_radar, width="stretch")
        display_data = genre_data[
            ["Filename", "Subject", "Comprehensive_Score"] + valid_indicators
        ].copy()
        display_data["Subject"] = display_data["Subject"].replace(t["subject_labels"])
        display_data = display_data.rename(
            columns={
                "Filename": t["filename"],
                "Subject": t["subject"],
                "Comprehensive_Score": t["score"],
                **t["indicator_labels"],
            }
        )
        st.dataframe(display_data, width="stretch")

elif menu_index == 3:
    st.subheader(t["p3_header"])
    c1, c2 = st.columns(2)
    with c1:
        debate_genre_key = choice_key("debate_genre", df["Genre"].iloc[0])
        sel_genre = st.selectbox(
            t["p3_sel1"],
            df["Genre"].unique(),
            format_func=genre_label,
            index=None,
            key=debate_genre_key,
            on_change=remember_choice,
            args=(debate_genre_key, "debate_genre"),
        )
    with c2:
        img_list = df[df["Genre"] == sel_genre]["Filename"].unique().tolist()
        sel_img_name = st.selectbox(t["p3_sel2"], img_list, key="debate_artwork")
    case = df[(df["Genre"] == sel_genre) & (df["Filename"] == sel_img_name)].iloc[0]
    st.divider()
    col_img, col_chat = st.columns([1, 1])

    if "Comparison_Image" in case and pd.notna(case["Comparison_Image"]):
        img_rel_path = Path(case["Comparison_Image"])
        possible_paths = [BASE_DIR / img_rel_path, BASE_DIR / "images" / img_rel_path.name]
    else:
        filename = Path(case["Filename"])
        possible_paths = [
            BASE_DIR / sel_genre / f"{filename.stem}_analysis.jpg",
            BASE_DIR / sel_genre / filename,
        ]
    final_img_path = next((p for p in possible_paths if p.is_file()), None)
    with col_img:
        if final_img_path:
            st.image(final_img_path, caption=sel_img_name, width="stretch")
            st.metric(t["p3_metric"], f"{case['Comprehensive_Score']:.4f}")
        else:
            st.error(t["image_missing"])

    with col_chat:
        st.subheader(t["p3_panel"])
        if "debates" not in st.session_state:
            st.session_state.debates = {}
        debate_key = (lang_code, sel_genre, sel_img_name, MODEL_NAME)
        if st.button(t["p3_btn"]):
            if not final_img_path:
                st.error(t["debate_image_missing"])
            else:
                metrics_context = [f"- {t['score']}: {case['Comprehensive_Score']:.4f}"]
                for indicator, number_format in [
                    ("Objectification_Score", ".2%"),
                    ("能动性 (Agency)", ".2f"),
                    ("主体性 (Subjectivity)", ".2f"),
                    ("空间感 (Space)", ".2f"),
                ]:
                    if indicator in case:
                        metrics_context.append(
                            f"- {indicator_label(indicator)}: {case[indicator]:{number_format}}"
                        )
                base_prompt = t["agent_prompt_prefix"].format(genre=genre_label(sel_genre))
                data_context = f"[{t['quantitative_data']}]:\n" + "\n".join(metrics_context)
                full_prompt = f"{base_prompt}\n\n{data_context}\n\n{t['agent_lang_instruction']}"
                response_area = st.empty()
                with st.spinner(t["p3_spinner"]):
                    try:
                        with response_area.container():
                            response = st.write_stream(
                                stream_siliconflow_vl(
                                    full_prompt,
                                    final_img_path,
                                    API_KEY,
                                    model=MODEL_NAME,
                                    base_url=BASE_URL,
                                )
                            )
                    except SiliconFlowError as exc:
                        response_area.empty()
                        st.error(t[exc.message_key].format(status=exc.status))
                        if debate_key in st.session_state.debates:
                            st.caption(t["p3_previous_result"])
                            st.markdown(st.session_state.debates[debate_key])
                    else:
                        st.session_state.debates[debate_key] = response
        elif debate_key in st.session_state.debates:
            st.markdown(st.session_state.debates[debate_key])
        else:
            st.info(t["p3_hint"])

st.sidebar.divider()
st.sidebar.caption(t["powered_by"].format(model_name=MODEL_NAME))

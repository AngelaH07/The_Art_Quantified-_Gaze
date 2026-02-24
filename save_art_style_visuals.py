import argparse
import os
import sys

import numpy as np
import pandas as pd
import matplotlib
import matplotlib.pyplot as plt
from matplotlib import font_manager


matplotlib.use("Agg")


CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.join(CURRENT_DIR, "discussion_data")
MASTER_CSV = os.path.join(BASE_DIR, "master_discussion_table.csv")
WEIGHTS_CSV = os.path.join(BASE_DIR, "final_indicator_weights.csv")


def setup_chinese_font():
    preferred_fonts = [
        "PingFang SC",
        "Heiti SC",
        "STHeiti",
        "Hiragino Sans GB",
        "Noto Sans CJK SC",
        "Source Han Sans SC",
        "WenQuanYi Zen Hei",
        "SimHei",
    ]
    available_fonts = {f.name for f in font_manager.fontManager.ttflist}
    for font_name in preferred_fonts:
        if font_name in available_fonts:
            plt.rcParams["font.sans-serif"] = [font_name]
            plt.rcParams["axes.unicode_minus"] = False
            return font_name
    return None


def load_data():
    if not os.path.exists(MASTER_CSV):
        raise FileNotFoundError(f"Missing data file: {MASTER_CSV}")
    if not os.path.exists(WEIGHTS_CSV):
        raise FileNotFoundError(f"Missing data file: {WEIGHTS_CSV}")
    df = pd.read_csv(MASTER_CSV)
    weights = pd.read_csv(WEIGHTS_CSV)
    return df, weights


def ensure_output_dir(path):
    os.makedirs(path, exist_ok=True)
    return path


def save_global_insights(df, weights, output_dir):
    outputs = []

    genre_avg = (
        df.groupby("Genre")["Comprehensive_Score"]
        .mean()
        .reset_index()
        .sort_values("Comprehensive_Score", ascending=False)
    )

    fig, ax = plt.subplots(figsize=(14, 6))
    norm = plt.Normalize(genre_avg["Comprehensive_Score"].min(), genre_avg["Comprehensive_Score"].max())
    colors = plt.cm.RdYlGn_r(norm(genre_avg["Comprehensive_Score"].values))
    ax.bar(genre_avg["Genre"], genre_avg["Comprehensive_Score"], color=colors)
    ax.set_title("得分越高 = 越符合传统男性凝视")
    ax.set_xlabel("艺术流派")
    ax.set_ylabel("综合凝视得分")
    ax.tick_params(axis="x", rotation=45, labelsize=9)
    for label in ax.get_xticklabels():
        label.set_ha("right")
    fig.tight_layout()
    fig.subplots_adjust(bottom=0.22)
    out_path = os.path.join(output_dir, "艺术风格_全局数据洞察_综合得分排名.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    outputs.append(out_path)

    fig, ax = plt.subplots(figsize=(7, 7))
    ax.pie(
        weights["Weight"],
        labels=weights["Indicator"],
        autopct="%1.1f%%",
        startangle=90,
        wedgeprops={"linewidth": 1, "edgecolor": "white"},
    )
    ax.set_title("评价指标客观权重 (熵权法)")
    fig.tight_layout()
    out_path = os.path.join(output_dir, "艺术风格_全局数据洞察_权重饼图.png")
    fig.savefig(out_path, dpi=300)
    plt.close(fig)
    outputs.append(out_path)

    return outputs


def _radar_angles(n):
    angles = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    angles += angles[:1]
    return angles


def save_deep_lab_radar(df, output_dir, genres=None):
    outputs = []
    indicators = ["能动性 (Agency)", "主体性 (Subjectivity)", "空间感 (Space)", "Objectification_Score"]
    valid_indicators = [col for col in indicators if col in df.columns]
    if not valid_indicators:
        return outputs

    genre_list = genres or sorted(df["Genre"].unique().tolist())
    for genre in genre_list:
        genre_data = df[df["Genre"] == genre]
        if genre_data.empty:
            continue

        avg_metrics = genre_data[valid_indicators].mean().tolist()
        angles = _radar_angles(len(valid_indicators))
        values = avg_metrics + avg_metrics[:1]

        fig = plt.figure(figsize=(7, 7))
        ax = plt.subplot(111, polar=True)
        ax.plot(angles, values, linewidth=2, color="#3B82F6")
        ax.fill(angles, values, alpha=0.2, color="#3B82F6")
        ax.set_thetagrids(np.degrees(angles[:-1]), valid_indicators)
        ax.set_title(f"{genre} 指标雷达图")
        ax.grid(True, linewidth=0.5, alpha=0.7)
        fig.tight_layout()

        safe_genre = str(genre).replace("/", "_").replace("\\", "_")
        out_path = os.path.join(
            output_dir,
            f"艺术风格_流派深度量化实验室_{safe_genre}_雷达图.png",
        )
        fig.savefig(out_path, dpi=300)
        plt.close(fig)
        outputs.append(out_path)

    return outputs


def main():
    parser = argparse.ArgumentParser(description="保存“全局数据洞察”和“流派深度量化实验室”的可视化图片")
    parser.add_argument(
        "--output-dir",
        default=os.path.join(CURRENT_DIR, "saved_visuals"),
        help="保存图片的目录",
    )
    parser.add_argument(
        "--genre",
        action="append",
        help="仅保存指定流派的雷达图（可重复传入）",
    )
    args = parser.parse_args()

    setup_chinese_font()

    df, weights = load_data()
    if df.empty:
        raise ValueError("数据为空，无法生成图片。")

    output_dir = ensure_output_dir(args.output_dir)

    outputs = []
    outputs.extend(save_global_insights(df, weights, output_dir))
    outputs.extend(save_deep_lab_radar(df, output_dir, genres=args.genre))

    print("已保存图片：")
    for path in outputs:
        print(path)


if __name__ == "__main__":
    try:
        main()
    except Exception as exc:
        print(f"生成失败：{exc}")
        sys.exit(1)

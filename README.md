# Art GazeQuant

A bilingual Streamlit application for exploring the project's existing art-analysis data and generating multimodal agent debates through SiliconFlow.

## Run locally

Use Python 3.11 or later, keep the original `discussion_data/` folder, and run:

```sh
python -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
streamlit run app.py
```

`app_local_debug.py` is a compatibility entry point that runs the same application, including on widget reruns.

## SiliconFlow configuration

Copy the settings from `secrets.toml.example` into `.streamlit/secrets.toml`, or into the Secrets settings of your Streamlit Cloud application. Replace the placeholder with your own SiliconFlow key. Environment variables with the same names also work; Streamlit Secrets take priority.

```toml
SILICONFLOW_API_KEY = "YOUR_SILICONFLOW_API_KEY"
SILICONFLOW_BASE_URL = "https://api.siliconflow.cn/v1"
SILICONFLOW_MODEL = "Qwen/Qwen3-VL-30B-A3B-Instruct"
```

Without a configured key, the sidebar provides a password field for the current session. Data exploration works without an API key. The debate request sends the selected analysis image and quantitative context to SiliconFlow only when you press the debate button. Choose a model that supports image input and is available to your account.

The client uses the documented [chat completions endpoint](https://docs.siliconflow.cn/docs/api/chat-completions-post) and [multimodal image input](https://docs.siliconflow.cn/docs/userguide/capabilities/vision). Model availability can change; override `SILICONFLOW_MODEL` as needed. The legacy provider and `QWEN_API_KEY` are no longer used.

## Languages and data

- A new session starts in **English**. Select **中文** for Chinese.
- Navigation, statistics, chart legends, hover labels, table headers, genre labels, and API errors use the selected language.
- CSV column names, stored genre identifiers, filenames, source images, scores, and weights remain unchanged. Model names and artwork filenames remain identifiers. Existing text embedded in source images is preserved.
- Switching languages preserves the current navigation page. Debate results are scoped to language, genre, artwork, and model.
- The statistical section retains the original hard-coded demonstration values and explicitly labels them as illustrative. It does not load the statistical reports or calculate new research results.
- The genre radar now displays both the existing genre mean and overall mean described by its title.

## Checks

```sh
python -m unittest discover -s tests -v
```

Tests exercise the multimodal request contract with mocked HTTP responses and run the actual Streamlit pages through AppTest, including language switching and chart/table labels. They do not make paid API calls or establish model response quality.

## 更新已有项目

将更新包中的文件复制到原仓库根目录，保留原有的 `discussion_data/`、`statistical_analysis/` 和图像文件。重新安装 `requirements.txt` 中的依赖，在 Streamlit 的 Secrets 中填写 `SILICONFLOW_API_KEY`，然后重新启动应用。

默认界面为 English；选择“中文”后，导航、图表与统计文案使用中文。`SILICONFLOW_MODEL` 可替换为你在硅基流动账户中可用的视觉模型。不要把真实密钥上传到 GitHub。

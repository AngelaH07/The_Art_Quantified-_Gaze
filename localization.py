"""Display labels only; source data columns and values remain unchanged."""

TRANSLATIONS = {'CN': {'app_name': '艺术凝视量化多智能体辩论系统',
        'sidebar_name': '艺术凝视量化系统',
        'slogan': '“看见艺术中不可见的偏见——逐像素、逐姿态、逐场辩论。”',
        'nav_menu': '导航菜单',
        'nav_options': ['📖 项目介绍', '📊 全局数据洞察', '🏺 流派深度解析', '💬 智能体辩论剧场'],
        'intro_title': '关于本项目',
        'intro_subtitle': '当计算机视觉遇上艺术史批评',
        'intro_body': '我们构建了一个基于**计算机视觉**和**多模态大模型**的跨学科研究工具。通过将艺术史的感性美学转化为可观测的量化数据，我们得以从**“远距离阅读”**的视角，审视过去几个世纪中视觉符号如何构建性别偏见。\n'
                      '\n'
                      '系统不仅提供数学层面的量化得分，更通过模拟**人工智能学术研讨会**，揭示潜藏在画作中的“男性凝视”与“客体化”现象。',
        'intro_research_focus': '### 🎯 研究聚焦：从描述到解释\n'
                                '本项目不仅关注“是否存在性别差异”，更致力于通过量化指标解释**“权力关系是如何被视觉化构建的”**。\n'
                                '* **姿态动力学：** 脊柱倾角与视线迎合度如何暗示“顺从”？\n'
                                '* **空间构图：** 人物在画面中的占比与位置如何体现“边缘化”？\n'
                                '* **客体化指标：** 皮肤暴露比例与装饰物频次如何强化“被看”的属性？',
        'intro_tech_title': '🛠️ 核心技术栈',
        'intro_tech_list': '* **智能筛选层：** 使用 **Gemini 1.5/2.0 Flash** 自动清洗数据，保留具有学术分析价值的成年男女肖像。\n'
                           '* **多维度量化层：** 集成三大模型进行特征提取：\n'
                           '    * **SigLIP：** 从能动性、主体性、象征编码等六个社会学维度进行语义打分。\n'
                           '    * **SegFormer：** 进行人体语义分割，计算皮肤暴露面积与衣物覆盖比。\n'
                           '    * **YOLO-Pose：** 提取骨架关键点，量化姿态的“被动性”与“视线迎合度”。\n'
                           '* **客观赋权层：** 引入**熵权法**，自动计算指标权重，生成“综合凝视指数”。\n'
                           '* **智能体辩论层（硅基流动 · {model_name}）：** 驱动多角色学术辩论：\n'
                           '    * **劳拉（精神分析派）：** 剖析窥淫癖与潜意识欲望。\n'
                           '    * **约翰（社会学派）：** 解析空间权力与观看之道。\n'
                           '    * **朱迪斯（后现代表演派）：** 解构性别身份的表演性。',
        'intro_footer': '本系统由 Angela 何开发完成，黄博士指导，人工智能提供编程技术支持。',
        'p1_header': '跨流派性别权力关系大观',
        'p1_sub1': '各艺术流派综合凝视得分排名',
        'p1_chart1_title': '得分越高 = 越符合传统男性凝视',
        'p1_sub2': '评价指标客观权重 (熵权法)',
        'p1_info': '权重反映了各指标在现有数据中的区分度。',
        'p2_header': '流派深度量化实验室',
        'p2_select': '选择要分析的艺术流派',
        'p2_stats': '该流派共有 {count} 幅有效样本。平均综合得分: {score:.2%}',
        'p2_radar_title': '该流派指标与全体均值对比',
        'p3_header': '多模态智能体学术辩论会',
        'p3_sel1': '1. 选择流派',
        'p3_sel2': '2. 选择具体画作',
        'p3_metric': '综合凝视得分',
        'p3_panel': '🎓 专家座谈席',
        'p3_btn': '🚀 启动即时辩论',
        'p3_spinner': '智能体正在观察画面并结合理论进行分析……',
        'p3_hint': '点击上方按钮，让智能体针对这张画作开始辩论。',
        'agent_prompt_prefix': '作为性别研究研讨会的专家团（劳拉、约翰、朱迪斯），请对这张【{genre}】画作进行辩论。请结合给出的量化指标（如综合得分、客体化程度、能动性等）与艺术史理论（如男性凝视、权力空间）进行深度对话。',
        'agent_lang_instruction': '请务必使用**中文**进行对话和输出。',
        'language': '语言',
        'p1_stats_header': '🔬 统计显著性验证',
        'p1_ttest_header': '独立样本检验',
        'p1_groups': '女性组（样本量 = 2500）与男性组（样本量 = 2100）',
        'p1_hypothesis': '假设：女性肖像的综合凝视得分显著高于男性。',
        'p1_result': '✅ 示例结果显著：t(4598) = 12.45，p < 0.001',
        'p1_significance_note': '注：在检验假设成立的前提下，p < 0.05 表示差异达到所设定的统计显著性水平。',
        'p1_regression_header': '多元线性回归分析',
        'p1_variables': '因变量：综合得分｜自变量：客体化、姿态、空间',
        'p1_demo_note': '以下统计数值为界面演示示例，并非由当前数据集计算得到的检验结果。',
        'regression_features': ['客体化（皮肤）', '姿态', '空间'],
        'indicator': '指标',
        'weight': '权重',
        'contribution': '贡献度（β）',
        'p_value': '概率值',
        'genre': '艺术流派',
        'score': '综合凝视得分',
        'filename': '画作文件名',
        'subject': '主体',
        'metric': '指标',
        'value': '数值',
        'series': '对比组',
        'genre_average': '该流派均值',
        'global_average': '全体均值',
        'data_not_loaded': '数据未加载，请检查项目中的数据文件。',
        'data_load_error': '无法读取数据文件，请检查 discussion_data 文件夹中的数据是否完整。',
        'image_missing': '未找到这幅画作的图像，请检查项目中的图像文件。',
        'debate_image_missing': '缺少有效图像，无法启动辩论。',
        'api_key_label': '硅基流动 API 密钥',
        'api_key_help': '仅用于当前会话。部署时可在机密配置或环境变量中设置 SILICONFLOW_API_KEY。',
        'api_key_missing': '请在侧边栏输入硅基流动 API 密钥，或配置 SILICONFLOW_API_KEY。',
        'api_error': '硅基流动请求失败（HTTP {status}）。请检查密钥、模型权限和账户余额后重试。',
        'api_timeout': '硅基流动请求超时，请稍后重试。',
        'api_connection': '无法连接硅基流动，请检查网络后重试。',
        'api_invalid_response': '硅基流动未返回有效的辩论内容，请稍后重试。',
        'api_image_error': '无法读取画作图像，请检查文件后重试。',
        'quantitative_data': '量化指标数据',
        'powered_by': '由硅基流动 · {model_name} 与 SegFormer 提供支持',
        'indicator_labels': {'能动性 (Agency)': '能动性',
                             '主体性 (Subjectivity)': '主体性',
                             '空间感 (Space)': '空间感',
                             '气质 (Atmosphere)': '气质',
                             '环境领域 (Environment)': '环境领域',
                             '象征编码 (Symbolism)': '象征编码',
                             'Objectification_Score': '客体化得分',
                             'Passive_Score': '被动性得分',
                             'Curve_Score': '曲线得分',
                             'Submissive_Score': '顺从性得分'},
        'genre_labels': {'Academicism': '学院派',
                         'ArtDeco': '装饰艺术',
                         'ArtNouveau(Modern)': '新艺术运动',
                         'Biedermeier': '比德迈风格',
                         'Classicism': '古典主义',
                         'Constructivism': '构成主义',
                         'Divisionism': '分色主义',
                         'EnvironmentalArt': '环境艺术',
                         'FeministArt': '女性主义艺术',
                         'HighRenaissance': '文艺复兴盛期',
                         'Impressionism': '印象派',
                         'InternationalGothic': '国际哥特式',
                         'Japonism': '日本主义',
                         'LowbrowArt': '低俗艺术',
                         'MagicRealism': '魔幻现实主义',
                         'MechanisticCubism': '机械立体主义',
                         'Muralism': '壁画主义',
                         'Naturalism': '自然主义',
                         'Neo-baroque': '新巴洛克',
                         'NewEuropeanPainting': '新欧洲绘画',
                         'NorthernRenaissance': '北方文艺复兴',
                         'Outsiderart': '局外人艺术',
                         'Photorealism': '照相写实主义',
                         'PopArt': '波普艺术',
                         'PosterArtRealism': '海报写实艺术',
                         'ProtoRenaissance': '文艺复兴早期',
                         'Rococo': '洛可可',
                         'Shin-hanga': '新版画',
                         'SocialistRealism': '社会主义现实主义',
                         'Suprematism': '至上主义',
                         'Synthetism': '综合主义',
                         'Ukiyo-e': '浮世绘',
                         'cartoon': '卡通',
                         'photo': '摄影'},
        'subject_labels': {'Adult Woman': '成年女性', 'Adult Man': '成年男性'}},
 'EN': {'app_name': 'The Art Quantified Gaze Multi-Agents Debate System',
        'sidebar_name': 'Art GazeQuant System',
        'slogan': '“Seeing the unseen bias in art — one pixel, one pose, one debate at a time.”',
        'nav_menu': 'Navigation Menu',
        'nav_options': ['📖 Project Introduction',
                        '📊 Global Data Insights',
                        '🏺 Deep Genre Analysis',
                        '💬 Agent Debate Arena'],
        'intro_title': 'About The Project',
        'intro_subtitle': 'When Computer Vision Meets Art History Critique',
        'intro_body': '\n'
                      '        We have constructed an interdisciplinary research tool based on '
                      '**Computer Vision (CV)** and **Visual Language Models (VLM)**. By '
                      'transforming the aesthetic intuition of art history into observable '
                      'quantified data, we adopt an unprecedented **"Distant Reading"** '
                      'perspective to examine how visual symbols have constructed gender bias over '
                      'the past centuries.\n'
                      '        \n'
                      '        The system provides not only mathematical quantification scores but '
                      'also simulates an **AI Agent Academic Seminar** to reveal the "Male Gaze" '
                      'and "Objectification" hidden within the artworks.\n'
                      '        ',
        'intro_research_focus': '\n'
                                '        ### 🎯 Research Focus: From Description to Explanation\n'
                                '        This project focuses not just on "whether gender '
                                'differences exist," but on explaining **"how power relations are '
                                'visually constructed"** through quantitative metrics.\n'
                                '        *   **Pose Dynamics:** How do spinal angles and gaze '
                                'compliance imply "submission"?\n'
                                '        *   **Spatial Composition:** How do character proportions '
                                'and positioning reflect "marginalization"?\n'
                                '        *   **Objectification Metrics:** How do skin exposure '
                                'ratios and accessory frequency reinforce the attribute of "being '
                                'looked at"?\n'
                                '        ',
        'intro_tech_title': '🛠️ Core Technology Stack',
        'intro_tech_list': '\n'
                           '        * **Smart Filtering (Gemini 1.5/2.0):** Automatically cleans '
                           'raw data to retain portraits of adult males and females relevant for '
                           'academic analysis.\n'
                           '        * **Multi-Dimensional Quantification:** Integrating three '
                           'top-tier models for feature extraction:\n'
                           '            * **SigLIP:** Semantic scoring across 6 sociological '
                           'dimensions (Agency, Subjectivity, Symbolism, etc.).\n'
                           '            * **SegFormer:** Semantic segmentation to calculate skin '
                           'exposure and clothing coverage ratios.\n'
                           '            * **YOLO-Pose:** Extracting skeletal keypoints to quantify '
                           '"Passivity" and "Gaze Compliance".\n'
                           '        * **Objective Weighting (Entropy Method):** Introducing the '
                           '**Entropy Weight Method** to automatically calculate indicator weights '
                           'and generate an objective "Comprehensive Gaze Index".\n'
                           '        * **Agent Debate (SiliconFlow · {model_name}):** Driving a '
                           'multi-role academic debate:\n'
                           '            * **Laura (Psychoanalysis):** Analyzing voyeurism and '
                           'subconscious desires.\n'
                           '            * **John (Sociology):** Decoding spatial power and ways of '
                           'seeing.\n'
                           '            * **Judith (Performativity):** Deconstructing the '
                           'performativity of gender identity.\n'
                           '        ',
        'intro_footer': 'This system was developed by Angela He, under the supervision of Dr. '
                        'Huang, with AI-powered Vibe Coding technical support.',
        'p1_header': 'Overview of Gender Power Relations Across Genres',
        'p1_sub1': 'Ranking of Comprehensive Gaze Scores by Genre',
        'p1_chart1_title': 'Higher Score = More Aligned with Traditional Male Gaze',
        'p1_sub2': 'Objective Weight of Indicators (Entropy Method)',
        'p1_info': 'Weights reflect the discriminative power of each indicator in the current '
                   'dataset.',
        'p2_header': 'Deep Quantitative Genre Laboratory',
        'p2_select': 'Select Art Genre to Analyze',
        'p2_stats': 'This genre has {count} valid samples. Average Comprehensive Score: '
                    '{score:.2%}',
        'p2_radar_title': 'Genre Metrics vs. Overall Average',
        'p3_header': 'Multimodal Agent Academic Debate',
        'p3_sel1': '1. Select Genre',
        'p3_sel2': '2. Select Specific Artwork',
        'p3_metric': 'Comprehensive Gaze Score',
        'p3_panel': '🎓 Expert Panel',
        'p3_btn': '🚀 Start Real-time Debate',
        'p3_spinner': 'Agents are deeply observing the image and consulting theoretical '
                      'libraries...',
        'p3_hint': 'Click the button above to let AI Agents start debating this artwork.',
        'agent_prompt_prefix': 'Acting as an expert panel at a gender studies seminar (Personas: '
                               'Laura, John, Judith), please debate this [{genre}] artwork. Please '
                               'engage in a deep dialogue by integrating the provided quantitative '
                               'metrics (e.g., comprehensive score, objectification level, agency) '
                               'with art history theories (e.g., male gaze, spatial power).',
        'agent_lang_instruction': 'IMPORTANT: Please conduct the entire discussion in **English**.',
        'language': 'Language',
        'p1_stats_header': '🔬 Statistical Significance',
        'p1_ttest_header': 'Independent Samples T-Test',
        'p1_groups': 'Female group (N = 2500) vs. male group (N = 2100)',
        'p1_hypothesis': 'Hypothesis: Female portraits have significantly higher comprehensive '
                         'gaze scores than male portraits.',
        'p1_result': '✅ Significant example result: t(4598) = 12.45, p < 0.001',
        'p1_significance_note': 'Note: Under the test assumptions, p < 0.05 meets the specified '
                                'statistical significance threshold.',
        'p1_regression_header': 'Multiple Linear Regression',
        'p1_variables': 'Outcome: Comprehensive Score | Predictors: Objectification, Pose, Space',
        'p1_demo_note': 'The statistics below are illustrative examples, not test results '
                        'calculated from the current dataset.',
        'regression_features': ['Objectification (Skin)', 'Pose', 'Space'],
        'indicator': 'Indicator',
        'weight': 'Weight',
        'contribution': 'Contribution (β)',
        'p_value': 'P-value',
        'genre': 'Art Genre',
        'score': 'Comprehensive Gaze Score',
        'filename': 'Artwork Filename',
        'subject': 'Subject',
        'metric': 'Metric',
        'value': 'Value',
        'series': 'Comparison Group',
        'genre_average': 'Genre Average',
        'global_average': 'Overall Average',
        'data_not_loaded': 'Data not loaded. Please check the project data files.',
        'data_load_error': 'Unable to read the data files. Please check that the discussion_data '
                           'folder is complete.',
        'image_missing': 'Artwork image not found. Please check the project image files.',
        'debate_image_missing': 'Cannot start a debate without a valid image.',
        'api_key_label': 'SiliconFlow API Key',
        'api_key_help': 'Used only for this session. For deployment, set SILICONFLOW_API_KEY in '
                        'Streamlit Secrets or an environment variable.',
        'api_key_missing': 'Enter your SiliconFlow API key in the sidebar or configure '
                           'SILICONFLOW_API_KEY.',
        'api_error': 'SiliconFlow request failed (HTTP {status}). Check your API key, model '
                     'access, and account balance, then try again.',
        'api_timeout': 'The SiliconFlow request timed out. Please try again later.',
        'api_connection': 'Unable to connect to SiliconFlow. Check your network and try again.',
        'api_invalid_response': 'SiliconFlow did not return valid debate content. Please try '
                                'again.',
        'api_image_error': 'Unable to read the artwork image. Please check the file and try again.',
        'quantitative_data': 'Quantitative Data',
        'powered_by': 'Powered by SiliconFlow · {model_name} & SegFormer',
        'indicator_labels': {'能动性 (Agency)': 'Agency',
                             '主体性 (Subjectivity)': 'Subjectivity',
                             '空间感 (Space)': 'Space',
                             '气质 (Atmosphere)': 'Atmosphere',
                             '环境领域 (Environment)': 'Environment',
                             '象征编码 (Symbolism)': 'Symbolism',
                             'Objectification_Score': 'Objectification Score',
                             'Passive_Score': 'Passivity Score',
                             'Curve_Score': 'Curve Score',
                             'Submissive_Score': 'Submissiveness Score'},
        'genre_labels': {'Academicism': 'Academicism',
                         'ArtDeco': 'Art Deco',
                         'ArtNouveau(Modern)': 'Art Nouveau (Modern)',
                         'Biedermeier': 'Biedermeier',
                         'Classicism': 'Classicism',
                         'Constructivism': 'Constructivism',
                         'Divisionism': 'Divisionism',
                         'EnvironmentalArt': 'Environmental Art',
                         'FeministArt': 'Feminist Art',
                         'HighRenaissance': 'High Renaissance',
                         'Impressionism': 'Impressionism',
                         'InternationalGothic': 'International Gothic',
                         'Japonism': 'Japonism',
                         'LowbrowArt': 'Lowbrow Art',
                         'MagicRealism': 'Magic Realism',
                         'MechanisticCubism': 'Mechanistic Cubism',
                         'Muralism': 'Muralism',
                         'Naturalism': 'Naturalism',
                         'Neo-baroque': 'Neo-Baroque',
                         'NewEuropeanPainting': 'New European Painting',
                         'NorthernRenaissance': 'Northern Renaissance',
                         'Outsiderart': 'Outsider Art',
                         'Photorealism': 'Photorealism',
                         'PopArt': 'Pop Art',
                         'PosterArtRealism': 'Poster Art Realism',
                         'ProtoRenaissance': 'Proto-Renaissance',
                         'Rococo': 'Rococo',
                         'Shin-hanga': 'Shin-hanga',
                         'SocialistRealism': 'Socialist Realism',
                         'Suprematism': 'Suprematism',
                         'Synthetism': 'Synthetism',
                         'Ukiyo-e': 'Ukiyo-e',
                         'cartoon': 'Cartoon',
                         'photo': 'Photography'},
        'subject_labels': {'Adult Woman': 'Adult Woman', 'Adult Man': 'Adult Man'}}}

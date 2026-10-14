import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

from streamlit.testing.v1 import AppTest

from localization import TRANSLATIONS
from siliconflow_client import SiliconFlowError


ROOT = Path(__file__).resolve().parents[1]
CJK = re.compile(r'[\u3400-\u9fff]')


class BilingualAppTests(unittest.TestCase):
    def open_app(self, entry='app.py'):
        app = AppTest.from_file(ROOT / entry, default_timeout=30).run()
        self.assertFalse(app.exception, [e.message for e in app.exception])
        return app

    def assert_page_ok(self, app):
        self.assertFalse(app.exception, [e.message for e in app.exception])

    def assert_main_is_english(self, app):
        for kind in ['markdown', 'header', 'subheader', 'caption', 'info', 'success', 'error', 'warning', 'metric']:
            for node in app.main.get(kind):
                value = str(node.value)
                self.assertIsNone(CJK.search(value), value)
        for chart in app.get('plotly_chart'):
            self.assertIsNone(CJK.search(chart.proto.spec), 'Chinese leaked into an English chart')
        for table in list(app.table) + list(app.dataframe):
            self.assertIsNone(CJK.search(table.value.to_json(force_ascii=False)), 'Chinese leaked into an English table')

    def test_default_and_all_english_pages(self):
        app = self.open_app()
        self.assertEqual(app.sidebar.radio[0].value, 'EN')
        for page in range(4):
            with self.subTest(page=page):
                app.sidebar.radio[1].set_value(page).run()
                self.assert_page_ok(app)
                self.assert_main_is_english(app)

    def test_global_labels_and_navigation_survive_language_switches(self):
        app = self.open_app()
        app.sidebar.radio[1].set_value(1).run()
        for language in ['CN', 'EN', 'CN', 'EN']:
            with self.subTest(language=language):
                app.sidebar.radio[0].set_value(language).run()
                self.assert_page_ok(app)
                self.assertEqual(app.sidebar.radio[1].value, 1)
                spec = json.loads(app.get('plotly_chart')[1].proto.spec)
                labels = spec['data'][0]['labels']
                self.assertEqual(set(labels), set(TRANSLATIONS[language]['indicator_labels'].values()))
                table = app.table[0].value
                self.assertEqual(list(table.columns), [TRANSLATIONS[language][key] for key in ['indicator', 'contribution', 'p_value']])
                self.assertEqual(table.iloc[:, 0].tolist(), TRANSLATIONS[language]['regression_features'])
                if language == 'EN':
                    self.assert_main_is_english(app)

    def test_deep_analysis_uses_localized_display_data(self):
        app = self.open_app()
        app.sidebar.radio[1].set_value(2).run()
        app.selectbox[0].set_value('PopArt').run()
        source_filename = app.dataframe[0].value.iloc[0, 0]
        for language in ['CN', 'EN']:
            app.sidebar.radio[0].set_value(language).run()
            self.assert_page_ok(app)
            self.assertEqual(app.sidebar.radio[1].value, 2)
            self.assertEqual(app.selectbox[0].value, 'PopArt')
            self.assertEqual(app.dataframe[0].value.iloc[0, 0], source_filename)
            self.assertEqual(app.dataframe[0].value.columns[1], TRANSLATIONS[language]['subject'])
            self.assertEqual(len(json.loads(app.get('plotly_chart')[0].proto.spec)['data']), 2)
            if language == 'EN':
                self.assert_main_is_english(app)

    @patch('siliconflow_client.stream_siliconflow_vl')
    def test_debate_prompts_and_results_are_scoped_to_language(self, call):
        app = self.open_app()
        app.sidebar.radio[1].set_value(3).run()
        call.return_value = iter(['English debate', ' result'])
        app.button[0].click().run()
        self.assert_page_ok(app)
        self.assertIsNone(CJK.search(call.call_args.args[0]))
        self.assertIn('English debate result', [m.value for m in app.markdown])
        app.sidebar.radio[0].set_value('CN').run()
        self.assert_page_ok(app)
        self.assertNotIn('English debate result', [m.value for m in app.markdown])
        call.return_value = iter(['中文', '辩论结果'])
        app.button[0].click().run()
        self.assertIn('中文', call.call_args.args[0])
        self.assertIn('中文辩论结果', [m.value for m in app.markdown])
        app.sidebar.radio[0].set_value('EN').run()
        self.assertIn('English debate result', [m.value for m in app.markdown])
        self.assertNotIn('中文辩论结果', [m.value for m in app.markdown])

    @patch('siliconflow_client.stream_siliconflow_vl', side_effect=SiliconFlowError('api_key_missing'))
    def test_api_error_uses_the_current_language(self, call):
        app = self.open_app()
        app.sidebar.radio[1].set_value(3).run()
        for language in ['CN', 'EN']:
            app.sidebar.radio[0].set_value(language).run()
            app.button[0].click().run()
            self.assert_page_ok(app)
            self.assertEqual(app.error[0].value, TRANSLATIONS[language]['api_key_missing'])

    @patch('siliconflow_client.stream_siliconflow_vl')
    def test_failed_retry_labels_the_previous_result_and_discards_partial_output(self, call):
        app = self.open_app()
        app.sidebar.radio[1].set_value(3).run()
        call.return_value = iter(['Last ', 'completed debate'])
        app.button[0].click().run()

        def interrupted(*args, **kwargs):
            yield 'Interrupted partial answer'
            raise SiliconFlowError('api_timeout')

        call.side_effect = interrupted
        app.button[0].click().run()
        self.assert_page_ok(app)
        self.assertEqual(app.error[0].value, TRANSLATIONS['EN']['api_timeout'])
        self.assertIn(TRANSLATIONS['EN']['p3_previous_result'], [c.value for c in app.main.get('caption')])
        self.assertIn('Last completed debate', [m.value for m in app.markdown])
        self.assertNotIn('Interrupted partial answer', [m.value for m in app.markdown])
        self.assertEqual(list(app.session_state['debates'].values()), ['Last completed debate'])

        call.side_effect = None
        call.return_value = iter(['Replacement completed debate'])
        app.button[0].click().run()
        self.assert_page_ok(app)
        self.assertFalse(app.error)
        self.assertIn('Replacement completed debate', [m.value for m in app.markdown])
        self.assertNotIn('Last completed debate', [m.value for m in app.markdown])
        self.assertEqual(list(app.session_state['debates'].values()), ['Replacement completed debate'])

    @patch('siliconflow_client.stream_siliconflow_vl')
    def test_failed_first_stream_is_not_cached(self, call):
        app = self.open_app()
        app.sidebar.radio[0].set_value('CN').run()
        app.sidebar.radio[1].set_value(3).run()

        def interrupted(*args, **kwargs):
            yield '未完成的辩论'
            raise SiliconFlowError('api_incomplete_response')

        call.side_effect = interrupted
        app.button[0].click().run()
        self.assert_page_ok(app)
        self.assertEqual(app.error[0].value, TRANSLATIONS['CN']['api_incomplete_response'])
        self.assertNotIn('未完成的辩论', [m.value for m in app.markdown])
        self.assertEqual(app.session_state['debates'], {})

    def test_debug_entry_point_reruns_the_shared_application(self):
        app = self.open_app('app_local_debug.py')
        app.sidebar.radio[1].set_value(1).run()
        app.sidebar.radio[0].set_value('CN').run()
        self.assert_page_ok(app)
        self.assertEqual(app.sidebar.radio[1].value, 1)
        self.assertTrue(app.get('plotly_chart'))
        self.assertEqual(app.subheader[-1].value, TRANSLATIONS['CN']['p1_stats_header'])


if __name__ == '__main__':
    unittest.main()

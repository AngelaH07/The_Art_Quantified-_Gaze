import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests

from siliconflow_client import DEFAULT_BASE_URL, DEFAULT_MODEL, SiliconFlowError, call_siliconflow_vl


class SiliconFlowClientTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.image = Path(self.temp.name) / 'artwork.png'
        self.image.write_bytes(b'example-image-bytes')

    @patch('siliconflow_client.requests.post')
    def test_multimodal_request_contract(self, post):
        post.return_value = Mock(status_code=200)
        post.return_value.json.return_value = {'choices': [{'message': {'content': 'Debate'}}]}
        result = call_siliconflow_vl('Discuss in English.', self.image, 'test-key')
        self.assertEqual(result, 'Debate')
        args, kwargs = post.call_args
        self.assertEqual(args[0], DEFAULT_BASE_URL + '/chat/completions')
        self.assertEqual(kwargs['headers']['Authorization'], 'Bearer test-key')
        self.assertEqual(kwargs['json']['model'], DEFAULT_MODEL)
        self.assertEqual(kwargs['json']['messages'][0]['content'][0]['text'], 'Discuss in English.')
        self.assertTrue(kwargs['json']['messages'][0]['content'][1]['image_url']['url'].startswith('data:image/png;base64,'))
        self.assertEqual(kwargs['timeout'], (10, 120))

    @patch('siliconflow_client.requests.post')
    def test_configuration_overrides(self, post):
        post.return_value = Mock(status_code=200)
        post.return_value.json.return_value = {'choices': [{'message': {'content': 'Result'}}]}
        call_siliconflow_vl('Prompt', self.image, 'test-key', model='account/vision-model', base_url='https://api.siliconflow.cn/v1/')
        self.assertEqual(post.call_args.args[0], DEFAULT_BASE_URL + '/chat/completions')
        self.assertEqual(post.call_args.kwargs['json']['model'], 'account/vision-model')

    @patch('siliconflow_client.requests.post')
    def test_missing_credentials_do_not_make_a_request(self, post):
        with self.assertRaises(SiliconFlowError) as error:
            call_siliconflow_vl('Prompt', self.image, '')
        self.assertEqual(error.exception.message_key, 'api_key_missing')
        post.assert_not_called()

    @patch('siliconflow_client.requests.post')
    def test_local_image_failure_does_not_make_a_request(self, post):
        with self.assertRaises(SiliconFlowError) as error:
            call_siliconflow_vl('Prompt', self.image.with_name('missing.jpg'), 'test-key')
        self.assertEqual(error.exception.message_key, 'api_image_error')
        post.assert_not_called()

    @patch('siliconflow_client.requests.post')
    def test_http_errors_are_localizable_without_raw_provider_text(self, post):
        post.return_value = Mock(status_code=401, text='Sensitive provider details')
        with self.assertRaises(SiliconFlowError) as error:
            call_siliconflow_vl('Prompt', self.image, 'test-key')
        self.assertEqual(error.exception.message_key, 'api_error')
        self.assertEqual(error.exception.status, 401)
        self.assertNotIn('Sensitive', str(error.exception))

    @patch('siliconflow_client.requests.post')
    def test_network_failures_are_localizable(self, post):
        for failure, key in [(requests.Timeout(), 'api_timeout'), (requests.ConnectionError(), 'api_connection')]:
            with self.subTest(key=key):
                post.side_effect = failure
                with self.assertRaises(SiliconFlowError) as error:
                    call_siliconflow_vl('Prompt', self.image, 'test-key')
                self.assertEqual(error.exception.message_key, key)

    @patch('siliconflow_client.requests.post')
    def test_invalid_or_empty_responses(self, post):
        for payload in [{}, {'choices': []}, {'choices': [{'message': {'content': ''}}]}, {'choices': [{'message': {'content': None}}]}]:
            with self.subTest(payload=payload):
                post.return_value = Mock(status_code=200)
                post.return_value.json.return_value = payload
                with self.assertRaises(SiliconFlowError) as error:
                    call_siliconflow_vl('Prompt', self.image, 'test-key')
                self.assertEqual(error.exception.message_key, 'api_invalid_response')


if __name__ == '__main__':
    unittest.main()

import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

import requests
from urllib3.exceptions import ReadTimeoutError

from siliconflow_client import (
    DEFAULT_BASE_URL,
    DEFAULT_MODEL,
    SiliconFlowError,
    call_siliconflow_vl,
    stream_siliconflow_vl,
)


def frame(content=None, finish_reason=None):
    return 'data: ' + json.dumps(
        {'choices': [{'delta': {'content': content}, 'finish_reason': finish_reason}]},
        ensure_ascii=False,
    )


def response_for(lines, status=200):
    response = Mock(status_code=status)
    response.iter_lines.side_effect = lambda **kwargs: iter(lines)
    return response


class SiliconFlowClientTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.image = Path(self.temp.name) / 'artwork.png'
        self.image.write_bytes(b'example-image-bytes')

    @patch('siliconflow_client.requests.post')
    def test_multimodal_stream_request_contract(self, post):
        response = response_for([
            ': heartbeat', '',
            'data: {"choices": [{"delta": {"role": "assistant"}}]}',
            frame('Debate'), frame(' result', 'stop'),
            'data: {"choices": [], "usage": {"completion_tokens": 2}}',
            'data: [DONE]',
        ])
        post.return_value = response
        self.assertEqual(call_siliconflow_vl('Discuss in English.', self.image, 'test-key'), 'Debate result')
        args, kwargs = post.call_args
        self.assertEqual(args[0], DEFAULT_BASE_URL + '/chat/completions')
        self.assertEqual(kwargs['headers']['Authorization'], 'Bearer test-key')
        self.assertEqual(kwargs['json']['model'], DEFAULT_MODEL)
        self.assertEqual(kwargs['json']['messages'][0]['content'][0]['text'], 'Discuss in English.')
        self.assertTrue(kwargs['json']['messages'][0]['content'][1]['image_url']['url'].startswith('data:image/png;base64,'))
        self.assertTrue(kwargs['json']['stream'])
        self.assertTrue(kwargs['stream'])
        self.assertEqual(kwargs['timeout'], (10, 300))
        response.close.assert_called_once()

    @patch('siliconflow_client.requests.post')
    def test_content_is_yielded_before_the_next_frame_is_read(self, post):
        consumed = []
        def lines():
            yield frame('First')
            consumed.append('next-frame')
            yield frame(' second', 'stop')
            yield 'data: [DONE]'
        response = Mock(status_code=200)
        response.iter_lines.side_effect = lambda **kwargs: lines()
        post.return_value = response
        stream = stream_siliconflow_vl('Prompt', self.image, 'test-key')
        self.assertEqual(next(stream), 'First')
        self.assertEqual(consumed, [])
        self.assertEqual(next(stream), ' second')
        self.assertEqual(consumed, ['next-frame'])
        self.assertEqual(list(stream), [])
        response.close.assert_called_once()

    @patch('siliconflow_client.requests.post')
    def test_utf8_chinese_content(self, post):
        post.return_value = response_for([frame('劳拉：').encode('utf-8'), frame('艺术中的凝视。', 'stop').encode('utf-8'), b'data: [DONE]'])
        self.assertEqual(call_siliconflow_vl('中文', self.image, 'test-key'), '劳拉：艺术中的凝视。')

    @patch('siliconflow_client.requests.post')
    def test_configuration_overrides(self, post):
        post.return_value = response_for([frame('Result', 'stop'), 'data: [DONE]'])
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
        response = response_for([], status=401)
        response.text = 'Sensitive provider details'
        post.return_value = response
        with self.assertRaises(SiliconFlowError) as error:
            call_siliconflow_vl('Prompt', self.image, 'test-key')
        self.assertEqual(error.exception.message_key, 'api_error')
        self.assertEqual(error.exception.status, 401)
        self.assertNotIn('Sensitive', str(error.exception))
        response.close.assert_called_once()

    @patch('siliconflow_client.requests.post')
    def test_initial_network_failures_are_localizable(self, post):
        for failure, key in [(requests.Timeout(), 'api_timeout'), (requests.ConnectionError(), 'api_connection')]:
            with self.subTest(key=key):
                post.side_effect = failure
                with self.assertRaises(SiliconFlowError) as error:
                    call_siliconflow_vl('Prompt', self.image, 'test-key')
                self.assertEqual(error.exception.message_key, key)

    @patch('siliconflow_client.requests.post')
    def test_mid_stream_timeouts_and_connection_failures_close_the_response(self, post):
        failures = [
            (requests.Timeout(), 'api_timeout'),
            (requests.ConnectionError(ReadTimeoutError(None, 'https://api.siliconflow.cn', 'Read timed out')), 'api_timeout'),
            (requests.ConnectionError(), 'api_connection'),
        ]
        for failure, key in failures:
            with self.subTest(key=key, failure=type(failure).__name__):
                def lines():
                    yield frame('Partial answer')
                    raise failure
                response = Mock(status_code=200)
                response.iter_lines.side_effect = lambda **kwargs: lines()
                post.return_value = response
                stream = stream_siliconflow_vl('Prompt', self.image, 'test-key')
                self.assertEqual(next(stream), 'Partial answer')
                with self.assertRaises(SiliconFlowError) as error:
                    list(stream)
                self.assertEqual(error.exception.message_key, key)
                response.close.assert_called_once()

    @patch('siliconflow_client.requests.post')
    def test_malformed_empty_and_provider_error_streams(self, post):
        for lines in [
            ['data: not-json'],
            ['data: {"choices": []}', 'data: [DONE]'],
            [frame('   ', 'stop'), 'data: [DONE]'],
            ['data: {"error": {"message": "provider error"}}'],
            ['data: {"choices": [{"delta": {"content": []}}]}'],
        ]:
            with self.subTest(lines=lines):
                post.return_value = response_for(lines)
                with self.assertRaises(SiliconFlowError) as error:
                    call_siliconflow_vl('Prompt', self.image, 'test-key')
                self.assertEqual(error.exception.message_key, 'api_invalid_response')

    @patch('siliconflow_client.requests.post')
    def test_abrupt_eof_does_not_return_a_partial_answer_as_complete(self, post):
        response = response_for([frame('Partial answer')])
        post.return_value = response
        with self.assertRaises(SiliconFlowError) as error:
            call_siliconflow_vl('Prompt', self.image, 'test-key')
        self.assertEqual(error.exception.message_key, 'api_incomplete_response')
        response.close.assert_called_once()

    @patch('siliconflow_client.requests.post')
    def test_explicit_finish_reason_is_accepted_without_done_marker(self, post):
        post.return_value = response_for([frame('Complete answer', 'stop')])
        self.assertEqual(call_siliconflow_vl('Prompt', self.image, 'test-key'), 'Complete answer')


if __name__ == '__main__':
    unittest.main()

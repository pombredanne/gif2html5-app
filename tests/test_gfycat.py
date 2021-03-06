import unittest

from unittest.mock import patch, Mock

from gif2html5.gfycat import convert_gif


class GfycatTests(unittest.TestCase):

    def setUp(self):
        self.test_gif = 'http://media.giphy.com/media/PTFRmGOgiPUS4/giphy.gif'
        self.big_gif = 'http://img.pandawhale.com/post-58020-Big-Hero-6-Baymax-hug-there-th-NwXV.gif'

    def test_convert_gif(self):
        response = convert_gif(self.test_gif)

        expected_mp4 = 'http://zippy.gfycat.com/GreatAgitatedCaimanlizard.mp4'
        expected_webm = 'http://zippy.gfycat.com/GreatAgitatedCaimanlizard.webm'
        self.assertEquals(expected_mp4, response['mp4'])
        self.assertEquals(expected_webm, response['webm'])

    def test_convert_bad_url(self):
        response = convert_gif('non gif')
        self.assertEquals(None, response)

    def test_large_gif(self):
        response = convert_gif(self.big_gif)

        expected_mp4 = 'http://zippy.gfycat.com/InfamousVillainousDore.mp4'
        expected_webm = 'http://zippy.gfycat.com/InfamousVillainousDore.webm'
        self.assertEquals(expected_mp4, response['mp4'])
        self.assertEquals(expected_webm, response['webm'])

    @patch('requests.get')
    def test_data_not_returned_correctly(self, mock_request):
        mock_request.json.return_value = {}

        response = convert_gif(self.test_gif)
        self.assertEquals(None, response)

    @patch('requests.get')
    def test_urls_are_none(self, mock_request):
        returned_json = {'mp4Url': None, 'webmUrl': None}
        mock_request.return_value = mock_response = Mock()
        mock_response.json.return_value = returned_json

        response = convert_gif(self.test_gif)
        self.assertEquals(response, None)

    @patch('requests.get')
    def test_one_of_the_url_is_none(self, mock_request):
        returned_json = {'mp4Url': None, 'webmUrl': 'url'}
        mock_request.return_value = mock_response = Mock()
        mock_response.json.return_value = returned_json

        response = convert_gif(self.test_gif)
        self.assertEquals(response, None)

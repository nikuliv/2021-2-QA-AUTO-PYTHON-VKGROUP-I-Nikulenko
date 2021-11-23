import pytest
from base import ApiBase
from api.client import ResponseStatusCodeException
from utils.name_gen import create_segment_name


class TestCampaign(ApiBase):

    @pytest.mark.API
    def test_create_campaign(self, api_client):
        campaign_id = api_client.post_campaign_create(name='test_campaign')
        assert api_client.get_campaign(campaign_id) == 200
        api_client.post_campaign_delete(campaign_id)


class TestSegment(ApiBase):

    @pytest.mark.API
    def test_create_segment(self, api_client):
        segment_name = create_segment_name()
        segment_id = api_client.post_segment_create(name=segment_name)
        assert api_client.get_segment(segment_id) == 200
        api_client.delete_segment(segment_id)

    @pytest.mark.API
    def test_delete_segment(self, api_client):
        segment_name = create_segment_name()
        segment_id = api_client.post_segment_create(name=segment_name)
        api_client.delete_segment(segment_id)
        with pytest.raises(ResponseStatusCodeException):
            assert api_client.get_segment(segment_id)
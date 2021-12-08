import pytest
import utils.log_analysis as log_analysis
from models.model import RequestsCount, NumberOfRequestsByType, MostFrequentRequests,\
                         Largest4xxRequests, UsersWith5xxRequests
from test_sql.base import BaseMySQL


class TestRequestsCount(BaseMySQL):

    def prepare(self, log_path):
        req_count = log_analysis.count_requests(log_path)
        self.builder.create_requests_count(req_count)

    def test_requests_count(self):
        assert len(self.client.session.query(RequestsCount).all()) == 1


class TestRequestTypesCount(BaseMySQL):

    def prepare(self, log_path):
        req_types_count = log_analysis.count_request_types(log_path)
        for req_type in req_types_count:
            self.builder.create_request_type_count(req_type=req_type[0], count=req_type[1])
        self.added_lines_count = len(req_types_count)

    def test_request_types_count(self):
        req_types_count = self.client.session.query(NumberOfRequestsByType).all()
        assert len(req_types_count) == self.added_lines_count


class TestMostFrequentRequests(BaseMySQL):

    def prepare(self, log_path):
        most_freq_reqs = log_analysis.most_frequent_requests(log_path)
        for most_freq_req in most_freq_reqs:
            self.builder.create_most_frequent_request(url=most_freq_req[0], count=most_freq_req[1])
        self.added_lines_count = len(most_freq_reqs)

    def test_most_frequent_requests(self):
        most_freq_reqs = self.client.session.query(MostFrequentRequests).all()
        assert len(most_freq_reqs) == self.added_lines_count


class TestLargest4xxRequests(BaseMySQL):

    def prepare(self, log_path):
        largest_4xx_reqs = log_analysis.largest_4xx_requests(log_path)
        for req in largest_4xx_reqs:
            self.builder.create_largest_4xx_request(url=req[0], size=req[1], ip=req[2])
        self.added_lines_count = len(largest_4xx_reqs)

    def test_largest_4xx_requests(self):
        largest_4xx_reqs = self.client.session.query(Largest4xxRequests).all()
        assert len(largest_4xx_reqs) == self.added_lines_count


class TestUsersWith5xxRequests(BaseMySQL):

    def prepare(self, log_path):
        users_with_5xx_reqs = log_analysis.users_with_5xx_requests(log_path)
        for user in users_with_5xx_reqs:
            self.builder.create_user_with_5xx_requests(ip=user[0], requests_number=user[1])
        self.added_lines_count = len(users_with_5xx_reqs)

    def test_users_with_5xx_requests(self):
        users_with_5xx_reqs = self.client.session.query(UsersWith5xxRequests).all()
        assert len(users_with_5xx_reqs) == self.added_lines_count

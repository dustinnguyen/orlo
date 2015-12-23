from __future__ import print_function
import unittest
from tests.test_contract import OrloTest

__author__ = 'alforbes'


class OrloStatsUrlTest(OrloTest):
    def test_info_root(self):
        """
        Test /info returns 200
        """
        response = self.client.get('/info')
        self.assert200(response)
        print(response.json)

    def test_info_users(self):
        """
        Test /info/users returns 200
        """
        self._create_release(user='userOne')
        response = self.client.get('/info/users')
        self.assert200(response)
        self.assertIn('userOne', response.json)

    def test_info_users_with_platform(self):
        """
        Test /info/<platform> returns 200
        """
        self._create_release(user='userOne', platforms=['platformOne'])
        response = self.client.get('/info/users/platformOne')
        self.assert200(response)
        self.assertIn('userOne', response.json)

    def test_info_platforms(self):
        """
        Test /info/platforms returns 200
        """
        self._create_release(platforms=['platformOne'])
        response = self.client.get('/info/platforms')
        self.assert200(response)
        self.assertIn('platformOne', response.json)

    def test_info_packages(self):
        """
        Test /info/packages
        """

        self._create_finished_release()
        response = self.client.get('/info/packages')
        self.assert200(response)
        self.assertIn('test-package', response.json)

    def test_info_package_list(self):
        """
        Test /info/package_list
        """

        self._create_finished_release()
        response = self.client.get('/info/package_list')
        self.assert200(response)
        self.assertIn('test-package', response.json['packages'])

    def test_info_package_versions(self):
        """
        Test /info/packages returns 200
        """
        self._create_finished_release()
        response = self.client.get('/info/package_versions')
        self.assert200(response)
        self.assertIn('test-package', response.json)

    def test_info_package_versions_with_platform(self):
        """
        Test /info/packages returns 200
        """
        self._create_finished_release()
        response = self.client.get('/info/package_versions/test_platform')
        self.assert200(response)
        self.assertIn('test-package', response.json)

    def test_info_package_versions_with_platform_negative(self):
        """
        Test /info/packages returns 200
        """
        self._create_finished_release()
        response = self.client.get('/info/package_versions/non-existant-platform')
        self.assert200(response)
        self.assertNotIn('test-package', response.json)

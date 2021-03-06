from __future__ import print_function
from tests import OrloLiveTest, OrloTest, ConfigChange
from orlo.deploy import BaseDeploy, HttpDeploy, ShellDeploy
from orlo.orm import db, Release, Package
from orlo.util import append_or_create_platforms
import unittest

__author__ = 'alforbes'


class DeployTest(OrloLiveTest):
    """
    Test the Deploy class
    """
    CLASS = BaseDeploy

    def setUp(self):
        # super(DeployTest, self).setUp()
        db.create_all()
        rid = self._create_release()
        pid = self._create_package(rid)
        self.release = db.session.query(Release).first()

    @staticmethod
    def _create_release(user='testuser',
                        team='test team',
                        platforms=None,
                        references=None,
                        success=True):
        """
        Create a release using internal methods

        :param user:
        :param team:
        :param platforms:
        :param references:
        :return:
        """

        if not platforms:
            platforms = ['test_platform']
        if type(platforms) is not list:
            raise AssertionError("Platforms parameter must be list")
        if not references:
            references = ['TestTicket-123']

        db_platforms = append_or_create_platforms(platforms)

        r = Release(
            platforms=db_platforms,
            user=user,
            references=references,
            team=team,
        )
        db.session.add(r)
        db.session.commit()

        return r.id

    @staticmethod
    def _create_package(release_id,
                        name='test-package',
                        version='1.2.3',
                        diff_url=None,
                        rollback=False,
                        ):
        """
        Create a package using internal methods

        :param release_id:
        :param name:
        :param version:
        :param diff_url:
        :param rollback:
        :return:
        """
        p = Package(
            release_id=release_id,
            name=name,
            version=version,
            diff_url=diff_url,
            rollback=rollback,
        )
        db.session.add(p)
        db.session.commit()

        return p.id

    def test_init(self):
        """
        Test that we can instantiate the class
        """
        o = self.CLASS(self.release)
        self.assertIsInstance(o, BaseDeploy)


class TestBaseDeploy(DeployTest):
    def test_not_implemented(self):
        """
        Base Deploy class should raise NotImplementedError on start
        """
        o = self.CLASS(self.release)
        with self.assertRaises(NotImplementedError):
            o.start()


class TestHttpDeploy(DeployTest):
    CLASS = HttpDeploy

    def test_start(self):
        """
        Test that start emits an http call
        """
        pass

    def test_kill(self):
        """
        Test that kill emits an http call
        """
        pass


class TestShellDeploy(DeployTest):
    CLASS = ShellDeploy

    def test_start(self):
        """
        Test that start emits a shell command
        :return:
        """
        with ConfigChange('deploy', 'timeout', '3'), \
                ConfigChange('deploy_shell', 'command_path', '/bin/true'):

            deploy = ShellDeploy(self.release)
            deploy.server_url = self.get_server_url()
            deploy.start()

    def test_kill(self):
        """
        Test that kill emits a shell command
        :return:
        """
        pass

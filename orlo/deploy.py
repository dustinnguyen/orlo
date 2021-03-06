from __future__ import print_function
import json
import subprocess
from threading import Timer
from orlo.config import config
from orlo.exceptions import OrloError


__author__ = 'alforbes'


# Stolen from http://stackoverflow.com/questions/1191374
def run(args, env, in_data, timeout_sec=3600):
    """
    Run a command in a separate thread

    :param env: Dict of environment variables
    :param in_data: String to pass to stdin
    :param args: List of arguments
    :param timeout_sec: Timeout in seconds, 1 hour by default
    :return:
    """
    proc = subprocess.Popen(
        args,
        env=env,
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    timer = Timer(timeout_sec, proc.kill)
    out = err = " "
    try:
        timer.start()
        out, err = proc.communicate(in_data)
    finally:
        timer.cancel()
        print("Out:\n{}".format(out))
        print("Err:\n{}".format(err))

    if proc.returncode is not 0:
        raise OrloError("Subprocess exited with code {}".format(
            proc.returncode
        ))
    print("end run")


class BaseDeploy(object):
    """
    A Deploy task

    Deploy tasks are simpler than releases, as they consist of just packages
    and versions. The backend deployer is responsible for creating Orlo Releases
    via the REST API.

    Integrations can either sub-class Deploy and override the start method and
    (optionally) the kill method, or use the pre-built shell and http
    integrations.
    """

    def __init__(self, release):
        """
        Perform a release
        """
        self.release = release
        self.server_url = config.get('main', 'base_url')

    def start(self):
        """
        Start the deployment
        """
        raise NotImplementedError("Please override the start method")

    def kill(self):
        """
        Kill a deployment in progress
        """
        raise NotImplementedError("Please override the kill method")


class HttpDeploy(BaseDeploy):
    """
    A http-based Deployment
    """

    def __init__(self, release):
        super(HttpDeploy, self).__init__(release)

    def start(self):
        pass

    def kill(self):
        pass


class ShellDeploy(BaseDeploy):
    """
    Deployment by shell command

    meta {} => stdin
    deployer pkg1=1
    capture stdout,
    """

    def __init__(self, release):
        super(ShellDeploy, self).__init__(release)
        self.pid = None

    def start(self):
        """
        Start the deploy
        """
        args = [config.get('deploy_shell', 'command_path')]
        for p in self.release.packages:
            args.append("{}={}".format(p.name, p.version))
        print("Args: {}".format(str(args)))

        env = {
            'ORLO_URL': self.server_url,
            'ORLO_RELEASE': str(self.release.id)
        }
        for key, value in self.release.to_dict().items():
            my_key = "ORLO_" + key.upper()
            env[my_key] = str(value)

        print("Env: {}".format(json.dumps(env)))

        metadata = {}
        for m in self.release.metadata:
            metadata.update(m.to_dict())
        in_data = json.dumps(metadata)

        run(args, env, in_data, timeout_sec=config.getint('deploy', 'timeout'))

    def kill(self):
        """
        Kill a deploy in progress
        """
        raise NotImplementedError

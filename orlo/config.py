from __future__ import print_function
import ConfigParser
import os
__author__ = 'alforbes'

config = ConfigParser.ConfigParser()

config.add_section('main')
config.set('main', 'debug_mode', 'true')
config.set('main', 'propagate_exceptions', 'true')
config.set('main', 'time_format', '%Y-%m-%dT%H:%M:%SZ')
config.set('main', 'time_zone', 'UTC')
config.set('main', 'strict_slashes', 'false')
config.set('main', 'base_url', 'http://localhost:8080')


config.add_section('security')
config.set('security', 'enabled', 'false')
config.set('security', 'passwd_file', os.path.dirname(__file__) + '/../etc/passwd')
config.set('security', 'secret_key', 'change_me')
# NOTE: orlo.__init__ checks that secret_key is not "change_me" when security is enabled
# Do not change the default here without updating __init__ as well.
config.set('security', 'token_ttl', '3600')
config.set('security', 'ldap_server', 'localhost.localdomain')
config.set('security', 'ldap_port', '389')
config.set('security', 'user_base_dn', 'ou=people,ou=example,o=test')

config.add_section('db')
config.set('db', 'uri', 'postgres://orlo:password@localhost:5432/orlo')
config.set('db', 'echo_queries', 'false')

config.add_section('logging')
config.set('logging', 'debug', 'false')
config.set('logging', 'file', 'disabled')

config.read('/etc/orlo/orlo.ini')

config.add_section('deploy')
config.set('deploy', 'timeout', '3600')  # How long to timeout external deployer calls

config.add_section('deploy_shell')
config.set('deploy_shell', 'command_path', os.path.dirname(os.path.abspath(__file__)) +
           '/../deployer.py')


from utils import YumUtils, ShellUtils
from common import Common

class Provision(object):

    def __init__(self, repolist):
        self.repolist = repolist
        self.yum = YumUtils()
        self.shell = ShellUtils()
        self.com = Common()

    def provision(self):
        # run instack
        self.com.set_user('stack', 'stack')
        self.com.set_repo(['http://trunk.rdoproject.org/centos7/delorean-deps.repo',])
        self._install_pkg(['epel-release', 'instack-undercloud'])
        self._deploy_instack()
        return self._get_instack_ip()

    def _install_pkg(self, pkgs):
        for pkg in pkgs:
            self.yum.yum_install(pkg)

    def _deploy_instack(self):
        return self.shell._exec_cmd('instack-virt-setup')

    def _get_instack_ip(self):
        return self.shell._exec_cmd("arp -n | grep virbr0 | awk '{print $5}")

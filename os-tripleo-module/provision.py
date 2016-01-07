from utils import YumUtils, ShellUtils
from common import Common
import libuser

class Provision(object):

    repo_path = "/etc/yum.repos.d/"

    def __init__(self, repolist):
        self.repolist = repolist
        yum = YumUtils()
        shell = ShellUtils()
        com = Common()

    def provision(self):
        # run instack
        self.com.set_user('stack', 'stack')
        self.com.set_repo(['http://trunk.rdoproject.org/centos7/delorean-deps.repo',])
        self._install_pkg(['epel-release', 'instack-undercloud'])
        self._deploy_instack()

    def _install_pkg(self, pkgs):
        for pkg in pkgs:
            yum.yum_install(pkg)

    def _deploy_instack(self):
        return shell._exec_cmd('instack-virt-setup')

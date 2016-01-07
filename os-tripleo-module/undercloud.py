from utils import YumUtils, ShellUtils
from common import Common
import libuser

class Undercloud(object):

    repo_path = "/etc/yum.repos.d/"

    def __init__(self, repolist):
        self.repolist = repolist
        self.yum = YumUtils()
        self.shell = ShellUtils()
        self.com = Common()

    def undercloud(self):
        self._install_pkg(['epel-release', 'yum-plugin-priorities', 'python-tripleoclient',])
        self.com.set_repo(['http://trunk.rdoproject.org/centos7/delorean-deps.repo',])

    def _install_pkg(self, pkgs):
        for pkg in pkgs:
            self.yum.yum_install(pkg)

    def _deploy_undercloud(self):
        return self.shell._exec_cmd('openstack undercloud install')

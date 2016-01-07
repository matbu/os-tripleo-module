import yum


class YumUtils(object):

    yb = None

    def __init__(self) :
        pass

    def yum_install(self, pkg):
        """ install package with the given package """
        for (package, matched_value) in self._yum_manage(pkg) :
            if package.name == pkg :
                self.yb.install(package)
                self.yb.buildTransaction()
                self.yb.processTransaction()

    def yum_remove(self, pkg):
        """ remove package """
        for (package, matched_value) in self._yum_manage(pkg) :
            if package.name == pkg :
                self.yb.remove(package)
                self.yb.buildTransaction()
                self.yb.processTransaction()

    def yum_update(self, pkg):
        """ update package """
        for (package, matched_value) in self._yum_manage(pkg) :
            if package.name == pkg :
                self.yb.update(package)
                self.yb.buildTransaction()
                self.yb.processTransaction()

    def _yum_manage(self, pkg, list='name'):
        """ manage yum packages """
        self.yb = yum.YumBase()
        searchlist=['name']
        arg=[pkg]
        return self.yb.searchGenerator(searchlist,arg)

class ShellUtils(object):

    def __init__(self):
        pass

    def _exec_shell_cmd(self, cmd):
        """ execute shell command """
        shell = subprocess.Popen(cmd,
                                    shell=True)
        return shell.wait()

    def _exec_cmd(self, cmd):
        """ exec command without shell """
        process = subprocess.Popen(cmd.split(), stdout=subprocess.PIPE)
        response = process.communicate()[0]
        return response

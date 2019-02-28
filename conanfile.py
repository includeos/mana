from conans import ConanFile,tools,CMake

class ManaConan(ConanFile):
    settings= "os","arch","build_type","compiler"
    name = "mana"
    license = 'Apache-2.0'
    description = 'Run your application with zero overhead'
    generators = 'cmake'
    
    url = "http://www.includeos.org/"

    default_user="includeos"
    default_channel="test"
    
    no_copy_source=True

    def requirements(self):
        self.requires("includeos/0.14.0@{}/{}".format(self.user,self.channel))

    def source(self):
        #TODO make the branch into a version tag ?
        repo = tools.Git(folder="mana")
        repo.clone("https://github.com/includeos/mana.git",branch="master")

    def _arch(self):
        return {
            "x86":"i686",
            "x86_64":"x86_64",
            "armv8" : "aarch64"
        }.get(str(self.settings.arch))
    def _cmake_configure(self):
        cmake = CMake(self)
        cmake.definitions['ARCH']=self._arch()
        cmake.configure(source_folder=self.source_folder+"/mana")
        return cmake

    def build(self):
        cmake = self._cmake_configure()
        cmake.build()

    def package(self):
        cmake = self._cmake_configure()
        cmake.install()

    def package_info(self):
        self.cpp_info.libs=['mana']

    def deploy(self):
        #the first is for the editable version
        self.copy("*.a",dst="lib",src="build/lib")
        #TODO fix this in mana cmake..
        self.copy("*.a",dst="lib",src="lib")
        self.copy("*",dst="include",src="include")

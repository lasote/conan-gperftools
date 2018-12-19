from conans import ConanFile, CMake, tools, AutoToolsBuildEnvironment
import os


class gperftoolsConan(ConanFile):
    name = "gperftools"
    version = "2.7"
    license = "https://github.com/gperftools/gperftools/blob/master/COPYING"
    url = "https://github.com/lasote/conan-gperftools"
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"
    
    @property
    def zipped_folder(self):
        return "gperftools-%s" % self.version
    
    def configure(self):
        if self.settings.os != "Linux":
            raise Exception("Only linux compatible")
    
    def source(self):
       tools.download("https://github.com/gperftools/gperftools/releases/download/gperftools-%s/gperftools-%s.tar.gz" % (self.version, self.version), "gperftools.tar.gz")
       tools.unzip("gperftools.tar.gz")

    def build(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            env = AutoToolsBuildEnvironment(self)
            env.fpic = True
#             if self.settings.os == "Macos":
#                 old_str = '-install_name $libdir/$SHAREDLIBM'
#                 new_str = '-install_name $SHAREDLIBM'
#                 replace_in_file("./%s/configure" % self.ZIP_FOLDER_NAME, old_str, new_str)
#    
            os.chdir(self.zipped_folder)
            with tools.environment_append(env.vars):
                self.run("./configure --with-pic")
                self.run("make")

    def package(self):
        self.copy("*.h", dst="include", src="%s/src" % self.zipped_folder, keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("COPYING", src=self.zipped_folder, dst="", keep_path=False)
           
        if self.options.shared:
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.so*", dst="lib", keep_path=False)
        else:
            self.copy("*.a", dst="lib", keep_path=False)


    def package_info(self):
        self.cpp_info.libs = ["tcmalloc", "profiler"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")

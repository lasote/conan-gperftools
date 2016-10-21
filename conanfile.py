from conans import ConanFile, CMake, tools, ConfigureEnvironment
import os


class gperftoolsConan(ConanFile):
    name = "gperftools"
    version = "2.5"
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
        
       tools.download("https://github.com/gperftools/gperftools/releases/download/gperftools-2.5/gperftools-%s.tar.gz" % self.version, "gperftools.tar.gz")
       tools.unzip("gperftools.tar.gz")

    def build(self):
        if self.settings.os == "Linux" or self.settings.os == "Macos":
            env = ConfigureEnvironment(self.deps_cpp_info, self.settings)
            env_line = env.command_line_env.replace('CFLAGS="', 'CFLAGS="-fPIC ')
#             if self.settings.os == "Macos":
#                 old_str = '-install_name $libdir/$SHAREDLIBM'
#                 new_str = '-install_name $SHAREDLIBM'
#                 replace_in_file("./%s/configure" % self.ZIP_FOLDER_NAME, old_str, new_str)
#
            self.run("cd %s && %s ./configure" % (self.zipped_folder, env_line))          
            self.run("cd %s && %s make" % (self.zipped_folder, env_line))

    def package(self):
        self.copy("*.h", dst="include", src="%s/src" % self.zipped_folder, keep_path=True)
        self.copy("*.lib", dst="lib", keep_path=False)
        self.copy("COPYING", src=self.zipped_folder, dst="", keep_path=False)
           
        if self.options.shared:
            self.copy("*.dll", dst="bin", keep_path=False)
            self.copy("*.so", dst="lib", keep_path=False)
        else:
            self.copy("*.a", dst="lib", keep_path=False)


    def package_info(self):
        self.cpp_info.libs = ["tcmalloc", "profiler"]
        if self.settings.os == "Linux":
            self.cpp_info.libs.append("pthread")

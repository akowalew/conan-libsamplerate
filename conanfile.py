from conans import ConanFile, CMake, tools

class LibsamplerateConan(ConanFile):
    name = "libsamplerate"
    version = "0.1.9"
    license = "BSD 2-Clause Simplified License"
    author = "Adam Kowalewski ram.techen@gmail.com"
    url = "<Package recipe repository url here, for issues about the package>"
    description = "libsamplerate (also known as Secret Rabbit Code) is a library for performing sample rate conversion of audio data."
    topics = ("<Put some tag here>", "<here>", "<and here>")
    settings = "os", "compiler", "build_type", "arch"
    options = {"shared": [True, False]}
    default_options = "shared=False"
    generators = "cmake"

    def source(self):
        self.run("git clone https://github.com/erikd/libsamplerate.git")
        # This small hack might be useful to guarantee proper /MT /MD linkage
        # in MSVC if the packaged project doesn't have variables to set it
        # properly
        tools.replace_in_file("libsamplerate/CMakeLists.txt", "project(libsamplerate VERSION 0.1.9 LANGUAGES C)",
                              '''project(libsamplerate VERSION 0.1.9 LANGUAGES C)
include(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
conan_basic_setup()''')

    def build(self):
        cmake = CMake(self)
        cmake.configure(source_folder="libsamplerate")
        cmake.build()

    def package(self):
        self.copy("*.h", dst="include", src="libsamplerate/src")
        self.copy("*libsamplerate.lib", dst="lib", keep_path=False)
        self.copy("*.dll", dst="bin", keep_path=False)
        self.copy("*.so", dst="lib", keep_path=False)
        self.copy("*.dylib", dst="lib", keep_path=False)
        self.copy("*.a", dst="lib", keep_path=False)

    def package_info(self):
        self.cpp_info.libs = ["samplerate"]


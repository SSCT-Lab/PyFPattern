def write_version_info(filename, git_version):
    'Write a c file that defines the version functions.\n\n  Args:\n    filename: filename to write to.\n    git_version: the result of a git describe.\n  '
    if ((b'"' in git_version) or (b'\\' in git_version)):
        git_version = 'git_version_is_invalid'
    contents = ('/*  Generated by gen_git_source.py  */\n#include <string>\nconst char* tf_git_version() {return "%s";}\nconst char* tf_compiler_version() {\n#ifdef _MSC_VER\n#define STRINGIFY(x) #x\n#define TOSTRING(x) STRINGIFY(x)\n  return "MSVC " TOSTRING(_MSC_FULL_VER);\n#else\n  return __VERSION__;\n#endif\n}\nconst int tf_cxx11_abi_flag() {\n#ifdef _GLIBCXX_USE_CXX11_ABI\n  return _GLIBCXX_USE_CXX11_ABI;\n#else\n  return 0;\n#endif\n}\nconst int tf_monolithic_build() {\n#ifdef TENSORFLOW_MONOLITHIC_BUILD\n  return 1;\n#else\n  return 0;\n#endif\n}\n' % git_version.decode('utf-8'))
    open(filename, 'w').write(contents)
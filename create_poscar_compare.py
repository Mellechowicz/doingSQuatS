import os
import shutil
from setuptools import setup
from setuptools.command.install import install
import subprocess

import git

INSTALLPREFIX=os.getcwd()+'/.local'
subprocess.check_call("export CPLUS_INCLUDE_PATH=${CPLUS_INCLUDE_PATH}:"+INSTALLPREFIX+"/lib", shell=True)
if "CPLUS_INCLUDE_PATH" in os.environ:
    os.environ["CPLUS_INCLUDE_PATH"] = os.environ["CPLUS_INCLUDE_PATH"]+':'+INSTALLPREFIX+'/include'
else:
    os.environ["CPLUS_INCLUDE_PATH"] = INSTALLPREFIX+'/include'

my_repos = {
        'spglib': "https://github.com/spglib/spglib",
        'XtalComp': "git@github.com:Mellechowicz/XtalComp.git"
        }

class Progress(git.remote.RemoteProgress):
    def update(self,*args,**kwargs):
        print('.',end='',flush=True)

def compile_and_install_software(repos):
    """Used the subprocess module to compile/install the C software."""
    for repo in repos:
        print('Downloading '+repo)
        try:
            git.Repo.clone_from(repos[repo],repo,progress=Progress())
        except git.exc.GitCommandError as err:
            if not os.path.isdir(repo):
                raise err
        print('')
        src_path = './'+repo

        subprocess.check_call("[ -d _build ] && rm -fr _build/* || mkdir _build",
                                                      cwd=src_path,           shell=True)
        subprocess.check_call("cmake ../ --install-prefix "+INSTALLPREFIX,
                                                      cwd=src_path+'/_build', shell=True)
        subprocess.check_call("cmake --build   .",    cwd=src_path+'/_build', shell=True)
        subprocess.check_call("cmake --install . ",   cwd=src_path+'/_build', shell=True)

        print("Deleting "+repo)
        shutil.rmtree(repo)
    subprocess.check_call("make",                  cwd=os.getcwd()+'/poscarComp',shell=True)
    subprocess.check_call("cp poscar_compare ../", cwd=os.getcwd()+'/poscarComp',shell=True)
    subprocess.check_call("make clean",            cwd=os.getcwd()+'/poscarComp',shell=True)

compile_and_install_software(my_repos)


from distutils.core import setup
import py2exe

setup(name="Tetris",
      version="1.0",
      description="Juego de tetris estilo retropy",
      author="Walterio Fuentes",
      author_email="walteriofuentes@gmail.com",
      url="---",
      license="libre",
      scripts=["main.py"],
      console = ["main.py"],
      options = {"py2exe": {"bundle_files": 1}},
      zipfile = None,
)
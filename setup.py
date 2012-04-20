from distutils.core import setup
import conversationbot


setup(name = "conversationbot",
      author = "Samuel Andersson",
      url = "http://github.com/trew/conversationbot",
      version = conversationbot.__version__,
      packages = [
          'conversationbot',
      ],
      install_requires = [
          'Twisted>=12.0.0',
      ]
)

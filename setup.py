from setuptools import setup

setup(
  name = 'pylods-msgpack',
  packages = ['pylodsmsgpack'], # this must be the same as the name above
  version = '0.1.0',
  description = 'Msgpack extension for pylods package',
  author = 'Salim Malakouti',
  author_email = 'salim.malakouti@gmail.com',
  license = 'MIT',
  url = 'https://github.com/salimm/pylods-msgpack', # use the URL to the github repo
  download_url = 'http://github.com/salimm/pylods-msgpack/archive/0.1.0.tar.gz', # I'll explain this in a second
  keywords = ['python','serialization','deserialization','paser','json','object oriented','fast','extendable','type based','jackson json', 'msgpack', 'umsgpack'], # arbitrary keywords
  classifiers = ['Programming Language :: Python'],
  install_requires=['pylods','msgpackstream', 'umsgpack'],
)

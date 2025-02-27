import toml

from mofa.utils.files.write import write_file

info = { "agent_name": "CountryInfoAgent", "module_name": "country_info"}
data = toml.load('/Users/chenzi/project/zcbc/mofa/python/examples/intelligent_agent_creation/CountryInfoAgent/pyproject.toml')
data['tool']['poetry']['name'] = info.get('agent_name')
data['tool']['poetry']['packages'][0]['include'] = info.get('module_name')
data['tool']['poetry']['scripts'] = {f"{info.get('agent_name')}": f"{info.get('module_name')}.main:main"}

write_file(data=data, file_path='/Users/chenzi/project/zcbc/mofa/python/examples/intelligent_agent_creation/CountryInfoAgent/pyproject.toml')
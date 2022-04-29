import configparser

config_file = configparser.ConfigParser()

config_file.add_section('Locale')
config_file.set('Locale', 'State', 'Michigan')
config_file.set('Locale', 'County', 'Washtenaw')
config_file.set('Locale', 'City', 'Ann Arbor')

with open('config.ini', 'w') as f:
    config_file.write(f)
    f.flush()

print("Config file 'config.ini' created.")

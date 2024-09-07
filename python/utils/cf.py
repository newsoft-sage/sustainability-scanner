import glob
from cfn_tools import load_yaml

def count_resources(file):
  with open(file) as f:
      raw = f.read()
      cf = load_yaml(raw)
      return len(cf['Resources'])

if __name__ == "__main__":
    for file in glob.glob(f'examples/*.yaml'):
      print(file)
      print(count_resources(file))
    for file in glob.glob(f'examples/*.template'):
      print(file)
      print(count_resources(file))
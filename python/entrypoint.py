#!/usr/bin/python
import sys
import glob
import subprocess
import json
import argparse
from pathlib import Path
from tabulate import tabulate

parser = argparse.ArgumentParser(
                    prog='NewsoftSage susscanner',
                    description='NewsoftSage wrapper around awslabs sustainability-scanner')

parser.add_argument('-d', '--templates-dir')      
parser.add_argument('-x', '--extensions', nargs='*', default=['template', 'yaml'])
parser.add_argument('-o', '--output-dir', default='/output/')

args = parser.parse_args()

files = []
for extension in args.extensions:
  files.extend(glob.glob(f'{args.templates_dir}/*.{extension}'))
# print(files)
outputs = []
for file in files:
  completed_process = subprocess.run(f'susscanner {file}', shell=True, capture_output=True)
  # it returns a byte type so convert it to string
  str_output = completed_process.stdout.decode('utf-8')
  filename = Path(file).stem
  output = json.loads(str_output)
  outputs.append(output)
  output_file = f'{args.output_dir}/{filename}_report.json' 
  with open(output_file, 'w', encoding='utf-8') as f:
      json.dump(output, f, ensure_ascii=False, indent=4)

  # json.dump()
  # print out our list of windows
  # for x in range(len(output)):
  #     print (output[x])
# print(outputs)
table = [['Score', 'Template File']]
for report in outputs:
  filename = report['file']
  score = report['sustainability_score']
  table.extend([score, filename])
  # print(f'{score} \t {filename}')
# table = [[1, 2222, 30, 500], [4, 55, 6777, 1]]
print(tabulate(table, headers='firstrow', tablefmt='fancy_grid'))

#!/usr/bin/python
import sys
import glob
import subprocess
import json
import argparse
import time
from pathlib import Path
from tabulate import tabulate
from report import build_report

parser = argparse.ArgumentParser(
                    prog='NewsoftSage susscanner',
                    description='NewsoftSage wrapper around awslabs sustainability-scanner')

parser.add_argument('-d', '--templates-dir')      
parser.add_argument('-x', '--extensions', nargs='*', default=['template', 'yaml'])
parser.add_argument('-o', '--output-dir', default='/output')
parser.add_argument('-r', '--junit-report', required=False)

args = parser.parse_args()
files = []
times = {}
times['start_time'] = time.perf_counter()
for extension in args.extensions:
  files.extend(glob.glob(f'{args.templates_dir}/*.{extension}'))
table = []
outputs = []
for file in files:
  filename = Path(file).stem
  report_file = f'{filename}_report.json'
  times[f'{report_file}_start_time'] = time.perf_counter()
  completed_process = subprocess.run(f'susscanner {file}', shell=True, capture_output=True)
  # it returns a byte type so convert it to string
  str_output = completed_process.stdout.decode('utf-8')
  print(f'str {str_output}')
  output = json.loads(str_output)
  outputs.append(output)
  output_file = f'{args.output_dir}/{report_file}' 
  with open(output_file, 'w', encoding='utf-8') as f:
      json.dump(output, f, ensure_ascii=False, indent=4)
  filename = output['file']
  score = output['sustainability_score']
  table.append([score, filename, output_file])
  times[f'{report_file}_end_time'] = time.perf_counter()

table.sort(key=lambda x: x[0])
table.reverse()
print(tabulate(table, headers=['Score', 'Template File', 'Report'], tablefmt='fancy_grid'))
times['end_time'] = time.perf_counter()
if args.junit_report:
   with open(args.junit_report, 'w', encoding='utf-8') as f:
      f.write(build_report(args.output_dir, times))
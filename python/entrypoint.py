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
from utils.cf import count_resources


def entrypoint(stub=None):
  parser = argparse.ArgumentParser(
                      prog='NewsoftSage susscanner',
                      description='NewsoftSage wrapper around awslabs sustainability-scanner')

  parser.add_argument('-d', '--templates-dir')      
  parser.add_argument('-x', '--extensions', nargs='*', default=['template', 'yaml'])
  parser.add_argument('-o', '--output-dir', default='/output')
  parser.add_argument('-r', '--junit-report', required=False)

  args = parser.parse_args()
  files = []
  metadata = {}
  metadata['start_time'] = time.perf_counter()
  for extension in args.extensions:
    files.extend(glob.glob(f'{args.templates_dir}/*.{extension}'))
  table = []
  outputs = []
  for file in files:
    filename = Path(file).stem
    report_file = f'{filename}_report'
    metadata[f'{report_file}_resource_count'] = count_resources(file)
    metadata[f'{report_file}_start_time'] = time.perf_counter()
    cmd = f'susscanner {file}'
    output = ''
    if stub:
       output = stub
       output['file'] = filename
    else:
      completed_process = subprocess.run(cmd, shell=True, capture_output=True)
      # it returns a byte type so convert it to string
      str_output = completed_process.stdout.decode('utf-8')
      print(f'str {str_output}')
      output = json.loads(str_output)
    outputs.append(output)
    output_file = f'{args.output_dir}/{report_file}.json' 
    with open(output_file, 'w', encoding='utf-8') as f:
        json.dump(output, f, ensure_ascii=False, indent=4)
    filename = output['file']
    score = output['sustainability_score']
    table.append([score, filename, output_file])
    metadata[f'{report_file}_end_time'] = time.perf_counter()

  table.sort(key=lambda x: x[0])
  table.reverse()
  print(tabulate(table, headers=['Score', 'Template File', 'Report'], tablefmt='fancy_grid'))
  metadata['end_time'] = time.perf_counter()
  if args.junit_report:
    print(metadata)
    with open(args.junit_report, 'w', encoding='utf-8') as f:
        report = build_report(args.output_dir, metadata) 
        print(report)
        f.write(report)

if __name__ == "__main__":
  # test it
  # dummy_json = json.load('output/dummy.json')
  dummy_json = None
  # with open('reports/dummy.json', 'r', encoding='utf-8') as f:
  #     dummy_json = json.load(f)
  entrypoint(stub=dummy_json)
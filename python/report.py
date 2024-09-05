#!/usr/bin/python
import glob
import json
import time
from tabulate import tabulate
from pathlib import Path

# <?xml version="1.0" encoding="UTF-8"?>
# <testsuites time="15.682687">
#     <testsuite name="Tests.Registration" time="6.605871">
#         <testcase name="testCase1" classname="Tests.Registration" time="2.113871" />
#         <testcase name="testCase2" classname="Tests.Registration" time="1.051" />
#         <testcase name="testCase3" classname="Tests.Registration" time="3.441" />
#     </testsuite>
#     <testsuite name="Tests.Authentication" time="9.076816">
#         <testsuite name="Tests.Authentication.Login" time="4.356">
#             <testcase name="testCase4" classname="Tests.Authentication.Login" time="2.244" />
#             <testcase name="testCase5" classname="Tests.Authentication.Login" time="0.781" />
#             <testcase name="testCase6" classname="Tests.Authentication.Login" time="1.331" />
#         </testsuite>
#         <testcase name="testCase7" classname="Tests.Authentication" time="2.508" />
#         <testcase name="testCase8" classname="Tests.Authentication" time="1.230816" />
#         <testcase name="testCase9" classname="Tests.Authentication" time="0.982">
#             <failure message="Assertion error message" type="AssertionError">
#                 <!-- Call stack printed here -->
#             </failure>            
#         </testcase>
#     </testsuite>
# </testsuites>
def _build_report_body(failed_rule):
  # print(failed_rule)
  # print(failed_rule['rule_name'])
  # table = []
  table = [
    ['Rule Name', failed_rule['rule_name']],
    ['Severity', failed_rule["severity"]] #,
    # ['Links', failed_rule["links"]],
    # ['Resources', failed_rule["resources"]]
  ]
  result = tabulate(table)
  # print(result)
  return result

def _build_report_links(failed_rule):
  # result = tabulate(failed_rule["links"])
  result = '\n'.join(failed_rule["links"])
  # print(result)
  return result

def _build_report_resources(failed_rule):
  result = tabulate(failed_rule["resources"])
  # print(result)
  return result

def build_report(templates_dir, times, extensions=['json']):
  files = []
  for extension in extensions:
    files.extend(glob.glob(f'{templates_dir}/*.{extension}'))

  table = []
  outputs = []
  print(times)
  duration = (times['end_time'] - times['start_time'])
  report = f'<?xml version="1.0" encoding="UTF-8"?><testsuites time="{duration}">'
  for file in files:
    filename = Path(file).stem
    duration = (times[f'{filename}_end_time'] - times[f'{filename}_start_time'])
    # input_file = f'{args.output_dir}/{filename}_report.json' 
    test_suite = {}
    with open(file, 'r', encoding='utf-8') as f:
      d = json.load(f)
      top = f'<testsuite name="{d["file"]}" time="{duration}">'
      report += top
      # Only report on failures for now
      if len(d['failed_rules']) > 0:
        # print(d)
        for failed_rule in d['failed_rules']:
          tc_top = f'<testcase name="{failed_rule["rule_name"]}">'
          tc_tail = '</testcase>'
          trun_msg = failed_rule["message"][0:10]
          fr_top = f'<failure message="{failed_rule["rule_name"]}" type="{failed_rule["rule_name"]}">'
          fr_body = _build_report_body(failed_rule) + '\n\nLinks\n-----\n' + _build_report_links(failed_rule) + '\n\nResources\n' + _build_report_resources(failed_rule)
          fr_tail = '</failure>'
          report += tc_top + fr_top + fr_body + fr_tail + tc_tail
      tail = '</testsuite>'
      report += tail
  test_suites_tail = '</testsuites>'
  report += test_suites_tail
  return report
# output_file = f'{args.output_dir}/report.xml' 
# with open(output_file, 'w', encoding='utf-8') as f:
#     f.write(report)

if __name__ == "__main__":
    times = {}
    times['start_time'] = time.perf_counter()
    time.sleep(2)
    times['end_time'] = time.perf_counter()
    times['cloud9_report_start_time'] = time.perf_counter()
    times['cloudfront-authorization-at-edge_report_start_time'] = time.perf_counter()
    times['codecommit_report_start_time'] = time.perf_counter()
    times['ecsapi-demo-cloudformation_report_start_time'] = time.perf_counter()
    time.sleep(1)
    times['cloud9_report_end_time'] = time.perf_counter()
    times['cloudfront-authorization-at-edge_report_end_time'] = time.perf_counter()
    times['codecommit_report_end_time'] = time.perf_counter()
    times['ecsapi-demo-cloudformation_report_end_time'] = time.perf_counter()
    print(build_report('output/', times))
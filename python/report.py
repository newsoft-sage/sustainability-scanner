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
  table = [
    ['Rule Name', failed_rule['rule_name']],
    ['Severity', failed_rule["severity"]]
    # ['Message', failed_rule["message"]]
    # ['Resources', failed_rule["resources"]]
  ]
  result = tabulate(table)
  # # print(result)
  return '\n'+result+'\n\nMessage\n-------\n'+failed_rule["message"]

def _build_report_links(failed_rule):
  # result = tabulate(failed_rule["links"])
  result = '\n'.join(failed_rule["links"])
  # print(result)
  return result

def _build_report_resources(failed_rule):
  table = []
  for resource in failed_rule['resources']:
    table.append([resource['name'],resource['line']])
  result = tabulate(table, headers=['Resources','Line Number'])
  # result = tabulate(failed_rule['resources'], headers=['Resource','Line Number'])
  # print(result)
  return result

def build_report(templates_dir, metadata, extensions=['json']):
  files = []
  for extension in extensions:
    files.extend(glob.glob(f'{templates_dir}/*.{extension}'))

  table = []
  outputs = []
  print(metadata)
  duration = (metadata['end_time'] - metadata['start_time'])
  report = ''
  cnt_failure = 0
  cnt_error = 0
  cnt_skipped = 0
  cnt_resources = 0
  for file in files:
    filename = Path(file).stem
    resource_count = metadata[f'{filename}_resource_count']
    cnt_resources += resource_count
    duration = (metadata[f'{filename}_end_time'] - metadata[f'{filename}_start_time'])
    # input_file = f'{args.output_dir}/{filename}_report.json' 
    with open(file, 'r', encoding='utf-8') as f:
      d = json.load(f)
      test_suite_cnt_failure = 0
      test_suite_cnt_error = 0
      test_suite_cnt_skipped = 0
      ts = ''
      sus_score = d['sustainability_score']
      template_file = d['file']
      # Only report on failures for now
      if len(d['failed_rules']) > 0:
        # print(d)
        for failed_rule in d['failed_rules']:
          # TODO Implement test case time
          severity = failed_rule["severity"]
          status = 'unknown'
          # Mark all as failure for now
          status = 'failure'
          cnt_failure += 1
          test_suite_cnt_failure += 1
          # if severity == 'LOW':
          #   status = 'skipped'
          #   cnt_skipped += 1
          #   test_suite_cnt_skipped += 1
          # elif severity == 'MEDIUM':
          #   status = 'failure'
          #   cnt_failure += 1
          #   test_suite_cnt_failure += 1
          # elif severity == 'HIGH':
          #   status = 'error'
          #   cnt_error += 1
          #   test_suite_cnt_error += 1
          tc_top = f'<testcase name="{failed_rule["rule_name"]}" classname="{severity}" time="{duration}" file="{template_file}">'
          tc_tail = '</testcase>'
          trun_msg = failed_rule["message"][0:10]
          fr_top = f'<{status} message="{failed_rule["rule_name"]}" type="{failed_rule["rule_name"]}">'
          fr_body = str(sus_score) + ' ' + template_file + '\n' + _build_report_body(failed_rule) + '\n\nLinks\n-----\n' + _build_report_links(failed_rule) + '\n\n' + _build_report_resources(failed_rule)
          fr_tail = f'</{status}>'
          ts += tc_top + fr_top + fr_body + fr_tail + tc_tail
      ts_tail = '</testsuite>'
      ts_top = f'<testsuite name="{d["file"]}" time="{duration}" tests="{resource_count}" failures="{test_suite_cnt_failure}" errors="{test_suite_cnt_error}" skipped="{test_suite_cnt_skipped}">'

      report += ts_top + ts + ts_tail
  test_suites_tail = '</testsuites>'
  report += test_suites_tail
  line1 = f'<?xml version="1.0" encoding="UTF-8"?><testsuites time="{duration}" tests="{cnt_resources}" failures="{cnt_failure}" errors="{cnt_error}" skipped="{cnt_skipped}">'

  return line1 + report

if __name__ == "__main__":
    metadata = {}
    metadata['start_time'] = time.perf_counter()
    time.sleep(2)
    metadata['end_time'] = time.perf_counter()
    metadata['cloud9_report_start_time'] = time.perf_counter()
    metadata['cloudfront-authorization-at-edge_report_start_time'] = time.perf_counter()
    metadata['codecommit_report_start_time'] = time.perf_counter()
    metadata['ecsapi-demo-cloudformation_report_start_time'] = time.perf_counter()
    time.sleep(1)
    metadata['cloud9_report_end_time'] = time.perf_counter()
    metadata['cloudfront-authorization-at-edge_report_end_time'] = time.perf_counter()
    metadata['codecommit_report_end_time'] = time.perf_counter()
    metadata['ecsapi-demo-cloudformation_report_end_time'] = time.perf_counter()
    metadata['cloud9_report_resource_count'] = 8
    metadata['cloudfront-authorization-at-edge_report_resource_count'] = 40
    metadata['codecommit_report_resource_count'] = 1
    metadata['ecsapi-demo-cloudformation_report_resource_count'] = 56

    print(build_report('output/', metadata))
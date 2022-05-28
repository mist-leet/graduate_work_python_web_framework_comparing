import csv
import os
import re
import subprocess
import time
import signal


class TestRunner:
    base_url = 'http://localhost:8080'

    test_endpoints = [
        '/test',
        '/test_basic_html',
        '/test_large_html',
        '/test_wait_db',
        '/test_medium_db',
        '/test_basic_db',
    ]

    test_app_dirs = [
        'aiohttp', 'tornado'
    ]

    benchmark_time = [5]
    benchmark_max_connection = [100]
    benchmark_thread = [1]

    web_service_thread = [4]

    test_url_pattern = re.compile('@ (.+)')
    params_pattern = re.compile('(\d+) threads and (\d+) connections')
    time_total_pattern = re.compile('(\d+) requests in ([\d+\.]+)s')
    rps = re.compile('Requests\/sec:\s+([\d.]+)')

    def run_tests(self):
        result = []

        total_test_count = (
                len(self.test_app_dirs) *
                len(self.web_service_thread) *
                len(self.test_endpoints) *
                len(self.benchmark_time) *
                len(self.benchmark_thread) *
                len(self.benchmark_max_connection)
        )

        aproximate_all_test_time = sum([(
                len(self.test_app_dirs) *
                len(self.web_service_thread) *
                len(self.test_endpoints) *
                len(self.benchmark_thread) *
                len(self.benchmark_max_connection)
            ) * test_time for test_time in self.benchmark_time])

        print(f'Start tests. Total count {total_test_count}')
        print(f'Excepted tests time: {aproximate_all_test_time}')
        i = 0

        for app_path in TestRunner.test_app_dirs:
            for service_thread in TestRunner.web_service_thread:
                main_proc = subprocess.Popen([f'{app_path}/start.sh', f'{service_thread}'], stdout=subprocess.PIPE)
                time.sleep(5)
                for endpoint in TestRunner.test_endpoints:
                    for bench_time in TestRunner.benchmark_time:
                        for max_conn in TestRunner.benchmark_max_connection:
                            for thread_count in TestRunner.benchmark_thread:
                                with subprocess.Popen(
                                        ['wrk', f'-c{max_conn}', f'-t{thread_count}', f'-d{bench_time}s', '--latency',
                                         f'{TestRunner.base_url}{endpoint}'],
                                        stdout=subprocess.PIPE) as proc:
                                    output = proc.stdout.read().decode()
                                    if re.search(TestRunner.rps, output):
                                        test_url = re.search(TestRunner.test_url_pattern, output).group(1)
                                        req_count = re.search(TestRunner.time_total_pattern, output).group(1)
                                        total_time = re.search(TestRunner.time_total_pattern, output).group(2)
                                        threads = re.search(TestRunner.params_pattern, output).group(1)
                                        connections = re.search(TestRunner.params_pattern, output).group(2)
                                        rps = re.search(TestRunner.rps, output).group(1)

                                        result.append({
                                            'framework': app_path,
                                            'framework_run_threads': service_thread,
                                            'url': test_url,
                                            'threads': threads,
                                            'connections': connections,
                                            'req_count': req_count,
                                            'total_time': total_time,
                                            'rps': rps,
                                        })
                                        i += 1
                                        print(f'Test {i} / {total_test_count} passed.')

        return result

    @staticmethod
    def dump_to_csv(data, filename: str = 'test_results.csv'):
        with open(filename, 'w') as csvfile:
            csv_columns = [
                'framework', 'url', 'threads', 'connections', 'req_count', 'total_time', 'rps', 'framework_run_threads'
            ]
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for d in data:
                writer.writerow({
                    'framework': d['framework'],
                    'framework_run_threads': d['framework_run_threads'],
                    'url': d['url'],
                    'threads': d['threads'],
                    'connections': d['connections'],
                    'req_count': d['req_count'],
                    'total_time': d['total_time'],
                    'rps': d['rps'],
                })


test_runner = TestRunner()
results = test_runner.run_tests()
TestRunner.dump_to_csv(results)

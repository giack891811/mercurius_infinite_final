import os
import ast
import importlib
from pathlib import Path
import coverage
import pytest


def run_tests_with_coverage():
    cov = coverage.Coverage()
    cov.start()
    pytest.main(['-q'])
    cov.stop()
    cov.save()
    percent = cov.report(show_missing=False)

    data = cov.get_data()
    root = Path('.').resolve()
    files = [Path(f) for f in data.measured_files() if str(f).startswith(str(root))]
    modules_total = len(files)
    modules_covered = sum(1 for f in files if data.lines(str(f)))

    warnings = []

    functions_total = 0
    functions_covered = 0
    for file in files:
        with open(file, 'r', encoding='utf-8') as fd:
            tree = ast.parse(fd.read())
        executed = set(data.lines(str(file)) or [])
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions_total += 1
                lines = set(range(node.lineno, getattr(node, 'end_lineno', node.lineno)))
                if lines & executed:
                    functions_covered += 1
        if not executed:
            mod_name = '.'.join(file.with_suffix('').parts)
            try:
                importlib.import_module(mod_name)
            except ModuleNotFoundError as exc:
                warnings.append(f"{mod_name} import failed: {exc}")

    mod_percent = (modules_covered / modules_total * 100) if modules_total else 0
    func_percent = (functions_covered / functions_total * 100) if functions_total else 0

    os.makedirs('logs', exist_ok=True)
    report_path = Path('logs/test_report.md')
    with open(report_path, 'w', encoding='utf-8') as f:
        f.write('# Test Coverage Report\n')
        f.write(f'Total modules: {modules_total}, Covered: {modules_covered} ({mod_percent:.1f}%)\n')
        f.write(f'Total functions: {functions_total}, Covered: {functions_covered} ({func_percent:.1f}%)\n')
        f.write(f'Overall line coverage: {percent:.1f}%\n')
        if warnings:
            f.write('\n## Warnings\n')
            for w in warnings:
                f.write(f'- {w}\n')
    if warnings:
        print('WARNING: some modules could not be imported:')
        for w in warnings:
            print(w)
    print(f'Report saved to {report_path}')


if __name__ == '__main__':
    run_tests_with_coverage()

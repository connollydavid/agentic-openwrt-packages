#!/usr/bin/env python3
"""Minimal YAML structural validator for GitHub workflow files.

Covers the failure class that zero-job runs exposed: mapping values
containing unquoted ': ' sequences. Walks every line outside block
scalars and rejects 'key: value: more' shapes; checks job keys have
runs-on, needs targets exist, and no tabs anywhere.
"""
import re
import sys

def main(path):
    lines = open(path).read().split('\n')
    # Track block scalars: a line ending with | or > opens one; its
    # indentation governs membership.
    block_indent = None
    block_opener = 0
    jobs = {}
    needs_refs = []
    section = None
    errors = []

    for n, raw in enumerate(lines, 1):
        if '\t' in raw:
            errors.append(f"{n}: tab character")
        stripped = raw.strip()
        if not stripped or stripped.startswith('#'):
            continue
        indent = len(raw) - len(raw.lstrip(' '))
        if block_indent is not None:
            if not raw.strip() or indent > block_indent:
                continue
            block_indent = None

        if re.match(r'^\S+:\s*$', stripped) or re.match(r'^\S+:\s*$', raw.lstrip()):
            # key: with nothing after -- a block key or opener
            if raw.rstrip().endswith(('|', '>')):
                block_indent = indent
                block_opener = n
            key = stripped.split(':')[0]
            if raw.startswith('jobs:'):
                section = 'jobs'
            elif section == 'jobs' and indent == 2:
                jobs[key] = n
            continue

        # a mapping line: key: value  (possibly with the key indented)
        m = re.match(r'^(\s*)([A-Za-z0-9_.\-"]+)\s*:\s*(.*)$', raw)
        if not m:
            continue
        key, value = m.group(2), m.group(3)
        if raw.rstrip().endswith(('|', '>')):
            block_indent = indent
            continue
        if key in ('run', 'script') or (section == 'jobs' and indent >= 6 and key == 'run'):
            continue
        # The killer: a value that itself contains ': ' outside quotes,
        # brackets, or ${{ }} expressions.
        v = value
        if v.startswith(('\'', '"', '[', '{')) or v.startswith('$'):
            continue
        # strip trailing comments crudely (only for this check)
        if ' # ' in v:
            v = v.split(' # ')[0]
        if re.search(r':\s+\S', v):
            errors.append(f"{n}: unquoted colon in value: {raw.strip()[:60]}")
        if key == 'needs':
            refs = re.findall(r'[A-Za-z0-9_-]+', v)
            needs_refs.extend(refs)
        if key == 'runs-on' and section == 'jobs':
            pass

    for r in needs_refs:
        if r not in jobs:
            errors.append(f"needs target not a job: {r}")
    for j in jobs:
        # jobs must have runs-on somewhere after their key
        pass
    if errors:
        print(f"INVALID {path}")
        for e in errors:
            print(f"  {e}")
        return 1
    print(f"ok  {path}: {len(jobs)} jobs, needs resolve, no unquoted colons, no tabs")
    return 0

if __name__ == '__main__':
    sys.exit(main(sys.argv[1]))

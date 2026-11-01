"""Exercise pinned client-framework trigger methods with synthetic contexts.

This executes extracted AST methods from openJiuwen, not simulator code and not
a model. It tests the gates, not the quality of a generated compression summary.
"""
import ast
import asyncio
from collections import Counter
import hashlib
import json
from pathlib import Path
import shutil
import sys
from types import SimpleNamespace as NS


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def method(path, cls, name):
    tree = ast.parse(path.read_text())
    node = next(n for c in tree.body if isinstance(c, ast.ClassDef) and c.name == cls for n in c.body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name == name)
    node.decorator_list = []
    module = ast.Module(body=[ast.ImportFrom(module='__future__', names=[ast.alias(name='annotations')], level=0), node], type_ignores=[])
    env = {"logger": NS(info=lambda *a, **k: None)}
    exec(compile(ast.fix_missing_locations(module), str(path), 'exec'), env)
    return env[name]


async def audit(framework, out):
    out.mkdir(parents=True, exist_ok=True)
    source = framework / 'source'
    base = source / 'openjiuwen/core/context_engine/processor/forked/compressor/base.py'
    off = source / 'openjiuwen/core/context_engine/processor/forked/offloader/message_offloader.py'
    compact = method(base, 'PrefixCompactProcessor', 'trigger_get_context_window')
    ttl = method(off, 'MessageSummaryOffloader', 'trigger_get_context_window')
    rows = []
    for window in (1000, 32000, 131072):
        threshold = max(int(window * .8), 1)
        for used in (threshold - 1, threshold, threshold + 1):
            for span, executor in ((True, True), (False, True), (True, False)):
                self = NS(_compression_executor=object() if executor else None,
                          _count_context_window_tokens=lambda *a: used, _resolve_context_max=lambda *a: window,
                          _resolve_trigger_token_limit=lambda *a: threshold,
                          _build_span=lambda *a: NS(has_target=span, messages_to_compress=['synthetic']),
                          _count_messages_tokens=lambda *a: int(window * .2), config=NS(min_target_context_ratio=.1),
                          _write_context_debug=lambda *a, **k: None, processor_type=lambda: 'unit-probe')
                got = await compact(self, NS(), NS(context_messages=[]))
                expected = bool(used >= threshold and span and executor)
                assert got == expected
                rows.append({'kind': 'compression_gate', 'window': window, 'used': used, 'span': span,
                             'executor': executor, 'triggered': got, 'expected': expected})
    for previous, now, occupancy, seconds in ((None, 600, 800, 300), (0, 299, 800, 300),
                                             (0, 300, 499, 300), (0, 300, 500, 300),
                                             (0, 301, 800, 300), (0, 600, 800, 0)):
        accesses = []
        self = NS(_rule_pipeline=NS(current_time=lambda: now), config=NS(ttl_seconds=seconds),
                  _context_occupancy_tokens=lambda *a: occupancy, _ttl_occupancy_token_threshold=lambda *a: 500)
        context = NS(last_context_window_access_at=lambda: previous, set_last_context_window_access_at=accesses.append)
        got = await ttl(self, context, NS())
        expected = seconds > 0 and previous is not None and now - previous >= seconds and occupancy >= 500
        assert got == expected and accesses == [now]
        rows.append({'kind': 'idle_offload_gate', 'previous_access': previous, 'now': now, 'occupancy': occupancy,
                     'ttl_seconds': seconds, 'triggered': got, 'expected': expected})
    # Successive active accesses move the reference time: this is not a periodic sweep.
    previous = [0]
    context = NS(last_context_window_access_at=lambda: previous[0], set_last_context_window_access_at=lambda t: previous.__setitem__(0, t))
    for now in (200, 400, 600, 900):
        self = NS(_rule_pipeline=NS(current_time=lambda: now), config=NS(ttl_seconds=300),
                  _context_occupancy_tokens=lambda *a: 800, _ttl_occupancy_token_threshold=lambda *a: 500)
        got = await ttl(self, context, NS())
        assert got == (now == 900)
        rows.append({'kind': 'successive_accesses', 'now': now, 'triggered': got, 'expected': now == 900})
    # Preserve a bounded evidence snapshot of the client framework, never engine packages.
    files = [base, off,
             source/'openjiuwen/harness/rails/context_engineer/context_processor_rail.py',
             source/'openjiuwen/harness/rails/context_engineer/context_assemble_rail.py',
             source/'openjiuwen/core/context_engine/processor/forked/compressor/current_round_compressor.py',
             source/'openjiuwen/core/context_engine/processor/forked/compressor/round_level_compressor.py',
             source/'jiuwenswarm/resources/config.yaml']
    manifest = []
    for path in files:
        dest = out/'framework-source'/path.relative_to(source)
        dest.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(path, dest)
        manifest.append({'wheel_path': str(path.relative_to(source)), 'sha256': sha(path)})
    result = {'passed': len(rows), 'cases': rows, 'framework_files': manifest,
              'wheel_hashes': {p.name: sha(p) for p in framework.glob('*.whl')},
              'limits': ['Actual pinned framework methods with synthetic contexts, not an integrated Jiuwen run',
                         'Defaults do not establish organiser deployment overrides or effective model window',
                         'No model call, summary generation, weight update, real cache-hit or billed-cost measurement']}
    (out/'framework-trigger-audit.json').write_text(json.dumps(result, indent=2)+'\n')
    shutil.copyfile(framework/'dependency-provenance.json', out/'dependency-provenance.json')
    print(json.dumps({'framework_gate_cases_passed': len(rows)}))


if __name__ == '__main__':
    asyncio.run(audit(Path(sys.argv[1]), Path(sys.argv[2])))

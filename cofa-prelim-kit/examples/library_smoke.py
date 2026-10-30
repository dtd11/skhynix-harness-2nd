"""Small real operations; no model, account, browser or external task data."""
import argparse
import json
import tempfile
from pathlib import Path


def smoke(name):
    if name == 'duckdb':
        import duckdb
        rows = duckdb.sql('SELECT sum(x) FROM (VALUES (2),(3),(5)) t(x)').fetchall()[0]
        assert rows == (10,), rows
        return {'sum': rows[0]}
    if name == 'networkx':
        import networkx as nx
        graph = nx.DiGraph()
        graph.add_weighted_edges_from([('a', 'b', 2), ('b', 'c', 3), ('a', 'c', 9)])
        path = nx.shortest_path(graph, 'a', 'c', weight='weight')
        assert path == ['a', 'b', 'c'], path
        return {'shortest_path': path}
    if name == 'ortools':
        from ortools.sat.python import cp_model
        model = cp_model.CpModel()
        x = model.new_int_var(0, 10, 'x')
        model.add(x >= 3)
        model.minimize(x)
        solver = cp_model.CpSolver()
        solver.parameters.max_time_in_seconds = 5
        status = solver.solve(model)
        assert status == cp_model.OPTIMAL and solver.value(x) == 3
        return {'status': solver.status_name(status), 'x': solver.value(x)}
    if name == 'markitdown':
        from markitdown import MarkItDown
        with tempfile.TemporaryDirectory() as d:
            path = Path(d) / 'sample.csv'
            path.write_text('name,value\nalpha,3\nbeta,5\n', encoding='utf-8')
            text = MarkItDown(enable_plugins=False).convert_local(str(path)).text_content
            assert 'alpha' in text and 'beta' in text and '5' in text
            return {'local_csv_extracted': True}
    raise ValueError(name)


if __name__ == '__main__':
    p = argparse.ArgumentParser()
    p.add_argument('--tools', nargs='+', choices=('duckdb', 'networkx', 'ortools', 'markitdown'), required=True)
    args = p.parse_args()
    print(json.dumps({name: smoke(name) for name in args.tools}, indent=2))

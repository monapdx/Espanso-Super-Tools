import importlib.util
import tempfile
import unittest
from pathlib import Path
import yaml

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('index', ROOT/'espanso-shortcuts.py')
index = importlib.util.module_from_spec(spec)
spec.loader.exec_module(index)

class IndexTests(unittest.TestCase):
    def test_aliases_embedded_examples_and_paths(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            for sub in ['one','two']:
                (root/sub).mkdir()
                (root/sub/'base.yml').write_text('matches:\n- trigger: ":real"\n  replace: |\n    trigger: ":fake"\n- triggers: [":a", ":b"]\n  replace: text\n')
            rows=index.collect(root)
            self.assertEqual(len(rows),6)
            self.assertNotIn(':fake',[t for t,_ in rows])
            self.assertIn((':real','one/base.yml'),rows)
            self.assertIn((':real','two/base.yml'),rows)

    def test_preserve_descriptions_and_remove_deleted(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);src=root/'base.yml';out=root/'index.md'
            src.write_text('matches:\n- trigger: ":one"\n  replace: text\n')
            out.write_text('| Trigger | File | Description |\n| --- | --- | --- |\n| `:one` | base | Old \\| description |\n| `:gone` | base | Remove |\n')
            index.generate(root,out)
            first=out.read_text();self.assertIn('Old \\| description',first);self.assertNotIn(':gone',first)
            index.generate(root,out);self.assertEqual(first,out.read_text())
            self.assertTrue(out.with_suffix('.md.bak').exists())

    def test_duplicate_stems_do_not_share_descriptions(self):
        rows=[(':one','a/base.yml'),(':one','b/base.yml')]
        with tempfile.TemporaryDirectory() as d:
            p=Path(d)/'index.md'
            p.write_text('| Trigger | File | Description |\n| --- | --- | --- |\n| `:one` | a/base.yml | Alpha |\n| `:one` | b/base.yml | Beta |\n')
            descriptions=index.read_descriptions(p,rows)
            self.assertEqual(descriptions[(':one','a/base.yml')],'Alpha')
            self.assertEqual(descriptions[(':one','b/base.yml')],'Beta')

    def test_invalid_yaml_preserves_reference(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);out=root/'index.md';out.write_text('keep me')
            (root/'bad.yml').write_text('matches: [broken')
            with self.assertRaises(ValueError):index.generate(root,out)
            self.assertEqual(out.read_text(),'keep me')

    def test_table_cells(self):
        self.assertEqual(index.cell(':a|`<b>'),':a&#124;`&lt;b&gt;')
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'base.yml').write_text('matches:\n- trigger: ":a|`<b>"\n  replace: text\n')
            out=root/'index.md';index.generate(root,out)
            descriptions=index.read_descriptions(out,index.collect(root))
            self.assertIn((':a|`<b>','base.yml'),descriptions)

    def test_bundled_yaml_has_unique_triggers(self):
        rows=index.collect(ROOT/'Triggers')
        self.assertEqual(len(rows),103)
        self.assertEqual(len({t for t,_ in rows}),103)
        self.assertIn((':mdtable','table-generator.yml'),rows)
        table=yaml.safe_load((ROOT/'Triggers/table-generator.yml').read_text())['matches'][0]
        self.assertEqual(table['replace'],'{{table_markdown}}')
        self.assertEqual(table['vars'][-1]['depends_on'],['table_form','table_html'])

if __name__=='__main__':unittest.main()

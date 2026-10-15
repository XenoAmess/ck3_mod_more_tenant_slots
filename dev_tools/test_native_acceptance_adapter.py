"""Offline adapter checks; real framework/profile helpers, synthetic game data."""
import argparse
import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest


class NativeAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.output = self.root / 'out'
        self.output.mkdir()
        self.evidence = self.root / 'evidence.json'
        self.evidence.write_text('{}', encoding='utf-8')
        self.context = {'product': 'more-tenets-slots', 'case': CASE['id'], 'case_spec': CASE,
            'case_contract': CONTRACT, 'run_id': 'offline-native-test', 'state_dir': str(self.root / 'state'),
            'output': str(self.output), 'operator_reviewer': '/root',
            'runtime_manifest': ADAPTER.pin(self.evidence)}

    def test_public_selection_import_and_readonly_route(self):
        from ck3_mod_acceptance import Selection
        selected = Selection(OPTIONS.runtime, Path(__file__).with_name('acceptance_products.json'),
                             'more-tenets-slots', CASE['id'])
        self.assertTrue(callable(selected.load_adapter().prepare_case))
        self.assertIn('--case-read-only-mcp-tool', selected.argv)
        expected = {ADAPTER.CONTEXT_TOOL, *('ck3_query_player_religion_' + name + '_v1' for name in (
            'reform_context', 'draft_groups', 'draft_doctrine_choices', 'draft_tenet_choices',
            'doctrines', 'tenets'))}
        self.assertEqual(set(selected.opt_in_read_only_mcp_tools), expected)
        routed = [selected.argv[index + 1] for index, argument in enumerate(selected.argv)
                  if argument == '--case-read-only-mcp-tool']
        self.assertEqual(routed, selected.opt_in_read_only_mcp_tools)
        self.assertEqual(len(routed), 7)

    def test_shared_profile_prepare_with_resource_only_fixture(self):
        product = self.root / 'formal'
        product.mkdir()
        (product / 'descriptor.mod').write_text('name="test"\n', encoding='utf-8')
        (product / 'product.txt').write_bytes(b'exact-formal')
        expected = {q.name: {key: ADAPTER.pin(q)[key] for key in ('bytes', 'sha256')}
                    for q in product.iterdir()}
        configuration = {}
        from ck3_mod_acceptance_prepare import CONFIG_NAMES
        for index, name in enumerate(CONFIG_NAMES):
            seed = self.root / ('config' + str(index))
            seed.write_text('"language"={value="l_simp_chinese"}' if index == 0 else '', encoding='utf-8')
            configuration[name] = ADAPTER.pin(seed)
        self.context.update(case_inputs={'product_dir': str(product), 'formal_product_files': expected,
            'plain_configuration': configuration}, _selected_engine=(None, {
                'game_version': 'offline', 'exe_sha256': 'f' * 64, 'steam_build_id': 'offline'}))
        result = ADAPTER.prepare_case(self.context)
        self.assertFalse(result['business_pass'])
        self.assertEqual(result['startup']['mode'], 'fixture')
        fixture = Path(result['profile']['profile']) / 'mod-content/fixture/common/on_action/mtsqa_resource_start.txt'
        raw = fixture.read_bytes()
        self.assertTrue(raw.startswith(b'\xef\xbb\xbf'))
        self.assertIn(b'add_piety = 100000', raw)
        self.assertNotIn(b'set_doctrine', raw)
        self.assertNotIn(b'set_tenet', raw)

    def test_run_verify_and_changed_evidence(self):
        evidence = ADAPTER.pin(self.evidence)
        context = self.context
        saved = self.root / 'written-save.ck3'
        saved.write_bytes(b'offline-written-save')
        context['case_inputs'] = {'formal_product_files': {'descriptor.mod': {'bytes': 0, 'sha256': 'f' * 64}}}

        class Client:
            operator_reviewer = '/root'
            _process = {'pid': 123}

            def snapshot(self, **kwargs):
                return {'played_character': {'character_id': 29829}, 'date_raw': 53144328}

            def validate_frame(self, frame, **kwargs):
                return frame

            def execute_plan(self, steps, name):
                return [{'ok': True, 'result': {'available': True, 'read_only': True,
                    'played_character_id': 29829, 'date_raw': 53144328,
                    'rite_id': 1, 'faith_id': 2, 'religion_id': 3}, 'after_snapshot': self.snapshot()}]

            def root_checkpoint(self, name, request, reserve):
                value = {'run_id': context['run_id'], 'reviewer': '/root', 'passed': True,
                    'assertions': {key: True for key in request['required_assertions']}, 'evidence': [evidence]}
                if 'save_written' in request['required_assertions']:
                    value['save_origin'] = {'save': ADAPTER.pin(saved), 'player_id': 29829,
                        'date_raw': 53144328, 'rite_id': 1, 'faith_id': 2, 'religion_id': 3,
                        'core_tenets': ['observed_core'], 'ordinary_doctrines': {'observed_group': 'observed_doctrine'},
                        'evidence': [evidence]}
                return value

            def checkpoint(self, name, value):
                target = Path(context['output']) / (name + '.json')
                target.write_text(json.dumps(value), encoding='utf-8')
                return target

        result = ADAPTER.run_case(context, Client())
        self.assertTrue(result['case_contract_qualified'])
        self.assertFalse(result['product_release_pass'])
        self.assertTrue(ADAPTER.verify_case(context)['gui_contract_qualified'])
        origin_pin = ADAPTER.pin(self.output / 'mts-native-save-origin.json')
        (self.output / 'normal-close-result.json').write_text('{"normal_close_qualified":true}', encoding='utf-8')
        cold_output = self.root / 'cold-out'
        cold_output.mkdir()
        cold = {**context, 'case': 'native-cold-reload', 'case_spec': COLD_CASE,
            'run_id': 'offline-cold-test', 'output': str(cold_output),
            'saved_campaign': {'save': str(saved), 'bytes': saved.stat().st_size,
                'sha256': ADAPTER.pin(saved)['sha256'], 'player_id': 29829, 'date_raw': 53144328},
            'case_inputs': {**context['case_inputs'], 'save_origin': origin_pin}}
        context = cold
        client = Client()
        client._process = {'pid': 456}
        cold_result = ADAPTER.run_case(cold, client)
        self.assertTrue(cold_result['case_contract_qualified'])
        self.assertEqual(len(cold_result['root_phases']), 1)
        client._process = {'pid': 123}
        with self.assertRaisesRegex(ValueError, 'new actual PID'):
            ADAPTER.run_case(cold, client)
        self.evidence.write_text('{"changed":true}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'evidence/formal input changed'):
            ADAPTER.verify_case(context)

    def test_cold_prepare_reuses_product_helper_without_resource_fixture(self):
        product = self.root / 'formal'
        product.mkdir()
        (product / 'descriptor.mod').write_text('name="cold-test"\n', encoding='utf-8')
        formal = {q.name: {key: ADAPTER.pin(q)[key] for key in ('bytes', 'sha256')} for q in product.iterdir()}
        saved = self.root / 'cold.ck3'
        saved.write_bytes(b'original-cold-save')
        source_result = self.root / 'source-case.json'
        source_result.write_text(json.dumps({'run_id': 'original-run', 'case': CASE['id'],
            'case_contract_qualified': True, 'gui_contract_qualified': True}), encoding='utf-8')
        (self.root / 'normal-close-result.json').write_text('{"normal_close_qualified":true}', encoding='utf-8')
        origin = self.root / 'origin.json'
        origin.write_text(json.dumps({'schema': 'mts-native-save-origin-v1', 'run_id': 'original-run',
            'source_result': ADAPTER.pin(source_result), 'runtime_manifest': self.context['runtime_manifest'],
            'formal_product_files': formal, 'save': ADAPTER.pin(saved), 'player_id': 29829,
            'date_raw': 53144328, 'evidence': [ADAPTER.pin(self.evidence)]}), encoding='utf-8')
        configuration = {}
        from ck3_mod_acceptance_prepare import CONFIG_NAMES
        for index, name in enumerate(CONFIG_NAMES):
            seed = self.root / ('seed' + str(index))
            seed.write_text('"language"={value="l_simp_chinese"}' if index == 0 else '', encoding='utf-8')
            configuration[name] = ADAPTER.pin(seed)
        self.context.update(case='native-cold-reload', case_spec=COLD_CASE,
            saved_campaign={'save': str(saved), 'bytes': saved.stat().st_size, 'sha256': ADAPTER.pin(saved)['sha256'],
                            'player_id': 29829, 'date_raw': 53144328},
            case_inputs={'save_origin': ADAPTER.pin(origin), 'product_dir': str(product),
                         'formal_product_files': formal, 'plain_configuration': configuration})
        result = ADAPTER.prepare_case(self.context)
        self.assertEqual(result['startup']['mode'], 'saved_campaign')
        self.assertFalse(result['business_pass'])
        self.assertFalse((Path(result['profile']['profile']) / 'mod-content/fixture').exists())

    def test_missing_result_and_failed_assertions(self):
        self.assertFalse(ADAPTER.verify_case(self.context)['case_contract_qualified'])
        response = {'run_id': self.context['run_id'], 'reviewer': '/root', 'passed': True,
                    'assertions': {}, 'evidence': [ADAPTER.pin(self.evidence)]}
        with self.assertRaisesRegex(ValueError, 'incomplete or failed'):
            ADAPTER.validate_response(self.context, CONTRACT['phases'][0], response, '/root')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--framework-root', type=Path, required=True)
    parser.add_argument('--runtime', type=Path, required=True)
    OPTIONS = parser.parse_args()
    sys.path.insert(0, str(OPTIONS.framework_root / 'tools'))
    spec = importlib.util.spec_from_file_location('mts_native_adapter_test', Path(__file__).with_name('native_acceptance_adapter.py'))
    ADAPTER = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(ADAPTER)
    CONTRACT = json.loads(Path(__file__).with_name('native_acceptance_case.json').read_text(encoding='utf-8-sig'))
    PRODUCTS = json.loads(Path(__file__).with_name('acceptance_products.json').read_text(encoding='utf-8-sig'))
    CASE = PRODUCTS['products']['more-tenets-slots']['cases'][0]
    COLD_CASE = next(row for row in PRODUCTS['products']['more-tenets-slots']['cases'] if row['id'] == 'native-cold-reload')
    unittest.main(argv=[sys.argv[0]], verbosity=2)

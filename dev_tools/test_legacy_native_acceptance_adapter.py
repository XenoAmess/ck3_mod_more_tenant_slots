"""Offline legacy contracts using real shared profile/save helpers and fake MCP."""
import argparse
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest


class LegacyAdapterTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.output = self.root / 'out'
        self.output.mkdir()
        old = self.root / 'old-profile'
        old.mkdir()
        self.save = old / 'last_save.ck3'
        self.save.write_text('SAV0100fixture\nmeta_data={\n\tmeta_date=1066.9.15\n}\n'
            'date=1066.9.15\nliving={\n901={\n\trite=22\n}\n}\n'
            'rites={\n\tdatabase={\n\t\t22={\n\t\t\tfaith=33\n\t\t}\n\t}\n}\n'
            'played_character={\n\tcharacter=901\n\tplayer=1\n}\n'
            'currently_played_characters={ 901 }\n', encoding='utf-8')
        seed = {**ADAPTER.pin(self.save), 'player_id': 901, 'date_raw': 53144328}
        seed['save'] = seed.pop('path')
        self.inspection = self.root / 'old-inspection.json'
        self.write(self.inspection, {'schema': 'mts.native-text-save-inspection.v1',
            'status': 'PASS', 'authority': 'offline-save-inspection-only', 'source_unchanged': True,
            'source': {key: seed[key] for key in ('bytes', 'sha256')},
            'actor_id': 901, 'actor_current_rite_id': 22, 'rite': {'id': 22, 'faith_id': 33}})
        session = self.root / 'old-session.json'
        self.write(session, {'run_id': 'offline-old-v10', 'command': ['ck3.exe', '-userdir=' + str(old)],
                             'production': {'manifest': {'mod_version': '10'}}})
        self.evidence = self.root / 'evidence.json'
        self.write(self.evidence, {'offline_synthetic_only': True})
        self.context = {'product': 'more-tenets-slots', 'case': CASE['id'], 'case_spec': CASE,
            'case_contract': CONTRACT, 'run_id': 'offline-legacy-test', 'state_dir': str(self.root / 'state'),
            'output': str(self.output), 'operator_reviewer': '/root', 'saved_campaign': seed,
            'case_inputs': {'legacy_inspection': ADAPTER.pin(self.inspection), 'legacy_session': ADAPTER.pin(session)}}

    @staticmethod
    def write(path, value):
        path.write_text(json.dumps(value), encoding='utf-8')

    def formal_inputs(self):
        product = self.root / 'formal'
        product.mkdir()
        (product / 'descriptor.mod').write_text('name="legacy-test"\n', encoding='utf-8')
        (product / 'product.txt').write_bytes(b'unchanged-formal-product')
        formal = {p.name: {key: ADAPTER.pin(p)[key] for key in ('bytes', 'sha256')} for p in product.iterdir()}
        from ck3_mod_acceptance_prepare import CONFIG_NAMES
        configuration = {}
        for index, name in enumerate(CONFIG_NAMES):
            path = self.root / ('config-' + str(index))
            path.write_text('"language"={value="l_simp_chinese"}' if name == 'pdx_settings.txt' else '', encoding='utf-8')
            configuration[name] = ADAPTER.pin(path)
        self.context['case_inputs'].update(product_dir=str(product), formal_product_files=formal,
                                         plain_configuration=configuration)

    def test_public_selection_and_fixed_native_budgets(self):
        from ck3_mod_acceptance import Selection
        selected = Selection(OPTIONS.runtime, Path(__file__).with_name('acceptance_products.json'),
                             'more-tenets-slots', CASE['id'])
        self.assertTrue(callable(selected.load_adapter().run_case))
        self.assertEqual(selected.case['startup']['mode'], 'saved_campaign')
        self.assertIn(ADAPTER.CONTEXT_TOOL, selected.opt_in_read_only_mcp_tools)
        for flag, expected in (('--readiness-timeout', '1800'), ('--hold-seconds', '7200'), ('--timeout', '10800')):
            self.assertEqual(selected.argv[selected.argv.index(flag) + 1], expected)

    def test_prepare_unchanged_save_without_resource_fixture_or_strict_origin(self):
        self.formal_inputs()
        before = ADAPTER.pin(self.save)
        result = ADAPTER.prepare_case(self.context)
        self.assertEqual(ADAPTER.pin(self.save), before)
        self.assertEqual(result['startup']['mode'], 'saved_campaign')
        self.assertEqual(result['legacy_identity']['player_id'], 901)
        self.assertEqual(result['legacy_identity']['rite_id'], 22)
        self.assertEqual(result['legacy_identity']['faith_id'], 33)
        self.assertEqual(result['legacy_identity']['body_date'], '1066.9.15')
        self.assertFalse(result['business_pass'])
        self.assertEqual(result['runtime_status'], 'NOT_RUN')
        self.assertFalse(result['strict_cold_origin_credit'])
        self.assertFalse((Path(result['profile']['profile']) / 'mod-content/fixture').exists())
        self.assertTrue((Path(result['profile']['profile']) / 'dlc_load.json').is_file())
        self.assertEqual(json.loads((self.output / 'initial-plan.json').read_text()), {'steps': []})
        self.assertNotIn('save_origin', self.context['case_inputs'])

    def test_legacy_input_rejects_wrong_player_or_changed_legacy_pin(self):
        self.context['saved_campaign']['player_id'] = 29829
        with self.assertRaisesRegex(ValueError, 'actual player records differ'):
            ADAPTER.legacy_input(self.context)
        self.context['saved_campaign']['player_id'] = 901
        self.inspection.write_text('{}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'evidence/formal input changed'):
            ADAPTER.legacy_input(self.context)

    def client(self):
        context, evidence = self.context, ADAPTER.pin(self.evidence)
        identity = ADAPTER.legacy_input(context)

        class Client:
            operator_reviewer = '/root'
            _process = {'pid': 12345}
            calls = []

            def snapshot(self, **kwargs):
                return {'played_character': {'character_id': 901}, 'date_raw': 53144328}

            def validate_frame(self, frame, **kwargs):
                return frame

            def execute_plan(self, steps, name):
                return [{'ok': True, 'result': {'available': True, 'read_only': True,
                    'played_character_id': 901, 'date_raw': 53144328, 'rite_id': 22,
                    'faith_id': 33, 'religion_id': 44}, 'after_snapshot': self.snapshot()}]

            def root_checkpoint(self, name, request, reserve):
                self.calls.append((name, reserve))
                return {'run_id': context['run_id'], 'reviewer': '/root', 'passed': True,
                    'assertions': {key: True for key in request['required_assertions']}, 'evidence': [evidence],
                    'legacy_readback': {
                        'loaded_identity': {key: identity[key] for key in
                            ('save', 'player_id', 'date_raw', 'rite_id', 'faith_id', 'body_date')},
                        'ordinary_doctrine': {'group': 'gender', 'old': 'male', 'new': 'equal',
                            'committed': True, 'current': ['equal']},
                        'core_tenets': {'old': 'old_tenet', 'new': 'new_tenet', 'committed': True,
                            'current': ['retained_tenet', 'new_tenet']},
                        'notifications': {'observed_seconds': 10, 'recurring': False,
                            'remaining_religion_change_notifications': 0}}}

            def checkpoint(self, name, value):
                path = Path(context['output']) / (name + '.json')
                LegacyAdapterTests.write(path, value)
                return path

        return Client()

    def test_native_bound_run_one_root_checkpoint_and_verify(self):
        client = self.client()
        result = ADAPTER.run_case(self.context, client)
        self.assertTrue(result['case_contract_qualified'])
        self.assertFalse(result['strict_cold_origin_credit'])
        self.assertEqual(client.calls, [('mts-legacy-v10-edit', 900)])
        self.assertTrue(ADAPTER.verify_case(self.context)['business_pass'])
        self.assertFalse(result['product_release_pass'])
        self.evidence.write_text('{"changed":true}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'evidence/formal input changed'):
            ADAPTER.verify_case(self.context)

    def test_draft_only_and_retained_old_tenet_do_not_pass(self):
        identity = ADAPTER.legacy_input(self.context)
        response = self.client().root_checkpoint('test', {'required_assertions': []}, reserve=900)
        draft = copy.deepcopy(response)
        draft['legacy_readback']['ordinary_doctrine']['committed'] = False
        with self.assertRaisesRegex(ValueError, 'committed unique replacement'):
            ADAPTER.validate_readback(draft, identity)
        duplicate = copy.deepcopy(response)
        duplicate['legacy_readback']['core_tenets']['current'].append('old_tenet')
        with self.assertRaisesRegex(ValueError, 'removed old item'):
            ADAPTER.validate_readback(duplicate, identity)
        response['legacy_readback']['notifications']['recurring'] = True
        with self.assertRaisesRegex(ValueError, 'timed convergence'):
            ADAPTER.validate_readback(response, identity)

    def test_unavailable_native_or_changed_loaded_rite_stops_before_root(self):
        for field, value, expected in (('available', False, 'context unavailable'),
                                       ('rite_id', 999, 'differs from original legacy save')):
            with self.subTest(field=field):
                client = self.client()
                execute = client.execute_plan

                def changed(steps, name):
                    rows = execute(steps, name)
                    rows[0]['result'][field] = value
                    return rows

                client.execute_plan = changed
                with self.assertRaisesRegex(ValueError, expected):
                    ADAPTER.run_case(self.context, client)
                self.assertEqual(client.calls, [])

    def test_missing_result_and_failed_root_review_remain_red(self):
        self.assertFalse(ADAPTER.verify_case(self.context)['business_pass'])
        phase = CONTRACT['phases'][0]
        response = self.client().root_checkpoint('test', {'required_assertions': phase['requirements']}, reserve=900)
        response['passed'] = False
        with self.assertRaisesRegex(ValueError, 'incomplete or failed'):
            ADAPTER.validate_response(self.context, phase, response, '/root')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--framework-root', type=Path, required=True)
    parser.add_argument('--runtime', type=Path, required=True)
    OPTIONS = parser.parse_args()
    sys.path.insert(0, str(OPTIONS.framework_root / 'tools'))
    from ck3_mod_acceptance import Selection
    PRODUCTS = Path(__file__).with_name('acceptance_products.json')
    selected = Selection(OPTIONS.runtime, PRODUCTS, 'more-tenets-slots', 'native-legacy-v10-edit')
    ADAPTER = selected.load_adapter()
    CASE = selected.case
    CONTRACT = json.loads(Path(__file__).with_name('legacy_native_acceptance_case.json').read_text(encoding='utf-8-sig'))
    unittest.main(argv=[sys.argv[0]], verbosity=2)

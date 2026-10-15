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
            '_selected_engine': (None, {'game_version': 'offline', 'exe_sha256': 'f' * 64,
                                       'steam_build_id': 'offline'}),
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

    def candidate_inputs(self):
        from lyd_c3_checkpoint_readback.dependencies.bounded_save_parser import extract_exact_indented_block
        self.save.write_text(self.save.read_text(encoding='utf-8') +
            'faiths={\n\tdatabase={\n\t\t33={\n\t\t\treligion=44\n\t\t}\n\t}\n}\n', encoding='utf-8')
        source = ADAPTER.pin(self.save)
        self.context['saved_campaign'].update(bytes=source['bytes'], sha256=source['sha256'])
        session_path = Path(self.context['case_inputs']['legacy_session']['path'])
        session = json.loads(session_path.read_text())
        session['source_commit'] = 'a' * 40
        session['production']['manifest'].update(git_sha='a' * 40, files=[{}] * 30)
        self.write(session_path, session)
        session_pin = ADAPTER.pin(session_path)
        self.context['case_inputs']['legacy_session'] = session_pin
        text = self.save.read_text(encoding='utf-8')
        specs = {'meta': ('meta_data', 'meta_data', 0, text),
                 'played': ('played_character', 'played_character', 0, text),
                 'actor': ('living', '901', 0, text),
                 'rite': ('rites/database', '22', 2, extract_exact_indented_block(text, 'rites', 0)),
                 'faith': ('faiths/database', '33', 2, extract_exact_indented_block(text, 'faiths', 0))}
        raw = self.save.read_bytes()
        import hashlib
        records = {}
        for name, (section, key, depth, parent) in specs.items():
            body = extract_exact_indented_block(parent, key, depth).replace('\r\n', '\n').encode('utf-8')
            # write_text uses native newlines; match the actual bytes, as the real inspection does.
            if body not in raw:
                body = body.replace(b'\n', b'\r\n')
            records[name] = {'section': section, 'key': key, 'byte_start': raw.index(body),
                'bytes': len(body), 'sha256': hashlib.sha256(body).hexdigest(), 'exact_ast_consumed': True}
        published = self.root / 'published.json'
        self.write(published, {'git_sha': 'b' * 40, 'files': [{}] * 46})
        anchor = self.root / 'date-anchor.json'
        self.write(anchor, [{'ok': True, 'result': {'available': True, 'read_only': True,
            'date_raw': 53144328, 'played_character_id': 901, 'current_context': {'rite_id': 99},
            'game_version': '1.20.0.4', 'executable_sha256': 'f' * 64}, 'after_snapshot': {'date_raw': 53144328}}])
        self.context['shared_game'] = {'version': '1.20.0.4', 'exe_sha256': 'f' * 64}
        inspection = {'schema': 'mts-legacy-save-candidate-offline-inspection-v1',
            'status': 'OFFLINE_CREATE_CANDIDATE_NO_EDIT_QUALIFICATION', 'authority': 'offline-save-inspection-only',
            'live_verified': False, 'source_unchanged_after_read': True, 'no_melt_performed': True, 'source': source,
            'saved_identity': {'actor_id': 901, 'rite_id': '22', 'faith_id': '33',
                'body_date': '1066.9.15', 'meta_date': '1066.9.15'}, 'records': records,
            'product_provenance': {'session': session_pin, 'source_commit': 'a' * 40, 'mod_version': '10',
                'candidate_file_count': 30, 'published_file_count': 46, 'published_source_commit': 'b' * 40,
                'classification': 'prepublication_v10_candidate_not_the_uploaded_v10_46_file_tree',
                'historical_fixture': 'Synthetic historical flag fixture disclosure',
                'fixture_paste_receipt': ADAPTER.pin(self.evidence), 'historical_report': ADAPTER.pin(self.evidence),
                'published_release_manifest': ADAPTER.pin(published)},
            'date_raw_seed': {'value': 53144328, 'saved_calendar_date': '1066.9.15',
                'not_direct_R0008_native_date_read': True, 'seed_must_be_verified_again_after_new_process_load': True,
                'native_actor_id': 901, 'native_rite_id': 99, 'evidence': ADAPTER.pin(anchor)}}
        self.write(self.inspection, inspection)
        self.context['case_inputs']['legacy_inspection'] = ADAPTER.pin(self.inspection)
        return inspection

    def test_public_selection_and_fixed_native_budgets(self):
        from ck3_mod_acceptance import Selection
        selected = Selection(OPTIONS.runtime, Path(__file__).with_name('acceptance_products.json'),
                             'more-tenets-slots', CASE['id'])
        self.assertTrue(callable(selected.load_adapter().run_case))
        self.assertEqual(selected.case['startup']['mode'], 'saved_campaign')
        self.assertIn(ADAPTER.CONTEXT_TOOL, selected.opt_in_read_only_mcp_tools)
        for flag, expected in (('--readiness-timeout', '1800'), ('--hold-seconds', '7200'), ('--timeout', '10800')):
            self.assertEqual(selected.argv[selected.argv.index(flag) + 1], expected)

    def test_actual_public_prepare_to_selected_host_static_boundary(self):
        if OPTIONS.full_host_inputs is None:
            self.skipTest('Explicit machine inputs required for full selected-host static chain')
        from ck3_mod_acceptance import Selection
        from ck3_mod_acceptance_host_preflight import dryrun
        from ck3_mod_acceptance_prepare import write_json
        output = OPTIONS.full_host_output.resolve()
        output.mkdir(parents=True, exist_ok=False)
        inputs = json.loads(OPTIONS.full_host_inputs.read_text(encoding='utf-8-sig'))
        inputs['state_dir'] = str(output / 'state')
        inputs_path = output / 'inputs.json'
        write_json(inputs_path, inputs)
        products = Path(__file__).with_name('acceptance_products.json')
        selected = Selection(OPTIONS.runtime, products, 'more-tenets-slots', CASE['id'])
        prepared = selected.prepare(inputs_path, output / 'prepared')
        selected = Selection(OPTIONS.runtime, products, 'more-tenets-slots', CASE['id'],
                             prepared_path=Path(prepared['prepared_case']['path']))
        argv_path = output / 'static-argv.json'
        write_json(argv_path, {'schema': 'ck3-unallocated-profile-static-argv-v1',
            'argv': selected.argv, 'state_dir': str(selected.state_dir), 'launch_authority': False})
        result = dryrun(OPTIONS.runtime, argv_path, output / 'full-host-static-preflight')
        self.assertEqual(result['status'], 'PASS')
        self.assertTrue(result['actual_wrapper_profile_phase_returned'])
        self.assertFalse(result['underlying_host_main_executed'])
        self.assertFalse(result['game_started'])
        self.assertFalse(result['actual_run_profile_modified'])
        self.assertFalse(result['business_pass'])
        self.assertEqual(prepared['preparation']['runtime_status'], 'NOT_RUN')
        write_json(output / 'RESULT.actual.json', {'prepared': prepared, 'full_host_static': result,
            'runtime_status': 'NOT_RUN', 'business_pass': False})

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

    def test_standard_preparation_reaches_real_normal_exit_projection(self):
        from types import SimpleNamespace
        from ck3_mod_acceptance_normal_exit_profile import project_profile
        self.formal_inputs()
        result = ADAPTER.prepare_case(self.context)
        profile = result['profile']
        preparation = json.loads(Path(profile['preparation']['path']).read_text(encoding='utf-8-sig'))
        self.assertEqual(preparation['schema'], 'ck3-mod-acceptance-prepared-product-v1')
        self.assertEqual(preparation['game_version'], 'offline')
        self.assertEqual(preparation['exe_sha256'], 'f' * 64)
        self.assertFalse(preparation['fixture_mounted'])
        self.assertEqual(preparation['product_inventory'], profile['product_inventory'])
        self.assertFalse((self.output / 'frontend-fixture-start-policy.json').exists())
        game = self.root / 'game'
        dll, injector = self.root / 'bridge.dll', self.root / 'injector.exe'
        runtime = {'game_dir': str(game), 'paths': {'dll': str(dll), 'injector': str(injector)}}
        manifest = {'game': {'version': 'offline', 'exe_sha256': 'f' * 64}, 'native': {
            'dll': {'path_key': 'dll', 'sha256': 'a' * 64},
            'injector': {'path_key': 'injector', 'sha256': 'b' * 64}}}
        args = SimpleNamespace(state_dir=Path(self.context['state_dir']), game_dir=game,
                               bridge_dll=dll, bridge_injector=injector, output=self.root / 'host.json')
        projected, guard = project_profile(args, runtime, manifest, {}, self.root / 'binding')
        self.assertEqual(projected['userdir'], profile['profile'])
        self.assertEqual(projected['game_version'], 'offline')
        self.assertFalse(guard['launch_authority'])
        manifest['game']['exe_sha256'] = '0' * 64
        with self.assertRaisesRegex(ValueError, 'runtime identities differ'):
            project_profile(args, runtime, manifest, {}, self.root / 'different-binding')

    def test_legacy_input_rejects_wrong_player_or_changed_legacy_pin(self):
        self.context['saved_campaign']['player_id'] = 29829
        with self.assertRaisesRegex(ValueError, 'actual player records differ'):
            ADAPTER.legacy_input(self.context)
        self.context['saved_campaign']['player_id'] = 901
        self.inspection.write_text('{}', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'evidence/formal input changed'):
            ADAPTER.legacy_input(self.context)

    def test_bounded_prepublication_candidate_keeps_historical_fixture_and_credit_limits(self):
        self.candidate_inputs()
        self.formal_inputs()
        value = ADAPTER.prepare_case(self.context)
        provenance = value['legacy_identity']['product_provenance']
        self.assertEqual(provenance['candidate_file_count'], 30)
        self.assertEqual(provenance['published_file_count'], 46)
        self.assertIn('historical flag fixture', provenance['historical_fixture'])
        self.assertFalse(provenance['published_v10_compatibility_credit'])
        self.assertFalse(provenance['fresh_fixture_changes'])
        self.assertFalse(value['fixture_mounted'])
        self.assertFalse(value['business_pass'])

    def test_bounded_candidate_rejects_forged_record_and_unbound_native_anchor(self):
        inspection = self.candidate_inputs()
        original = copy.deepcopy(inspection)
        inspection['records']['actor']['sha256'] = '0' * 64
        self.write(self.inspection, inspection)
        self.context['case_inputs']['legacy_inspection'] = ADAPTER.pin(self.inspection)
        with self.assertRaisesRegex(ValueError, 'bounded record bytes changed'):
            ADAPTER.legacy_input(self.context)
        inspection = original
        inspection['date_raw_seed']['value'] += 24
        self.write(self.inspection, inspection)
        self.context['case_inputs']['legacy_inspection'] = ADAPTER.pin(self.inspection)
        with self.assertRaisesRegex(ValueError, 'same-calendar native anchor'):
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
    parser.add_argument('--full-host-inputs', type=Path)
    parser.add_argument('--full-host-output', type=Path)
    OPTIONS = parser.parse_args()
    if bool(OPTIONS.full_host_inputs) != bool(OPTIONS.full_host_output):
        parser.error('--full-host-inputs and --full-host-output must be supplied together')
    sys.path.insert(0, str(OPTIONS.framework_root / 'tools'))
    from ck3_mod_acceptance import Selection
    PRODUCTS = Path(__file__).with_name('acceptance_products.json')
    selected = Selection(OPTIONS.runtime, PRODUCTS, 'more-tenets-slots', 'native-legacy-v10-edit')
    ADAPTER = selected.load_adapter()
    CASE = selected.case
    CONTRACT = json.loads(Path(__file__).with_name('legacy_native_acceptance_case.json').read_text(encoding='utf-8-sig'))
    unittest.main(argv=[sys.argv[0]], verbosity=2)

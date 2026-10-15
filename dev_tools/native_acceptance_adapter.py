"""MTS business evidence on the selected common native runtime.

Only product fixture/data live here. The common entry owns runtime selection,
MCP transport, process/screen custody, once-only controls and normal Quit.
"""
from __future__ import annotations

import json
from pathlib import Path

from ck3_mod_acceptance_prepare import (
    finish_product_profile, materialize_fixture_profile, materialize_product_profile, pin, write_json,
)


BUDGETS = {'command_timeout': 300, 'readiness_timeout': 1800, 'timeout': 25200,
           'hold_seconds': 21600, 'poll_interval': 0.5}
QUIT_RESERVE = 900
CONTEXT_TOOL = 'ck3_query_player_religion_context_v1'


def require(value, message):
    if not value:
        raise ValueError(message)


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def checked(row):
    actual = pin(row['path'])
    require(actual == row, 'Actual evidence/formal input changed: ' + str(row['path']))
    return actual


def validate_contract(context):
    contract = case_contract(context)
    require(contract['schema'] in ('mts-native-reported-bugs-v1', 'mts-native-cold-reload-v1') and
            contract['product'] == context['product'] and contract['case'] == context['case'],
            'MTS native case identity differs')
    require(context['case_spec']['budgets'] == BUDGETS, 'Declared native case budget changed')
    require(CONTEXT_TOOL in context['case_spec']['required_mcp_tools'] and
            CONTEXT_TOOL in context['case_spec']['opt_in_read_only_mcp_tools'],
            'Religion context must be explicitly declared and read-only opted in')
    keys = [key for phase in contract['phases'] for key in phase['requirements']]
    require(len(keys) == len(set(keys)) == (4 if is_cold(context) else 8), 'Declared product facts required')


def is_cold(context):
    return context['case'] == 'native-cold-reload'


def case_contract(context):
    value = context['case_contract']
    return value['cold_case'] if is_cold(context) else value


def formal_files(inputs):
    if inputs.get('formal_manifest'):
        row = inputs['formal_manifest']
        checked(row)
        value = read(row['path'])['files']
        if isinstance(value, list):
            return {x['path']: {'bytes': x.get('bytes', x.get('size')), 'sha256': x['sha256'].lower()} for x in value}
        return {key: {'bytes': x.get('bytes', x.get('size')), 'sha256': x['sha256'].lower()} for key, x in value.items()}
    return inputs['formal_product_files']


def prepare_case(context):
    validate_contract(context)
    if is_cold(context):
        return prepare_cold(context)
    inputs, contract = context['case_inputs'], case_contract(context)
    product = Path(inputs['product_dir']).resolve()
    expected = formal_files(inputs)
    require(expected, 'Exact formal product inventory required')
    settings = Path(inputs['plain_configuration']['pdx_settings.txt']['path'])
    require('value="l_simp_chinese"' in settings.read_text(encoding='utf-8-sig'),
            'Native acceptance must use the explicit simplified-Chinese settings seed')
    fixture = Path(context['output']) / 'mts-resource-only-fixture'
    fixture.mkdir()
    (fixture / 'descriptor.mod').write_text('name="MTS native acceptance resource fixture"\nsupported_version="1.20.*"\n', encoding='utf-8')
    on_action = fixture / 'common/on_action/mtsqa_resource_start.txt'
    on_action.parent.mkdir(parents=True)
    # The common frontend selects the ordinary Robert bookmark. Only his test
    # resource budget changes; no faith/rite/doctrine/tenet/culture setter exists.
    on_action.write_text('on_game_start_after_lobby = { on_actions = { mtsqa_resource_start } }\n'
        'mtsqa_resource_start = {\n effect = {\n  every_player = {\n   limit = { is_ai = no }\n'
        '   add_piety = 100000\n   debug_log = "MTSQA: RESOURCE GRANT player"\n  }\n }\n}\n', encoding='utf-8-sig')
    write_json(fixture / '_mts_case_contract.json', contract)
    profile = materialize_fixture_profile(context, fixture, product, inputs['plain_configuration'])
    actual = {key.removeprefix('mod-content/product/'): row for key, row in profile['files'].items()
              if key.startswith('mod-content/product/')}
    require(set(actual) == set(expected) and all(all(actual[key][field] == expected[key][field]
            for field in ('bytes', 'sha256')) for key in expected), 'Mounted product differs from exact formal staging')
    initial = Path(context['output']) / 'initial-plan.json'
    write_json(initial, {'steps': []})
    return {'startup': {'mode': 'fixture', 'state_dir': profile['state_dir'],
                        'fixture_start_policy': profile['fixture_start_policy']},
            'initial_plan': pin(initial), 'profile': profile, 'formal_product_unchanged': True,
            'fixture_changes': ['player piety +100000 only'], 'runtime_status': 'NOT_RUN',
            'business_pass': False, 'product_release_pass': False}


def product_matches(profile, inputs):
    actual = {key.removeprefix('mod-content/product/'): row for key, row in profile['files'].items()
              if key.startswith('mod-content/product/')}
    expected = formal_files(inputs)
    require(set(actual) == set(expected) and all(all(actual[key][field] == expected[key][field]
        for field in ('bytes', 'sha256')) for key in expected), 'Cold formal product bytes changed')


def cold_origin(context):
    inputs = context['case_inputs']
    checked(inputs['save_origin'])
    origin = read(inputs['save_origin']['path'])
    require(origin.get('schema') == 'mts-native-save-origin-v1', 'Actual MTS save origin required')
    checked(origin['source_result'])
    source = read(origin['source_result']['path'])
    require(source['run_id'] == origin['run_id'] and source['case'] == 'native-october-reported-bugs' and
            source['case_contract_qualified'] is True and source['gui_contract_qualified'] is True,
            'Cold input must originate in the actual completed reported-bug case')
    normal_path = Path(origin['source_result']['path']).parent / 'normal-close-result.json'
    normal = read(normal_path)
    require(normal.get('normal_close_qualified') is True, 'Source case normal Quit must be complete before cold preparation')
    require(origin['runtime_manifest'] == context['runtime_manifest'] and
            origin['formal_product_files'] == formal_files(inputs), 'Cold input runtime/formal source bytes differ from save origin')
    checked(origin['save'])
    for row in origin['evidence']:
        checked(row)
    seed = context['saved_campaign']
    require(seed['player_id'] == origin['player_id'] and seed['date_raw'] == origin['date_raw'] and
            Path(seed['save']).resolve() == Path(origin['save']['path']).resolve() and
            seed['bytes'] == origin['save']['bytes'] and seed['sha256'].lower() == origin['save']['sha256'],
            'Saved-campaign input differs from actual saved origin')
    return origin, pin(normal_path)


def prepare_cold(context):
    inputs = context['case_inputs']
    origin, normal = cold_origin(context)
    profile = materialize_product_profile(context, inputs['product_dir'], inputs['plain_configuration'])
    product_matches(profile, inputs)
    settings = Path(profile['profile']) / 'pdx_settings.txt'
    require('value="l_simp_chinese"' in settings.read_text(encoding='utf-8-sig'), 'Cold profile must be simplified Chinese')
    output = Path(context['output'])
    profile = finish_product_profile(context, profile, provenance={
        'kind': 'mts-native-cold-reload', 'origin': inputs['save_origin'],
        'original_normal_close': normal})
    seed = {key: context['saved_campaign'][key] for key in ('save', 'bytes', 'sha256', 'player_id', 'date_raw')}
    seed['product_inventory'] = profile['product_inventory']['path']
    initial = output / 'initial-plan.json'
    write_json(initial, {'steps': []})
    return {'startup': {'mode': 'saved_campaign', 'state_dir': profile['state_dir'], 'saved_campaign': seed},
        'initial_plan': pin(initial), 'profile': profile, 'files': profile['files'],
        'source_origin': inputs['save_origin'], 'source_normal_close': normal,
        'runtime_status': 'NOT_RUN', 'business_contract_applicable': True,
        'business_pass': False, 'product_release_pass': False}


def observe_context(context, client, name):
    rows = client.execute_plan([{'id': name, 'tool': CONTEXT_TOOL, 'args': {},
                                'fresh_revision': True, 'continue_on_error': True}], name)
    require(len(rows) == 1 and rows[0].get('ok') is True, 'Actual native religion context query failed')
    row = rows[0]
    value = row['result']
    frame = client.validate_frame(row['after_snapshot'], allow_actor_change=True, require_event_free=False)
    require(value.get('available') is True and value.get('read_only') is True and
            value.get('played_character_id') == frame['played_character']['character_id'] and
            value.get('date_raw') == frame['date_raw'] and
            all(type(value.get(key)) is int for key in ('rite_id', 'faith_id', 'religion_id')),
            'Actual religion context unavailable or crossed its native actor/date')
    return {'row': row, 'frame': frame, 'credit': 'Native current actor/Rite/Faith/Religion/resource observation only'}


def root_phase(context, client, phase, native):
    response = client.root_checkpoint(phase['id'], {
        'product': context['product'], 'case': context['case'], 'required_assertions': phase['requirements'],
        'actual_native': native, 'instructions': phase['instructions'],
        'action_priority': 'Use available typed MCP first; record actual capability gaps before official UI fallback',
        'no_business_PASS_from_ACK': True, 'no_direct_fixture_setter_for_tested_doctrines': True,
    }, reserve=QUIT_RESERVE)
    validate_response(context, phase, response, client.operator_reviewer)
    client.checkpoint(phase['id'] + '-accepted', response)
    return response


def validate_response(context, phase, response, reviewer):
    require(response.get('run_id') == context['run_id'] and response.get('reviewer') == reviewer,
            'Actual reviewer crossed native scene')
    require(response.get('passed') is True and all(response.get('assertions', {}).get(key) is True
            for key in phase['requirements']), 'Reported-bug phase is incomplete or failed')
    require(response.get('evidence'), 'Real GUI/native/save evidence pins required')
    if not is_cold(context) and phase['id'] == 'mts-doctrines-and-tenets':
        require(response.get('initial_actor_identity_verified') is True,
                'Actual Robert name/title must be reviewed; runtime entity IDs are not fixed')
    for row in response['evidence']:
        checked(row)


def initial_actor_binding(context, client, frame):
    """Join this start's semantic bookmark with its actual runtime actor ID."""
    report = client.read_report()
    start = report['frontend_fixture_start_submission']
    result = start['result']
    selected = result['selected_candidate']
    actual = report['frontend_fixture_business_context']
    binding = actual['binding']
    expected = case_contract(context)['initial_bookmark']
    require(start.get('acknowledged') is True and result.get('pre_start_identity_proven') is True and
            all(selected.get(key) == value for key, value in expected.items()) and
            actual.get('actual_current_actor_bound') is True and actual.get('qualification_observed') is True and
            binding.get('actor_character_id') == frame['played_character']['character_id'] and
            binding.get('date_raw') == frame['date_raw'] == selected['selected_bookmark_start_date_raw'],
            'Actual initial actor differs from this native Robert start and current role binding')
    return {'selected_bookmark': selected, 'actual_binding': binding,
            'fixture_target_identity_proven': actual.get('fixture_target_identity_proven'),
            'semantic_name_and_title_review_required': True}


def run_case(context, client):
    validate_contract(context)
    contract = case_contract(context)
    before = client.snapshot(require_event_free=False)
    origin = cold_origin(context)[0] if is_cold(context) else None
    initial = None if origin else initial_actor_binding(context, client, before)
    require(not origin or before['played_character']['character_id'] == origin['player_id'],
            'Cold saved actor differs from actual save origin')
    if origin:
        process = getattr(client, '_process', None)
        require(process and process['pid'] != origin['actual_process']['pid'] and
                before['date_raw'] == origin['date_raw'], 'Cold reload must have a new actual PID and exact saved date')
    observations, phases = {}, {}
    try:
        observations['initial'] = observe_context(context, client, 'mts-native-context-initial')
        if origin:
            value = observations['initial']['row']['result']
            require(all(value.get(key) == origin[key] for key in ('rite_id', 'faith_id', 'religion_id')),
                    'Cold native religion identity differs from saved origin')
    except Exception as error:
        client.checkpoint('mts-native-context-capability-red', {'run_id': context['run_id'], 'error': repr(error),
            'native_context_pass': False, 'business_pass': False, 'original_process_replay_forbidden': True})
        client.root_checkpoint('mts-native-context-diagnostic', {'actual_snapshot': before, 'error': repr(error),
            'action': 'Retain actual process and inspect the capability RED; do not mark business/native PASS'}, reserve=QUIT_RESERVE)
        raise
    for phase in contract['phases']:
        for index, step in enumerate(contract.get('native_observations', [])):
            if step.get('phase') == phase['id']:
                require(step['tool'] in context['case_spec']['required_mcp_tools'], 'Optional MCP query must be declared in case tools')
                identifier = 'mts-extra-' + phase['id'] + '-' + str(index)
                observations[identifier] = client.execute_plan([{'id': identifier, 'tool': step['tool'],
                    'args': step.get('args', {}), 'fresh_revision': True}], identifier)
        phases[phase['id']] = root_phase(context, client, phase,
            {'observations': observations, 'saved_origin': origin} if origin else
            {'observations': observations, 'initial_actor_binding': initial})
        observations[phase['id']] = observe_context(context, client, 'mts-native-context-after-' + phase['id'])
    facts = {'schema': 'mts-native-reported-bugs-result-v1', 'run_id': context['run_id'],
        'product': context['product'], 'case': context['case'], 'contract': contract,
        'actual_initial_snapshot': before, 'actual_native_observations': observations, 'root_phases': phases,
        'initial_actor_binding': initial,
        'actual_process': getattr(client, '_process', None), 'case_contract_qualified': True,
        'gui_contract_qualified': True, 'native_credit': 'snapshot and current religion context only; extra queries retain their own actual results',
        'business_contract_applicable': True, 'business_pass': True, 'product_release_pass': False}
    if not origin:
        save = phases[contract['phases'][-1]['id']].get('save_origin')
        require(isinstance(save, dict) and save.get('evidence') and save.get('core_tenets') and
                save.get('ordinary_doctrines'), 'Save-written phase requires actual saved religion readback origin')
        checked(save['save'])
        for row in save['evidence']:
            checked(row)
        latest = observations[contract['phases'][-1]['id']]['row']['result']
        require(all(save.get(key) == latest.get('played_character_id' if key == 'player_id' else key)
            for key in ('player_id', 'date_raw', 'rite_id', 'faith_id', 'religion_id')),
            'Written save origin differs from actual final native context')
        facts['saved_origin_readback'] = save
    result_path = client.checkpoint('mts-native-case-result', facts)
    if not origin:
        client.checkpoint('mts-native-save-origin', {**save, 'schema': 'mts-native-save-origin-v1',
            'run_id': context['run_id'], 'actual_process': facts['actual_process'],
            'source_result': pin(result_path), 'runtime_manifest': context['runtime_manifest'],
            'formal_product_files': formal_files(context['case_inputs'])})
    return facts


def verify_case(context):
    validate_contract(context)
    path = Path(context['output']) / 'mts-native-case-result.json'
    if not path.is_file():
        return {'status': 'NOT_RUN_OR_INCOMPLETE', 'case_contract_qualified': False,
                'gui_contract_qualified': False, 'business_pass': False, 'product_release_pass': False}
    facts = read(path)
    require(facts['run_id'] == context['run_id'] and facts['product'] == context['product'] and
            facts['case'] == context['case'] and facts['contract'] == case_contract(context),
            'Actual result or contract crossed native case')
    for phase in case_contract(context)['phases']:
        validate_response(context, phase, facts['root_phases'][phase['id']], context.get('operator_reviewer', '/root'))
    return {**facts, 'product_release_pass': False,
            'verification_scope': 'Eight product facts with actual native observations; shared normal Quit still required'}

"""v10 saved-campaign regression data over the common native acceptance entry.

This case loads an unchanged historical save. It neither creates a fixture nor
claims the stricter new-save/new-process cold-reload contract.
"""
from __future__ import annotations

from pathlib import Path

from ck3_mod_acceptance_prepare import materialize_product_profile, pin, write_json
from inspect_ck3_save_player_topology import _player_records
from native_campaign_autoplay import read_plaintext_save
from lyd_c3_checkpoint_readback.dependencies.bounded_save_parser import (
    block_body, extract_exact_indented_block, one, parse_block,
)

from .native_acceptance_adapter import (
    BUDGETS, CONTEXT_TOOL, QUIT_RESERVE, checked, observe_context,
    product_matches, read, require, root_phase, validate_response,
)


FACTS = {'ordinary_doctrine_candidates_and_unique_replacement',
         'core_tenet_replacement_old_removed', 'notifications_converge',
         'legacy_save_identity_loaded'}


def validate_contract(context):
    contract = context['case_contract']
    require(contract.get('schema') == 'mts-native-legacy-v10-edit-v1' and
            contract.get('product') == context['product'] and
            contract.get('case') == context['case'] == 'native-legacy-v10-edit',
            'Legacy v10 case identity differs')
    require(context['case_spec']['budgets'] == BUDGETS and QUIT_RESERVE == 900,
            'Legacy case must retain the declared readiness/hold/Quit budgets')
    require(CONTEXT_TOOL in context['case_spec']['required_mcp_tools'] and
            CONTEXT_TOOL in context['case_spec']['opt_in_read_only_mcp_tools'],
            'Legacy religion context must be required and read-only opted in')
    phases = contract['phases']
    require(len(phases) == 1 and len(phases[0]['requirements']) == 4 and
            set(phases[0]['requirements']) == FACTS, 'Four legacy facts in one Root checkpoint required')


def legacy_input(context):
    """Read the full pinned plaintext save and only its bounded identity records."""
    seed, inputs = context['saved_campaign'], context['case_inputs']
    save = {'path': str(Path(seed['save']).resolve()), 'bytes': seed['bytes'],
            'sha256': seed['sha256'].lower()}
    raw, proof = read_plaintext_save(Path(save['path']))
    require(all(proof[key] == save[key] for key in save), 'Legacy saved-campaign bytes changed')
    played, current = _player_records(Path(save['path']))
    require(len(played) == 1 and played[0]['player_id'] == 1 and
            current == [played[0]['character_id']] and current == [seed['player_id']],
            'Legacy actual player records differ from the explicit saved-campaign seed')
    require(type(seed['date_raw']) is int and seed['date_raw'] > 0,
            'Legacy native date_raw must be an explicit positive seed; the text parser has no native date decoder')
    text = raw.decode('utf-8').replace('\r\n', '\n')
    # This plaintext generation writes character records at indentation zero,
    # unlike the nested Rite database. Require the numeric actor record unique.
    actor = extract_exact_indented_block(text, str(seed['player_id']), 0)
    rite_id = int(one(parse_block(block_body(actor)), 'rite', required=True))
    rites = extract_exact_indented_block(text, 'rites', 0)
    database = extract_exact_indented_block(rites, 'database', 1)
    rite = extract_exact_indented_block(database, str(rite_id), 2)
    faith_id = int(one(parse_block(block_body(rite)), 'faith', required=True))
    checked(inputs['legacy_inspection'])
    inspection = read(inputs['legacy_inspection']['path'])
    require(inspection.get('schema') == 'mts.native-text-save-inspection.v1' and
            inspection.get('authority') == 'offline-save-inspection-only' and
            inspection.get('status') == 'PASS' and inspection.get('source_unchanged') is True and
            all(inspection['source'][key] == save[key] for key in ('bytes', 'sha256')) and
            inspection['actor_id'] == seed['player_id'] and inspection['actor_current_rite_id'] == rite_id and
            inspection['rite']['id'] == rite_id and inspection['rite']['faith_id'] == faith_id,
            'Historical offline inspection differs from the actual legacy save')
    checked(inputs['legacy_session'])
    session = read(inputs['legacy_session']['path'])
    userdirs = [arg.split('=', 1)[1] for arg in session['command'] if arg.startswith('-userdir=')]
    require(str(session['production']['manifest']['mod_version']) == '10' and len(userdirs) == 1 and
            Path(save['path']).is_relative_to(Path(userdirs[0]).resolve()),
            'Legacy save must come from the pinned v10 original session profile')
    return {'save': save, 'body_date': proof['body_date'], 'meta_date': proof['meta_date'],
            'player_id': seed['player_id'], 'date_raw': seed['date_raw'],
            'rite_id': rite_id, 'faith_id': faith_id, 'inspection': inputs['legacy_inspection'],
            'source_session': inputs['legacy_session'], 'source_run_id': session['run_id'],
            'date_binding': 'Explicit native seed; actual snapshot plus Root save-date review required',
            'strict_cold_origin_credit': False, 'offline_only': True}


def prepare_case(context):
    validate_contract(context)
    identity = legacy_input(context)
    inputs = context['case_inputs']
    profile = materialize_product_profile(context, inputs['product_dir'], inputs['plain_configuration'])
    product_matches(profile, inputs)
    require('value="l_simp_chinese"' in (Path(profile['profile']) / 'pdx_settings.txt').read_text(encoding='utf-8-sig'),
            'Legacy profile must use simplified Chinese')
    output = Path(context['output'])
    preparation = output / 'profile-preparation.json'
    write_json(preparation, {'schema': 'mts-native-legacy-v10-preparation-v1', **profile,
        'legacy_identity': identity, 'runtime_status': 'NOT_RUN', 'business_pass': False})
    write_json(Path(context['state_dir']) / 'preparation.json', {
        'schema': 'ck3-mod-acceptance-profile-startup-evidence-v1',
        'profile_dir': profile['profile'], 'profile_files': list(profile['files']),
        'profile_input_sha256': {key: row['sha256'] for key, row in profile['files'].items()},
        'preparation': pin(preparation), 'runtime_status': 'NOT_RUN'})
    seed = {key: context['saved_campaign'][key] for key in ('save', 'bytes', 'sha256', 'player_id', 'date_raw')}
    seed['product_inventory'] = profile['product_inventory']['path']
    initial = output / 'initial-plan.json'
    write_json(initial, {'steps': []})
    return {'startup': {'mode': 'saved_campaign', 'state_dir': profile['state_dir'], 'saved_campaign': seed},
        'initial_plan': pin(initial), 'profile': profile, 'files': profile['files'],
        'legacy_identity': identity, 'fixture_mounted': False, 'strict_cold_origin_credit': False,
        'runtime_status': 'NOT_RUN', 'business_contract_applicable': True,
        'business_pass': False, 'product_release_pass': False}


def validate_readback(response, identity):
    """Require committed current-state evidence, beyond a selectable draft."""
    value = response.get('legacy_readback', {})
    loaded = value.get('loaded_identity', {})
    require(all(loaded.get(key) == identity[key] for key in
                ('player_id', 'date_raw', 'rite_id', 'faith_id', 'body_date', 'save')),
            'Root must bind the original legacy save identity and actual displayed date')
    ordinary = value.get('ordinary_doctrine', {})
    core = value.get('core_tenets', {})
    require(ordinary.get('group') and ordinary.get('old') and ordinary.get('new') and
            ordinary['old'] != ordinary['new'] and ordinary.get('committed') is True and
            ordinary.get('current') == [ordinary['new']],
            'Legacy ordinary doctrine needs committed unique replacement, not draft selection')
    require(core.get('old') and core.get('new') and core['old'] != core['new'] and
            core.get('committed') is True and isinstance(core.get('current'), list) and
            core['new'] in core['current'] and core['old'] not in core['current'] and
            len(core['current']) == len(set(core['current'])),
            'Legacy core tenet needs committed new item and removed old item')
    notices = value.get('notifications', {})
    require(type(notices.get('observed_seconds')) in (int, float) and notices['observed_seconds'] > 0 and
            notices.get('recurring') is False and
            type(notices.get('remaining_religion_change_notifications')) is int and
            notices['remaining_religion_change_notifications'] == 0,
            'Legacy notifications need actual timed convergence evidence')


def run_case(context, client):
    validate_contract(context)
    identity = legacy_input(context)
    before = client.snapshot(require_event_free=False)
    process = getattr(client, '_process', None)
    require(process and type(process.get('pid')) is int and process['pid'] > 0,
            'Original retained native process binding required')
    initial = observe_context(context, client, 'mts-legacy-native-context-initial')
    value = initial['row']['result']
    require(before['played_character']['character_id'] == identity['player_id'] and
            before['date_raw'] == identity['date_raw'] and
            all(value.get('played_character_id' if key == 'player_id' else key) == identity[key]
                for key in ('player_id', 'date_raw', 'rite_id', 'faith_id')),
            'Loaded native actor/date/Rite/Faith differs from original legacy save')
    phase = context['case_contract']['phases'][0]
    response = root_phase(context, client, phase, {'legacy_identity': identity,
        'initial_observation': initial, 'actual_process': process})
    validate_readback(response, identity)
    after = observe_context(context, client, 'mts-legacy-native-context-after-edits')
    require(after['row']['result']['played_character_id'] == identity['player_id'],
            'Legacy edit evidence crossed the original saved actor')
    facts = {'schema': 'mts-native-legacy-v10-result-v1', 'run_id': context['run_id'],
        'product': context['product'], 'case': context['case'], 'contract': context['case_contract'],
        'legacy_identity': identity, 'actual_initial_snapshot': before, 'actual_process': process,
        'actual_native_observations': {'initial': initial, 'after': after}, 'root_phases': {phase['id']: response},
        'case_contract_qualified': True, 'gui_contract_qualified': True,
        'native_credit': 'Actual snapshot/current religion identity only; Root evidence supplies committed edits and timed notifications',
        'strict_cold_origin_credit': False, 'business_contract_applicable': True,
        'business_pass': True, 'product_release_pass': False}
    client.checkpoint('mts-legacy-native-case-result', facts)
    return facts


def verify_case(context):
    validate_contract(context)
    path = Path(context['output']) / 'mts-legacy-native-case-result.json'
    if not path.is_file():
        return {'status': 'NOT_RUN_OR_INCOMPLETE', 'case_contract_qualified': False,
                'gui_contract_qualified': False, 'business_pass': False, 'product_release_pass': False}
    facts = read(path)
    require(facts.get('schema') == 'mts-native-legacy-v10-result-v1' and
            all(facts[key] == context[key] for key in ('run_id', 'product', 'case')) and
            facts['contract'] == context['case_contract'], 'Legacy actual result crossed its run or contract')
    identity = legacy_input(context)
    require(facts['legacy_identity'] == identity, 'Legacy source evidence changed after the run')
    phase = context['case_contract']['phases'][0]
    response = facts['root_phases'][phase['id']]
    validate_response(context, phase, response, context.get('operator_reviewer', '/root'))
    validate_readback(response, identity)
    return {**facts, 'product_release_pass': False,
            'verification_scope': 'Four historical v10 facts; shared original normal Quit/native zero still required'}

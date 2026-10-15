"""v10 saved-campaign regression data over the common native acceptance entry.

This case loads an unchanged historical save. It neither creates a fixture nor
claims the stricter new-save/new-process cold-reload contract.
"""
from __future__ import annotations

import hashlib
from pathlib import Path

from ck3_mod_acceptance_prepare import finish_product_profile, materialize_product_profile, pin, write_json
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


def candidate_inspection(context, inspection, raw, proof, rite_id, faith_id, session):
    """Validate the real bounded report; its candidate status grants no live credit."""
    seed = context['saved_campaign']
    saved = inspection['saved_identity']
    require(inspection.get('status') == 'OFFLINE_CREATE_CANDIDATE_NO_EDIT_QUALIFICATION' and
            inspection.get('live_verified') is False and inspection.get('source_unchanged_after_read') is True and
            inspection.get('no_melt_performed') is True and
            saved['actor_id'] == seed['player_id'] and int(saved['rite_id']) == rite_id and
            int(saved['faith_id']) == faith_id and saved['body_date'] == proof['body_date'] and
            saved['meta_date'] == proof['meta_date'], 'Candidate inspection identity differs from the original save')
    expected = {'meta': ('meta_data', 'meta_data'), 'played': ('played_character', 'played_character'),
                'actor': ('living', str(seed['player_id'])), 'rite': ('rites/database', str(rite_id)),
                'faith': ('faiths/database', str(faith_id))}
    require(set(inspection['records']) == set(expected), 'Complete bounded legacy records required')
    for key, (section, identity) in expected.items():
        record = inspection['records'][key]
        start, length = record['byte_start'], record['bytes']
        require(type(start) is int and type(length) is int and start >= 0 and length > 0 and
                start + length <= len(raw) and record['section'] == section and record['key'] == identity and
                record.get('exact_ast_consumed') is True, 'Candidate bounded record identity/range differs')
        body = raw[start:start + length]
        require(hashlib.sha256(body).hexdigest() == record['sha256'], 'Candidate bounded record bytes changed')
        parse_block(block_body(body.decode('utf-8')))
    provenance = inspection['product_provenance']
    require(provenance['session'] == context['case_inputs']['legacy_session'] and
            provenance['source_commit'] == session['source_commit'] == session['production']['manifest']['git_sha'] and
            provenance['mod_version'] == str(session['production']['manifest']['mod_version']) == '10' and
            provenance['candidate_file_count'] == len(session['production']['manifest']['files']) and
            provenance['classification'] == 'prepublication_v10_candidate_not_the_uploaded_v10_46_file_tree' and
            provenance.get('historical_fixture'), 'Actual prepublication v10 session provenance required')
    for key in ('fixture_paste_receipt', 'historical_report', 'published_release_manifest'):
        checked(provenance[key])
    published = read(provenance['published_release_manifest']['path'])
    require(provenance['published_file_count'] == len(published['files']) and
            provenance['published_source_commit'] == published['git_sha'] and
            provenance['source_commit'] != provenance['published_source_commit'],
            'Candidate must not claim the uploaded v10 source identity')
    anchor = inspection['date_raw_seed']
    checked(anchor['evidence'])
    require(anchor['value'] == seed['date_raw'] and anchor['saved_calendar_date'] == proof['body_date'] and
            anchor['not_direct_R0008_native_date_read'] is True and
            anchor['seed_must_be_verified_again_after_new_process_load'] is True,
            'Candidate raw date is only an explicit same-calendar native anchor')
    game = context['shared_game']
    rows = read(anchor['evidence']['path'])
    require(any(row.get('ok') is True and row.get('result', {}).get('available') is True and
                row['result'].get('read_only') is True and row['result'].get('date_raw') == seed['date_raw'] and
                row['result'].get('played_character_id') == anchor['native_actor_id'] and
                row['result'].get('current_context', {}).get('rite_id') == anchor['native_rite_id'] and
                row['result'].get('game_version') == game['version'] and
                row['result'].get('executable_sha256', '').lower() == game['exe_sha256'].lower() and
                row.get('after_snapshot', {}).get('date_raw') == seed['date_raw'] for row in rows),
            'Actual selected-build native raw-date anchor unavailable')
    return {**provenance, 'date_raw_anchor': anchor,
            'published_v10_compatibility_credit': False, 'fresh_fixture_changes': False}


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
    require(inspection.get('authority') == 'offline-save-inspection-only' and
            all(inspection['source'][key] == save[key] for key in ('bytes', 'sha256')),
            'Historical offline inspection differs from the actual legacy save')
    checked(inputs['legacy_session'])
    session = read(inputs['legacy_session']['path'])
    userdirs = [arg.split('=', 1)[1] for arg in session['command'] if arg.startswith('-userdir=')]
    require(str(session['production']['manifest']['mod_version']) == '10' and len(userdirs) == 1 and
            Path(save['path']).is_relative_to(Path(userdirs[0]).resolve()),
            'Legacy save must come from the pinned v10 original session profile')
    schema = inspection.get('schema')
    if schema == 'mts.native-text-save-inspection.v1':
        require(inspection.get('status') == 'PASS' and inspection.get('source_unchanged') is True and
                inspection['actor_id'] == seed['player_id'] and inspection['actor_current_rite_id'] == rite_id and
                inspection['rite']['id'] == rite_id and inspection['rite']['faith_id'] == faith_id,
                'Historical offline inspection differs from the actual legacy save')
        provenance = {'classification': 'historical-v10-session', 'source_commit': session.get('source_commit')}
    elif schema == 'mts-legacy-save-candidate-offline-inspection-v1':
        provenance = candidate_inspection(context, inspection, raw, proof, rite_id, faith_id, session)
    else:
        raise ValueError('Unsupported actual legacy inspection schema')
    return {'save': save, 'body_date': proof['body_date'], 'meta_date': proof['meta_date'],
            'player_id': seed['player_id'], 'date_raw': seed['date_raw'],
            'rite_id': rite_id, 'faith_id': faith_id, 'inspection': inputs['legacy_inspection'],
            'source_session': inputs['legacy_session'], 'source_run_id': session['run_id'],
            'product_provenance': provenance,
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
    profile = finish_product_profile(context, profile, provenance={
        'kind': 'unchanged-historical-v10-save-and-exact-formal-product',
        'legacy_identity': identity, 'strict_cold_origin_credit': False})
    output = Path(context['output'])
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

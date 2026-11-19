"""Generate and build the independent Potential Output map product.

Machine paths and the interpreter are supplied by the caller. Structural parsing,
reversible native projection, localization parsing and deterministic packaging
come from ck3_eternal_recurrence. Structural checks do not certify engine scopes.
"""

from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import struct
import sys

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = "mod_potential_output"
MOD = ROOT / PRODUCT
VERSION = "0.1.0"
CONTRACT = Path(__file__).with_name("potential_output_sources.json")
LOCALIZATION = Path(__file__).with_name("potential_output_localization.json")
NATIVE_FILES = (
    "gui/map_icon_layer.gui",
    "gfx/map/map_modes/map_modes.txt",
    "common/trade/trade_good_types/basic_trade_goods.txt",
    "common/trade/trade_good_categories/01_need_type_trade_good_categories.txt",
    "common/trade/county_potential_trade_goods/county_potential_trade_goods.txt",
    "gui/window_activity_planner.gui",
    "gui/window_activity_list.gui",
)
ACTIVITY = "activity_xapo_potential_output"
ACTIVE = f"And( IsGameViewOpen( 'activity_planner' ), EqualTo_string( ActivityPlanner.GetActivityType.GetKey, '{ACTIVITY}' ) )"


def projections(game: Path) -> dict[str, list[tuple[str, str]]]:
    from ck3_text_projection import blocks, named_block

    source = native_text(game, NATIVE_FILES[0])
    block = named_block(source, "widget", "activity_planner_widget")
    old = source[block.start:block.end]
    anchor = '\tflowcontainer = {\n'
    added = ('\txapo_county_potential_icons = {}\n\n' + anchor +
             f'\t\tvisible = "[Not( EqualTo_string( ActivityType.GetKey, \'{ACTIVITY}\' ) )]"\n')
    new = old.replace(anchor, added, 1)
    planner = native_text(game, NATIVE_FILES[5])
    planner_block = named_block(planner, "window", "activity_planner")
    planner_old = planner[planner_block.start:planner_block.end]
    body_start = next(b.end for b in blocks(planner_old) if b.key == 'state' and re.match(r'\s*name\s*=\s*_hide\b', planner_old[b.opening + 1:b.end]))
    planner_header = planner_old[:body_start].replace('using = Animation_FadeOut_Quick', 'using = Animation_FadeOut_Quick\n        on_start = "[GetScriptedGui( \'xapo_reset_filters\' ).Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"', 1)
    planner_new = planner_header + f'''
    xapo_goods_panel = {{}}
    xapo_view_controls = {{}}
    widget = {{
        name = "xapo_native_planner_content"
        size = {{ 100% 100% }}
        alwaystransparent = yes
        visible = "[Not( EqualTo_string( ActivityType.GetKey, '{ACTIVITY}' ) )]"
''' + planner_old[body_start:-1] + '\n    }\n}'
    host_source = native_text(game, NATIVE_FILES[6])
    host_block = named_block(host_source, "window", "activity_list_detail_host")
    host_old = host_source[host_block.start:host_block.end]
    host_anchor = '\t vbox = {'.replace('\t ', '\t')
    host_new = host_old.replace(host_anchor, f'''    xapo_host_intro = {{}}
{host_anchor}
        visible = "[Not( EqualTo_string( ActivityListDetailHostView.GetType.GetKey, '{ACTIVITY}' ) )]"''', 1)
    return {NATIVE_FILES[0]: [(old, new)], NATIVE_FILES[5]: [(planner_old, planner_new)],
            NATIVE_FILES[6]: [(host_old, host_new)]}



def framework_tools(framework: Path) -> None:
    if not (framework / "tools/ck3_text_projection.py").is_file():
        raise ValueError("framework directory has no ck3_text_projection.py")
    sys.path.insert(0, str(framework / "tools"))


def native_text(game: Path, relative: str) -> str:
    from ck3_text_projection import digest, normalize

    source = normalize((game / "game" / relative).read_text(encoding="utf-8-sig"))
    expected = json.loads(CONTRACT.read_text(encoding="utf-8"))["native_text_sha256"]
    if digest(source) != expected[relative]:
        raise ValueError(f"native source changed; review before regenerating: {relative}")
    return source


def catalog(game: Path) -> tuple[list[str], set[str], list[tuple[str, list[str]]]]:
    from ck3_text_projection import blocks, masked

    text = native_text(game, NATIVE_FILES[2])
    goods: list[str] = []
    basic: set[str] = set()
    for block in blocks(text):
        if not block.key.startswith("trade_good_"):
            continue
        goods.append(block.key)
        if re.search(r"\bis_basic\s*=\s*yes\b", masked(text[block.opening:block.end])):
            basic.add(block.key)
    categories: list[tuple[str, list[str]]] = []
    categories_text = native_text(game, NATIVE_FILES[3])
    assigned: list[str] = []
    for block in blocks(categories_text):
        if not block.key.startswith("trade_category_"):
            continue
        body = categories_text[block.opening + 1:block.end - 1]
        trade = [b for b in blocks(body) if b.key == "trade_goods"]
        if len(trade) != 1:
            raise ValueError(f"expected one trade_goods list: {block.key}")
        members = re.findall(r"\btrade_good_\w+\b", masked(body[trade[0].opening:trade[0].end]))
        if len(members) > 1:
            categories.append((block.key, members))
            assigned.extend(members)
    if len(set(goods)) != len(goods) or not goods:
        raise ValueError("native goods must be nonempty and unique")
    if len(set(assigned)) != len(assigned) or not set(assigned) <= set(goods):
        raise ValueError("native need categories overlap or reference unknown goods")
    potential = {block.key for block in blocks(native_text(game, NATIVE_FILES[4]))}
    goods = [good for good in goods if good in potential]
    basic &= set(goods)
    categories = [(key, [good for good in members if good in potential]) for key, members in categories]
    categories.append(("xapo_misc", [good for good in goods if good not in assigned]))
    return goods, basic, categories


def hidden_key(good: str) -> str:
    # Both getters were confirmed by this build's dump_data_types. The native
    # text-icon token identifies the good independently of language or markup.
    return f"Concatenate( 'xapo_hidden_', GetTradeGoodType( '{good}' ).GetTextIconNoFormat )"


def is_hidden(good: str) -> str:
    return f"GetVariableSystem.HasValue( {hidden_key(good)}, 'yes' )"


def conjunction(expressions: list[str]) -> str:
    if not expressions:
        raise ValueError("empty conjunction")
    result = expressions[-1]
    for expression in reversed(expressions[:-1]):
        result = f"And( {expression}, {result} )"
    return result


def set_goods(goods: list[str], value: str, sync: bool = True) -> str:
    actions = "\n".join(
        f'\t\t\t\t\tonclick = "[GetVariableSystem.Set( {hidden_key(good)}, {value} )]"\n' +
        (f'\t\t\t\t\tonclick = "[{sync_good(good)}]"' if sync else '')
        for good in goods
    )
    if sync:
        actions += '\n                    onclick = "[GetVariableSystem.Toggle( \'xapo_refresh\' )]"'
    return actions


def sync_good(good: str) -> str:
    return (f"GetScriptedGui( Select_CString( {is_hidden(good)}, 'xapo_hide_{good}', 'xapo_show_{good}' ) )"
            ".Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )")


def count_context(goods: list[str]) -> str:
    return "GuiScope.SetRoot( County.GetTitle.MakeScope ).AddScope( 'host', GetPlayer.MakeScope )"


def filter_effects(goods: list[str]) -> str:
    effects = []
    for good in goods:
        effects.append(f"xapo_hide_{good} = {{ scope = character effect = {{ set_variable = {{ name = xapo_hidden_{good} value = 1 }} }} }}")
        effects.append(f"xapo_show_{good} = {{ scope = character effect = {{ remove_variable = xapo_hidden_{good} }} }}")
    effects.append("xapo_reset_filters = { scope = character effect = {\n" + "\n".join(f"    remove_variable = xapo_hidden_{good}" for good in goods) + "\n} }\n")
    return "\n".join(effects)


def empty_option_texture() -> bytes:
    # Original transparent 4x4 DDS: the invisible refresh choices need valid
    # engine texture slots. No native or third-party bitmap bytes are copied.
    header = [124, 0x100f, 4, 4, 16, 0, 0] + [0] * 11
    header += [32, 0x41, 0, 32, 0xff0000, 0xff00, 0xff, 0xff000000]
    header += [0x1000, 0, 0, 0, 0]
    return b"DDS " + struct.pack("<31I", *header) + bytes(64)


def good_button(good: str) -> str:
    return f"""
            button_standard = {{
                name = "xapo_toggle_{good}"
                size = {{ 40 40 }}
                tooltip = "{good}"
                using = tooltip_ne
                down = "[Not( {is_hidden(good)} )]"
                onclick = "[GetVariableSystem.Set( {hidden_key(good)}, Select_CString( {is_hidden(good)}, 'no', 'yes' ) )]"
                onclick = "[{sync_good(good)}]"
                onclick = "[GetVariableSystem.Toggle( 'xapo_refresh' )]"
                icon = {{
                    size = {{ 32 32 }}
                    parentanchor = center
                    alwaystransparent = yes
                    texture = "gfx/interface/icons/trade/trade_goods/{good}.dds"
                    alpha = "[Select_float( {is_hidden(good)}, '(float)0.25', '(float)1' )]"
                }}
            }}
"""


def category_row(key: str, members: list[str], basic_section: bool) -> str:
    all_selected = conjunction([f"Not( {is_hidden(g)} )" for g in members])
    group_id = f"{key}_{'basic' if basic_section else 'other'}"
    return f"""
        hbox = {{
            name = "xapo_group_{group_id}"
            spacing = 3
            margin_bottom = 3
            button_tertiary = {{
                name = "xapo_group_toggle_{group_id}"
                size = {{ 64 40 }}
                text = "{key}"
                tooltip = "{key}"
                onclick = "[GetVariableSystem.Set( 'xapo_batch_hide', Select_CString( {all_selected}, 'yes', 'no' ) )]"
{set_goods(members, "GetVariableSystem.Get( 'xapo_batch_hide' )")}
            }}
            flowcontainer = {{
                wrap_count = 5
                spacing = 3
{''.join(good_button(g) for g in members)}
            }}
        }}
"""


def panel(goods: list[str], basic: set[str], categories: list[tuple[str, list[str]]]) -> str:
    sections: list[str] = []
    for basic_section in (True, False):
        rows = []
        for key, members in categories:
            selected = [g for g in members if (g in basic) == basic_section]
            if selected:
                rows.append(category_row(key, selected, basic_section))
        sections.append(f"""
            text_single = {{
                text = "{'xapo_basic' if basic_section else 'xapo_other'}"
                margin_top = 8
                margin_bottom = 6
                layoutpolicy_horizontal = expanding
                align = center|nobaseline
                using = Font_Size_Medium
            }}
            {''.join(rows)}
        """)
    return f"""# GENERATED by dev_tools/potential_output.py; edit the generator.
window = {{
    name = "xapo_map_launcher"
    layer = middle
    parentanchor = bottom|right
    position = {{ -184 -112 }}
    size = {{ 140 36 }}
    movable = no
    visible = "[And( GetPlayer.IsValid, CanChangeMapMode )]"
    alwaystransparent = yes

    button_standard = {{
        name = "xapo_open_map"
        size = {{ 100% 100% }}
        text = "xapo_potential_output"
        tooltip = "xapo_potential_output_desc"
        onclick = "[GetVariableSystem.Set( 'xapo_previous_mapmode', GetCurrentMapMode.GetKey )]"
        onclick = "[GetVariableSystem.Clear( 'xapo_panel_collapsed' )]"
{set_goods(goods, "'no'", sync=False)}
        onclick = "[GetScriptedGui( 'xapo_reset_filters' ).Execute( GuiScope.SetRoot( GetPlayer.MakeScope ).End )]"
        onclick = "[GetVariableSystem.Clear( 'xapo_refresh' )]"
        onclick = "[OpenGameViewData( 'activity_list_detail_host_window', GetActivityType( '{ACTIVITY}' ).Self )]"
    }}

}}

types XapoPotentialOutput {{
    type xapo_host_intro = vbox {{
        using = Window_Margins
        spacing = 20
        visible = "[EqualTo_string( ActivityListDetailHostView.GetType.GetKey, '{ACTIVITY}' )]"
        header_pattern = {{
            layoutpolicy_horizontal = expanding
            blockoverride "header_text" {{ text = "xapo_potential_output" }}
            blockoverride "button_close" {{ onclick = "[ActivityListDetailHostView.Close]" }}
        }}
        text_multi = {{
            text = "xapo_potential_output_desc"
            max_width = 550
            autoresize = yes
        }}
        button_primary = {{
            name = "xapo_show_map"
            size = {{ 380 50 }}
            text = "xapo_show_map"
            onclick = "[ActivityListDetailHostView.Confirm]"
        }}
    }}
type xapo_goods_panel = widget {{
    name = "xapo_goods_panel"
    layer = middle
    parentanchor = top|right
    position = {{ -16 100 }}
    size = {{ 330 640 }}
    visible = "[And( {ACTIVE}, Not( GetVariableSystem.Exists( 'xapo_panel_collapsed' ) ) )]"
    using = Window_Background
    background = {{ using = Background_Area_Dark }}

    vbox = {{
        margin = {{ 14 14 }}
        layoutpolicy_horizontal = expanding
        layoutpolicy_vertical = expanding
        spacing = 5
        hbox = {{
            layoutpolicy_horizontal = expanding
            text_single = {{
                text = "xapo_potential_output"
                using = Font_Size_Medium
            }}
            expand = {{}}
            button_tertiary = {{
                name = "xapo_collapse_panel"
                size = {{ 28 28 }}
                raw_text = "-"
                tooltip = "xapo_panel"
                onclick = "[GetVariableSystem.Toggle( 'xapo_panel_collapsed' )]"
            }}
            button_close = {{
                name = "xapo_exit_map"
                size = {{ 28 28 }}
                tooltip = "xapo_exit"
                onclick = "[CloseGameView( 'activity_planner' )]"
                onclick = "[SetMapMode( Select_CString( GetVariableSystem.Exists( 'xapo_previous_mapmode' ), GetVariableSystem.Get( 'xapo_previous_mapmode' ), 'realms' ) )]"
            }}
        }}
        text_multi = {{
            text = "xapo_hint"
            max_width = 298
            autoresize = yes
            default_format = "#weak"
            using = Font_Size_Small
        }}
        hbox = {{
            spacing = 8
            button_standard = {{
                name = "xapo_select_all"
                size = {{ 142 32 }}
                text = "xapo_all"
{set_goods(goods, "'no'")}
            }}
            button_standard = {{
                name = "xapo_clear_all"
                size = {{ 142 32 }}
                text = "xapo_none"
{set_goods(goods, "'yes'")}
            }}
        }}
        text_single = {{
            name = "xapo_no_goods_selected"
            text = "xapo_empty"
            visible = "[{conjunction([is_hidden(g) for g in goods])}]"
            default_format = "#high"
            layoutpolicy_horizontal = expanding
            align = center|nobaseline
        }}
        scrollbox = {{
            name = "xapo_goods_scroll"
            layoutpolicy_horizontal = expanding
            layoutpolicy_vertical = expanding
            blockoverride "scrollbox_content" {{
                vbox = {{
                    layoutpolicy_horizontal = expanding
                    {''.join(sections)}
                }}
            }}
        }}
        text_multi = {{
            text = "xapo_scope"
            max_width = 298
            autoresize = yes
            default_format = "#weak"
            using = Font_Size_Small
        }}
        text_multi = {{
            text = "xapo_legend"
            max_width = 298
            autoresize = yes
            using = Font_Size_Small
        }}
    }}
}}

    type xapo_view_controls = widget {{
        parentanchor = bottom|right
        position = {{ -200 -112 }}
        size = {{ 160 36 }}
        visible = "[{ACTIVE}]"
        hbox = {{
            size = {{ 8 4 }}
            alwaystransparent = yes
            datacontext = "[GetActivityType( '{ACTIVITY}' ).GetOptionCategoryByKey( 'special_type' )]"
            datamodel = "[ActivityOptionCategory.GetOptions]"
            item = {{
                widget = {{
                    size = {{ 4 4 }}
                    alwaystransparent = yes
                    state = {{
                        name = "xapo_refresh_scores"
                        trigger_when = "[And( EqualTo_string( ActivityPlanner.GetActivityType.GetKey, '{ACTIVITY}' ), EqualTo_int32( ActivityOption.GetIndexInCategory, Select_int32( GetVariableSystem.Exists( 'xapo_refresh' ), '(int32)1', '(int32)0' ) ) )]"
                        duration = 0.3
                        position_x = 1
                        on_finish = "[ActivityPlanner.OpenSpecialOptionSelection]"
                        on_finish = "[ActivityPlanner.SelectOption( ActivityOption.Self )]"
                        on_finish = "[ActivityPlanner.StartLocationPicking]"
                    }}
                }}
            }}
        }}
        button_standard = {{
            size = {{ 120 36 }}
            text = "xapo_potential_output"
            onclick = "[GetVariableSystem.Toggle( 'xapo_panel_collapsed' )]"
        }}
        button_close = {{
            position = {{ 126 4 }}
            size = {{ 28 28 }}
            shortcut = "close_window"
            tooltip = "xapo_exit"
            onclick = "[CloseGameView( 'activity_planner' )]"
            onclick = "[SetMapMode( Select_CString( GetVariableSystem.Exists( 'xapo_previous_mapmode' ), GetVariableSystem.Get( 'xapo_previous_mapmode' ), 'realms' ) )]"
        }}
    }}
    type xapo_county_potential_icons = flowcontainer {{
        name = "xapo_county_potential_icons"
        parentanchor = center
        position = {{ 0 -30 }}
        direction = vertical
        allow_outside = yes
        ignoreinvisible = yes
        visible = "[And( EqualTo_string( ActivityPlannerMapIcon.GetActivityType.GetKey, '{ACTIVITY}' ), And( LessThan_int32( GetZoomLevel, '(int32)10' ), ObjectsEqual( ActivityPlannerMapIcon.GetProvince, ActivityPlannerMapIcon.GetProvince.GetCountyCapitalProvince ) ) )]"
        datacontext = "[ActivityPlannerMapIcon.GetProvince.GetCounty]"
        datacontext = "[{count_context(goods)}]"

        text_single = {{
            raw_text = "[County.GetTitle.GetNameNoTooltip] ([TopScope.ScriptValue( 'xapo_selected_potential_count' )|0])"
            using = Font_Size_Small
        }}

        flowcontainer = {{
            name = "xapo_filtered_potential_goods"
            datamodel = "[County.GetPotentialTradeGoodTypes]"
            wrap_count = 6
            spacing = 1
            ignoreinvisible = yes
            item = {{
                icon = {{
                    name = "xapo_potential_good"
                    visible = "[Not( GetVariableSystem.HasValue( Concatenate( 'xapo_hidden_', TradeGoodType.GetTextIconNoFormat ), 'yes' ) )]"
                    size = {{ 26 26 }}
                    texture = "[TradeGoodType.GetSmallIcon]"
                    tooltipwidget = trade_good_type_tooltip
                    using = tooltip_ne
                    background = {{ using = Background_Area_Dark }}
                }}
            }}
        }}
    }}
}}
"""


def activity_type(goods: list[str]) -> str:
    return f"""# Display-only planner. Never exposed as a hostable activity.
{ACTIVITY} = {{
    is_shown = {{ always = no }}
    can_plan = {{ always = yes }}
    can_start = {{ always = no }}
    can_always_plan = yes
    is_valid = {{ always = no }}
    province_filter = all
    ai_province_filter = capital
    is_location_valid = {{ exists = county }}
    province_score = {{
        value = 0
        if = {{ limit = {{ exists = county }} county = {{ add = xapo_selected_potential_count }} }}
    }}
    special_option_category = special_type
    options = {{
        special_type = {{
            xapo_refresh_a = {{ default = yes }}
            xapo_refresh_b = {{}}
        }}
    }}
    max_guests = 1
    can_be_activity_guest = {{ always = no }}
    host_intents = {{ default = survey_overseer_intent intents = {{ survey_overseer_intent }} }}
    guest_intents = {{ default = survey_learning_intent_guest intents = {{ survey_learning_intent_guest }} }}
    header_background = "gfx/interface/illustrations/event_scenes/bp2_courtyard.dds"
    phases = {{
        phase_surveying = {{
            is_predefined = yes
            is_valid = {{ always = yes }}
        }}
    }}
    ai_check_interval_by_tier = {{ barony = 0 county = 0 duchy = 0 kingdom = 0 empire = 0 hegemony = 0 }}
    ai_will_do = {{ value = 0 }}
}}
"""


def count_value(goods: list[str]) -> str:
    return "xapo_selected_potential_count = {\n    value = 0\n" + "\n".join(
        f"    if = {{ limit = {{ has_potential_for_trade_good = trade_good_type:{good} scope:host = {{ NOT = {{ has_variable = xapo_hidden_{good} }} }} }} add = 1 }}"
        for good in goods
    ) + "\n}\n"


def generated(game: Path) -> dict[str, bytes]:
    from ck3_text_projection import project

    for relative in NATIVE_FILES:
        native_text(game, relative)
    goods, basic, categories = catalog(game)
    source = native_text(game, NATIVE_FILES[0])
    sha = json.loads(CONTRACT.read_text())["native_text_sha256"][NATIVE_FILES[0]]
    files = {
        "descriptor.mod": ('version="' + VERSION + '"\n'
                           'tags={ "Utilities" "Interface" }\n'
                           'name="Potential Output (XA)"\n'
                           'supported_version="1.21.*"\n'),
        "gui/map_icon_layer.gui": project(source, sha, projections(game)[NATIVE_FILES[0]]),
        "gui/xapo_potential_output.gui": panel(goods, basic, categories),
        "gui/scripted_widgets/xapo_potential_output.txt":
            "gui/xapo_potential_output.gui = xapo_map_launcher\n",
        "common/activities/activity_types/xapo_potential_output.txt": activity_type(goods),
        "common/script_values/xapo_potential_output.txt": count_value(goods),
        "common/scripted_guis/xapo_potential_output.txt": filter_effects(goods),
        "common/defines/graphic/zz_xapo_potential_output.txt":
            "# Shared activity score presentation palette; no gameplay values.\n"
            "NMapModes = {\n"
            "    ACTIVITY_PLANNER_SCORE_LOW = { 0.78 0.80 0.82 1 }\n"
            "    ACTIVITY_PLANNER_SCORE_HIGH = { 0.04 0.22 0.10 1 }\n"
            "}\n",
    }
    for relative, replacements in projections(game).items():
        files[relative] = project(native_text(game, relative), json.loads(CONTRACT.read_text())["native_text_sha256"][relative], replacements)
    output = {name: text.encode("utf-8-sig") for name, text in files.items()}
    for option in ("xapo_refresh_a", "xapo_refresh_b"):
        for directory in ("gfx/interface/icons/activity_types", "gfx/interface/illustrations/activity_types"):
            output[f"{directory}/{option}.dds"] = empty_option_texture()
    localizations = json.loads(LOCALIZATION.read_text(encoding="utf-8"))
    for language, entries in localizations.items():
        lines = [f"l_{language}:"]
        lines.extend(f" {key}:0 {json.dumps(value, ensure_ascii=False)}" for key, value in entries.items())
        output[f"localization/{language}/xapo_l_{language}.yml"] = ("\n".join(lines) + "\n").encode("utf-8-sig")
    return output


def validate(framework: Path, game: Path) -> dict:
    framework_tools(framework)
    from ck3_text_projection import blocks, recover
    from ck3_installation import installed_game_version
    from translate_localization_minimax import parse_ck3_localization

    version = installed_game_version(game / "binaries/ck3.exe")
    expected_version = json.loads(CONTRACT.read_text())["game_version"]
    if version != expected_version:
        raise ValueError(f"game version differs: {version} != {expected_version}")
    expected = generated(game)
    actual = {p.relative_to(MOD).as_posix(): p.read_bytes() for p in MOD.rglob("*") if p.is_file()}
    if expected != actual:
        raise ValueError("product differs from generated allowlist; run generate")
    for relative, data in expected.items():
        if relative.endswith((".gui", ".txt", ".mod")):
            blocks(data.decode("utf-8-sig"))
    for relative, replacements in projections(game).items():
        sha = json.loads(CONTRACT.read_text())["native_text_sha256"][relative]
        recover(actual[relative].decode("utf-8-sig"), sha, replacements)
    goods, _, _ = catalog(game)
    for good in goods:
        if not (game / f"game/gfx/interface/icons/trade/trade_goods/{good}.dds").is_file():
            raise ValueError(f"missing native icon: {good}")
    baseline = None
    for language in json.loads(LOCALIZATION.read_text(encoding="utf-8")):
        path = MOD / f"localization/{language}/xapo_l_{language}.yml"
        entries = parse_ck3_localization(path)
        if path.read_text(encoding="utf-8-sig").splitlines()[0] != f"l_{language}:":
            raise ValueError(f"invalid localization header: {language}")
        if baseline is None:
            baseline = set(entries)
        if set(entries) != baseline or not all(entries.values()) or any(re.search(r"\?{2}", value) for value in entries.values()):
            raise ValueError(f"localization coverage differs: {language}")
    return {"status": "structural-static-pass", "game_version": version,
            "files": len(expected), "goods": len(goods),
            "languages": list(json.loads(LOCALIZATION.read_text(encoding="utf-8"))),
            "native_projection_reversible": True, "live_verified": False,
            "scope_validation": "requires CK3 engine acceptance"}


def build(framework: Path, game: Path, destination: Path, revision: str) -> dict:
    validate(framework, game)
    from build_release import create_manifest, manifest_bytes, write_deterministic_zip

    if destination.exists():
        raise ValueError("build destination must be new")
    staging = destination / PRODUCT
    staging.mkdir(parents=True)
    for relative, data in generated(game).items():
        target = staging / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(data)
    manifest = create_manifest(staging, revision, VERSION)
    # The framework helper defaults to its own published product. This is a new
    # independent mod; never inherit its Workshop identity.
    manifest["workshop_item_id"] = None
    manifest["product"] = PRODUCT
    path = destination / f"{PRODUCT}.manifest.json"
    path.write_bytes(manifest_bytes(manifest))
    archive = destination / f"{PRODUCT}.zip"
    write_deterministic_zip(staging, archive, manifest)
    return {"manifest": manifest, "zip_sha256": hashlib.sha256(archive.read_bytes()).hexdigest()}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("mode", choices=("generate", "validate", "build"))
    parser.add_argument("--framework", type=Path, required=True)
    parser.add_argument("--game", type=Path, required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    framework_tools(args.framework)
    if args.mode == "generate":
        for relative, data in generated(args.game).items():
            target = MOD / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
    report = validate(args.framework, args.game)
    if args.mode == "build":
        if args.output is None:
            parser.error("build requires --output")
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
        report["build"] = build(args.framework, args.game, args.output, revision)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

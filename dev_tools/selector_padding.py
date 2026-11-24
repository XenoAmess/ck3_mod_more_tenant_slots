"""Generate inert doctrine metadata for CK3's shared selector index.

These are doctrines, never core tenets. Empty native tenet slots remain empty.
"""

from pathlib import Path


COUNT = 100
HEADER = "# GENERATED FILE - MTS native selector index compatibility\n"
# Frozen from CK3 1.20.0.3 launcher/settings-layout.json and game/localization.
# The launcher language provider owns this list; jomini is an engine directory.
LANGUAGES = ("english", "french", "german", "japanese", "korean", "polish",
             "russian", "simp_chinese", "spanish")


EDIT_TENET_LISTS = ("added_tenets", "removed_tenets", "changed_tenet_status")


def edit_padding() -> tuple[str, str, str, list[str]]:
    """Give the native EditRite reader a valid key for each vacant draft slot."""
    keys = [f"tenet_mts_edit_blank_{slot:03}" for slot in range(1, COUNT + 1)]
    definitions = HEADER + "".join(
        f"{key} = {{\n"
        "\ticon = { reference = tenet_peace_of_god }\n"
        "\tvisible = no\n"
        "\tpiety_cost = { value = 0 }\n"
        "\tdivergence_multiplier = 0\n"
        "\tis_shown = { always = no }\n"
        "\tcan_pick = { always = no }\n"
        "\tcan_pick_as_personal_tenet = { always = no }\n"
        "}\n"
        for key in keys
    )
    fill = "".join(
        "\tif = {\n"
        f"\t\tlimit = {{ NOT = {{ any_rite_tenet = {{ count >= {COUNT} }} }} "
        f"NOT = {{ rite_has_tenet = {key} }} }}\n"
        f"\t\tadd_rite_tenet = tenet:{key}\n"
        "\t}\n"
        for key in keys
    )
    cleanup = "".join(
        f"\tif = {{ limit = {{ rite_has_tenet = {key} }} "
        f"remove_rite_tenet = tenet:{key} }}\n"
        for key in keys
    )
    effects = (
        "\nmts_fill_edit_blanks_effect = {\n" + fill + "}\n"
        "\nmts_remove_edit_blanks_effect = {\n" + cleanup + "}\n"
    )
    triggers = (
        "\nmts_is_edit_blank_trigger = {\n\tOR = {\n"
        + "".join(f"\t\tthis = tenet:{key}\n" for key in keys)
        + "\t}\n}\n"
    )
    localization = [
        f' {key}_{suffix}:0 ""\n' for key in keys for suffix in ("name", "desc")
    ]
    return definitions, effects, triggers, localization


def generated_files() -> dict[str, str]:
    files = {}
    effects = []
    definitions, edit_effects, edit_triggers, localization = edit_padding()
    files["common/religion/tenet_types/mts_edit_blanks.txt"] = definitions
    for shard in range(10):
        groups, doctrines = [], []
        for slot in range(shard * 10 + 1, shard * 10 + 11):
            group = f"mts_selector_group_{slot:03}"
            doctrine = f"mts_selector_doctrine_{slot:03}"
            # Native metadata resolves these keys even for invisible doctrines.
            # Empty text keeps internal selector metadata out of player content.
            localization.extend((f' {group}_name:0 ""\n',
                                 f' {doctrine}_name:0 ""\n',
                                 f' {doctrine}_desc:0 ""\n'))
            groups.append(f"{group} = {{\n\tcategory = not_creatable\n"
                          "\tdivergence = category\n\tdoctrine_lock = none\n"
                          "\tis_available_on_create = { always = yes }\n}\n")
            doctrines.append(f"{doctrine} = {{\n\tdoctrine_group_type = {group}\n"
                             "\tvisible = no\n\tdivergence = 0\n"
                             "\tpiety_cost = { value = 0 }\n}\n")
            effects.append("\tif = {\n\t\tlimit = { NOT = { rite_has_doctrine = " +
                           doctrine + " } }\n\t\tchange_rite_doctrine = " + doctrine + "\n\t}\n")
        files[f"common/religion/doctrine_group_types/mts_selector_{shard:02}.txt"] = (
            HEADER + "\n".join(groups))
        files[f"common/religion/doctrine_types/mts_selector_{shard:02}.txt"] = (
            HEADER + "\n".join(doctrines))
    files["common/scripted_effects/mts_selector.txt"] = (
        HEADER + "mts_prepare_selector_rite_effect = {\n" + "".join(effects) + "}\n" + edit_effects)
    files["common/scripted_guis/mts_selector.txt"] = HEADER + """mts_prepare_selector_gui = {
    scope = character
    saved_scopes = { mts_rite }
    effect = {
        if = {
            limit = { is_ai = no exists = scope:mts_rite }
            set_variable = { name = mts_rite_edit_source value = scope:mts_rite }
            scope:mts_rite = {
                mts_prepare_selector_rite_effect = yes
                mts_fill_edit_blanks_effect = yes
            }
        }
    }
}

mts_selector_ready_gui = {
    scope = character
    saved_scopes = { mts_rite }
    is_shown = {
        is_ai = no
        exists = scope:mts_rite
        scope:mts_rite = {
            mts_selector_ready_trigger = yes
            any_rite_tenet = { count >= 100 }
        }
    }
}

mts_cleanup_edit_blanks_gui = {
    scope = character
    saved_scopes = { mts_rite mts_should_cleanup }
    effect = {
        if = {
            limit = {
                is_ai = no
                exists = scope:mts_rite
                scope:mts_should_cleanup = yes
            }
            scope:mts_rite = { mts_remove_edit_blanks_effect = yes }
            if = {
                limit = { exists = var:mts_rite_edit_source scope:mts_rite = var:mts_rite_edit_source }
                remove_variable = mts_rite_edit_source
            }
        }
    }
}

mts_recover_edit_blanks_gui = {
    scope = character
    is_shown = {
        is_ai = no
        OR = {
            has_variable = mts_rite_edit_source
            rite ?= { any_rite_tenet = { mts_is_edit_blank_trigger = yes } }
        }
    }
    effect = {
        if = {
            limit = { is_ai = no }
            if = {
                limit = { has_variable = mts_rite_edit_source }
                var:mts_rite_edit_source ?= { mts_remove_edit_blanks_effect = yes }
                remove_variable = mts_rite_edit_source
            }
            else = {
                rite ?= { mts_remove_edit_blanks_effect = yes }
            }
        }
    }
}
"""
    internal = "".join(f"\t\tthis = doctrine:mts_selector_doctrine_{slot:03}\n"
                       for slot in range(1, COUNT + 1))
    ready = "".join(f"\trite_has_doctrine = mts_selector_doctrine_{slot:03}\n"
                    for slot in range(1, COUNT + 1))
    files["common/scripted_triggers/mts_selector.txt"] = HEADER + (
        "mts_selector_ready_trigger = {\n" + ready + "}\n\n"
        "mts_selector_internal_doctrine_trigger = {\n\tOR = {\n" + internal + "\t}\n}\n\n"
        "mts_selector_only_metadata_update_trigger = {\n"
        "\tOR = {\n"
        "\t\tany_in_list = { list = added_doctrines count >= 1 }\n"
        "\t\tany_in_list = { list = removed_doctrines count >= 1 }\n"
        + "".join(f"\t\tany_in_list = {{ list = {name} count >= 1 }}\n"
                  for name in EDIT_TENET_LISTS) +
        "\t}\n"
        + "".join(f"\tNOT = {{ any_in_list = {{ list = {name} "
                  "NOT = { mts_is_edit_blank_trigger = yes } } }\n"
                  for name in EDIT_TENET_LISTS) +
        "\tNOT = {\n\t\tany_in_list = {\n\t\t\tlist = added_doctrines\n"
        "\t\t\tNOT = { mts_selector_internal_doctrine_trigger = yes }\n\t\t}\n\t}\n"
        "\tNOT = {\n\t\tany_in_list = {\n\t\t\tlist = removed_doctrines\n"
        "\t\t\tNOT = { mts_selector_internal_doctrine_trigger = yes }\n\t\t}\n\t}\n}\n" + edit_triggers)
    for language in LANGUAGES:
        files[f"localization/{language}/religion/mts_selector_l_{language}.yml"] = (
            f"l_{language}:\n" + HEADER + "".join(localization))
    return files


def generate_padding(mod: Path, check: bool = False) -> dict:
    files = generated_files()
    for relative, source in files.items():
        target = mod / relative
        content = source.encode("utf-8-sig")
        if check:
            if target.read_bytes() != content:
                raise ValueError(f"selector compatibility source differs: {relative}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(content)
    return {"doctrine_count": COUNT, "group_count": COUNT,
            "temporary_edit_tenets": COUNT, "files": len(files), "live_verified": False}

"""Generate inert doctrine metadata for CK3 1.20's shared selector index.

These are doctrines, never core tenets. Empty native tenet slots remain empty.
"""

from pathlib import Path


COUNT = 100
HEADER = "# GENERATED FILE - MTS native selector index compatibility\n"


def generated_files() -> dict[str, str]:
    files = {}
    effects = []
    for shard in range(10):
        groups, doctrines = [], []
        for slot in range(shard * 10 + 1, shard * 10 + 11):
            group = f"mts_selector_group_{slot:03}"
            doctrine = f"mts_selector_doctrine_{slot:03}"
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
        HEADER + "mts_prepare_selector_rite_effect = {\n" + "".join(effects) + "}\n")
    files["common/scripted_guis/mts_selector.txt"] = HEADER + """mts_prepare_selector_gui = {
    scope = character
    effect = {
        if = {
            limit = { is_ai = no exists = scope:mts_rite }
            scope:mts_rite = { mts_prepare_selector_rite_effect = yes }
        }
    }
}
"""
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
            "tenet_placeholders": 0, "files": len(files), "live_verified": False}

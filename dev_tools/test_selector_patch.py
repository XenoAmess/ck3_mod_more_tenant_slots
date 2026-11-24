"""Check actual native projections; engine trigger execution is a live check."""

import argparse
from pathlib import Path
import re
import unittest

from migrate_to_ck3_1_20 import changes, framework_tools


class SelectorProjection(unittest.TestCase):
    def test_edit_open_waits_for_metadata_instead_of_racing_the_queued_command(self):
        from ck3_text_projection import named_block
        native = (GAME / "game/gui/window_faith.gui").read_text(encoding="utf-8-sig")
        projected = native
        for before, after in changes(native, "gui/window_faith.gui"):
            projected = projected.replace(before, after, 1)
        span = named_block(projected, "button_standard", "edit_rite")
        edit = projected[span.start:span.end]
        clicks = re.findall(r'onclick = "([^"]+)"', edit)
        self.assertEqual(len(clicks), 2)
        self.assertIn("mts_prepare_selector_gui", clicks[0])
        self.assertIn("mts_edit_rite_pending", clicks[1])
        self.assertTrue(all("OpenGameViewData" not in click for click in clicks))
        state = named_block(edit, "state", "mts_open_prepared_rite")
        waiting = edit[state.start:state.end]
        self.assertIn("mts_selector_ready_gui", waiting)
        self.assertIn("FaithWindow.CanEditRite", waiting)
        self.assertLess(waiting.index("GetVariableSystem.Clear"), waiting.index("OpenGameViewData"))
        hide = projected.index("name = _hide\n\t\tposition = { -60 0 }")
        hide_state = projected[hide:projected.index("\n\t}", hide)]
        self.assertIn("mts_cleanup_edit_blanks_gui", hide_state)
        self.assertIn("MakeScopeBool( GetVariableSystem.Exists( 'mts_edit_rite_pending' ) )",
                      hide_state)
        self.assertLess(hide_state.index("mts_cleanup_edit_blanks_gui"),
                        hide_state.index("GetVariableSystem.Clear"))

    def test_switching_rites_cancels_pending_edit_before_changing_selection(self):
        native = (GAME / "game/gui/window_faith.gui").read_text(encoding="utf-8-sig")
        projected = native
        for before, after in changes(native, "gui/window_faith.gui"):
            projected = projected.replace(before, after, 1)
        selection = r'(?m)^([ \t]*)onclick = "\[FaithWindow\.SetSelectedRite[^\n]+'
        native_actions = list(re.finditer(selection, native))
        actions = list(re.finditer(selection, projected))
        self.assertTrue(native_actions)
        self.assertEqual([m[0] for m in native_actions], [m[0] for m in actions])
        for action in actions:
            preceding = projected[:action.start()].splitlines()[-1]
            self.assertEqual(
                preceding,
                action[1] + 'onclick = "[GetVariableSystem.Clear( \'mts_edit_rite_pending\' )]"',
            )

    def test_readiness_requires_every_metadata_doctrine(self):
        from ck3_text_projection import blocks
        from selector_padding import COUNT, generated_files
        files = generated_files()
        source = files["common/scripted_triggers/mts_selector.txt"]
        ready = next(b for b in blocks(source) if b.key == "mts_selector_ready_trigger")
        required = re.findall(r"rite_has_doctrine\s*=\s*(\w+)", source[ready.start:ready.end])
        self.assertEqual(len(required), COUNT)
        self.assertEqual(set(required), {f"mts_selector_doctrine_{n:03}" for n in range(1, COUNT + 1)})
        self.assertNotIn("OR", source[ready.start:ready.end])
        gui = files["common/scripted_guis/mts_selector.txt"]
        ready_gui = next(b for b in blocks(gui) if b.key == "mts_selector_ready_gui")
        guard = gui[ready_gui.start:ready_gui.end]
        self.assertIn("mts_selector_ready_trigger = yes", guard)
        self.assertIn(f"any_rite_tenet = {{ count >= {COUNT} }}", guard)

    def test_opening_a_new_rite_keeps_the_native_source_rite_unchanged(self):
        from ck3_text_projection import named_block
        native = (GAME / "game/gui/window_faith.gui").read_text(encoding="utf-8-sig")
        projected = native
        for before, after in changes(native, "gui/window_faith.gui"):
            self.assertEqual(projected.count(before), 1)
            projected = projected.replace(before, after, 1)
        for key, name in (("button_standard", "create_rite"),
                          ("button_standard_puppet", "create_rite_puppet")):
            before = named_block(native, key, name)
            after = named_block(projected, key, name)
            self.assertEqual(native[before.start:before.end], projected[after.start:after.end])
        edit = named_block(projected, "button_standard", "edit_rite")
        self.assertIn("mts_prepare_selector_gui", projected[edit.start:edit.end])

    def test_hud_recovery_runs_only_outside_pending_and_open_edits(self):
        from selector_padding import generated_files
        native = (GAME / "game/gui/hud.gui").read_text(encoding="utf-8-sig")
        [(before, after)] = changes(native, "gui/hud.gui")
        self.assertEqual(native.count(before), 1)
        self.assertIn("Not( IsGameViewOpen( 'rite_creation' ) )", after)
        self.assertIn("Not( GetVariableSystem.Exists( 'mts_edit_rite_pending' ) )", after)
        self.assertIn("mts_recover_edit_blanks_gui').IsShown", after)
        self.assertIn("mts_recover_edit_blanks_gui').Execute", after)
        gui = generated_files()["common/scripted_guis/mts_selector.txt"]
        self.assertIn("name = mts_rite_edit_source value = scope:mts_rite", gui)
        self.assertIn("var:mts_rite_edit_source ?= { mts_remove_edit_blanks_effect = yes }",
                      gui)

    def test_metadata_filter_wraps_and_preserves_the_entire_native_effect(self):
        from ck3_text_projection import blocks
        from migrate_to_ck3_1_20 import EDIT_BLANK_FILTER
        native = (GAME / "game/common/on_action/religion_on_actions.txt").read_text(encoding="utf-8-sig")
        patches = changes(native, "common/on_action/religion_on_actions.txt")
        self.assertEqual(len(patches), 1)
        before, after = patches[0]
        effect = next(b for b in blocks(before) if b.key == "effect")
        body = before[effect.opening + 1:effect.end - 1]
        nested = "\n".join("\t" + line if line else line for line in body.split("\n"))
        restored = re.sub(r"(?m)^([ \t]*)limit = \{ " +
                          re.escape(EDIT_BLANK_FILTER) + r" \}\n", "", after)
        restored = restored.replace(" " + EDIT_BLANK_FILTER, "")
        self.assertIn(nested, restored)
        self.assertIn("exists = scope:consume_rite_edit_token", after)
        self.assertIn("mts_remove_edit_blanks_effect = yes", after)
        self.assertIn(EDIT_BLANK_FILTER, after)
        self.assertEqual(after.count("mts_selector_only_metadata_update_trigger = yes"), 1)
        self.assertIn("send_interface_message", after)
        self.assertIn("head_of_rite", after)
        blocks(after)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--framework", type=Path, required=True)
    parser.add_argument("--game", type=Path, required=True)
    args, remaining = parser.parse_known_args()
    framework_tools(args.framework)
    GAME = args.game
    unittest.main(argv=[__file__] + remaining)

"""Check actual native projections; engine trigger execution is a live check."""

import argparse
from pathlib import Path
import unittest

from migrate_to_ck3_1_20 import changes, framework_tools


class SelectorProjection(unittest.TestCase):
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

    def test_metadata_filter_wraps_and_preserves_the_entire_native_effect(self):
        from ck3_text_projection import blocks
        native = (GAME / "game/common/on_action/religion_on_actions.txt").read_text(encoding="utf-8-sig")
        patches = changes(native, "common/on_action/religion_on_actions.txt")
        self.assertEqual(len(patches), 1)
        before, after = patches[0]
        effect = next(b for b in blocks(before) if b.key == "effect")
        body = before[effect.opening + 1:effect.end - 1]
        nested = "\n".join("\t" + line if line else line for line in body.split("\n"))
        self.assertIn(nested, after)
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

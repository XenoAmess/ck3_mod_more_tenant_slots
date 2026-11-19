"""Offline contracts against generated GUI actions and reviewed native inputs.

Supply XAPO_FRAMEWORK_DIR and XAPO_GAME_DIR explicitly. These tests do not run
CK3 or establish GUI rendering, map icon allocation, or engine scope validity.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import re
import tempfile
import unittest

import potential_output as product


def arguments(body: str) -> list[str]:
    result: list[str] = []
    depth = 0
    quoted = False
    start = 0
    for index, char in enumerate(body):
        if char == "'":
            quoted = not quoted
        elif not quoted:
            if char == "(":
                depth += 1
            elif char == ")":
                depth -= 1
            elif char == "," and depth == 0:
                result.append(body[start:index].strip())
                start = index + 1
    if body.strip():
        result.append(body[start:].strip())
    return result


class GuiActions:
    """Small independent interpreter of the actual button filter expressions."""

    def __init__(self) -> None:
        self.values: dict[str, str] = {}
        self.planning: dict[str, float] = {}

    def evaluate(self, expression: str) -> str | bool:
        expression = expression.strip()
        if expression.startswith("'") and expression.endswith("'"):
            if expression.startswith("'(CFixedPoint)"):
                return float(expression[len("'(CFixedPoint)"):-1])
            return expression[1:-1]
        good = re.fullmatch(r"GetTradeGoodType\(\s*'([^']+)'\s*\)\.GetTextIconNoFormat", expression)
        if good:
            return f"@{good[1]}!"
        match = re.fullmatch(r"([\w.]+)\s*\((.*)\)", expression)
        if not match:
            raise AssertionError(f"unsupported GUI expression: {expression}")
        name = match[1]
        args = [self.evaluate(arg) for arg in arguments(match[2])]
        if name == "Localize":
            return f"localized:{args[0]}"
        if name == "Concatenate":
            return str(args[0]) + str(args[1])
        if name == "GetVariableSystem.HasValue":
            return self.values.get(str(args[0])) == args[1]
        if name == "GetVariableSystem.Get":
            return self.values[str(args[0])]
        if name == "GetVariableSystem.Set":
            self.values[str(args[0])] = str(args[1])
            return True
        if name == "Not":
            return not args[0]
        if name == "And":
            return bool(args[0] and args[1])
        if name == "Select_CString":
            return args[1] if args[0] else args[2]
        if name == "Select_CFixedPoint":
            return args[1] if args[0] else args[2]
        if name == "MakeScopeValue":
            return args[0]
        if name == "ActivityPlanner.AddOrSetOnCreationObject":
            self.planning[str(args[0])] = float(args[1])
            return True
        raise AssertionError(f"unsupported GUI function: {name}")

    def click(self, gui: str, key: str, kind: str = "button_standard") -> None:
        from ck3_text_projection import named_block

        block = named_block(gui, kind, key)
        body = gui[block.opening:block.end]
        actions = re.findall(r'onclick\s*=\s*"\[(.*?)\]"', body)
        if not actions:
            raise AssertionError(f"no button actions: {key}")
        for action in actions:
            self.evaluate(action)

    def visible(self, good: str) -> bool:
        if f"xapo_hidden_{good}" in self.planning:
            assert (self.planning[f"xapo_hidden_{good}"] == 1) == (self.values.get(f"xapo_hidden_@{good}!") == "yes")
        return self.values.get(f"xapo_hidden_@{good}!") != "yes"


class PotentialOutputTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.framework = Path(os.environ["XAPO_FRAMEWORK_DIR"])
        cls.game = Path(os.environ["XAPO_GAME_DIR"])
        product.framework_tools(cls.framework)
        cls.files = product.generated(cls.game)
        cls.gui = cls.files["gui/xapo_potential_output.gui"].decode("utf-8-sig")
        cls.goods, cls.basic, cls.categories = product.catalog(cls.game)

    def test_generation_matches_complete_product_and_native_inputs(self) -> None:
        report = product.validate(self.framework, self.game)
        self.assertEqual(report["goods"], 35)
        self.assertFalse(report["live_verified"])
        for good in self.goods:
            self.assertEqual(self.gui.count(f'name = "xapo_toggle_{good}"'), 1)

    def test_default_clear_multiselect_and_select_all(self) -> None:
        state = GuiActions()
        self.assertTrue(all(state.visible(g) for g in self.goods))
        state.click(self.gui, "xapo_clear_all")
        self.assertFalse(any(state.visible(g) for g in self.goods))
        state.click(self.gui, "xapo_toggle_trade_good_grain")
        state.click(self.gui, "xapo_toggle_trade_good_silk")
        self.assertEqual({g for g in self.goods if state.visible(g)},
                         {"trade_good_grain", "trade_good_silk"})
        state.click(self.gui, "xapo_toggle_trade_good_grain")
        self.assertEqual({g for g in self.goods if state.visible(g)}, {"trade_good_silk"})
        state.click(self.gui, "xapo_select_all")
        self.assertTrue(all(state.visible(g) for g in self.goods))

    def test_every_good_toggles_independently(self) -> None:
        for selected in self.goods:
            state = GuiActions()
            state.click(self.gui, f"xapo_toggle_{selected}")
            self.assertEqual({g for g in self.goods if not state.visible(g)}, {selected})
            state.click(self.gui, f"xapo_toggle_{selected}")
            self.assertTrue(all(state.visible(g) for g in self.goods))

    def test_group_batch_uses_preclick_snapshot_and_preserves_other_groups(self) -> None:
        for key, members in self.categories:
            for basic in (True, False):
                group = [g for g in members if (g in self.basic) == basic]
                if not group:
                    continue
                state = GuiActions()
                name = f"xapo_group_toggle_{key}_{'basic' if basic else 'other'}"
                state.click(self.gui, name, "button_tertiary")
                self.assertEqual({g for g in self.goods if not state.visible(g)}, set(group))
                state.click(self.gui, name, "button_tertiary")
                self.assertTrue(all(state.visible(g) for g in self.goods))
                state.click(self.gui, f"xapo_toggle_{group[0]}")
                state.click(self.gui, name, "button_tertiary")
                self.assertTrue(all(state.visible(g) for g in self.goods))

    def test_map_reads_native_potential_and_shares_filter_keys(self) -> None:
        self.assertIn('datamodel = "[County.GetPotentialTradeGoodTypes]"', self.gui)
        self.assertIn("ActivityPlannerMapIcon.GetProvince.GetCounty", self.gui)
        self.assertIn("Concatenate( 'xapo_hidden_', TradeGoodType.GetTextIconNoFormat )", self.gui)
        potential = product.native_text(self.game, product.NATIVE_FILES[4])
        from ck3_text_projection import blocks

        by_county: dict[str, set[str]] = {}
        for block in blocks(potential):
            if block.key in self.goods:
                for county in re.findall(r"\bc_\w+\b", potential[block.opening:block.end]):
                    by_county.setdefault(county, set()).add(block.key)
        self.assertGreater(len(by_county), 1000)
        state = GuiActions()
        state.click(self.gui, "xapo_clear_all")
        for good in ("trade_good_iron", "trade_good_grain"):
            state.click(self.gui, f"xapo_toggle_{good}")
        for potential_goods in by_county.values():
            shown = {g for g in potential_goods if state.visible(g)}
            self.assertEqual(shown, potential_goods & {"trade_good_iron", "trade_good_grain"})

    def test_projection_is_reversible_and_rejects_changed_native_bytes(self) -> None:
        from ck3_text_projection import digest, project, recover

        native = product.native_text(self.game, product.NATIVE_FILES[0])
        output = self.files[product.NATIVE_FILES[0]].decode("utf-8-sig")
        replacements = product.projections(self.game)[product.NATIVE_FILES[0]]
        self.assertEqual(recover(output, digest(native), replacements), native)
        with self.assertRaises(ValueError):
            project(native + "# changed\n", digest(native), replacements)

    def test_native_window_animation_stays_on_root(self) -> None:
        from ck3_text_projection import blocks, named_block

        text = self.files["gui/window_activity_planner.gui"].decode("utf-8-sig")
        root = named_block(text, "window", "activity_planner")
        states = [block for block in blocks(text) if block.key == "state" and root.opening < block.start < root.end]
        for name in ("_show", "_hide"):
            state = next(block for block in states if re.match(r"\s*name\s*=\s*" + name + r"\b", text[block.opening + 1:block.end]))
            ancestors = [block for block in blocks(text) if block.opening < state.start < block.end]
            self.assertEqual(ancestors, [root])
        self.assertNotIn("xapo_seed_filters", self.gui)

    def test_build_is_deterministic_and_has_independent_identity(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            first = product.build(self.framework, self.game, Path(directory) / "a", "test-revision")
            second = product.build(self.framework, self.game, Path(directory) / "b", "test-revision")
        self.assertEqual(first, second)
        self.assertIsNone(first["manifest"]["workshop_item_id"])
        self.assertEqual(first["manifest"]["product"], product.PRODUCT)
        self.assertEqual({e["path"] for e in first["manifest"]["files"]}, set(self.files))
        descriptor = self.files["descriptor.mod"].decode("utf-8-sig")
        self.assertNotIn("remote_file_id", descriptor)
        self.assertNotIn("replace_path", descriptor)
        self.assertFalse(any(p.startswith("events/") for p in self.files))
        self.assertEqual({p for p in self.files if p.startswith("common/")},
                         {"common/activities/activity_types/xapo_potential_output.txt",
                          "common/script_values/xapo_potential_output.txt",
                          "common/defines/graphic/zz_xapo_potential_output.txt"})
        activity = self.files["common/activities/activity_types/xapo_potential_output.txt"].decode("utf-8-sig")
        self.assertIn("can_start = { always = no }", activity)
        self.assertIn("is_shown = { always = no }", activity)
        self.assertNotIn("on_start", activity)


if __name__ == "__main__":
    unittest.main()

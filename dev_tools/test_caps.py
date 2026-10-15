"""Regression for the reported forced culture cap, using production validation."""

import argparse
from pathlib import Path
import tempfile
import unittest

from migrate_to_ck3_1_20 import framework_tools
from validate_and_build import MOD, validate_caps


class Caps(unittest.TestCase):
    def test_product_inherits_culture_limits(self):
        validate_caps(MOD)

    def test_old_bundle_is_rejected_even_in_another_filename(self):
        with tempfile.TemporaryDirectory() as directory:
            mod = Path(directory)
            defines = mod / "common/defines"
            defines.mkdir(parents=True)
            (defines / "tenets.txt").write_text(
                "NReligion = { FAITH_CORE_TENETS_CAP = 100 }", encoding="utf-8-sig")
            (defines / "unrelated.txt").write_text(
                "NCulture = { DEFAULT_MAX_TRADITIONS = 10000 }", encoding="utf-8-sig")
            with self.assertRaisesRegex(ValueError, "inherit native culture"):
                validate_caps(mod)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--framework", type=Path, required=True)
    args, remaining = parser.parse_known_args()
    framework_tools(args.framework)
    unittest.main(argv=[__file__] + remaining)

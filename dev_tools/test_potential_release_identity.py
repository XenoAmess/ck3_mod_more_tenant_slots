"""Release identity checks use a disposable real Git repository."""
import argparse
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import potential_output as builder


class PotentialReleaseTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="xapo-release-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.mod = self.root / builder.PRODUCT
        self.mod.mkdir()
        (self.mod / "descriptor.mod").write_bytes(b'name="Fixture"\n')
        (self.root / "dev_tools").mkdir()
        (self.root / "dev_tools/workshop_products.json").write_text(json.dumps({
            "forbidden_upstream_target_ids": ["99"],
            "products": [{"directory": builder.PRODUCT, "workshop_item_id": "123"}]}))
        self.git("init", "-b", "master")
        self.git("add", ".")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "commit", "-m", "Fixture source")
        self.revision = self.git("rev-parse", "HEAD").strip()
        self.git("tag", "reviewed")
        for name, value in (("ROOT", self.root), ("MOD", self.mod)):
            mock = patch.object(builder, name, value)
            mock.start()
            self.addCleanup(mock.stop)
        for name, kwargs in (("validate", {"return_value": {}}),
                             ("generated", {"return_value": {"descriptor.mod": b'name="Fixture"\n'}})):
            mock = patch.object(builder, name, **kwargs)
            mock.start()
            self.addCleanup(mock.stop)

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True,
                                       stderr=subprocess.STDOUT)

    def build(self, revision=None, item=None):
        return builder.build(FRAMEWORK, self.root, self.root / "build",
                             revision or self.revision, "reviewed", item)

    def test_actual_tag_and_registered_item_are_recorded(self):
        manifest = self.build(item="123")["manifest"]
        self.assertEqual(manifest["git_sha"], self.revision)
        self.assertEqual(manifest["git_tag"], "reviewed")
        self.assertEqual(manifest["workshop_item_id"], "123")

    def test_wrong_revision_is_rejected_before_staging(self):
        with self.assertRaisesRegex(ValueError, "release tag"):
            self.build("0" * 40)
        self.assertFalse((self.root / "build").exists())

    def test_changed_product_is_rejected(self):
        (self.mod / "descriptor.mod").write_bytes(b'name="Changed"\n')
        with self.assertRaises(subprocess.CalledProcessError):
            self.build()
        self.assertFalse((self.root / "build").exists())

    def test_other_product_or_upstream_item_is_rejected(self):
        for item in ("3182367229", "99"):
            with self.assertRaisesRegex(ValueError, "canonical registry"):
                self.build(item=item)
        self.assertFalse((self.root / "build").exists())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--framework", type=Path, required=True)
    args, remaining = parser.parse_known_args()
    FRAMEWORK = args.framework.resolve()
    unittest.main(argv=[__file__, *remaining])

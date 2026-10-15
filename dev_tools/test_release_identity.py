"""Check tagged build identity against a real disposable Git repository."""
import argparse
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import validate_and_build as builder


class TaggedBuildTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory(prefix="mts-release-identity-")
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.mod = self.root / "product"
        self.mod.mkdir()
        (self.mod / "descriptor.mod").write_bytes(b'name="Fixture"\n')
        self.git("init", "-b", "master")
        self.git("add", ".")
        self.git("-c", "user.name=Fixture", "-c", "user.email=fixture@example.invalid",
                 "commit", "-m", "Fixture source")
        self.revision = self.git("rev-parse", "HEAD").strip()
        self.git("tag", "reviewed")
        for key, value in (("ROOT", self.root), ("MOD", self.mod), ("RELEASE_FILES", ("descriptor.mod",))):
            change = patch.object(builder, key, value)
            change.start()
            self.addCleanup(change.stop)

    def git(self, *args):
        return subprocess.check_output(["git", *args], cwd=self.root, text=True, stderr=subprocess.STDOUT)

    def test_actual_tag_is_written_into_manifest(self):
        result = builder.build(FRAMEWORK, self.root / "build", self.revision, "reviewed")
        self.assertEqual(result["manifest"]["git_tag"], "reviewed")
        self.assertEqual(result["manifest"]["git_sha"], self.revision)
        self.assertEqual((self.root / "build" / builder.PRODUCT / "descriptor.mod").read_bytes(),
                         (self.mod / "descriptor.mod").read_bytes())

    def test_tag_for_another_revision_is_rejected_before_staging(self):
        with self.assertRaisesRegex(ValueError, "release tag"):
            builder.build(FRAMEWORK, self.root / "build", "0" * 40, "reviewed")
        self.assertFalse((self.root / "build").exists())

    def test_changed_product_cannot_claim_tagged_bytes(self):
        (self.mod / "descriptor.mod").write_bytes(b'name="Changed"\n')
        with self.assertRaises(subprocess.CalledProcessError):
            builder.build(FRAMEWORK, self.root / "build", self.revision, "reviewed")
        self.assertFalse((self.root / "build").exists())


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--framework-root", required=True, type=Path)
    args, remaining = parser.parse_known_args()
    FRAMEWORK = args.framework_root.resolve()
    unittest.main(argv=[__file__, *remaining])

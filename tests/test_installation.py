"""Offline regression tests; mocked installer outputs are not public installation evidence."""
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import smoke_install as smoke
from validate import validate


class InstallationChecks(unittest.TestCase):
    def test_installed_packages_need_no_repository_files(self):
        with tempfile.TemporaryDirectory() as tmp:
            dest = Path(tmp) / 'skills'
            shutil.copytree(ROOT / 'skills', dest)
            self.assertEqual(validate(dest, installed=True), [])
            reference = dest / 'objective-audit/references/objective-diagnostics.md'
            reference.unlink()
            self.assertTrue(any('broken link' in error for error in validate(dest, installed=True)))

    def test_missing_installed_skill_is_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            self.assertEqual(sum('Missing' in error for error in validate(Path(tmp), installed=True)), 4)

    def run_mock_install(self, *, fail=False, corrupt=False, moved=False):
        sha = 'a' * 40
        expected = smoke.installed_manifest(ROOT / 'skills')
        recorded = []
        def installer(command, **kwargs):
            self.assertIn('--repo', command)
            self.assertEqual(command[command.index('--repo') + 1], smoke.REPOSITORY)
            self.assertEqual(command[command.index('--ref') + 1], 'test-ref')
            self.assertNotIn('GH_TOKEN', kwargs['env'])
            dest = Path(command[command.index('--dest') + 1])
            recorded.append(dest)
            if fail:
                (dest / 'partial').write_text('partial install', encoding='utf-8')
                raise subprocess.CalledProcessError(1, command)
            shutil.copytree(ROOT / 'skills', dest, dirs_exist_ok=True)
            if corrupt:
                (dest / 'objective-audit/references/objective-diagnostics.md').write_text('Changed content', encoding='utf-8')
        with tempfile.TemporaryDirectory() as tmp:
            helper = Path(tmp) / 'helper.py'
            helper.write_text('# synthetic helper for unit test only', encoding='utf-8')
            with patch.object(smoke, 'resolve_ref', side_effect=[sha, 'b' * 40 if moved else sha]), \
                 patch.object(smoke, 'public_manifest', return_value=expected), \
                 patch.object(smoke.subprocess, 'run', side_effect=installer):
                if fail or corrupt or moved:
                    with self.assertRaises((ValueError, subprocess.CalledProcessError)):
                        smoke.smoke_install('test-ref', helper, Path(tmp))
                else:
                    result = smoke.smoke_install('test-ref', helper, Path(tmp))
                    self.assertEqual(result['commit'], sha)
                    self.assertEqual(result['files_verified'], len(expected))
                    self.assertTrue(result['temporary_installation_removed'])
            self.assertEqual(len(recorded), 1)
            self.assertFalse(recorded[0].exists())
            self.assertTrue(helper.exists())

    def test_public_command_manifest_and_success_cleanup(self):
        self.run_mock_install()

    def test_cleanup_after_partial_installer_failure(self):
        self.run_mock_install(fail=True)

    def test_modified_download_is_rejected_and_cleaned(self):
        self.run_mock_install(corrupt=True)

    def test_moving_ref_is_rejected_and_cleaned(self):
        self.run_mock_install(moved=True)


if __name__ == '__main__':
    unittest.main()

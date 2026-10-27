import sys
import unittest
from pathlib import Path
from PIL import Image

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/"scripts"))
from pet_assets import ROOT, build_from_frames, load_manifest, validate_image


class AssetTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = load_manifest()

    def test_both_presets_reproduce_published_pixels(self):
        for preset in ("dance", "original"):
            with self.subTest(preset=preset):
                rebuilt = build_from_frames(self.manifest, preset)
                with Image.open(ROOT/self.manifest["variants"][preset]["spritesheet"]) as saved:
                    self.assertEqual(rebuilt.tobytes(), saved.tobytes())

    def test_mixing_old_idle_preserves_every_other_dance_row(self):
        mixed = build_from_frames(self.manifest, "dance", {"idle":"original"})
        original = build_from_frames(self.manifest, "original")
        dance = build_from_frames(self.manifest, "dance")
        self.assertEqual(mixed.crop((0,0,1536,208)).tobytes(), original.crop((0,0,1536,208)).tobytes())
        self.assertEqual(mixed.crop((0,208,1536,2288)).tobytes(), dance.crop((0,208,1536,2288)).tobytes())

    def test_rejects_artwork_in_unused_cell(self):
        atlas = build_from_frames(self.manifest)
        atlas.putpixel((7*192+96,100),(255,0,0,255))
        with self.assertRaisesRegex(ValueError,"Unused cell"):
            validate_image(atlas)

    def test_rejects_missing_required_frame(self):
        atlas = build_from_frames(self.manifest)
        atlas.paste(Image.new("RGBA",(192,208)),(0,0))
        with self.assertRaisesRegex(ValueError,"Required cell.*empty"):
            validate_image(atlas)

    def test_rejects_invalid_geometry(self):
        with self.assertRaisesRegex(ValueError,"1536x2288"):
            validate_image(Image.new("RGBA",(1536,1872)))


if __name__ == "__main__":
    unittest.main()

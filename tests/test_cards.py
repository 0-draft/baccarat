#!/usr/bin/env python3
"""
Tests for the table art.

A missing or wrongly sized file fails nothing at render time — it ships a
broken image to the page. These cover that every image the generator draws is
well-formed, sized to its viewBox, and paints its own felt.
"""

import pathlib
import sys
import unittest
import xml.etree.ElementTree as ET

ROOT = pathlib.Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))

import make_cards  # noqa: E402

CARDS = ROOT / ".github" / "cards"
NS = "{http://www.w3.org/2000/svg}"


class Art(unittest.TestCase):
    def test_the_set_is_complete(self):
        expected = {f"{r}{s}" for r in make_cards.RANKS for s in make_cards.SUITS}
        expected |= {"slot", "blank", "bead-empty"}
        expected |= {f"chip{v}" for v in make_cards.CHIPS}
        expected |= {f"spot-{k}" for k in make_cards.SPOTS}
        expected |= {f"label-{s}{w}" for s in ("player", "banker") for w in ("", "-won")}
        expected |= {f"bead-{o}{p}" for o in make_cards.OUTCOMES for p in make_cards.PAIRS}
        self.assertEqual({p.stem for p in CARDS.glob("*.svg")}, expected)

    def test_each_file_is_sized_and_opaque(self):
        for path in sorted(CARDS.glob("*.svg")):
            with self.subTest(path.name):
                root = ET.parse(path).getroot()
                w, h = root.get("width"), root.get("height")
                self.assertEqual(root.get("viewBox"), f"0 0 {w} {h}")
                first = root.find(f"{NS}rect")
                self.assertEqual(first.get("fill"), make_cards.FELT)
                self.assertEqual((first.get("width"), first.get("height")), (w, h))


if __name__ == "__main__":
    unittest.main()

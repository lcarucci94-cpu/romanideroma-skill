"""Test del validatore. python3 -m unittest discover tests"""

import shutil
import sys
import tempfile
import unittest
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / "scripts"))

import importlib.util

_spec = importlib.util.spec_from_file_location(
    "validate_skill", RADICE / "scripts" / "validate-skill.py"
)
validate_skill = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(validate_skill)


class SkillReale(unittest.TestCase):
    def test_la_skill_di_questo_repo_e_valida(self):
        self.assertEqual(validate_skill.valida(RADICE), [])


class Frontmatter(unittest.TestCase):
    def test_legge_i_campi_di_primo_livello(self):
        campi = validate_skill.leggi_frontmatter(
            "---\nname: romanideroma\ndescription: prova\nmetadata:\n  version: 1\n---\ncorpo"
        )
        self.assertEqual(campi["name"], "romanideroma")
        self.assertEqual(campi["description"], "prova")
        self.assertNotIn("version", campi)

    def test_senza_delimitatori_torna_vuoto(self):
        self.assertEqual(validate_skill.leggi_frontmatter("# Titolo\ntesto"), {})

    def test_frontmatter_non_chiuso_torna_vuoto(self):
        self.assertEqual(validate_skill.leggi_frontmatter("---\nname: x\ncorpo"), {})


class CasiRotti(unittest.TestCase):
    def setUp(self):
        self.tmp = Path(tempfile.mkdtemp())
        self.skill = self.tmp / "skills" / "romanideroma"
        (self.skill / "references").mkdir(parents=True)
        self.addCleanup(shutil.rmtree, self.tmp)

    def scrivi(self, testo, refs=()):
        (self.skill / "SKILL.md").write_text(testo, encoding="utf-8")
        for nome in refs:
            (self.skill / "references" / nome).write_text("contenuto", encoding="utf-8")

    def test_skill_mancante(self):
        errori = validate_skill.valida(self.tmp)
        self.assertTrue(any("manca" in e for e in errori))

    def test_nome_diverso_dalla_cartella(self):
        self.scrivi("---\nname: altra\ndescription: d\n---\ncorpo")
        self.assertTrue(any("diverso dalla cartella" in e for e in validate_skill.valida(self.tmp)))

    def test_nome_con_maiuscole(self):
        self.scrivi("---\nname: RomaniDeRoma\ndescription: d\n---\ncorpo")
        self.assertTrue(any("minuscolo" in e for e in validate_skill.valida(self.tmp)))

    def test_description_troppo_lunga(self):
        lunga = "x" * (validate_skill.MAX_DESCRIPTION + 1)
        self.scrivi(f"---\nname: romanideroma\ndescription: {lunga}\n---\ncorpo")
        self.assertTrue(any("description" in e for e in validate_skill.valida(self.tmp)))

    def test_corpo_oltre_il_budget(self):
        corpo = "parola " * (validate_skill.MAX_PAROLE_SKILL + 1)
        self.scrivi(f"---\nname: romanideroma\ndescription: d\n---\n{corpo}")
        self.assertTrue(any("massimo" in e for e in validate_skill.valida(self.tmp)))

    def test_reference_citato_ma_assente(self):
        self.scrivi("---\nname: romanideroma\ndescription: d\n---\nvedi references/fantasma.md")
        self.assertTrue(any("non esiste" in e for e in validate_skill.valida(self.tmp)))

    def test_reference_orfano(self):
        self.scrivi("---\nname: romanideroma\ndescription: d\n---\ncorpo", refs=("solo.md",))
        self.assertTrue(any("mai caricato" in e for e in validate_skill.valida(self.tmp)))

    def test_reference_vuoto(self):
        self.scrivi("---\nname: romanideroma\ndescription: d\n---\nvedi references/vuoto.md")
        (self.skill / "references" / "vuoto.md").write_text("   ", encoding="utf-8")
        self.assertTrue(any("vuoto" in e for e in validate_skill.valida(self.tmp)))

    def test_caso_valido(self):
        self.scrivi(
            "---\nname: romanideroma\ndescription: d\n---\nvedi references/uno.md",
            refs=("uno.md",),
        )
        self.assertEqual(validate_skill.valida(self.tmp), [])


if __name__ == "__main__":
    unittest.main()

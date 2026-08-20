"""Test dello scorer. python3 -m unittest discover tests"""

import importlib.util
import sys
import unittest
from pathlib import Path

RADICE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(RADICE / "scripts"))

_spec = importlib.util.spec_from_file_location(
    "score_eval", RADICE / "scripts" / "score_eval.py"
)
score_eval = importlib.util.module_from_spec(_spec)
sys.modules["score_eval"] = score_eval
_spec.loader.exec_module(score_eval)


CASI = """## C01 — saluto
registro: R1
budget: ≤12 parole
prompt: "Ciao"
criteri:
- niente premesse

## C02 — lista
registro: R2
budget: max 5 punti, ≤8 parole a punto
prompt: "Dammi 3 cose"
criteri:
- punti secchi

## C03 — spiegazione
registro: R1
budget: quella che serve, niente filler
prompt: "Spiegami X"
criteri:
- corretto
"""


class LetturaCasi(unittest.TestCase):
    def test_estrae_id_e_budget(self):
        casi = score_eval.leggi_casi(CASI)
        self.assertEqual(casi["C01"].budget, "≤12 parole")
        self.assertEqual(casi["C02"].budget, "max 5 punti, ≤8 parole a punto")
        self.assertEqual(casi["C03"].budget, "quella che serve, niente filler")


class LetturaRisposte(unittest.TestCase):
    def test_estrae_risposta_per_id(self):
        testo = "## C01\nRisposta uno.\n\n## C02\nRisposta due.\n"
        risposte = score_eval.leggi_risposte(testo)
        self.assertEqual(risposte["C01"], "Risposta uno.")
        self.assertEqual(risposte["C02"], "Risposta due.")


class ValutaBudget(unittest.TestCase):
    def test_budget_parole_entro_il_limite(self):
        esito = score_eval.valuta_budget("≤12 parole", "una due tre")
        self.assertTrue(esito.ok)

    def test_budget_parole_fuori_limite(self):
        esito = score_eval.valuta_budget("≤3 parole", "una due tre quattro")
        self.assertFalse(esito.ok)

    def test_budget_righe(self):
        esito = score_eval.valuta_budget("≤2 righe", "riga uno\nriga due\nriga tre")
        self.assertFalse(esito.ok)

    def test_budget_lista_punti_e_parole(self):
        risposta = "- una due\n- tre quattro\n- cinque sei sette otto nove dieci undici dodici tredici"
        esito = score_eval.valuta_budget("max 5 punti, ≤8 parole a punto", risposta)
        self.assertFalse(esito.ok)

    def test_budget_lista_dentro_i_limiti(self):
        risposta = "- una due tre\n- quattro cinque"
        esito = score_eval.valuta_budget("max 5 punti, ≤8 parole a punto", risposta)
        self.assertTrue(esito.ok)

    def test_budget_qualitativo_torna_none(self):
        self.assertIsNone(score_eval.valuta_budget("quella che serve", "qualsiasi cosa"))


class FrasiVietate(unittest.TestCase):
    def test_trova_frase_vietata(self):
        trovate = score_eval.cerca_frasi_vietate("Certo, ecco la risposta.")
        self.assertIn("certo, ecco", trovate)

    def test_risposta_pulita_non_segnala_nulla(self):
        self.assertEqual(score_eval.cerca_frasi_vietate("Le tre e mezza, daje."), [])



class RisposteMancanti(unittest.TestCase):
    """Una risposta assente non deve passare come 'zero parole'."""

    def setUp(self):
        import tempfile

        self.tmp = Path(tempfile.mkdtemp())
        self.addCleanup(__import__("shutil").rmtree, self.tmp)
        (self.tmp / "cases.md").write_text(CASI, encoding="utf-8")

    def esegui(self, responses: str) -> int:
        (self.tmp / "responses.md").write_text(responses, encoding="utf-8")
        return score_eval.esegui(self.tmp / "cases.md", self.tmp / "responses.md")

    def test_risposta_assente_fa_fallire_il_run(self):
        self.assertEqual(self.esegui("## C01\nCiao a te.\n"), 1)

    def test_risposta_vuota_fa_fallire_il_run(self):
        self.assertEqual(self.esegui("## C01\nCiao.\n\n## C02\n   \n\n## C03\nX.\n"), 1)

    def test_tutte_presenti_ed_entro_budget_passa(self):
        completo = "## C01\nCiao a te.\n\n## C02\n- una due\n- tre\n\n## C03\nSpiegazione.\n"
        self.assertEqual(self.esegui(completo), 0)


class ConfiniDeiBlocchi(unittest.TestCase):
    """Il testo fra un caso e l'altro non deve entrare nella risposta precedente."""

    def test_intestazione_di_sezione_non_finisce_nel_caso_precedente(self):
        testo = (
            "## C01\nRisposta breve.\n\n"
            "---\n\n"
            "# Run del 2026-08-20\n\n"
            "Prosa di contorno che non e' una risposta.\n\n"
            "## C02\nAltra risposta.\n"
        )
        risposte = score_eval.leggi_risposte(testo)
        self.assertEqual(risposte["C01"], "Risposta breve.")
        self.assertEqual(risposte["C02"], "Altra risposta.")

    def test_ignora_blocchi_che_non_sono_casi(self):
        testo = "## Premessa\nRoba.\n\n## C01\nRisposta.\n"
        risposte = score_eval.leggi_risposte(testo)
        self.assertEqual(list(risposte), ["C01"])

    def test_separatore_finale_non_conta_come_contenuto(self):
        testo = "## C01\nRisposta.\n\n---\n\n## C02\nAltra.\n"
        self.assertEqual(score_eval.leggi_risposte(testo)["C01"], "Risposta.")


if __name__ == "__main__":
    unittest.main()

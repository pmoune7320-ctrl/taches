import unittest
import main


class TestTaches(unittest.TestCase):
    def test_ajouter(self):
        taches = []
        t = main.ajouter(taches, "Apprendre Python")
        self.assertEqual(t["id"], 1)
        self.assertFalse(t["faite"])
        self.assertEqual(len(taches), 1)

    def test_ids_uniques(self):
        taches = []
        main.ajouter(taches, "a")
        main.ajouter(taches, "b")
        main.supprimer(taches, 1)
        t = main.ajouter(taches, "c")
        self.assertEqual(t["id"], 3)

    def test_terminer(self):
        taches = []
        main.ajouter(taches, "a")
        self.assertTrue(main.terminer(taches, 1))
        self.assertTrue(taches[0]["faite"])
        self.assertFalse(main.terminer(taches, 99))

    def test_supprimer(self):
        taches = []
        main.ajouter(taches, "a")
        self.assertTrue(main.supprimer(taches, 1))
        self.assertEqual(taches, [])
        self.assertFalse(main.supprimer(taches, 1))


if __name__ == "__main__":
    unittest.main()

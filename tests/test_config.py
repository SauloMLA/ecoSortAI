import unittest

from src.config import (
    CLASES,
    NUM_CLASES,
    CONFIDENCE_THRESHOLD,
    MODEL_SAVE_PATH,
    TFLITE_MODEL_PATH,
)


class TestConfig(unittest.TestCase):
    def test_class_count_matches_list(self):
        self.assertEqual(NUM_CLASES, len(CLASES))

    def test_expected_labels_exist(self):
        for expected in ("plastico", "papel", "carton", "aluminio"):
            self.assertIn(expected, CLASES)

    def test_confidence_threshold_is_valid(self):
        self.assertGreaterEqual(CONFIDENCE_THRESHOLD, 0.0)
        self.assertLessEqual(CONFIDENCE_THRESHOLD, 1.0)

    def test_model_paths_point_to_models_folder(self):
        self.assertTrue(MODEL_SAVE_PATH.startswith("models/"))
        self.assertTrue(TFLITE_MODEL_PATH.startswith("models/"))


if __name__ == "__main__":
    unittest.main()

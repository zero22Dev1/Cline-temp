import importlib.util
import tempfile
import unittest
from pathlib import Path

from reportlab.pdfgen import canvas


SCRIPT = Path(__file__).parents[1] / "scripts" / "pdf_to_context.py"
SPEC = importlib.util.spec_from_file_location("pdf_to_context", SCRIPT)
MODULE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MODULE)


class PdfContextConverterTest(unittest.TestCase):
    def make_pdf(self, path: Path) -> None:
        pdf = canvas.Canvas(str(path))
        pdf.drawString(72, 720, "First page " + "content " * 20)
        pdf.showPage()
        pdf.drawString(72, 720, "<second & page> " + "detail " * 20)
        pdf.showPage()
        pdf.showPage()
        pdf.save()

    def test_chunking_status_and_html_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, output = root / "sample.pdf", root / "out"
            self.make_pdf(source)
            metadata = MODULE.convert(source, output, "both", 2, False)
            self.assertEqual(metadata["pages"], 3)
            self.assertEqual(len(metadata["chunks"]), 2)
            self.assertEqual(metadata["status_counts"]["OCR_REQUIRED"], 1)
            self.assertIn("pages-0001-0002.md", (output / "index.md").read_text())
            html = (output / "document.html").read_text()
            self.assertIn("&lt;second &amp; page&gt;", html)
            self.assertNotIn("<second & page>", html)

    def test_existing_output_requires_overwrite(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, output = root / "sample.pdf", root / "out"
            self.make_pdf(source)
            MODULE.convert(source, output, "markdown", 5, False)
            with self.assertRaises(FileExistsError):
                MODULE.convert(source, output, "markdown", 5, False)
            MODULE.convert(source, output, "markdown", 5, True)

    def test_overwrite_rejects_unrecognized_directory(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source, output = root / "sample.pdf", root / "unrelated"
            self.make_pdf(source)
            output.mkdir()
            sentinel = output / "keep.txt"
            sentinel.write_text("keep", encoding="utf-8")

            with self.assertRaises(ValueError):
                MODULE.convert(source, output, "markdown", 5, True)

            self.assertEqual("keep", sentinel.read_text(encoding="utf-8"))

    def test_overwrite_rejects_input_parent(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            source = root / "sample.pdf"
            self.make_pdf(source)
            (root / "metadata.json").write_text('{"generated_by":"pdf-context-converter"}', encoding="utf-8")

            with self.assertRaises(ValueError):
                MODULE.convert(source, root, "markdown", 5, True)

            self.assertTrue(source.exists())


if __name__ == "__main__":
    unittest.main()


import common


from src.DocumentProcessor.pdf_converter import convert_pdf_to_images
from src.DocumentProcessor.LayoutAnalisis.Preprocess.image_processor import ImageProcessor
from src.DocumentProcessor.LayoutAnalisis.TableDetector.find_table_candidates import FindTableCadidates
from src.DocumentProcessor.LayoutAnalisis.TableDetector.table import BBox


class TestPreprocess:

    def test_converter(self):
        pdf_bytes = common.load_pdf_bytes(1)

        doc_images = convert_pdf_to_images(pdf_bytes)


        for image in doc_images:
            res = ImageProcessor().process(image)
            cnts = FindTableCadidates().find(res)



            # common.draw_table(image, cnts).show()




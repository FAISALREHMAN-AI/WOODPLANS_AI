import os
from typing import Dict, Any, List
from pypdf import PdfReader
from PIL import Image

class PDFExtractor:
    @staticmethod
    def extract_pdf_data(pdf_path: str, extract_images_dir: str = None) -> Dict[str, Any]:
        """
        Extracts textual content, metadata, and embedded images from an uploaded woodworking PDF plan.
        """
        if not os.path.exists(pdf_path):
            raise FileNotFoundError(f"PDF file not found at: {pdf_path}")

        reader = PdfReader(pdf_path)
        total_pages = len(reader.pages)
        full_text = []
        page_summaries = []
        extracted_images = []

        for i, page in enumerate(reader.pages):
            text = page.extract_text() or ""
            full_text.append(f"--- PAGE {i+1} ---\n{text}")
            
            page_summaries.append({
                "page_number": i + 1,
                "character_count": len(text),
                "preview": text[:200].replace("\n", " ").strip()
            })

            # Extract images if available and target dir provided
            if extract_images_dir:
                try:
                    for img_idx, img_obj in enumerate(page.images):
                        img_filename = f"page_{i+1}_img_{img_idx}_{img_obj.name}"
                        out_path = os.path.join(extract_images_dir, img_filename)
                        with open(out_path, "wb") as f:
                            f.write(img_obj.data)
                        extracted_images.append(out_path)
                except Exception:
                    pass

        metadata = reader.metadata or {}
        extracted_title = metadata.get("/Title") or os.path.splitext(os.path.basename(pdf_path))[0]

        return {
            "total_pages": total_pages,
            "title": str(extracted_title),
            "full_text": "\n\n".join(full_text),
            "page_summaries": page_summaries,
            "extracted_images": extracted_images,
        }

pdf_extractor = PDFExtractor()

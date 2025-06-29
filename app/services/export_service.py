"""
Servicio para exportar documentos Markdown a Word (.docx) con tabla de contenido automática.
"""
from typing import Any
from io import BytesIO
from docx import Document
from docx.shared import Pt
import markdown2
from bs4 import BeautifulSoup
from docx.oxml import OxmlElement
from docx.oxml.ns import qn

async def markdown_to_docx(markdown_text: str) -> BytesIO:
    """
    Convierte un texto Markdown a un archivo Word (.docx) en memoria.
    Incluye una tabla de contenido automática y aplica estilos a títulos, listas y negritas.
    """
    # Convertir Markdown a HTML
    html = markdown2.markdown(markdown_text)
    soup = BeautifulSoup(html, "html.parser")
    doc = Document()

    # Añadir título para la tabla de contenido
    doc.add_heading("Tabla de contenido", level=1)
    # Instrucción para el usuario (en un párrafo aparte, antes del campo TOC)
    doc.add_paragraph("(Pulsa Ctrl + A -o Ctrl + E en algunas configuraciones regionales- y luego F9 para actualizar la tabla de contenido y ver los títulos)", style="Intense Quote")

    # Insertar tabla de contenido automática (campo TOC) en un párrafo propio, sin texto adicional
    p = doc.add_paragraph()
    fldChar_begin = OxmlElement('w:fldChar')
    fldChar_begin.set(qn('w:fldCharType'), 'begin')
    instrText = OxmlElement('w:instrText')
    instrText.text = 'TOC \\o "1-3" \\h \\z \\u'
    fldChar_separate = OxmlElement('w:fldChar')
    fldChar_separate.set(qn('w:fldCharType'), 'separate')
    fldChar_end = OxmlElement('w:fldChar')
    fldChar_end.set(qn('w:fldCharType'), 'end')
    r = p.add_run()._r
    r.append(fldChar_begin)
    r.append(instrText)
    r.append(fldChar_separate)
    r.append(fldChar_end)
    p.alignment = 0  # left

    # Salto de página tras la TOC
    doc.add_page_break()

    def clean_heading(text: str) -> str:
        # Elimina patrones tipo {#...} al final del texto
        import re
        return re.sub(r'\s*\{#.*?\}\s*$', '', text).strip()

    def add_element(element: Any):
        if element.name == "h1":
            doc.add_heading(clean_heading(element.get_text()), level=1)
        elif element.name == "h2":
            doc.add_heading(clean_heading(element.get_text()), level=2)
        elif element.name == "h3":
            doc.add_heading(clean_heading(element.get_text()), level=3)
        elif element.name == "ul":
            for li in element.find_all("li", recursive=False):
                doc.add_paragraph(li.get_text(), style="List Bullet")
        elif element.name == "ol":
            for li in element.find_all("li", recursive=False):
                doc.add_paragraph(li.get_text(), style="List Number")
        elif element.name == "p":
            p = doc.add_paragraph()
            for child in element.children:
                if getattr(child, "name", None) == "strong":
                    run = p.add_run(clean_heading(child.get_text()))
                    run.bold = True
                else:
                    p.add_run(str(child))
        elif element.name == "strong":
            run = doc.add_paragraph().add_run(clean_heading(element.get_text()))
            run.bold = True
        elif element.name is None:
            doc.add_paragraph(element)
        # Puedes agregar más reglas para otros elementos

    for el in soup.body.contents if soup.body else soup.contents:
        add_element(el)

    output = BytesIO()
    doc.save(output)
    output.seek(0)
    return output

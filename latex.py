from pdflatex import PDFLaTeX
from os import path

def convert_latex_to_pdf(latex: str, file_name: str = 'default'):
    file_path = path.abspath(path.join('assets/documents', file_name + '.pdf'))


    with open(file_path, 'w+') as f:
        f.write(latex)


    pdfl = PDFLaTeX.from_texfile(file_path)
    pdfl.add_args({
        '-output-directory': './assets/documents',
    })
    pdfl.create_pdf(keep_pdf_file=True)
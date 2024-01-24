import subprocess
import argparse
import fitz
from PIL import Image
import os
 
packages = ['PyMuPDF', 'argparse', 'Pillow']
 
for package in packages:
    try:
        subprocess.check_call(['pip', 'install', package])
        print(f"Instalado com sucesso: {package}")
    except subprocess.CalledProcessError:
        print(f"Erro ao instalar: {package}")
 
def convert_pdf_to_images(input_file, output_dir, dpi=300, passwords=None):
    images = []
 
    try:
        pdf_document = fitz.open(input_file)
    except ValueError as e:
        if "document closed or encrypted" in str(e):
            if passwords:
                for password in passwords.split():
                    try:
                        pdf_document = fitz.open(input_file, password=password)
                        break
                    except RuntimeError:
                        print(f"Senha incorreta: {password}")
                else:
                    print("Todas as senhas testadas são incorretas.")
                    return
            else:
                print("O PDF está protegido por senha, mas nenhuma senha foi fornecida.")
                return
        else:
            print("Erro ao abrir o PDF: ", e)
            return
 
    for page_number in range(len(pdf_document)):
        page = pdf_document.load_page(page_number)
        image = page.get_pixmap(matrix=fitz.Matrix(dpi / 72, dpi / 72))
        image_path = os.path.join(output_dir, f'page_{page_number + 1}.jpeg')
        Image.frombytes("RGB", [image.width, image.height], image.samples).save(image_path, 'JPEG', dpi=(dpi, dpi))
        images.append(image_path)
 
    pdf_document.close()
    return images
 
def main():
    parser = argparse.ArgumentParser(description='Convert PDF to images.')
    parser.add_argument('input_file', help='Path to the input PDF file')
    parser.add_argument('--output_dir', default='output', help='Directory to save output images (default: "output")')
    parser.add_argument('--passwords', help='Password(s) for password-protected PDFs')
    parser.add_argument('--dpi', type=int, default=300, help='Quality in DPI (800, 500, or 300)')
 
    args = parser.parse_args()
 
    if not os.path.exists(args.output_dir):
        os.makedirs(args.output_dir)
 
    images = convert_pdf_to_images(args.input_file, args.output_dir, dpi=args.dpi, passwords=args.passwords)
 
    if images:
        print(f"PDF convertido para imagens com sucesso!")
        for image in images:
            print(f"Imagem gerada: {image}")
    else:
        print("Erro ao converter PDF para imagens.")
 
if __name__ == '__main__':
    main()

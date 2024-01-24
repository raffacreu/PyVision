import os
import win32com.client
import argparse

def doc_to_pdf(input_file, output_dir):
    word = win32com.client.Dispatch("Word.Application")
    doc = word.Documents.Open(input_file)

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    output_file = os.path.join(output_dir, os.path.splitext(os.path.basename(input_file))[0] + ".pdf")
    doc.SaveAs(output_file, FileFormat=17)

    doc.Close()
    word.Quit()

    print(f"Arquivo {input_file} convertido com sucesso para {output_file}")

def main():
    parser = argparse.ArgumentParser(description='Convert DOC to PDF')
    parser.add_argument('input_file', help='Caminho para o arquivo DOC')
    parser.add_argument('output_dir', help='Caminho para o diretório de saída')
    args = parser.parse_args()

    input_file = args.input_file
    output_dir = args.output_dir

    doc_to_pdf(input_file, output_dir)

if __name__ == "__main__":
    main()
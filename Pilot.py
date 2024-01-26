import subprocess
import os
import shutil

def convert_pdf_to_images(input_file, output_dir, dpi):
    images = []
    try:
        pdf_to_image_script = "Convert.py"
        subprocess.check_call(['python', pdf_to_image_script, input_file, '--output_dir', output_dir, '--dpi', str(dpi)])
        
        # Nome do arquivo original sem a extensão
        original_filename = os.path.splitext(os.path.basename(input_file))[0]
        
        # Listar os arquivos JPEG e ordená-los pelo nome
        files = sorted([f for f in os.listdir(output_dir) if f.lower().endswith(".jpeg")], key=lambda x: int(x.split('_')[1].split('.')[0]) if x.split('_')[1].split('.')[0].isdigit() else float('inf'))
        
        for i, file_name in enumerate(files):
            # Renomear os arquivos com o nome original do PDF e manter a extensão .pdf
            if file_name == f"page_{i + 1}.jpeg":
                new_filename = f"{original_filename}_{i + 1}.jpeg"
                new_filepath = os.path.join(output_dir, new_filename)
                old_filepath = os.path.join(output_dir, file_name)
                os.rename(old_filepath, new_filepath)
                images.append(new_filepath)

        print("Arquivos renomeados com sucesso!")
    except subprocess.CalledProcessError as e:
        print(f"Erro ao converter PDF para imagens: {e}")
    return images
    

def process_images_with_textract(images, access_key, secret_key, output_dir, dpi):
    textract_script = "Textract.py"
    try:
        all_text = ""  # Variável para armazenar o texto de todas as páginas

        for image in images:
            try:
                subprocess.check_call(['python', textract_script, image, '--access_key', access_key, '--secret_key', secret_key, '--output_dir', output_dir])
                print(f"Texto extraído da imagem {image} com sucesso!")
            except subprocess.CalledProcessError as e:
                print(f"Erro ao extrair texto da imagem {image}: {e}")
                # Se a extração falhar, tentar com uma qualidade (DPI) menor
                return False

        print("Texto de todas as páginas salvo com sucesso!")
    except IOError as e:
        print(f"Erro ao abrir o arquivo de saída: {e}")
        return False
    return True

def clean_output_directory(output_directory):
    for file_name in os.listdir(output_directory):
        if file_name.lower().endswith(".jpeg"):
            file_path = os.path.join(output_directory, file_name)
            os.remove(file_path)

def main():
    input_pdf = input("Informe o caminho do arquivo PDF: ")
    output_directory = input("Informe o diretório de saída para as imagens: ")
    access_key = input("Informe a chave de acesso AWS: ")
    secret_key = input("Informe a chave secreta AWS: ")
    output_text_file = "output_text.txt"

    dpi_values = [800, 500, 300]

    for dpi in dpi_values:
        images = convert_pdf_to_images(input_pdf, output_directory, dpi)
        if images:
            if process_images_with_textract(images, access_key, secret_key, output_directory, dpi):
                print("Processo concluído com sucesso!")
                break
            else:
                print("Negado, diminuindo a qualidade...")
                clean_output_directory(output_directory)
                # Verificar se o arquivo PDF ainda existe antes de tentar converter novamente
                if not os.path.exists(input_pdf):
                    print(f"Arquivo PDF não encontrado: {input_pdf}")
                    break
        else:
            print("Erro inesperado, analise a situação")
            break

if __name__ == '__main__':
    main()
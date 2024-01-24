import subprocess
import argparse
import boto3
import os

# Lista de pacotes a serem instalados
packages = ['boto3']

for package in packages:
    try:
        subprocess.check_call(['pip', 'install', package])
        print(f"Instalado com sucesso: {package}")
    except subprocess.CalledProcessError:
        print(f"Erro ao instalar: {package}")

def detect_text_in_image(image_path, access_key, secret_key, output_dir):
    client = boto3.client(
        'textract',
        region_name='us-east-1',
        aws_access_key_id=access_key,
        aws_secret_access_key=secret_key
    )

    with open(image_path, 'rb') as image:
        img = bytearray(image.read())

    response = client.detect_document_text(
        Document={'Bytes': img}
    )

    text = ""
    for item in response["Blocks"]:
        if item["BlockType"] == "LINE":
            text += item["Text"] + "\n"

    # Certificar-se de que o diretório existe antes de salvar
    os.makedirs(output_dir, exist_ok=True)

    # Obter o nome do arquivo a partir do caminho da imagem
    file_name = os.path.splitext(os.path.basename(image_path))[0]

    # Salvar o texto em um arquivo .txt no mesmo diretório das imagens
    output_file = os.path.join(output_dir, f"{file_name}_output_text.txt")
    with open(output_file, 'w', encoding='utf-8') as txt_file:
        txt_file.write(text)

def main():
    parser = argparse.ArgumentParser(description='Convert image to text using Amazon Textract')
    parser.add_argument('image_path', help='Path to the input image (PNG)')
    parser.add_argument('--access_key', required=True, help='AWS access key')
    parser.add_argument('--secret_key', required=True, help='AWS secret access key')
    parser.add_argument('--output_dir', required=True, help='Directory to save output text files (TXT)')

    args = parser.parse_args()
    detect_text_in_image(args.image_path, args.access_key, args.secret_key, args.output_dir)

    print("Arquivo extraído com sucesso!")

if __name__ == '__main__':
    main()

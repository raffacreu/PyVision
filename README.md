# PDF to Text Extraction Script

## Resumo do Projeto

Este projeto consiste em um script em Python que automatiza a extração de texto de um arquivo PDF. O script realiza as seguintes etapas:

1. Converte cada página do PDF em uma imagem JPEG com qualidade de DPI especificada (800, 500 ou 300).
2. Utiliza o serviço Textract da AWS para extrair o texto de cada imagem.
3. Concatena o texto de todas as páginas em um único arquivo TXT.

O script foi desenvolvido para lidar com casos em que a qualidade inicial de 800 DPI pode ser muito alta, levando a problemas na extração de texto. Nesses casos, o script diminui progressivamente a qualidade para 500 DPI e, em seguida, para 300 DPI, até que o texto seja extraído com sucesso. Se o processo falhar em todas as três qualidades, uma mensagem de erro é exibida.

## Como Usar

### Requisitos

Certifique-se de ter instalado as bibliotecas necessárias executando:

```bash 
pip install PyMuPDF argparse Pillow boto3
```

## Execução
Execute o script Pilot.py para iniciar o processo de conversão de PDF para texto. O script solicitará informações como o caminho do arquivo PDF, o diretório de saída para as imagens e as chaves de acesso da AWS.

```bash 
python Pilot.py
```
Siga as instruções no console para fornecer as informações necessárias.

## Estrutura do Código
- **Convert.py**: Converte um arquivo PDF em imagens JPEG com qualidade DPI especificada.
- **Textract.py**: Utiliza o serviço Textract da AWS para extrair texto de uma imagem.
- **Pilot.py**: Orquestra o processo completo, chamando os scripts anteriores e gerenciando a diminuição da qualidade em caso de falhas.

## Notas Importantes
- Certifique-se de fornecer as chaves de acesso da AWS para garantir o acesso ao serviço Textract.
- O script lida automaticamente com senhas de PDF protegidos.
- Se o processo for concluído com sucesso, será exibida a mensagem "Processo concluído com sucesso!".
- Em caso de falha em todas as qualidades de DPI, a mensagem de erro "Erro inesperado, analise a situação" será exibida.


Este projeto visa simplificar o processo de extração de texto de arquivos PDF, tornando-o automatizado e adaptável às diferentes condições de qualidade do documento.

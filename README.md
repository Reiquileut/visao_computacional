# Contador de Dedos - Aprendendo Matemática

Sistema de visão computacional para crianças aprenderem matemática usando os dedos! O programa usa a webcam para detectar quantos dedos a criança está mostrando e verifica se a resposta está correta.

## Descrição

Este projeto utiliza Python, OpenCV e MediaPipe para criar uma experiência interativa de aprendizado matemático. A criança vê uma pergunta de soma na tela (ex: 5 + 2 = ?) e responde mostrando a quantidade correta de dedos para a câmera.

## Funcionalidades

- **Detecção de mãos em tempo real** - Tracking visual dos movimentos das mãos
- **Contagem automática de dedos** - Suporta uma ou duas mãos
- **Perguntas de soma aleatórias** - Resultados sempre entre 1 e 10 (número de dedos)
- **Feedback visual imediato** - A criança vê quantos dedos o sistema detectou
- **Mensagem de parabéns** - Quando acertar a resposta
- **Interface amigável** - Botões e instruções claras na tela
- **Sistema de confirmação** - Aguarda 1 segundo para confirmar a resposta (evita falsos positivos)

## Objetivo

Ajudar crianças a aprenderem matemática básica de forma lúdica e interativa, usando uma ferramenta natural: seus próprios dedos!

## Pré-requisitos

- Python 3.7 ou superior
- Webcam conectada ao computador
- Windows, Linux ou macOS

## Instalação

### 1. Clone o repositório (ou baixe os arquivos)

```bash
git clone <url-do-repositorio>
cd visao_computacional
```

### 2. Crie um ambiente virtual (recomendado)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**Linux/macOS:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

## Como Usar

### Executar o programa

```bash
python contador_dedos_matematica.py
```

### Instruções durante o uso

1. **Uma pergunta de soma aparecerá na tela** (ex: 3 + 4 = ?)
2. **Mostre a resposta usando seus dedos** na frente da câmera
3. **Você verá o tracking da sua mão em tempo real** com pontos verdes e linhas azuis
4. **O número de dedos detectados aparece no canto superior esquerdo**
5. **Quando acertar:**
   - Uma mensagem "PARABÉNS! Você acertou!" aparecerá
   - Aguarde 1.5 segundos e um botão "Próxima" aparecerá
   - Clique no botão ou pressione **ESPAÇO** para a próxima pergunta
6. **Pressione ESC para sair** do programa

## Controles

- **ESPAÇO** - Próxima pergunta (após acertar)
- **ESC** - Sair do programa
- **Clique do mouse** - Clicar no botão "Próxima" (após acertar)

## Dicas para Melhor Detecção

1. **Iluminação** - Use ambiente bem iluminado
2. **Posição** - Mantenha as mãos à frente da câmera
3. **Fundo** - Evite fundos muito confusos
4. **Distância** - Fique a cerca de 50-70cm da câmera
5. **Dedos abertos** - Mantenha os dedos bem separados e visíveis

## Tecnologias Utilizadas

- **Python 3** - Linguagem de programação
- **OpenCV** - Processamento de imagem e vídeo
- **MediaPipe** - Detecção e tracking de mãos
- **NumPy** - Operações numéricas

## Como Funciona

### Detecção de Dedos

O sistema usa MediaPipe Hands para detectar 21 pontos de referência (landmarks) em cada mão. Para cada dedo:

- **Polegar**: Verifica a posição horizontal da ponta em relação à articulação
- **Outros dedos**: Verifica se a ponta está acima da articulação PIP (segunda articulação)

### Geração de Perguntas

As perguntas são geradas aleatoriamente com:
- Resultado entre 1 e 10 (número máximo de dedos)
- Dois números não-negativos que somam o resultado

### Sistema de Confirmação

Para evitar falsos positivos, o sistema:
1. Detecta a resposta correta
2. Aguarda 1 segundo confirmando que o número de dedos permanece correto
3. Mostra a mensagem de parabéns
4. Aguarda mais 1.5 segundos antes de mostrar o botão "Próxima"

## Solução de Problemas

### Câmera não é detectada
- Verifique se a webcam está conectada
- Certifique-se de que nenhum outro programa está usando a câmera
- Tente reiniciar o computador

### Dedos não são detectados corretamente
- Melhore a iluminação do ambiente
- Ajuste sua distância da câmera
- Certifique-se de que seus dedos estão completamente visíveis
- Evite fundos muito confusos ou da mesma cor da sua pele

### Programa lento ou travando
- Feche outros programas que usam muita memória
- Reduza a resolução da câmera (editar linha 218 do código)

## Personalização

Você pode personalizar o sistema editando `contador_dedos_matematica.py`:

- **Intervalo de respostas**: Altere linha 30 para mudar o máximo (atualmente 1-10)
- **Tempo de confirmação**: Altere linha 245 para ajustar o delay (atualmente 1.0 segundo)
- **Cores da interface**: Modifique as variáveis de cores nas linhas 40-44
- **Resolução da câmera**: Ajuste linhas 217-218

## Contribuindo

Sinta-se à vontade para contribuir com melhorias:
1. Fork o projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## Licença

Este projeto é livre para uso educacional.

## Suporte

Se encontrar problemas ou tiver sugestões, por favor abra uma issue no repositório.

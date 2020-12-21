# Quant_bot - bot trader do grupo de Quant do FEA.Dev

## Como baixar/modificar o código

1. É necessário baixar o Metatrader5 do site: <a href=https://www.metatrader5.com/en/download>https://www.metatrader5.com/en/download</a>
2. No CMD vá ao diretório no qual você quer o programa e rode: `git clone https://github.com/thomas-yasuoka/quant_bot.git`, isso irá criar uma pasta quant_bot
3. Vá para a pasta `cd quant_bot` e instale as dependências (é recomendado a criação de um ambiente virtual): `pip install -r requirements.txt`

## Rodando o programa

<img src=https://i.ibb.co/v4GHsBt/metatrader.png></img>

1. Ao clicar em Accounts há a opção Login to Trade Account, após realizar o login a conta irá aparecer ali

<img src=https://i.ibb.co/qRm04xS/1.png></img>

2. Antes de poder utilizar qualquer script é necessário habilitar a opção Algo Trading (a setinha verde indica que está habilitado)

<img src=https://i.ibb.co/M71gBrH/2.png></img>

3. A aba do Market Watch é importante, pois só é possível realizar operações através de script se o símbolo estiver presente nela

<img src=https://i.ibb.co/31syXtM/3.png></img>

Vá até o diretório `/quant_bot/src` e rode: `py main.py`

## Como criar uma branch

### Primeiro setup

1. git checkout -b branch_name (cria uma nova branch com o nome branch_name)
2. git add . (para adicionar o código que você clonou)

## Após o setup

1. git branch --show-current (pra verificar se você está na sua branch criada)
2. fazer as alterações no código
3. git add . (pra adicionar as alterações)
4. git commit -m "commit message"
5. git push --set-upstream https://github.com/thomas-yasuoka/quant_bot
6. Abrir a pull request a partir do github

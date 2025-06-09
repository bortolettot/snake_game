# Snake Game

O jogo agora pode ser executado tanto em computadores quanto em dispositivos Android.
Para jogar no computador utilize a versão original em Pygame:

```
pip install -r requirements.txt
python main.py
```

Para dispositivos Android foi adicionado o arquivo `kivy_main.py` baseado no Kivy e otimizado para toque. Após instalar as dependências (
`pip install -r requirements.txt`), execute:

```
python kivy_main.py
```

Para gerar um APK é possível usar o [Buildozer](https://github.com/kivy/buildozer).
Consulte a documentação do projeto para preparar o ambiente e então executar:

```
buildozer android debug
```

Ou utilize o script `./build_android_docker.sh` para compilar em um container Docker:
```
./build_android_docker.sh
```

Use as setas do teclado ou toques (deslizes) para mover sua cobra. A pontuação exibida no topo indica quantas comidas cada cobra coletou. Na tela
inicial também é possível selecionar a dificuldade tocando nos botões ou pressionando as teclas **1**, **2** ou **3**.

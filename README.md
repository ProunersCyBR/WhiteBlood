# WhiteBlood

## Sobre

WhiteBlood é um programa desenvolvido em Python e C++ que realiza a injeção de DLL e possui uma interface gráfica intuitiva. O programa foi projetado para monitorar chamadas para a função `NtWriteFile` e, se essa função for chamada mais de 5 vezes em um intervalo de 1 segundo, a chamada é alterada para `NtClose`. Isso não só impede o processo, mas também dá tempo para que o processo se auto-encerre.

## Instalação

A instalação do WhiteBlood é simples e direta. Basta baixar o instalador e executá-lo. Recomendamos manter o diretório padrão de instalação (Program Files (x86)). Após a instalação, basta executar o programa e ele funcionará conforme esperado.

## Funcionamento

O WhiteBlood foi desenvolvido em duas linguagens: Python e C++. O Python é usado para criar a interface gráfica do usuário e realizar a injeção de DLL. O C++ é usado para programar a DLL.

A DLL reescreve a função `NtWriteFile` do Windows. Ela monitora essa função em uma janela de tempo de 1 segundo. Se a função for chamada mais de 5 vezes nesse intervalo, a DLL troca a chamada de `NtWriteFile` para `NtClose`. Isso é feito sem que o processo saiba da mudança.

O objetivo dessa troca é duplo. Primeiro, ela impede o processo. Segundo, ela dá tempo para que o processo se auto-encerre.

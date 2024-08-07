**Universidade Federal do Agreste de Pernambuco**

**Compiladores – professora Maria Sibaldo**

# **Legenda:**

* Terminais serão estilizados em negrito  
* \< e \>: Definem uma variável (símbolo não-terminal);  
* ::=: Símbolo utilizado para geração;  
* \[ e \]: Definem um conteúdo que pode existir 0 ou 1 vez;  
* { e }: Definem um conteúdo que pode ser gerado 0 ou infinitas vezes;  
* ( e ): Agrupam símbolos e/ou regras;  
* |: Agrupa produções;  
* Espaços em branco serão desconsiderados e estão sendo usados apenas para organização;  
* □: É um terminal especial que representa um espaço em branco necessário.

* EOF: É um terminal especial que simboliza o fim do código fonte.

# **Produções:**

## **Programa:**

* \<program\> ::= \<cmd\_block\> \<program\>  
  * **procedure** \<id\> **(** \<params\> **)** \<block\> \<program\>  
  * **function** \<type\> \<id\> **(** \<params\> **)** **{** \<cmd\_block\> **return** \<expr\> **;** **}** \<program\>  
  * EOF

## **Valores:**

* \<d\> ::= **0** | **1** | **2** | **3** | **4** | **5** | **6** | **7** | **8** | **9**  
* \<c\> ::= **a** | **b** | **c** | **d** | **e** | **f** | **g** | **h** | **i** | **j** | **k** | **l** | **m** | **n** | **o** | **p** | **q** | **r** | **s** | **t** | **u** | **v** | **w** | **x** | **y** | **z** | **A** | **B** | **C** | **D** | **E** | **F** | **G** | **H** | **I** | **J** | **K** | **L** | **M** | **N** | **O** | **P** | **Q** | **R** | **S** | **T** | **U** | **V** | **W** | **X** | **Y** | **Z**  
* \<bool\> ::= **true** | **false**  
* \<num\> ::= \[ **\+** | **\-** \] \<d\> { \<d\> }

## 

## **Declarações:**

* \<id\> ::= \<c\> { \<c\> | \<d\> }  
* \<type\> ::= **int** | **bool**  
* \<var\_def\> ::= \<type\> \<id\>  
* \<params\> ::=  \<var\_def\> \<params\_separator\> | ε  
* \<params\_separator\> ::= **,** \<var\_def\> \<params\_separator\> |  ε


## **Comandos:**

* \<block\> ::= **{** \<cmd\_block\> **}**  
* \<cmd\_block\> ::= \<cmd\> \<cmd\_block\> | ε  
* \<cmd\> ::= \<id\> **\=** \<expr\> **;**  
  * \<id\> **(** \<args\> **)** **;**  
  * **if** \<expr\> \<block\> \<else\>  
  * **while** \<expr\> \<block\>  
  * **break;**  
  * **continue;**  
  * \<var\_def\> **;**  
  * **write(** \<expr\> **)** **;**  
  * \<read\> **;**  
* \<else\> ::= **else** \<block\> | ε

## 

## **Operadores:**

* \<log\_op\> ::= **&&** | **||**  
* \<rel\_op\> ::= **\==** | **\!=** | **\>=** | **\<=** | **\>** | **\<**  
* \<math\_op\> ::= **\+** | **\-** | **\*** | **/**

## **Expressões:**

* \<expr\> ::= **(** \<expr\> **)** \<expr\_2\>  
  * \<num\> \<expr\_2\>  
  * \<bool\> \<expr\_2\>  
  * \<id\> **(** \<args\> **)** \<expr\_2\>  
  * \<id\> \<expr\_2\>  
  * \<read\> \<expr\_2\>  
* \<expr\_2\> ::= □ \<log\_op\> □ \<expr\>  
  * □ \<rel\_op\> □ \<expr\>  
  * □ \<math\_op\> □ \<expr\>  
  * ε  
* \<read\> ::= **read()**  
* \<args\> ::= \<expr\> \<args\_separator\> | ε  
* \<args\_separator\> ::= **,** \<expr\> \<args\_separator\> | ε

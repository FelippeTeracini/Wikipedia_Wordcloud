# **Wikipedia Wordcloud**

Pipeline de Engenharia de Dados utilizando TF-IDF.

![](https://upload.wikimedia.org/wikipedia/commons/8/8a/V_wordcloud_skill.png)

## Introdução e Objetivos

Uma _Word Cloud_ é uma representação visual inovadora de dados de texto, normalmente usada para representar metadados de palavras-chave (tags) em sites ou para visualizar texto em formato livre. Tags são geralmente palavras únicas, e a importância de cada tag é mostrada com tamanho ou cor da fonte. Esse formato é útil para perceber rapidamente os termos mais importantes para determinar sua importância relativa. 

O objetivo desse trabalho é gerar uma _Word Cloud_ das palavras mais relevantes à outra palavra da Wikipedia. Isso pode ser realizado a partir de uma pipeline utilizando nossos conhecimentos de engenharia de dados. Essa pipeline ainda possui uma sub-pipeline que realiza o cálculo do TF-IDF das palavras relacionadas e com esses valores em mãos é possível gerar a WordCloud resultante.

## Metodologia

Para determinar os pesos foi utilizado o método TF-IDF, que é uma estatística numérica cujo objetivo é refletir a importância de uma palavra para um documento em uma coleção ou corpus. É frequentemente usado como um fator de ponderação em pesquisas de recuperação de informações, mineração de texto e modelagem de usuários. O valor TF-IDF aumenta proporcionalmente ao número de vezes que uma palavra aparece no documento e é compensado pelo número de documentos no corpus que contém a palavra, o que ajuda a ajustar o fato de que algumas palavras aparecem com mais frequência em geral.

O valor TF-IDF de uma palavra aumenta proporcionalmente à medida que aumenta o número de ocorrências dela em um documento, no entanto, esse valor é equilibrado pela frequência da palavra no corpus. Isso auxilia a distinguir o fato de a ocorrência de algumas palavras serem geralmente mais comuns que outras.

A pipeline pode ser reduzida a seis passos:

* Primeiramente os textos das páginas do .xml do wikipedia são obtidos e salvos em formato .parquet.
* Em seguida é gerado um dicionário com o valor IDF de cada palavra a partir da base de textos.
* O mesmo é relizado para os valores de TF de cada palavra.
* Assim obtêm-se o valor TF-IDF de cada uma e as top dez palavavras de cada página são filtradas.
* Essas dez palavras são permutadas para adquirir 90 pares.
* Finalmente há a contagem dos pares e cria-se um dicionário que será necessário para a formação do _Word Cloud_.

O dicionário final é salvo no cluster através do pickle e a biblioteca react-wordcloud consegue requisitá-lo, após a conversão para um formato compatível com ela, e assim gerar a _Word Cloud_ resultante.

## Infraestrutura e Conclusões

Foi utilizado o serviço de Clusters e Buckets da AWS S3 com a seguinte composição de máquinas:

* 1 Master - m4xLarge
* 2 Core - m4xLarge
* 35 Task - m4xLarge

Essa configuração foi pensada de modo que o número de Cores necessário para realizar a atividade num nível baixo, mas aceitável, seria pequeno, pois o trabalho não é muito custoso. Assim, mesmo que a AWS derrube as Tasks o projeto consegue continuar mesmo que mais lento.

Após realizados os teste com o banco completo, ficou claro que a pipeline estava lenta demais para que as queries pudessem ser feitas com eficiência. O que dificultou o debugging na medida que cada iteração do código demorava muito para ser testado. Para testar realmente o resultado do projeto foi feito um recorte da base de textos e essa tentativa obteve sucesso, provando a integridade da pipeline.

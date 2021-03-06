
# NOLEdge 🧠 🔎 📖

This repository hosts the source code, paper, and other documents created to support my Honors in the Major Thesis at Florida State University (home of the [Noles](https://seminoles.com)). 

Here's a screenshot of the demo Chrome Extension frontend for NOLEDGE:

![](./furc-poster/imgs/chromeextension.png)

And the Streamlit app that comes prepackaged with the [Deepset AI Haystack Docker Image](https://github.com/deepset-ai/haystack):

![](./furc-poster/imgs/streamlit.png)

## Contents of Repository:

### [Helpful Articles](https://github.com/comacrae/noledge/tree/main/helpful-articles)

Tutorials I used while implementing my deployment

### [FURC Poster](https://github.com/comacrae/noledge/tree/main/furc-poster)

The poster, images, and Bibtex reference for my presentation at [FURC 2022](https://www.floridaundergradresearch.org/furc22).

### [Scripts](https://github.com/comacrae/noledge/tree/main/scripts)

Scripts for a Flask deployment demo (now deprecated, but was the original method of deployment before Haystack 1.0 was released) and a ScraPy scraper which can clean up webscraped text.

### [Corpus](https://github.com/comacrae/noledge/tree/main/cs-fsu-domain-corpus)

The documents used as the corpus for NOLEdge, as well as the source of documents to annotate for training.

### [Colab Notebooks](https://github.com/comacrae/noledge/tree/main/colab-notebooks)

The Google Colab notebooks I used for the majority of my workflow, from training to evaluating models and creating plots.

### [Chrome Extension](https://github.com/comacrae/noledge/tree/main/chrome-extension)

The source code for the demo Chrome Extension I used to deploy my finetuned model.

### [Thesis](https://github.com/comacrae/noledge/tree/main/thesis)

Final draft of my Honors in the Major thesis as well as images and Bibtex references.

### [Evaluations](https://github.com/comacrae/noledge/tree/main/evaluations)

Plots and JSON data used to create them. Google Colab notebooks used to create the plots are in the notebook section.

### [Training Sets](https://github.com/comacrae/noledge/tree/main/training-sets)

The training sets used to train the various forms of the model. Includes the unsplit version, the unaugmented (but split) version, and the augmented versions.

## Hugging Face Model
[Go here to check out/download my finetuned model](https://huggingface.co/comacrae/roberta-paraphrasev2)


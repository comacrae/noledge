import json
from flask import jsonify
import sys, os
import time
from haystack.document_store.memory import InMemoryDocumentStore
from haystack.document_store.elasticsearch import ElasticsearchDocumentStore
from haystack.preprocessor.utils import convert_files_to_dicts
from haystack.reader.farm import FARMReader
from haystack.reader.transformers import TransformersReader
from haystack.retriever.sparse import TfidfRetriever
from haystack.preprocessor import PreProcessor
from haystack.pipeline import ExtractiveQAPipeline

"""To ensure that the Flask app can handle results as expected"""
def print_answers_demo(top_k=0):
    fp = open('./response.json', 'r')
    entries = json.load(fp)
    answers = process_answers(entries)
    return answers[0:min(len(answers),top_k)]

"""Makes the probablility metric easier to read when printed to the web interface"""
def process_answers(results):
    answers = results['answers']
    processed_answers = []
    for ans in answers:
        ans['probability'] = format(ans['probability'], '.2f')
    answers = sorted(answers, key= lambda k: k['probability'], reverse=True)
    return answers

def get_answers(question = None, pipeline=None, top_k=10):
    if question and pipeline is not None:
        if top_k < 10 and top_k >0:
            response_dict = {'answers':None, 'question':question}
            response_dict['answers'] = pipeline.run(query=question, top_k_reader=top_k, top_k_retriever=top_k)
            return response_dict
    elif question is None:
        return jsonify({'error':'no question'})
    elif pipeline is None:
        return jsonify({'error':'pipeline not initialized'})

"""Converts all json files in directory to a list of dicts"""
def convert_json_to_dict(dir_path):
    file_list = os.listdir(dir_path)
    dicts = []
    for filename in file_list:
        if ".json" in filename:
            with open(os.path.join(dir_path,filename)) as fp:
                dicts.append(json.load(fp))
    return dicts

def setup_reader(model_name_or_path="",hf_reader=False):
    reader = None
    if len(model_name_or_path) == 0:
        print("Error: no model or path entered")
    else:
        if not hf_reader:
            reader = FARMReader(model_name_or_path, use_gpu=False)
        else:
            reader = TransformerReader(model_name_or_path, use_gpu=True)

    return reader

def setup_retriever(document_store=None):
    if document_store is None:
        print("Document_store object must be initialized.",file=sys.stderr)
        return None
    else:
            return TfidfRetriever(document_store)

def setup_document_store(dir_path=None):
    doc_store =InMemoryDocumentStore(similarity="cosine", duplicate_documents="skip")

    if dir_path is not None:
        processor = PreProcessor(
            clean_empty_lines=True,
            clean_whitespace=True,
            clean_header_footer=True,
            split_by="word",
            split_length=2000,
            split_respect_sentence_boundary=True,
            split_overlap=0
        )
        processed_docs = []
        docs = convert_json_to_dict(dir_path)
        for doc in docs:
            splits = processor.process(doc)
            for split in splits:
                processed_doc = {'text': '', 'meta': {'url': ''}} # for finding url later 
                processed_doc['text'] = split['text']
                processed_doc['meta']['url'] = doc['url']
                processed_docs.append(processed_doc)
        doc_store = InMemoryDocumentStore()
        doc_store.write_documents(processed_docs)

    return doc_store

def setup_pipeline(model_name_or_path=None, dir_path = None ):
    doc_store = setup_document_store(dir_path=dir_path)
    retriever = setup_retriever(document_store = doc_store)
    reader = setup_reader(model_name_or_path=model_name_or_path)
    pipeline = ExtractiveQAPipeline(reader, retriever)
    return pipeline

if __name__ == "__main__":
    print(print_answers_demo(int(input("enter top_k"))))





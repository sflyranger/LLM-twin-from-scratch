# LLM-twin-from-scratch
My Version of the LLM Engineers Handbook, I chose to make my own instead of forking because I wanted to code all of the files from scratch to gain a more in depth understanding of the underlying processes for the model.

One major thing I learned in grad school is that to truly understand something you have to do it, not just read about it. While I have read through most of the LLM Engineers Handbok already, I felt that I was lacking in understanding of some of the files and how they operate within the FTI pipeline framework. That is why I set up this repository. While many of the files I will be coding here will be very similar or at times exactly like the files from the LLM Engineers Handbook Repo, I will be making modifications when necessary to fit my needs while extensively documenting the process. 

The goal is to create my own LLM Twin chatbot and deploy it as an example on the Huggingface platform so that others can view my work and as a proof of concept to future employers. The LLM Twin creation process will broaden my knowledge base of how to fully enact a model of my own that can be scaled to production. It is important to note that I have limited resources for future scaling so this project may never get that far, but the goal is not to use this model personally. I want to learn and broaden my knowledge. Let's get started.


Day 1:
For the first day of me copying the files I chose to begin by setting up the pyproject.toml file and the docker-composition file. I did this because at the beginning of the book the pyproject file sets the precendent for the entire file system by setting up the neccessary package installations and dependencies. I made some edits to the file to set up my own personal etl pipeline instead of the one from the original authors. Based on this, I set out to create the file system and dependencies to create the etl pipeline for my own personal data.

Day 2:
I began exploring the crawl_links.py file and followed the file lineage to really understand where each file pulled its functions and classes from. Based on my learning I began crafting each python file and documenting my learning of each class and function. Since the crawl_links.py file is designed to crawl different webpages specified in the authors etl_configurations.yaml files, I chose to begin creating the llm_engineering framwework files needed to make mongodb connections and create the necessary crawler dispatchers for each document class. 

Day 3:
Today is a continuation of yesterday with the creation and typing of the file system. Already I have begun to understand how the crawler uses the different document classes to create and access mongodb for NoSQL documents. I have written many files that perform various functions for the etl pipeline. Today my plan is to keep writing with the goal of finishing the digital_data_etl.py file and all of its dependencies. Over the next couple of days when I finish these files I plan on attempting to run the pipeline from the book but with my own data. I should be able to get the mongo db connection and the docker containers up and running without using the authors full file set, hopefully. From there I will continue building each pipeline and building my own personal LLM Twin.


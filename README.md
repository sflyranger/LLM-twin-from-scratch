# LLM-twin-from-scratch

My Version of the LLM Engineers Handbook. I chose to make my own instead of forking because I wanted to code all of the files from scratch to gain a more in depth understanding of the underlying processes for the model.

One major thing I learned in grad school is that to truly understand something you have to do it, not just read about it. While I have read through most of the LLM Engineers Handbook already, I felt that I was lacking in understanding of some of the files and how they operate within the FTI pipeline framework. That is why I set up this repository. While many of the files I will be coding here will be very similar or at times exactly like the files from the LLM Engineers Handbook Repo, I will be making modifications when necessary to fit my needs while extensively documenting the process.

The goal is to create my own LLM Twin chatbot and deploy it as an example on the Huggingface platform so that others can view my work and as a proof of concept to future employers. The LLM Twin creation process will broaden my knowledge base of how to fully enact a model of my own that can be scaled to production. It is important to note that I have limited resources for future scaling so this project may never get that far, but the goal is not to use this model personally. I want to learn and broaden my knowledge. Let's get started.

---

### Day 1:

For the first day of me copying the files I chose to begin by setting up the `pyproject.toml` file and the docker-composition file. I did this because at the beginning of the book the pyproject file sets the precedent for the entire file system by setting up the necessary package installations and dependencies. I made some edits to the file to set up my own personal etl pipeline instead of the one from the original authors. Based on this, I set out to create the file system and dependencies to create the etl pipeline for my own personal data.

---

### Day 2:

I began exploring the `crawl_links.py` file and followed the file lineage to really understand where each file pulled its functions and classes from. Based on my learning I began crafting each python file and documenting my learning of each class and function. Since the `crawl_links.py` file is designed to crawl different webpages specified in the authors `etl_configurations.yaml` files, I chose to begin creating the `llm_engineering` framework files needed to make mongodb connections and create the necessary crawler dispatchers for each document class.

---

### Day 3:

Today is a continuation of yesterday with the creation and typing of the file system. Already I have begun to understand how the crawler uses the different document classes to create and access mongodb for NoSQL documents. I have written many files that perform various functions for the etl pipeline. Today my plan is to keep writing with the goal of finishing the `digital_data_etl.py` file and all of its dependencies. Over the next couple of days when I finish these files I plan on attempting to run the pipeline from the book but with my own data. I should be able to get the mongo db connection and the docker containers up and running without using the authors full file set, hopefully. From there I will continue building each pipeline and building my own personal LLM Twin.

---

#### Important Notes:

- Based on todays creation of the first pipeline being used via Zenml I want to make my knowledge more concrete by writing out my thoughts and understanding.
- The authors have created the file system intricately such that we can use any orchestrator to execute the knowledge necessary to run the pipelines.
- **What does this mean?**
  - It means that all of the `@pipeline` steps and `@step` portions of the pipeline are stored separately from the pipelines module in the `llm_engineering` file folder.
  - This allows the user to easily switch orchestrators if necessary since all of the application and domain logic is stored in `llm_engineering` and the zenml orchestrator logic is stored in the pipelines and steps folders. So, to make the switch I would only need to change the zenml code, not the full logic.
  - Within the steps and pipeline module, they only used the things needed from the `llm_engineering` module, this keeps the logic separate.
- Values that are to be returned from zenml have to be serializable, meaning that it can be converted to a format suitable for storage or transmission and later reconstructed (deserialized) into its original form.
- All data and artifacts along with their metadata are stored in the zenml dashboard and can be viewed there.
- Metadata is added manually to the artifact allowing me to precompute and attach anything that is helpful for dataset discovery across projects.

---

#### `run.py`:

- Everything for zenml can be run via this file.
- Given that this file holds and entails all of the pipelines and commands within the code, I want to save writing this file until I have fully finished the book and all of the logic, pipelines, etc.

---

#### MongoDB:

MongoDB is chosen as the storage location for the etl pipeline because not many documents are used in the proof of concept. Thus small scale statistics can be calculated and little cost incurred. Should the twin be scaled out to include millions of documents or more then a large scale data warehouse such as Snowflake or BigQuery should be used.

---

#### Crawlers:

Each of the crawler classes implements custom logic to access the articles, posts, and repositories with the exception of the `CustomArticleCrawler`:

- **GithubCrawler** - Crawls and stores Github repos.
- **MediumCrawler** - Crawls and stores Medium articles based on HTML.
- **LinkedInCrawler** - Crawls and stores LinkedIn posts.
- **CustomArticleCrawler** - Crawls articles outside of the designated domains for the other crawlers. (No custom logic - primarily a fallback.)

---

#### Decisions:

I coded each of these crawlers, later to find out that based on the sources I will be using for my data, I will not be using the `CustomArticleCrawler` or the `MediumCrawler`.

- The `CustomArticleCrawler` uses LangChain packages as a fallback method to crawl different domains and is generally not used in production environments anyway.

    

        

        






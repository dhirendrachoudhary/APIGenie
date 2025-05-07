# APIGenie 🧞

**APIGenie: Your AI-Powered Assistant for Navigating and Composing Software APIs.**

APIGenie helps developers discover relevant API components through natural language queries and conceptualizes how these can be combined to achieve specific goals. It aims to simplify API interaction and accelerate development workflows, starting with scikit-learn and designed for broader applicability.

**Project Status:** Prototype / Proof of Concept

## 🌟 Key Features

* **Natural Language Querying:** Find APIs by describing your needs in plain English.
* **Semantic API Retrieval:** Utilizes vector embeddings (via Sentence Transformers) and a vector database (ChromaDB) for intelligent, context-aware API search.
* **Conceptual Workflow Suggestion:** Generates structured prompts, based on your query and retrieved APIs, ready for a Large Language Model (LLM) to help outline a potential implementation pipeline. (Note: Direct LLM integration for automated pipeline generation is a planned enhancement).
* **Interactive Command-Line Interface (CLI):** Allows for easy querying, data inspection, and session management.
* **Data Dumping:** Enables exporting processed and flattened API information to a JSON file.
* **Extensible Data Source:** Designed to load API information from a JSON file, adaptable for other structured data sources.

## 🤔 Why APIGenie?

Developers often face challenges like:
* Navigating extensive and complex API documentation.
* Identifying the precise function or class for a specific task.
* Figuring out the correct sequence and combination of API calls for a complete workflow.

APIGenie aims to mitigate these challenges by offering an intelligent search and suggestion system, making API discovery and initial workflow design more intuitive and efficient.

## 🛠️ How It Works (High-Level)

1.  **Data Ingestion & Processing:**
    * API documentation (e.g., from an input `sklearn_apis.json`) is loaded.
    * This data is flattened into individual API "documents," each detailing an API's name, module, signature, example code, etc.
2.  **Embedding Generation:**
    * A Sentence Transformer model (e.g., `all-MiniLM-L6-v2`) converts the textual description of each API into a numerical vector embedding, capturing its semantic meaning.
3.  **Vector Database Storage:**
    * These embeddings, along with associated API metadata, are stored in a ChromaDB collection. This allows for fast and efficient similarity searches. The database persists locally.
4.  **User Interaction (CLI):**
    * The user inputs a natural language query (e.g., "How do I build a text classifier for multi-class problems?").
5.  **Query Embedding & Semantic Search:**
    * The user's query is transformed into an embedding using the same Sentence Transformer model.
    * A similarity search is performed against the API embeddings in ChromaDB to find and rank the most relevant APIs.
6.  **Results & LLM Prompt Formulation:**
    * The top N relevant APIs are presented to the user.
    * A structured prompt is automatically generated. This prompt includes the user's original goal and the details of the retrieved APIs, designed to be fed into a Large Language Model (LLM) for generating conceptual pipeline suggestions or code snippets.

## 📋 Prerequisites

* Python 3.8+
* Pip (Python package installer)

## 🚀 Installation & Setup

1.  **Clone the Repository (if applicable) or Download the Script:**
    ```bash
    # If you have a git repository:
    # git clone https://your-repository-url/APIGenie.git
    # cd APIGenie
    ```

2.  **Create and Activate a Virtual Environment (Recommended):**
    ```bash
    python -m venv venv
    # On macOS/Linux:
    source venv/bin/activate
    # On Windows:
    # venv\Scripts\activate
    ```

3.  **Install Dependencies:**
    ```bash
    pip install sentence-transformers chromadb numpy
    ```

4.  **Prepare Your API Data:**
    * Ensure your API data is in the expected JSON format. The script defaults to looking for `sklearn_apis.json`.
        *Example structure:*
        ```json
        {
            "module.name": {
                "link": "[https://docs.example.com/module](https://docs.example.com/module)",
                "subsections": {
                    "ClassName": {
                        "link": "[https://docs.example.com/module/ClassName](https://docs.example.com/module/ClassName)",
                        "class_signature": "class ClassName(param1, param2)",
                        "example_code": "from module import ClassName\nobj = ClassName()"
                    }
                    // ... more classes within the module
                }
            }
            // ... more modules
        }
        ```
    * Place this JSON file in the same directory as the main script, or update the `JSON_FILE_PATH` variable within the script.

## 💻 Usage

Execute the interactive script from your terminal:
```bash
python api_genie.py
```

## 🔮 Future Enhancements & Roadmap

* **Direct LLM Integration:** Implement direct calls to LLMs (e.g., via OpenAI API, Hugging Face Transformers, or locally hosted models) to automatically generate pipeline suggestions and code snippets.
* **Expanded API Compatibility:**
* Develop parsers for various API documentation formats (e.g., OpenAPI/Swagger, Javadoc, ReStructuredText from Sphinx).
* Create tools for easier scraping and ingestion of documentation from diverse software libraries.
* **Deeper API Understanding:**
* Implement robust classification of API types (e.g., transformer, estimator, data loader, utility function).
* Analyze parameter types, dependencies, and constraints for more accurate and reliable workflow construction.
* **Advanced Code Generation:** Progress from conceptual pipelines to generating executable and well-commented code blocks.
* **User Feedback Loop:** Incorporate a system for users to rate the relevance of retrieved APIs and the quality of suggested pipelines to iteratively improve APIGenie's performance.
* **Graphical User Interface (GUI):** Develop a web-based or desktop GUI for a more user-friendly experience.
* **Sophisticated Ranking Algorithms:** Enhance API ranking by considering factors beyond semantic similarity, such as API popularity, version compatibility, or project-specific context.

## 🤝 Contributing

Contributions are highly encouraged! If you have ideas for new features, improvements, or bug fixes, please feel free to:

1. Fork the repository.
2. Create a new branch (`git checkout -b feature/YourAmazingFeature`).
3. Make your changes.
4. Commit your changes (`git commit -m 'Add some AmazingFeature'`).
5. Push to the branch (`git push origin feature/YourAmazingFeature`).
6. Open a Pull Request.

Please open an issue first to discuss significant changes.
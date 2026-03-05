# PDF Search Engine & Analytical Indexer
An advanced Python-based search engine that transforms static PDF documents into a searchable Graph structure. By utilizing Tries for indexing and Boyer-Moore for pattern matching, the engine provides high-speed keyword search, phrase matching, and logical query parsing

## Key Features
PDF to Graph Conversion: Converts a PDF document into a Graph where each page is a node. Edges are created based on sequential page flow and cross-reference links (e.g., "see page 42")

- Trie-Based Indexing: Every page's content is indexed in a Trie (Prefix Tree), allowing for efficient word lookups and autocomplete suggestions.

- Advanced Search Modes:

  - Keyword Search: Finds individual words using the Trie.
  
  - Phrase Search: Matches exact phrases using the Boyer-Moore algorithm.
  
  - Logical Operators: Supports AND, OR, and NOT logic via an Infix-to-Postfix tokenizer.

- Intelligent Ranking: Results are ranked based on word frequency, phrase proximity, and page importance within the graph.

- Snippet Extraction: Displays search results with highlighted keywords and surrounding context (KWIC).

- Result Export: Dynamically generates a new PDF containing only the pages that matched your search criteria.


## Technical 
- StackPyMuPDF (fitz): For high-performance PDF parsing and page extraction
- Data Structures:
  - Graph: To represent the document structure and page relationships
  - Trie: For $O(L)$ time complexity word searching (where $L$ is word length)
  - Deque & Sets: For optimized DFS (Depth First Search) traversals
- Algorithms:
  - Merge Sort: To rank search results based on calculated relevance
  - Boyer-Moore: For efficient substring searching in phrase mode
  - Shunting-yard Algorithm: To parse complex logical search queries
 
## About the Implementation
This project goes beyond simple text searching by treating a book like a web of interconnected information.

### The "PageRank" Inspiration
The engine calculates a page_rank for each result. It doesn't just look at how many times a word appears on a page; it also considers the relevance of linked pages. If Page A contains a link to Page B, the relevance of Page B is influenced by the content of its parent page

### Prefix Searching & Autocomplete
By leveraging the Trie structure, the engine supports wildcard searching (e.g., graph*). It can instantly extract all words sharing a common prefix across hundreds of pages, providing real-time suggestions for common terms found in the specific document

### Logical Query Processing
The search engine includes a custom tokenizer that handles nested logic. It converts human-readable queries (Infix) into a machine-readable format (Postfix) to evaluate boolean conditions across the page nodes

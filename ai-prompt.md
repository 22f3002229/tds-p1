
## Phase A: Handle Operations Tasks

The DataWorks operations team has identified these tasks that need to be automated:

-   **A1**. Install  `uv`  (if required) and run  `https://raw.githubusercontent.com/sanand0/tools-in-data-science-public/tds-2025-01/project-1/datagen.py`  with  `${user.email}`  as the only argument. (**NOTE**: This will generate data files required for the next tasks.)
-   **A2**. Format the contents of  `/data/format.md`  using  `prettier@3.4.2`, updating the file in-place
-   **A3**. The file  `/data/dates.txt`  contains a list of dates, one per line. Count the number of Wednesdays in the list, and write just the number to  `/data/dates-wednesdays.txt`
-   **A4**. Sort the array of contacts in  `/data/contacts.json`  by  `last_name`, then  `first_name`, and write the result to  `/data/contacts-sorted.json`
-   **A5**. Write the first line of the 10 most recent  `.log`  file in  `/data/logs/`  to  `/data/logs-recent.txt`, most recent first
-   **A6**. Find all Markdown (`.md`) files in  `/data/docs/`. For each file, extract the first occurrance of each H1 (i.e. a line starting with  `#` ). Create an index file  `/data/docs/index.json`  that maps each filename (without the  `/data/docs/`  prefix) to its title (e.g.  `{"README.md": "Home", "path/to/large-language-models.md": "Large Language Models", ...}`)
-   **A7**.  `/data/email.txt`  contains an email message. Pass the content to an LLM with instructions to extract the sender’s email address, and write just the email address to  `/data/email-sender.txt`
-   **A8**.  `/data/credit-card.png`  contains a credit card number. Pass the image to an LLM, have it extract the card number, and write it without spaces to  `/data/credit-card.txt`
-   **A9**.  `/data/comments.txt`  contains a list of comments, one per line. Using embeddings, find the most similar pair of comments and write them to  `/data/comments-similar.txt`, one per line
-   **A10**. The SQLite database file  `/data/ticket-sales.db`  has a  `tickets`  with columns  `type`,  `units`, and  `price`. Each row is a customer bid for a concert ticket. What is the total sales of all the items in the “Gold” ticket type? Write the number in  `/data/ticket-sales-gold.txt`

Developers will call the  `/run?task=`  endpoint with a task description  **similar**  (but certainly not identical) to the ones listed above.

For example,  **Task A3**  can be written in these ways - all are equivalent.

-   The file  `/data/dates.txt`  contains a list of dates, one per line. Count the number of Wednesdays in the list, and write just the number to  `/data/dates-wednesdays.txt`
-   Write the # of Thursdays in  `/data/extracts.txt`  into  `/data/extracts-count.txt`
-   `/data/contents.log`  में कितने रविवार हैं? गिनो और /data/contents.dates में लिखो
-   `/data/contents.log`ல எத்தனை ஞாயிறு இருக்குனு கணக்கு போட்டு, அதை  `/data/contents.dates`ல எழுது

Your task is to build an agent that uses an LLM to parse the task description and execute the required steps.
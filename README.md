 # IG-SRL
<br />
<p align="center">
  <h2 align="center">Documentation</h2>


##Google Colab 

Google Colab is a cloud-based platform provided by Google that allows you to run and execute Python code in a Jupyter Notebook environment. It offers free access to a GPU and is commonly used for machine learning, data analysis, and prototyping.

###To get started with Google Colab, follow these steps:

- pen your web browser and go to the Google Colab website: https://colab.research.google.com/
- You'll be presented with the Google Colab welcome page. Here, you have the option to create a new notebook or open an existing one from your Google Drive.
- To create a new notebook, click on "New Notebook" or go to "File" -> "New Notebook."
- A new notebook will open in a new tab, similar to a Jupyter Notebook interface. You can now write and execute Python code in the cells of the notebook.
- To add a new cell, click on the "+" button in the toolbar or go to "Insert" -> "Code cell."
- To execute a code cell, either click on the "Play" button in the left margin of the cell or use the keyboard shortcut "Shift + Enter." The code will be executed, and the output will be displayed below the cell.
- To add text and documentation using Markdown cells. To add a Markdown cell, go to "Insert" -> "Text cell."
- To install and import libraries, upload files, access Google Drive, and perform other operations just like in a regular Jupyter Notebook.

##SRL- Semantic Role Labeling

###What is SRL?
SRL helps us understand sentences better. Imagine you have a sentence like "The cat chased the mouse." SRL helps us figure out what each word or phrase is doing in the sentence. For example, it tells us that "cat" is doing the action of chasing, and "mouse" is the thing being chased. It's like assigning roles to the words in a sentence!

###How Does SRL Work?
To use SRL, we need to train a computer program using lots of examples. These examples have sentences with annotated roles for each word or phrase. The program learns patterns from these examples to understand how words relate to each other in different roles.

Once the program is trained, we can give it new sentences, and it will tell us the roles of the words. For example, if we give it the sentence "The cat chased the mouse," it will say that "cat" is the "chaser" and "mouse" is the "chased."

###Why is SRL Useful?
SRL has many uses. Here are a few examples:

- Information Extraction: SRL helps us extract important information from sentences. We can find out who did what to whom and understand the relationships between different parts of the sentence.

- Question Answering: SRL helps us answer questions based on the information in a sentence. For example, if we're asked, "Who chased the mouse?" SRL can help us find the answer by identifying the role of the words in the sentence.

- Machine Translation: SRL can improve machine translation by understanding the roles and relationships of words in different languages. This helps in accurately translating sentences from one language to another.

###How Can We Use SRL?
We can use a library called AllenNLP to work with SRL. AllenNLP provides pre-built models and tools to make it easier for us to use SRL in our projects.

###To use SRL with AllenNLP, we follow these steps:

- Prepare Data: We need to gather examples of sentences with annotated roles. These examples help the computer program learn the patterns.

- Train the Model: We train the computer program using the annotated examples. It learns to predict the roles of words based on the patterns it sees in the data.

- Evaluate the Model: We check how well the program performs by testing it on new examples that it hasn't seen before. This helps us understand if it can accurately predict the roles.

- Predict Roles: Once the program is trained and evaluated, we can use it to predict the roles of words in new sentences. It will tell us the roles of each word, like who is doing the action and who is receiving the action.

- SRL and tools like AllenNLP make it easier for computers to understand sentences and extract meaningful information. By using SRL, we can teach computers to understand language better and help them perform tasks like answering questions or translating languages.

##Institutional Grammar

Institutional grammar is a way of looking at sentences and understanding how they work based on rules and relationships. It's like a set of guidelines that help us understand how words fit together to make sense.

Imagine you have a big box of puzzle pieces, and you want to put them together to create a beautiful picture. Institutional grammar is like having a set of rules that tell you how each puzzle piece should connect with the others. It helps you figure out the right places for each piece so that the puzzle makes sense as a whole.

Institutional grammar goes beyond just the words themselves. It also considers the bigger context, like the situation or the social interactions surrounding the sentence. It looks at how sentences are structured and the meanings behind them in specific situations, like in a legal case or a social interaction.

By following the rules of institutional grammar, we can analyze sentences and understand their deeper meaning. It helps us see the relationships between words and how they work together to convey information or express ideas.

So, institutional grammar is like a set of puzzle-solving rules for understanding sentences. It helps us put the pieces of a sentence together correctly and make sense of the bigger picture they create.




##Differences between the Approaches : Institutional Grammar & SRL

Institutional Grammar is a way to understand sentences by looking at the rules and logical relationships between the words. It focuses on how sentences are structured and the meanings behind them in specific situations, like in a legal or social context. It uses specific rules and principles to analyze sentences and figure out their meaning based on the actions and commitments involved.

On the other hand, Semantic Role Labeling (SRL) is all about understanding the roles of words in a sentence. It helps us figure out who is doing what in a sentence. For example, if we have the sentence "The dog chased the ball," SRL would tell us that "dog" is the one doing the action of chasing, and "ball" is the thing being chased. It labels the words in a sentence with specific roles, like "chaser" and "chased," to show how they relate to each other.

Institutional Grammar takes a more formal and rule-based approach to understand sentences, while SRL uses machine learning techniques to learn from examples and predict the roles of words in a sentence. Institutional Grammar looks at the bigger picture, considering social and institutional interactions, while SRL focuses on individual sentences and extracting meaningful information from them.

Institutional Grammar represents sentence structure and meaning using logical or symbolic representations, while SRL uses labels or tags to show the roles of words. For example, SRL might label a verb as the "action" and nouns as "doers" or "receivers" based on their roles in the sentence.

To summarize, Institutional Grammar helps us understand sentence structure and meaning in specific contexts, while SRL helps us identify the roles of words in sentences. Institutional Grammar uses rules and principles, while SRL uses machine learning to predict word roles.












##Datasets
Our main dataset is called the Standardized Siddiki Dataset which comprises of below given datasets-

###NationalOrganicProgramRegulations_Siddiki
- Econ Development Mechanisms
###FPC_Siddiki
- Camden Food Security
- Colorado Food systems Advisory
- Connecticut Food policy
- Denver Sustainable FPC
- Douglas County FPC
- Grant County FPC
- Hartford Food Commission
- Homegrown Minneapolis Council
- Louisville FPC
- Mass FPC
- Michigan FPC
- Nashville FPC
- New Haven FPC
- New Orleans Food advisory
- NewYork Council on Food
- San Francisco FPC
- Rio Arriba County
- Knoxville Knox County
- Saint Paul Ramsey 
###Colorado_AcquacultureRegulations_Siddiki
- Fish Health Board
- CAA Statute
- CAA Rules

All of them have a raw institutional statement, and corresponding Attribute, Deontic, Aim, Object, Conditions columns respectively as the primary important columns.










##Results

###Institutional Grammar Results

###Semantic Role Labeling Results 

###Comparison of both results

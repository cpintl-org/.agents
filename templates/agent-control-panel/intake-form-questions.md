# Request form (Google Forms) - questions to add

Create a Google Form named `agent-task-request` (**Google Forms → Blank form**). Add these questions in order. Link responses to a Sheet with **Responses → Link to Sheets**, then copy new rows into `AgentTasks` after a person has checked them.

1. What do you want done? (Paragraph, required)
2. Which approved sources should be used? (Short answer, required)
3. Is any information about a person, patient, or safeguarding case involved? (Multiple choice: Yes / No / Not sure, required)
4. Who will review the result before it is shared? (Short answer, required)
5. Where should the result go? (Multiple choice: Google Doc / Google Sheet / Markdown file / A person will do it by hand)

If the answer to question 3 is **Yes** or **Not sure**, the request is treated as `restricted` and handled by a person, not by AI.

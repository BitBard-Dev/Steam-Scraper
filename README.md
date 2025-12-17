## About
- A local Steam Marketplace scraper which acts as an independent Python program (no Jupyter Notebook dependency).
- Coding originally done as the final project/writeup for an _Introduction to Python_ course.
- Due to my lack of Python skills, steps of the project are divided across multiple files, requiring a lot of manual oversight. This is not ideal.

#### Steps
- [x] Upload original code
- [x] Refactor lump of spaghetti code into helper functions to main.py
  - [ ] config.py
  - [ ] API (steam & steamspy APIs)
  - [ ] Database (format API data into SQLite file & prepare for import into MongoDB)
  - [ ] Data Cleaning (general & language cleaning)
  - [ ] Analysis (Matplotlib)
  - [ ] Streamlit (Fancy UI for data analysis)
- [ ] Ensure functionality of each helper function
- [ ] Develop program UI (Necessary with Streamlit???)
- [ ] Compile program
  - [ ] Ensure functionality of compiled program
#### Features/Improvements
- [ ] Program has persistent memory of appids, reducing subsequent API query time (72hrs is __way__ too long)
- [ ] Progam automatically conducts data analysis
- [ ] Improve UI/UX
  - [ ] Graphs & charts
  - [ ] "Sexy" (non-placeholder) buttons

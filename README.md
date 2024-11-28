# AI Calc
This is the backend for the project. It leverages the Gemini API and MongoDB to perform its operations. This guide will walk you through setting up and running the project on your local machine.

---

## Prerequisites

Before getting started, ensure you have the following installed:

- **Python 3.8 or higher**: [Download here](https://www.python.org/downloads/)
- **pip** (Python package installer): Comes with Python installations.
- **MongoDB**: You need a MongoDB URL for connecting to your database.
- **Gemini API key**: Obtain it from [Gemini's official website](https://www.gemini.com/).

---

## Setup Instructions

### 1. Clone the Repository

To get started, clone the repository from GitHub:

```bash
git clone https://github.com/itspranaw/Shankhyasutra-be.git
cd Shankhyasutra-be

```
### 2. Create and activate the virutal environment 

```
python3 venv -v env
source env/bin/activate #for linux
env\Scripts\activate #for windows
```
### 3. Install the dependencies
```
pip install -r requirements.txt
```

### 4. Configure Environment variables
```
GEMINI_API_KEY = 
MONGODB_URL=
DB_NAME=
```

### 5. Run the server
```
python main.py
```


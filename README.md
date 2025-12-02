# 🚀 User Management REST API with SQLite & Automation

A robust, lightweight RESTful Web Service built with **Flask** (Python). This project demonstrates a complete Backend Engineering cycle: from API development and Database persistence to Automated Integration Testing.

> **Key Features:**
> - 🐍 **Flask Backend:** Handles HTTP Verbs (GET, POST, DELETE) efficiently.
> - 🗄️ **SQLite Persistence:** Self-contained database with auto-increment logic.
> - 🤖 **Automated Testing:** Python `unittest` script ensuring endpoint reliability.
> - 🌐 **Hybrid Data Source:** Merges local database records with external API data (JSONPlaceholder).
> - 🖥️ **Interactive Frontend:** Simple HTML/JS Dashboard for testing operations.

## 🛠️ Tech Stack
* **Language:** Python 3.x, JavaScript (ES6)
* **Framework:** Flask
* **Database:** SQLite3
* **Testing:** Unittest (Built-in Python library)
* **Frontend:** Bootstrap 5, Fetch API

## ⚙️ Installation & Setup

1.  **Clone the repository**
    ```bash
    git clone [https://github.com/username-anda/flask-sqlite-api.git](https://github.com/username-anda/flask-sqlite-api.git)
    cd flask-sqlite-api
    ```

2.  **Install Dependencies**
    ```bash
    pip install flask requests
    ```

3.  **Run the Server**
    ```bash
    python app.py
    ```
    The server will start at `http://127.0.0.1:5000`.

## 🧪 Automated Testing (Quality Assurance)
This project includes an automated test script to validate the CRUD lifecycle and database integrity (ensuring ID auto-increment works as expected).

Run the test suite:
```bash
python test_api.py

Expected Output:
[TEST 1] Mengecek Koneksi Server... ✅ OK
[TEST 2] Menguji Siklus Create & Delete... ✅ VALIDASI SUKSES
Ran 2 tests in 0.xxx seconds
OK

💡 Project Philosophy
This project was built to simulate a real-world Microservice architecture where data consistency and testing are paramount. The application handles data synchronization logic where local IDs automatically continue from the last external API ID index to prevent conflicts.

Created by Azhar Alzaki Rosanto - Software Engineering Student
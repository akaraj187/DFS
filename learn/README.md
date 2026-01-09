## Distributed File System Simulator

> **A fault-tolerant, self-healing file system simulation built in Python.**

##  About The Project
This project simulates the core architecture of a Distributed File System (like Google File System or HDFS) on a local machine. It demonstrates how large-scale systems handle data storage by treating local folders as distinct "Data Nodes."

The goal is to understand the trade-offs between **Sharding** (Speed) and **Replication** (Reliability) without needing a massive cluster of servers.

##  Key Features
* **Data Sharding:** Breaks large files (Images, PDFs) into binary chunks to distribute load.
* **Replication (Factor 2):** Automatically mirrors every chunk to a backup node.
* **Fault Tolerance:** The system detects if a "Primary Node" is missing (deleted) and automatically recovers data from the "Backup Node."
* **Binary Safety:** Handles raw byte streams, ensuring images and videos are restored byte-perfect.

##  Architecture
The system follows a Master-Worker architecture simulation:
1.  **The Client (Splitter):** Chops files into fixed-size blocks (default 1MB).
2.  **The Nodes (Storage):** Three separate directories (`node_1`, `node_2`, `node_3`) acting as independent servers.
3.  **The Logic (Distributor):** Uses Round-Robin scheduling to distribute chunks and ensures `Chunk N` is stored on `Node i` and `Node i+1`.


## Networked Mobile and Laptop as server to store data

       +-----------------------+
       |    CLIENT (Laptop)    |
       +-----------+-----------+
                   |
         +---------v---------+
         |     Reads File    |
         +---------+---------+
                   |
      +------------v------------+
      |  Splits into 1MB Chunks |
      +------------+------------+
                   |
          /--------+--------\
          |                 |
    +-----v------+    +-----v------+
    |  SOCKET 1  |    |  SOCKET 2  |
    +-----+------+    +-----+------+
          |                 |
    +-----v------+    +-----v------+
    |   NODE 1   |    |   NODE 2   |
    |  (Android) |    |  (Laptop)  |
    +------------+    +------------+


  ![WhatsApp Image 2026-01-09 at 2 03 27 PM](https://github.com/user-attachments/assets/072efc86-dd20-4667-94f5-bd876c2c48c8)

  

  

<img width="1626" height="915" alt="Screenshot (87)" src="https://github.com/user-attachments/assets/31b442e3-cc49-4965-93e0-ce785771a4d4" />

  

## 💻 How to Run
### Prerequisites
* Python 3.x
* No external libraries required (uses standard `os` and `shutil`).

### Usage
1.  **Clone the Repo:**
    ```bash
    git clone [https://github.com/akaraj187/DFS.git](https://github.com/akaraj187/DFS.git)
    cd DFS/learn/Distributor
    ```

2.  **Run the Simulation:**
    * Place an image (e.g., `test.jpg`) in the folder.
    * Run the script:
        ```bash
        python main.py
        ```
    *(Note: Replace `main.py` with your actual script name)*

3.  **Test the Fault Tolerance (The "Chaos Monkey"):**
    * After uploading, go to the `node_1` folder and **delete all files**.
    * Run the retrieval function.
    * Watch the console logs: You will see it detecting the failure and recovering from `node_2` or `node_3`.

## 🧠 What I Learned
* **Systems Programming:** Handling binary file I/O and buffer management.
* **Distributed Concepts:** Implementing **Striping** for performance and **Mirroring** for redundancy.
* **Failover Logic:** Writing code that anticipates hardware failure (FileNotFoundError) and reroutes requests.

## 🔮 Future Roadmap
* [ ] Implement a centralized **Metadata Server** (NameNode) to map filenames to block IDs.
* [ ] Add **Heartbeat signals** to detect dead nodes automatically.
* [ ] Upgrade from Replication to **Erasure Coding** (RAID 5 logic) to save storage space.

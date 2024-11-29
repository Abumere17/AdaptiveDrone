
# **Adaptive Drone Codebase**

Welcome to the Adaptive Drone codebase! This guide provides instructions for setting up Git and following best practices for version control to ensure smooth collaboration.

---

## **Setup Instructions**

Follow these steps to set up Git and start contributing:

1. **Ensure Git is Installed**:
   - Verify Git is installed by running:
     ```
     git --version
     ```
     If not, install Git from [Git's official website](https://git-scm.com/).

2. **Set Up SSH for GitHub**:
   - Add GitHub’s SSH address to your system PATH.
   - Generate an SSH key:
     ```
     ssh-keygen -t rsa -b 4096 -C "your_email@example.com"
     ```
   - Add the generated SSH key to GitHub:
     - Go to **GitHub > Settings > SSH and GPG Keys > New SSH Key**.
     - Paste the public key (`id_rsa.pub`).

3. **Configure Git User Info**:
   - Set your username and email:
     ```
     git config --global user.name "Your Name"
     git config --global user.email "your_email@example.com"
     ```

4. **Clone the Repository**:
   - Clone the repo using the SSH address:
     ```
     git clone git@github.com:Abumere17/AdaptiveDrone.git
     ```

---

## **Regular Workflow**

To maintain an organized and efficient workflow, follow these best practices:

### **1. Branch Management**
- **Purpose of Branches**:
  - Branches are used for specific tasks (e.g., new features or bug fixes).
- **Creating a Branch**:
  - To create a new branch and switch to it:
    ```
    git checkout -b feature-branch-name
    ```
- **Switching Branches**:
  - Use `git checkout` to switch to an existing branch:
    ```
    git checkout branch-name
    ```

### **2. Syncing with Remote**
- **Pull Changes**:
  - Always pull the latest changes before starting a new coding session:
    ```
    git pull origin main
    ```

### **3. Making Changes**
- Use the **Source Control Tab** in VS Code to:
  1. **Stage Changes**: Select the files you want to include in the commit.
  2. **Commit Changes**: Add a clear and descriptive commit message.
  3. **Push Changes**: Push your branch to the remote repository.

### **4. Merging Changes**
- Once your feature is complete, merge it into the `main` branch:
  1. Switch to the `main` branch:
     ```
     git checkout main
     ```
  2. Pull the latest changes:
     ```
     git pull origin main
     ```
  3. Merge your feature branch:
     ```
     git merge feature-branch-name
     ```

---

## **Key Git Commands**
Here’s a quick reference for common Git commands:
| **Command**                    | **Description**                             |
|--------------------------------|---------------------------------------------|
| `git clone <repo-url>`         | Clone a repository.                        |
| `git checkout -b <branch>`     | Create and switch to a new branch.         |
| `git checkout <branch>`        | Switch to an existing branch.              |
| `git pull origin <branch>`     | Pull changes from the remote branch.       |
| `git add <file>`               | Stage changes.                             |
| `git commit -m "message"`      | Commit staged changes with a message.      |
| `git push origin <branch>`     | Push your branch to the remote repository. |
| `git merge <branch>`           | Merge a branch into the current branch.    |

---

## **Best Practices**
1. **Commit Messages**:
   - Use clear and descriptive messages for your commits.
   - Example: `Added facial detection module to the drone controller.`

2. **Keep `main` Stable**:
   - Avoid pushing incomplete or unstable code directly to `main`.

3. **Communicate**:
   - Coordinate with teammates to avoid conflicts, especially during merges.
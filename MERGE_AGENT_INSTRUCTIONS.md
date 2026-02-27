# AI Agent Instructions: Feature Merge & Git Bundle Workflow

This document provides precise instructions for an AI agent to handle the feature development and offline merge process using Git bundles.

## 🛠️ Context
- **Project Type**: Flet (Python) for mobile/desktop.
- **Workflow**: Offline (USB-based) using Git bundles.
- **Goal**: Implement a specific feature from `FUTURE_FEATURES.md` and prepare it for merging.

---

## 🚀 Step 1: Feature Implementation
**Agent Role**: Developer
1.  **Identify Feature**: Read `FUTURE_FEATURES.md`.
2.  **Verify Exclusions**:
   - Ensure `venv/`, `__pycache__/`, `.apk/`, and `build/` are **NOT** tracked by Git.
   - Run `git status` to check for large untracked folders that should be ignored.
3.  **Create Branch**:
    ```bash
    git checkout -b feat-[feature-name]
    ```
4.  **Implement**: Apply changes to `main.py`, `database.py`, or `views/` as specified.
5.  **Verify**: Run `python main.py`.

---

## 📦 Step 2: Preparing the Shareable Bundle
**Agent Role**: Exporter
1.  **Commit Changes**:
    ```bash
    git add .
    git commit -m "Implementation of [Feature Name]"
    ```
2.  **Create Bundle**:
    - **Crucial**: Use the branch name for the bundle content.
    ```bash
    git bundle create "[feature_name].bundle" master..feat-[feature-name]
    ```
3.  **Instruction**: Inform the user to copy `[feature_name].bundle` to the common USB stick.

---

## 🔗 Step 3: Merging External Features (Integrator Role Only)
**Agent Role**: Integrator
*Use this only on the "Main Integrator" machine.*

1.  **Add Bundle as Remote**:
    ```bash
    git remote add [alias] /path/to/usb/[feature_name].bundle
    ```
2.  **Fetch & Merge**:
    ```bash
    git fetch [alias]
    git merge [alias]/feat-[feature-name]
    ```
3.  **Conflict Resolution**: If conflicts occur, prioritize structural changes (Schema) before UI changes.
4.  **Final Verification**: Run the app and check all features in `FUTURE_FEATURES.md`.

---

## 📝 Best Practices for Agents
- **No Internet**: Never attempt to use `git push` or `git pull` to/from a remote URL.
- **Semantic Commits**: Use clear, descriptive commit messages.
- **Modularity**: Follow the "Modularité avant tout" rule in `FUTURE_FEATURES.md`.

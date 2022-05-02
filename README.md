# KDiscord

Litigation system for Yeecord Community

This project **is current WIP**, it is **NOT WORKING** yet so don't try to host it.**

## Quickstart

Before you start, you will need these things:

* **Python** 3.10+
* **pip** 21.3.1+
* **MongoDB**
* **Basic English reading skills.**

  ### 1. Install the requirements
  Go to the project directory and run the following command:
    ```shell
    pip install -r requirements.txt
    ```

  ### 2. Edit the configuration and .env
  Rename the `.env.example` to `.env` and fill in the following information:
    ```
    TOKEN=Discord Bot Token
    MONGO_DB_URL=Your MongoDB URL
    CASES_CHANNEL=Channel to send new case notifications
    ADMIN_ROLES=A list of roles ids that allowed to accept cases
    OWNER=Bot owner ID
    ```

  ### 3. Run the bot
  Make sure your python is in your PATH
    ```shell 
    python main.py
    ```

## Todo

* Court system
* Ban Appeal 
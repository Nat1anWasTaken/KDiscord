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
  Rename the `config.json.example` to `config.json` and fill in the following information:
    ```json
    {
      "channels": {
        "cases": "Channel ID to send cases notification to (int)"
      },
      "admin_roles": [
        "Role ID to be able to accept cases (int)"
      ],
      "owner": "Bot owner's Discord ID (int)"
    }
    ```
  Rename the `.env.example` to `.env` and fill in the following information:
    ```
    TOKEN=Discord Bot Token
    MONGO_DB_URL=Your MongoDB URL
    ```

  ### 3. Run the bot
  Make sure your python is in your PATH
    ```shell 
    python main.py
    ```

## Todo

* Court system
* Ban Appeal 
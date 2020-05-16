from General import Functions

google_sheets_json = Functions.get_curr_parent_dir("\\API Keys\\Google API - StevensLTBots.json")

groupme_access_token = open(Functions.get_curr_parent_dir("\\API Keys\\Groupme Access Token.txt")).read()
groupme_character_limit = 450
groupme_tab = "    "

stevens_update_duration = 60 * 60 * 24

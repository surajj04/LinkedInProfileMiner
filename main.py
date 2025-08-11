import config
from login import linkedin_login
from scrape_profile import scrape_profile_skills
from process_bs import parse_profile

driver = linkedin_login()
scrape_profile_skills(driver, config.PROFILE_URL)

profile_data = parse_profile()

print(profile_data)

import config
from login import linkedin_login
from scrape_profile import scrape_profile_skills
from process_bs import parse_profile

driver = linkedin_login()
scrape_profile_skills(driver, config.PROFILE_URL)

profile_data = parse_profile()

# Save as CSV in processed folder
csv_path = config.PROCESSED_DATA_PATH + "profile_experience.csv"
profile_data.to_csv(csv_path, index=False, encoding="utf-8")

print('Name: ', profile_data['Name'])
print('Headline: ', profile_data['Headline'])
print('Location: ', profile_data['Location'])
print('About: ', profile_data['About'])
print('Education: ')
for edu in profile_data['Education']:
    print(edu)
print('\n')
print('Experience: ')
for exp in profile_data['Experience']:
    print(exp)
print('\n')
print('Skills: ', profile_data['Skills'])

import config
from bs4 import BeautifulSoup
import re
import pandas as pd

KEYWORDS = [
    "college",
    "school",
    "institute",
    "university",
    "academy",
    "polytechnic",
    "training center",
    "campus",
]


def clean_text(value):
    if not value:
        return None
    # Replace multiple spaces/newlines/tabs with a single space
    value = re.sub(r"\s+", " ", value)
    return value.strip()


def parse_profile():
    with open(config.RAW_DATA_PATH + "profile.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    name = soup.find("h1").get_text(strip=True) if soup.find("h1") else None
    headline = soup.find("div", class_="text-body-medium").get_text(strip=True)
    location = soup.find(
        "span", class_="text-body-small inline t-black--light break-words"
    ).get_text(strip=True)
    about = soup.find(
        "div",
        class_="zxCxqSvRjxaSbaugnxLfvNUTBJWicPjquw full-width t-14 t-normal t-black display-flex align-items-center",
    ).get_text(strip=True)

    experience_items = soup.select("section:has(h2:contains('Experience')) ul > li")

    job_data = []
    skills = []
    education_data = []

    # ------------------- experience -------------------------------
    for item in experience_items:
        title = item.select_one(".t-bold span[aria-hidden='true']")
        company = item.select_one(".t-14.t-normal span[aria-hidden='true']")
        date_range = item.select_one(
            ".pvs-entity__caption-wrapper span[aria-hidden='true']"
        )
        ex_location = item.select_one(".t-black--light span[aria-hidden='true']")
        description = item.select_one(".pvs-list__outer-container p")
        if title is not None and company is not None:
            job_data.append(
                {
                    "Job Title": (
                        clean_text(title.get_text(strip=True)) if title else None
                    ),
                    "Company": (
                        clean_text(company.get_text(strip=True)) if company else None
                    ),
                    "Date Range": (
                        clean_text(date_range.get_text(strip=True))
                        if date_range
                        else None
                    ),
                    "Location": (
                        clean_text(ex_location.get_text(strip=True))
                        if ex_location
                        else None
                    ),
                    "Description": (
                        clean_text(description.get_text(strip=True))
                        if description
                        else None
                    ),
                }
            )

    # ------------------- education -------------------------------

    for li in soup.select("ul.CcPTLnqQqRzyebUepUmLiAtEiwlybuYmQSI > li"):
        school_name = li.select_one(".t-bold span[aria-hidden='true']")
        degree = li.select_one(".t-14.t-normal span[aria-hidden='true']")
        years = li.select_one(".t-14.t-normal.t-black--light span[aria-hidden='true']")
        activities = li.select_one(
            ".inline-show-more-text--is-collapsed span[aria-hidden='true']"
        )

        if school_name:
            sname = school_name.get_text(strip=True).lower()
            if any(keyword in sname for keyword in KEYWORDS):
                education_data.append(
                    {
                        "School": clean_text(
                            school_name.get_text() if school_name else None
                        ),
                        "Degree": clean_text(degree.get_text() if degree else None),
                        "Years": clean_text(years.get_text() if years else None),
                        "Activities": clean_text(
                            activities.get_text().replace(
                                "Activities and societies:", ""
                            )
                            if activities
                            else None
                        ),
                    }
                )

    # Clean out None-only entries
    education_data = [
        entry for entry in education_data if any(v for v in entry.values())
    ]

    # ------------------- skills -------------------------------

    with open(config.RAW_DATA_PATH + "skills.html", "r", encoding="utf-8") as f:
        soup = BeautifulSoup(f, "html.parser")

    for li in soup.select("ul.CcPTLnqQqRzyebUepUmLiAtEiwlybuYmQSI > li"):
        skill_tag = li.select_one(".t-bold span[aria-hidden='true']")
        if skill_tag:  # Check if the element exists
            skill = skill_tag.get_text(strip=True)
            skills.append(skill)

    profile_data = {
        "Name": name,
        "Headline": headline,
        "Location": location,
        "About": clean_text(about),
        "Education": education_data,
        "Experience": job_data,
        "Skills": list(set(skills)),
    }

    df = pd.DataFrame([profile_data])

    return df

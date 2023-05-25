import re
import requests
from bs4 import BeautifulSoup
from models.app_details import AppDetails


class AptoideService:
    """
    Service for the business logic related to getting the contents from a specific app and
    parsing its contents to extract app details.
    """

    def get_app_details(self, url: str) -> AppDetails:
        """
        Submits a request to a url and parses the contents to extract the app details.
        The url must be a valid apptoide link.

        Args:
            url (str): a link to an app in the Aptoide store

        Returns:
            AppDetails
        """
        page_body = self._get_page_contents(url)
        return self._parse_soup(page_body)

    def _get_page_contents(self, url: str) -> str:
        """
        Uses the requests library to get the contents from the url parameter
        Returns the page body
        """
        r = requests.get(url)
        return r.text

    def _parse_soup(self, body: str) -> AppDetails:
        """
        Parses the contents of a page to search for details about an application.
        The parsing uses the Beautiful Soup library to parse the page elements and transform
        them into collections that can be searched and iterated over.

        Beautiful Soup documentation:
        https://www.crummy.com/software/BeautifulSoup/bs4/doc/

        Args:
            body (str): the whole body for a page

        Returns:
            str: _description_
        """

        soup = BeautifulSoup(body, "html.parser")
        """
        The div with the class "app-view__AppDetailsContainer-sc-oiuh9w-3 fKqGIB" corresponts
        to the section on the page containing:
        - The app name
        - Category
        - Downloads
        - Size
        - Ratings
        - Version
        - The download button 
        - Release date

        We are extracting its contents into the app_details variable so we only parse that
        section for app name, version, number of downloads and release date, as opposed to
        parsing the whole body.

        During development we can see that some of these CSS classes vary, but some portions
        of it remain like the app-view__AppDetailsContainer prefix remain the same (for now).
        We use regex to search for divs containing some portions less likely to change.

        At this moment (2023-05-19) the current tag for that section is:
        <div class="app-view__AppDetailsContainer-sc-oiuh9w-3 fKqGIB">...</div>
        """

        # app_details container
        app_details = soup.find_all(
            "div", class_=re.compile("app\\-view__AppDetailsContainer.*"), limit=1
        )[0]

        title = app_details.find_all(
            "h1", class_=re.compile("app\\-informations__Title.*")
        )[0]
        # app name
        name = title.get_text()

        # upper details container
        upper_details_items = app_details.find_all(
            "div", class_=re.compile("app\\-informations__DetailsItem.*")
        )

        downloads: str = (
            ""  # failsafe in case we can't find the number of downloads element
        )
        for details_item in upper_details_items:
            details_text = details_item.get_text()
            if "Downloads" in details_text:
                downloads = details_text.replace("Downloads", "").strip()

        # the lower_details_items contains the version and release date
        lower_details_items = app_details.find_all(
            "div", class_=re.compile(".+LatestVersionContainer.*"), limit=1
        )[0]
        # version and date is in the format "2.104(28-04-2023)""
        version_and_date = lower_details_items.get_text()
        version = version_and_date.split("(")[0]
        release_date = version_and_date.split("(")[1][0:10]

        """
        The app description is in a div right below the app_details described above.
        We could maybe have saved the position of app_details to search the next element,
        but as the page may change, is probably better to search the body for the app
        description div. Also it keeps the code simpler, and easier to maintain later.
        """
        description_paragraphs = soup.find_all(
            "div", class_=re.compile("details__DescriptionParagraphs.+"), limit=1
        )[0].children

        description_paragraph_texts = [
            paragraph.get_text().strip() for paragraph in description_paragraphs
        ]
        description = "\n".join(description_paragraph_texts)

        return AppDetails(name, version, downloads, release_date, description)

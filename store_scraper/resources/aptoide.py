import falcon
import json
import re

from models.app_details import AppDetails
from services.aptoide_service import AptoideService
from structlog import get_logger

logger = get_logger()


class AptoideResource:
    def __init__(self):
        logger.info("AptoideResource __init__")
        self.service = AptoideService()

    def on_get(self, req: falcon.Request, resp: falcon.Response) -> None:
        search = req.params["search"]
        logger.info("/aptoide", search=search)

        # verify if search contains a valid aptoide url, in the format
        # https://{app_name}.en.aptoide.com/app
        pattern = "^https:\\/\\/[0-9A-z\\-]+\\.en\\.aptoide\\.com/app"
        result = re.match(pattern, search)
        if not result:
            err_msg = (
                "Invalid URL. The app url defined in the search parameter must be "
                "in the format https://{app-name}.en.aptoide.com/app"
            )
            logger.error("invalid-search-parameter", search=search)
            resp.text = err_msg
            resp.content_type = falcon.MEDIA_TEXT
            resp.status = falcon.HTTP_400
            return

        logger.info("app-search", search=search)
        app_details: AppDetails = self.service.get_app_details(search)

        response = {
            "name": app_details.name,
            "version": app_details.version,
            "downloads": app_details.downloads,
            "release_date": app_details.release_date,
            "description": app_details.description,
        }

        resp.text = json.dumps(response)
        resp.content_type = falcon.MEDIA_JSON
        resp.status = falcon.HTTP_200

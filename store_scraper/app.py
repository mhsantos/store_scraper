import falcon

from structlog import get_logger

from resources.aptoide import AptoideResource

logger = get_logger()


def create_app():
    aptoide_resource = AptoideResource()
    logger.info("Creating Falcon app")
    app = falcon.App()
    logger.info("Falcon app created")
    app.add_route("/aptoide", aptoide_resource)
    return app


def get_app():
    return create_app()

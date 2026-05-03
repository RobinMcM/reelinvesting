from sqlalchemy.orm import Session

from app.models.article_asset_impact import ArticleAssetImpact


class ArticleImpactRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def insert_many(self, impacts: list[ArticleAssetImpact]) -> None:
        for impact in impacts:
            self.session.add(impact)
        self.session.flush()

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.news_article import ArticleStatus, NewsArticleIndex


class NewsArticleRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def exists_by_stable_id(self, stable_id: str) -> bool:
        return self.session.execute(
            select(NewsArticleIndex.id).where(NewsArticleIndex.stable_id == stable_id)
        ).first() is not None

    def insert(self, article: NewsArticleIndex) -> NewsArticleIndex:
        self.session.add(article)
        self.session.flush()
        return article

    def update_classification(self, article: NewsArticleIndex, **fields: object) -> None:
        for key, value in fields.items():
            setattr(article, key, value)
        self.session.flush()

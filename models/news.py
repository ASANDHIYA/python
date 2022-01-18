from base import BaseModel, db


class News(BaseModel, db.Model):
    __tablename__ = 'news'
    news_id = db.Column(db.Integer, primary_key=True)
    headline = db.Column(db.String, nullable=False)
    Details = db.Column(db.String)
    edited_by = db.Column(db.String)
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)

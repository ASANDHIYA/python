# from flask_sqlalchemy import SQLAlchemy
# import datetime
#
# db = SQLAlchemy()
#
#
# class BaseModel(db.Model):
#     """Base data model for all objects"""
#     __abstract__ = True
#
#     def before_save(self, *args, **kwargs):
#         pass
#
#     def after_save(self, *args, **kwargs):
#         pass
#
#     def save(self, commit=True):
#         self.before_save()
#         db.session.add(self)
#         if commit:
#             try:
#                 db.session.commit()
#             except Exception as e:
#                 db.session.rollback()
#                 raise e
#
#         self.after_save()
#
#     def before_update(self, *args, **kwargs):
#         pass
#
#     def after_update(self, *args, **kwargs):
#         pass
#
#     def update(self, *args, **kwargs):
#         self.before_update(*args, **kwargs)
#         db.session.commit()
#         self.after_update(*args, **kwargs)
#
#     def delete(self, commit=True):
#         db.session.delete(self)
#         if commit:
#             db.session.commit()
#
#     # def __init__(self, *args: object) -> object:
#     #     super().__init__(*args)
#
#     # def __repr__(self):
#     #     """Define a base way to print models"""
#     #     return '%s(%s)' % (self.__class__.__name__, {
#     #         column: value
#     #         for column, value in self._to_dict().items()
#     #     })
#
#     # def json(self):
#     #     """
#     #             Define a base way to jsonify models, dealing with datetime objects
#     #     """
#     #     return {
#     #         column: value if not isinstance(value, datetime.date) else value.strftime('%Y-%m-%d')
#     #         for column, value in self._to_dict().items()
#     #     }
#
#
# class Station(BaseModel, db.Model):
#     """Model for the stations table"""
#     __tablename__ = 'stations'
#
#     id = db.Column(db.Integer, primary_key=True)
#     lat = db.Column(db.Float)
#     lng = db.Column(db.Float)
#
#
# class Category(BaseModel, db.Model):
#     __tablename__ = 'category'
#     id = db.Column(db.Integer, primary_key=True)
#     name = db.Column(db.String, nullable=False)
#
#
# class News(BaseModel, db.Model):
#     __tablename__ = 'news'
#     news_id = db.Column(db.Integer, primary_key=True)
#     headline = db.Column(db.String, nullable=False)
#     Details = db.Column(db.String)
#     edited_by = db.Column(db.String)
#     category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=False)
#

from db import db


class StoreModel(db.Model):
    __tablename__ = 'stores'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80))
    items = db.relationship('ItemModel', lazy='dynamic', backref="stores")
    #items = db.relationship('ItemModel', back_populates="store", lazy='dynamic')

    #(*) if we dont apply the lazy='dynamic' it will return list of items but poor performance
    # when we create a store, it will load all the item

    def __init__(self, name):
        self.name = name

    def json(self):
        # use it when we dont use lazy='dynamic'
        #return {'name': self.name, 'items': self.items}

        return {'name': self.name, 'items': [item.json() for item in self.items.all()]}
        #because we apply lazy=dynamic -> self.items -> it's a query builder -> we need to load will all() method
        #poor perfomance when parse to json
        # => trade-off (*) when creation store or parse to json.

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    @classmethod
    def find_by_name(cls, name):
        item = cls.query.filter_by(name=name).first()
        return item

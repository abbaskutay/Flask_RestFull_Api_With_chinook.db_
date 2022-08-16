import datetime
from flask_restful import Api, Resource, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, abort
from flask_marshmallow import Marshmallow
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from datetime import *

app = Flask(__name__)
api = Api(app)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + 'chinook.db'
db = SQLAlchemy(app)

ma = Marshmallow(app)
app.config['JSON_SORT_KEYS'] = False


class Invoices(db.Model):
    InvoiceId = db.Column(db.Integer, primary_key=True)
    CustomerId = db.Column(db.Integer)
    InvoiceDate = db.Column(db.DateTime)
    BillingAddress = db.Column(db.NVARCHAR)
    BillingCity = db.Column(db.NVARCHAR)
    BillingState = db.Column(db.NVARCHAR)
    BillingCountry = db.Column(db.NVARCHAR)
    BillingPostalCode = db.Column(db.NVARCHAR)
    Total = db.Column(db.FLOAT)

    def __init__(self, InvoiceId, CustomerId, InvoiceDate, BillingAddress, BillingCity, BillingState, BillingCountry, BillingPostalCode, Total):
        self.InvoiceId = InvoiceId
        self.CustomerId = CustomerId
        self.InvoiceDate = InvoiceDate
        self.BillingAddress = BillingAddress
        self.BillingCity = BillingCity
        self.BillingState = BillingState
        self.BillingCountry = BillingCountry
        self.BillingPostalCode = BillingPostalCode
        self.Total = Total

    def __repr__(self):
        return f"{{'InvoiceId': {self.InvoiceId}, 'CustomerId': {self.CustomerId}, 'InvoiceDate': {self.InvoiceDate}, 'BillingAddress': {self.BillingAddress}, 'BillingCity': {self.BillingCity}, 'BillingState': {self.BillingState}, 'BillingCountry': {self.BillingCountry}, 'BillingPostalCode': {self.BillingPostalCode}, 'Total': {self.Total}}}"


class ProductSchema(SQLAlchemyAutoSchema):
    InvoiceId = fields.Integer,
    CustomerId = fields.Integer,
    InvoiceDate = fields.DateTime,
    BillingAddress = fields.String,
    BillingCity = fields.String,
    BillingState = fields.String,
    BillingCountry = fields.String,
    BillingPostalCode = fields.String,
    Total = fields.Float

    class Meta:
        model = Invoices
        include_relationships = True
        ordered = True


products_schema = ProductSchema(many=True)

resource_fields = {
    'InvoiceId': fields.Integer,
    'CustomerId': fields.Integer,
    'InvoiceDate': fields.DateTime(dt_format='rfc822'),
    'BillingAddress': fields.String,
    'BillingCity': fields.String,
    'BillingState': fields.String,
    'BillingCountry': fields.String,
    'BillingPostalCode': fields.String,
    'Total': fields.Float,

}

invoice_post_args = reqparse.RequestParser()
invoice_post_args.add_argument("InvoiceId", type=int, help="InvoiceId is required", required=True)
invoice_post_args.add_argument("CustomerId", type=int, help="CustomerId required", required=True)
invoice_post_args.add_argument("InvoiceDate", type=datetime.date, help="InvoiceDate is required")
invoice_post_args.add_argument("BillingAddress", type=str)
invoice_post_args.add_argument("BillingCity", type=str)
invoice_post_args.add_argument("BillingState", type=str)
invoice_post_args.add_argument("BillingCountry", type=str)
invoice_post_args.add_argument("BillingPostalCode", type=str)
invoice_post_args.add_argument("Total", type=float, help="Total is required", required=True)

invoice_update_args = reqparse.RequestParser()
invoice_update_args.add_argument("InvoiceId", type=int, help="InvoiceId is required")
invoice_update_args.add_argument("CustomerId", type=int, help="CustomerId required", required=True)
invoice_update_args.add_argument("InvoiceDate", type=datetime.date, help="InvoiceDate is required")
invoice_update_args.add_argument("BillingAddress", type=str)
invoice_update_args.add_argument("BillingCity", type=str)
invoice_update_args.add_argument("BillingState", type=str)
invoice_update_args.add_argument("BillingCountry", type=str)
invoice_update_args.add_argument("BillingPostalCode", type=str)
invoice_update_args.add_argument("Total", type=float, help="Total is required", required=True)


class InvoicesAll(Resource):
    @marshal_with(resource_fields)
    def get(self) -> list:
        all_invoices = Invoices.query.order_by(Invoices.InvoiceId).all()
        result = products_schema.dump(all_invoices)
        for i in result:
            year = int(i['InvoiceDate'][:4])
            month = int(i['InvoiceDate'][5:7])
            today = int(i['InvoiceDate'][8:10])
            invoice_date = datetime(year, month, today)
            i['InvoiceDate'] = invoice_date

            billing_address = i['BillingAddress'].rstrip("\\u00")
            i['BillingAddress'] = billing_address

        return result


class InvoiceSingle(Resource):
    @marshal_with(resource_fields)
    def get(self, invoice_id: int) -> list:
        single_invoice = Invoices.query.get(invoice_id)
        return single_invoice


class InvoicePost(Resource):
    @marshal_with(resource_fields)
    def post(self):
        args = invoice_post_args.parse_args()
        invoice = Invoices(InvoiceId=args['InvoiceId'], CustomerId=args['CustomerId'], InvoiceDate=datetime.today(),
                           BillingAddress=args['BillingAddress'], BillingCity=args['BillingCity'],
                           BillingState=args['BillingState'], BillingCountry=args['BillingCountry'],
                           BillingPostalCode=args['BillingPostalCode'],
                           Total=args['Total'])
        db.session.add(invoice)
        db.session.commit()
        return invoice, 201


class UpdateInvoice(Resource):
    @marshal_with(resource_fields)
    def put(self, invoice_id: int):
        args = invoice_update_args.parse_args()
        result = Invoices.query.filter_by(InvoiceId=invoice_id).first()
        today = datetime.today()
        if not result:
            abort(404, message="Invoice doesn't exist, cannot update")
        invoice = Invoices(InvoiceId=invoice_id, CustomerId=args['CustomerId'], InvoiceDate=today,
                           BillingAddress=args['BillingAddress'], BillingCity=args['BillingCity'],
                           BillingState=args['BillingState'], BillingCountry=args['BillingCountry'],
                           BillingPostalCode=args['BillingPostalCode'],
                           Total=args['Total'])
        db.session.commit()
        return invoice, 201


class DeleteInvoice(Resource):
    @marshal_with(resource_fields)
    def delete(self, invoice_id: int):
        invoice = Invoices.query.filter_by(InvoiceId=invoice_id).first()
        if not invoice:
            abort(404, message="Invoice doesn't exist, cannot be deleted")

        db.session.delete(invoice)
        db.session.commit()

        return invoice, 201


api.add_resource(InvoicesAll, "/api/invoices")
api.add_resource(InvoiceSingle, "/api/invoices/<int:invoice_id>")
api.add_resource(InvoicePost, "/api/invoices/add")
api.add_resource(UpdateInvoice, "/api/invoices/put/<int:invoice_id>")
api.add_resource(DeleteInvoice, "/api/invoices/delete/<int:invoice_id>")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')

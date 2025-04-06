from ..database import db
from datetime import datetime

class Adquisiciones(db.Model):
    __tablename__ = 'adquisiciones'
    id = db.Column(db.Integer, primary_key=True)
    presupuesto = db.Column(db.Float, nullable=False)
    unidad_administrativa = db.Column(db.String(100), nullable=False)
    tipo_bien = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    valor_total = db.Column(db.Float, nullable=False)
    fecha_adquisicion = db.Column(db.DateTime, default=datetime.utcnow)
    proveedor = db.Column(db.String(100), nullable=False)
    documentacion = db.Column(db.String(100), nullable=False)
    fecha_creacion = db.Column(db.DateTime, default=datetime.utcnow)
    fecha_modificacion = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    activo = db.Column(db.Boolean, default=True)

    def to_dict(self):
        return {
            'id': self.id,
            'presupuesto': self.presupuesto,
            'unidad_administrativa': self.unidad_administrativa,
            'tipo_bien': self.tipo_bien,
            'cantidad': self.cantidad,
            'valor_total': self.valor_total,
            'fecha_adquisicion': self.fecha_adquisicion.isoformat() if self.fecha_adquisicion else None,
            'proveedor': self.proveedor,
            'documentacion': self.documentacion,
            'activo': self.activo
        }
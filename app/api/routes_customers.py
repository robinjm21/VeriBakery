from fastapi import APIRouter, Depends, HTTPException, status, Response
from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from app.db.database import SessionLocal
from app.schemas.customer_schema import CustomerCreate, CustomerOut, CustomerUpdate
from app.db.models import Customer

router = APIRouter(prefix="/customers", tags=["customers"])

# Dependecia para sesion
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=CustomerOut, status_code=status.HTTP_201_CREATED)
def create_customer(customer: CustomerCreate, db: Session = Depends(get_db)):
    try:
        db_customer = Customer(**customer.model_dump())
        db.add(db_customer)
        db.commit()
        db.refresh(db_customer)
        return db_customer
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error interno de base de datos")

@router.get("/", response_model=list[CustomerOut])
def get_customers(
    db: Session = Depends(get_db),
    response: Response = None,
    limit: int = 10,
    offset: int = 0,
    search: str | None = None,
    email: str | None = None,
    district: str | None = None,
    sort_by: str = "id",
    order: str = "asc",
):
    try:
        query = db.query(Customer)
        # Filtros
        if email:
            query = query.filter(Customer.email == email)
        if district:
            query = query.filter(Customer.district == district)
        if search:
            s = f"%{search.lower()}%"
            query = query.filter(
                or_(
                    func.lower(Customer.name).like(s),
                    func.lower(Customer.email).like(s),
                    func.lower(Customer.phone).like(s),
                    func.lower(Customer.address).like(s),
                    func.lower(Customer.district).like(s),
                )
            )
        # Total antes de paginar
        total = query.count()
        # Ordenación segura
        allowed = {"id", "name", "email", "phone", "address", "district"}
        if sort_by not in allowed:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Campo de orden inválido")
        column = getattr(Customer, sort_by)
        if order not in {"asc", "desc"}:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Orden inválido (asc|desc)")
        order_expr = column.asc() if order == "asc" else column.desc()
        query = query.order_by(order_expr)
        # Paginación
        customers = query.offset(offset).limit(limit).all()
        # Header total
        if response is not None:
            response.headers["X-Total-Count"] = str(total)
        return customers
    except SQLAlchemyError:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al consultar clientes")

@router.get("/{customer_id}", response_model=CustomerOut)
def get_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    return customer

@router.put("/{customer_id}", response_model=CustomerOut)
def update_customer(customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    try:
        data = payload.model_dump()
        for field, value in data.items():
            setattr(customer, field, value)
        db.commit()
        db.refresh(customer)
        return customer
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar cliente")

@router.patch("/{customer_id}", response_model=CustomerOut)
def patch_customer(customer_id: int, payload: CustomerUpdate, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    try:
        data = payload.model_dump(exclude_unset=True)
        for field, value in data.items():
            setattr(customer, field, value)
        db.commit()
        db.refresh(customer)
        return customer
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="El email ya está registrado")
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al actualizar cliente parcialmente")

@router.delete("/{customer_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_customer(customer_id: int, db: Session = Depends(get_db)):
    customer = db.query(Customer).filter(Customer.id == customer_id).first()
    if not customer:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cliente no encontrado")
    try:
        db.delete(customer)
        db.commit()
    except SQLAlchemyError:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error al eliminar cliente")

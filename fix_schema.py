from db.database import engine

# Execute raw SQL to drop tables
with engine.connect() as conn:
    conn.execute('DROP TABLE IF EXISTS order_items CASCADE;')
    conn.execute('DROP TABLE IF EXISTS orders CASCADE;')
    conn.commit()
    print('✅ Dropped orders and order_items tables')

# Now recreate all tables
from db.database import Base
from models.user import User
from models.product import Product, ProductVariant, ProductFeature
from models.cart import Cart
from models.cart_items import CartItem
from models.order import Order, OrderItem
from models.review import Review
from models.admin import Admin

Base.metadata.create_all(engine)
print('✅ Recreated all tables with correct schema including total_amount column')

"""
Database optimization utilities - Indexes, query optimization
"""
from sqlalchemy import Index, text
from sqlalchemy.orm import Session
from .connection import Base, engine

# Database indexes for performance
INDEXES = [
    # User Service indexes
    Index('idx_users_email', 'users.email'),
    Index('idx_users_username', 'users.username'),
    Index('idx_users_created_at', 'users.created_at'),
    
    # Content Service indexes
    Index('idx_posts_user_id', 'posts.user_id'),
    Index('idx_posts_created_at', 'posts.created_at'),
    Index('idx_posts_is_published', 'posts.is_published'),
    Index('idx_comments_post_id', 'comments.post_id'),
    Index('idx_comments_user_id', 'comments.user_id'),
    Index('idx_likes_post_id', 'likes.post_id'),
    Index('idx_likes_user_id', 'likes.user_id'),
    
    # Product Service indexes
    Index('idx_products_seller_id', 'products.seller_id'),
    Index('idx_products_category', 'products.category'),
    Index('idx_products_price', 'products.price'),
    Index('idx_products_is_active', 'products.is_active'),
    Index('idx_products_created_at', 'products.created_at'),
    Index('idx_products_sku', 'products.sku'),
    Index('idx_reviews_product_id', 'reviews.product_id'),
    Index('idx_reviews_user_id', 'reviews.user_id'),
    
    # Order Service indexes
    Index('idx_carts_user_id', 'carts.user_id'),
    Index('idx_carts_product_id', 'carts.product_id'),
    Index('idx_orders_user_id', 'orders.user_id'),
    Index('idx_orders_status', 'orders.status'),
    Index('idx_orders_created_at', 'orders.created_at'),
    Index('idx_orders_order_number', 'orders.order_number'),
    Index('idx_order_items_order_id', 'order_items.order_id'),
    Index('idx_order_items_product_id', 'order_items.product_id'),
    
    # Composite indexes for common queries
    Index('idx_posts_user_published', 'posts.user_id', 'posts.is_published', 'posts.created_at'),
    Index('idx_products_category_active', 'products.category', 'products.is_active'),
    Index('idx_orders_user_status', 'orders.user_id', 'orders.status', 'orders.created_at'),
]

def create_indexes():
    """Create all performance indexes"""
    print("Creating database indexes...")
    for index in INDEXES:
        try:
            index.create(engine)
            print(f"✅ Created index: {index.name}")
        except Exception as e:
            print(f"⚠️  Index {index.name} may already exist: {e}")

def optimize_database():
    """Run database optimization commands"""
    with engine.connect() as conn:
        # Analyze tables for query optimization
        conn.execute(text("ANALYZE TABLE users, posts, products, orders, carts"))
        print("✅ Database tables analyzed")
        
        # Optimize tables
        conn.execute(text("OPTIMIZE TABLE users, posts, products, orders, carts"))
        print("✅ Database tables optimized")
        
        conn.commit()

def get_query_stats(session: Session, query):
    """Get query execution statistics"""
    # Enable query profiling
    session.execute(text("SET profiling = 1"))
    
    # Execute query
    result = query.all()
    
    # Get profiling info
    stats = session.execute(text("SHOW PROFILES")).fetchall()
    
    return {
        "result_count": len(result),
        "profiles": stats
    }

# Query optimization helpers
class QueryOptimizer:
    """Helper class for query optimization"""
    
    @staticmethod
    def paginate_query(query, page: int = 1, per_page: int = 20):
        """Add pagination to query"""
        offset = (page - 1) * per_page
        return query.offset(offset).limit(per_page)
    
    @staticmethod
    def eager_load_relationships(query, relationships: list):
        """Eager load relationships to avoid N+1 queries"""
        from sqlalchemy.orm import joinedload
        for rel in relationships:
            query = query.options(joinedload(rel))
        return query
    
    @staticmethod
    def use_index_hint(query, table, index_name):
        """Hint MySQL to use specific index"""
        # MySQL specific - use_index hint
        return query.execution_options(
            mysql_use_index=index_name
        )

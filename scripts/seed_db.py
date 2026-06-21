from pathlib import Path
import sys

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from app.core.database import SessionLocal
from app.models import Category, Product, Review


def seed_database() -> None:
    db = SessionLocal()

    try:
        existing_category = db.query(Category).first()
        if existing_category:
            print("Database already contains data. Skipping seed.")
            return

        fruits = Category(
            name="Fruits",
            description="Fresh organic fruits for everyday shopping.",
        )
        vegetables = Category(
            name="Vegetables",
            description="Organic vegetables for healthy meals.",
        )
        pantry = Category(
            name="Pantry",
            description="Pantry essentials and shelf-stable groceries.",
        )

        db.add_all([fruits, vegetables, pantry])
        db.flush()

        organic_apples = Product(
            name="Organic Apples",
            category_id=fruits.id,
            price=4.99,
            description="Crisp organic apples sold in a family pack.",
            is_organic=True,
            stock_quantity=50,
            is_active=True,
        )
        organic_bananas = Product(
            name="Organic Bananas",
            category_id=fruits.id,
            price=2.49,
            description="Naturally sweet organic bananas.",
            is_organic=True,
            stock_quantity=80,
            is_active=True,
        )
        fresh_spinach = Product(
            name="Fresh Spinach",
            category_id=vegetables.id,
            price=3.25,
            description="Leafy green spinach for salads and cooking.",
            is_organic=True,
            stock_quantity=35,
            is_active=True,
        )
        organic_carrots = Product(
            name="Organic Carrots",
            category_id=vegetables.id,
            price=2.99,
            description="Crunchy carrots for snacks and meals.",
            is_organic=True,
            stock_quantity=60,
            is_active=True,
        )
        raw_honey = Product(
            name="Raw Honey",
            category_id=pantry.id,
            price=8.5,
            description="Unprocessed raw honey in a glass jar.",
            is_organic=True,
            stock_quantity=20,
            is_active=True,
        )
        brown_rice = Product(
            name="Brown Rice",
            category_id=pantry.id,
            price=6.75,
            description="Whole grain brown rice for balanced meals.",
            is_organic=True,
            stock_quantity=40,
            is_active=True,
        )

        db.add_all(
            [
                organic_apples,
                organic_bananas,
                fresh_spinach,
                organic_carrots,
                raw_honey,
                brown_rice,
            ]
        )
        db.flush()

        reviews = [
            Review(
                product_id=organic_apples.id,
                rating=5,
                reviewer_name="Amina",
                review_text="Very fresh and crisp apples.",
            ),
            Review(
                product_id=organic_apples.id,
                rating=4,
                reviewer_name="Rahim",
                review_text="Good taste and quality.",
            ),
            Review(
                product_id=fresh_spinach.id,
                rating=5,
                reviewer_name="Nabila",
                review_text="Perfect for smoothies and salads.",
            ),
            Review(
                product_id=raw_honey.id,
                rating=4,
                reviewer_name="Imran",
                review_text="Rich flavor and nice texture.",
            ),
        ]

        db.add_all(reviews)
        db.commit()
        print("Database seeded successfully.")
    except Exception:
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    seed_database()

# Django Book Store Management System

A web-based Book Store Management System built using **Python, Django, MySQL, HTML, CSS, and Bootstrap**. The application allows users to browse books, search and filter the catalogue, manage a shopping cart, place orders, and track order status. Staff users can manage book categories and order statuses.

## Features

### Day 1 — Authentication and Book Management

- User registration with form validation.
- User login and logout.
- User profile management.
- Secure password hashing using Django authentication.
- Create, view, update, and delete books.
- Book details include title, author, ISBN, price, description, category, stock, and cover image.
- Image uploads using Django media files.
- Responsive frontend using Bootstrap.
- Django admin integration.

### Day 2 — Categories, Shopping Cart, and Orders

**Category Management**
- Create, view, update, and delete categories.
- Restrict category management to staff users.
- Prevent deletion of categories that contain books.

**Book Search and Filtering**
- Search books by title or author.
- Filter books by category.
- Filter books by minimum and maximum price.
- Sort by newest, oldest, price, or title.

**Shopping Cart**
- Add books to the cart.
- Update item quantities.
- Remove items from the cart.
- Calculate item subtotals and the overall total.
- Store cart data using Django sessions.
- Validate stock availability.

**Checkout and Order Management**
- Collect delivery address and phone number.
- Create orders and order items.
- Save book title and price snapshots in order items.
- Validate stock before placing an order.
- Update stock within a database transaction.
- Display order history and order details.
- Track order status: Pending, Processing, Shipped, Delivered, and Cancelled.
- Restrict customers to viewing their own orders.
- Allow staff users to update order status.

> **Note:** This project demonstrates order creation and stock management. It does not currently process real online payments.

## Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Django | Web framework |
| MySQL | Relational database |
| HTML5 | Page structure |
| CSS3 | Styling |
| Bootstrap 5 | Responsive frontend |
| Django ORM | Database operations |
| Django Authentication | Login, registration, and permissions |
| Django Sessions | Shopping cart storage |
| Pillow | Image upload support |

## Project Structure

```text
django_bookstore/
│
├── accounts/
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── books/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── ...
│
├── categories/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── cart/
│   ├── views.py
│   ├── urls.py
│   └── ...
│
├── orders/
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   ├── admin.py
│   └── ...
│
├── dashboard/
│   └── ...
│
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── ...
│
├── templates/
│   ├── accounts/
│   ├── books/
│   ├── categories/
│   ├── cart/
│   ├── orders/
│   └── base.html
│
├── static/
│   └── css/
│       └── style.css
│
├── media/
│   └── book_covers/
│
├── manage.py
├── README.md
└── requirements.txt
```

*Note: The exact files and folders may vary slightly depending on your local implementation.*

## Prerequisites

Install the following before running the project:

- Python 3.13 or another compatible Python version.
- MySQL Server 8.x.
- MySQL Workbench (optional, for database management).
- Visual Studio Code or another Python editor.
- Git (optional).

## Installation and Setup

### 1. Clone the repository

If the project is hosted on GitHub:

```bash
git clone YOUR_GITHUB_REPOSITORY_URL
cd django_bookstore
```

Alternatively, open your existing project directory directly.

### 2. Create a virtual environment

Windows PowerShell:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

### 3. Install dependencies

```powershell
python -m pip install --upgrade pip
pip install "Django>=5.2,<5.3" mysqlclient Pillow
```

### 4. Create the MySQL database

Open MySQL Workbench or the MySQL command line and execute:

```sql
CREATE DATABASE bookstore_db
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
```

### 5. Configure the database

Open `config/settings.py` and configure the database settings:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "bookstore_db",
        "USER": "root",
        "PASSWORD": "YOUR_MYSQL_PASSWORD",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

Replace `YOUR_MYSQL_PASSWORD` with your local MySQL password.

**Security recommendation:** Do not commit real database passwords or secret keys to GitHub. For a public repository, load them from environment variables or a `.env` file excluded by `.gitignore`.

### 6. Apply database migrations

```powershell
python manage.py makemigrations
python manage.py migrate
```

### 7. Create a superuser

```powershell
python manage.py createsuperuser
```

Follow the prompts to create the admin account.

### 8. Run the development server

```powershell
python manage.py runserver
```

Open the application in your browser:

- Home page: http://127.0.0.1:8000/
- Book catalogue: http://127.0.0.1:8000/books/
- Django admin: http://127.0.0.1:8000/admin/
- Category management: http://127.0.0.1:8000/categories/
- Shopping cart: http://127.0.0.1:8000/cart/
- Checkout: http://127.0.0.1:8000/orders/checkout/
- Order history: http://127.0.0.1:8000/orders/history/

Some pages require login, and category management requires a staff/admin account.

## Main Application Routes

| Feature | URL |
|---|---|
| Home / Book List | `/` |
| Book List | `/books/` |
| Add Book | `/books/add/` |
| Book Details | `/books/<id>/` |
| Edit Book | `/books/<id>/edit/` |
| Delete Book | `/books/<id>/delete/` |
| Register | `/accounts/register/` |
| Login | `/accounts/login/` |
| Profile | `/accounts/profile/` |
| Category Management | `/categories/` |
| Add Category | `/categories/add/` |
| Shopping Cart | `/cart/` |
| Add to Cart | `/cart/add/<book_id>/` |
| Checkout | `/orders/checkout/` |
| Order History | `/orders/history/` |
| Order Details | `/orders/<id>/` |
| Django Admin | `/admin/` |

## Database Models

### Category
Stores category names and descriptions.

### Book
Stores book information, category relationships, prices, ISBN, stock quantities, and cover images.

### Order
Stores the customer, unique order number, total amount, delivery details, order status, and timestamps.

### OrderItem
Stores each book included in an order, its quantity, unit price, and subtotal. Book title and price are saved as snapshots for historical accuracy.

The application also uses Django's built-in user model for authentication and customer accounts.

## Testing

Run Django's system checks:

```powershell
python manage.py check
```

Run the project's automated tests:

```powershell
python manage.py test
```

Manually verify the following workflows:

1. Register a user and log in.
2. Add, edit, and view books.
3. Upload and display a book cover.
4. Create and manage categories using a staff account.
5. Search, filter, and sort books.
6. Add books to the cart and update quantities.
7. Remove items from the cart.
8. Place an order using valid delivery details.
9. Confirm that book stock decreases after a successful checkout.
10. Verify order history, order details, and status updates.
11. Test insufficient-stock handling and customer order access restrictions.

## Security and Validation

- Django handles password hashing and authentication.
- CSRF tokens protect POST forms.
- Django ORM is used for database queries.
- Category management is restricted to staff users.
- Customers can access only their own orders.
- Checkout validates stock and uses database transactions.
- Form validation checks important user input.
- Uploaded images are stored using Django's media storage configuration.

For production deployment, configure HTTPS, secure cookies, environment-based secrets, appropriate upload validation, and a production web server. Review permissions on book management and other staff-only operations before public deployment.

## Future Enhancements

- Online payment gateway integration.
- Order cancellation and stock restoration.
- Email order confirmations.
- Product reviews and ratings.
- Pagination and advanced filtering.
- Wishlist functionality.
- Admin sales reports and analytics.
- Automated unit and integration tests.
- Production deployment.

## Project Status

- Day 1: Authentication and Book Management.
- Day 2: Categories, Search, Shopping Cart, Checkout, and Orders.

**Status:** Day 1 and Day 2 implementation completed.

## Author

**S. Gaviprawin**

B.Tech Information Technology Graduate

Project: Django Book Store Management System

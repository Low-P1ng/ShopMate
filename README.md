# ShopMate - Modern Full-Stack E-Commerce Application

ShopMate is a responsive full-stack e-commerce web application built using **Django, Python, Tailwind CSS, and SQLite**. It features a modern minimal UI, session-based shopping cart engine, asynchronous AJAX user interactions, user authentication, address management, and database-driven order processing.

---

## 🌟 Key Features

- **Product Catalog & Search**:
  - Grid view with stock status badges, prices in Indian Rupees (₹), product ratings, and details.
  - Asynchronous live search filtering by product name.
  
- **AJAX Shopping Cart Engine**:
  - Session-based shopping cart supporting both guest users and authenticated members.
  - Asynchronous (no page reload) Add-to-Cart, Quantity Update, and Delete actions with toast notifications.
  
- **Authentication & User Management**:
  - Account Registration, Login, Logout with flash message toasts.
  - User profile updating & primary shipping address manager.
  - Built-in admin interface (`/admin/`) for store management.

- **Checkout & Order System**:
  - 2-Column Checkout supporting pre-filled saved address or guest checkout.
  - Relational database schema linking `Order` and `OrderItem` models.
  - Automatic cart clearing upon successful order placement.

---

## 🛠️ Tech Stack

- **Backend**: Python 3, Django 5
- **Frontend**: HTML5, Tailwind CSS, JavaScript (jQuery AJAX)
- **Database**: SQLite3
- **Authentication**: Django Auth & Sessions

---

## 🚀 Quick Start & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/Low-P1ng/ShopMate.git
cd ShopMate
```

### 2. Create and Activate Virtual Environment
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install django pillow
```

### 4. Run Migrations & Start Server
```bash
python manage.py migrate
python manage.py runserver
```

Open your browser and navigate to `http://127.0.0.1:8000/`.

---

## 📝 License
Distributed under the MIT License.

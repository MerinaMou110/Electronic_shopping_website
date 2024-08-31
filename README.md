                                                                   Electronic Shopping Website
Welcome to the Electronic Shopping Website, a robust e-commerce platform designed to provide a seamless shopping experience with secure authentication and role-based access. This project showcases advanced features such as JWT authentication, user roles, and comprehensive product management.

Features
1. Authentication System :lock:
JWT Authentication: Secure user authentication using JSON Web Tokens.
User Registration, Login & Logout: Users can easily register, log in, and log out of their accounts.
Password Management: Users can change their passwords and reset them if forgotten.
2. Role-Based Access :key:
Three Types of Users:
User: Regular users who can browse products, make purchases, and view their profile information.
Admin: Can manage products with full CRUD (Create, Read, Update, Delete) capabilities.
Superadmin: Has all the privileges of an admin and can also manage other users and administrative settings.
3. Product Management :shopping_cart:
Product Catalog: A wide range of products available for purchase.
Search & Filter: Users can search for products by name and apply filters to find what they need quickly.
User Purchases: Users can add products to their cart, make purchases, and view their order history.
4. Profile Management :bust_in_silhouette:
User Profile: Users can view and update their personal information, such as name, email, and address.
Installation
To set up the project locally, follow these steps:

Clone the repository:

git clone https://github.com/yourusername/electronic-shopping-website.git
cd electronic-shopping-website

Install the required dependencies:

pip install -r requirements.txt

Setup the database:

python manage.py migrate

Create a superuser for site management:

python manage.py createsuperuser

Run the development server:

python manage.py runserver
Access the website: Open your web browser and go to http://127.0.0.1:8000/.

Usage
User Registration & Login: Create a new account or log in to an existing one.
Explore Products: Browse through the catalog, use the search and filter options, and add items to your cart.
Admin & Superadmin Features: Log in as an admin or superadmin to manage products and users.
Manage Profile: Update your profile information and review your order history.

Technologies Used
Frontend: HTML, CSS, Bootstrap
Backend: Django (Python), Django Rest Framework
Authentication: JWT (JSON Web Tokens)
Database: PostgreSQL (or specify the database you used)
Deployment: Deployed on [Your Hosting Platform] (e.g.,render, Heroku, AWS, etc.)

Contributing
Contributions are welcome! Please fork the repository and submit a pull request with your changes.

Acknowledgements
Gratitude to my mentors and peers for their support and feedback.
Inspiration from leading e-commerce platforms to provide an intuitive and secure shopping experience.

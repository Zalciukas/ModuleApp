VAPA - Student Module Management System
=====================================

Demo Users:
-----------
Username: student1
Password: testpass123
Email: student1@example.com

Username: student2  
Password: testpass123
Email: student2@example.com

Username: admin
Password: admin123
Email: admin@example.com

Features:
--------
- User authentication (login/logout)
- User-specific module access (each user sees only their modules)
- Add/Edit/Delete module functionality
- PDF generation for all user modules

Usage:
------
1. Login with demo credentials
2. View your modules on the dashboard
3. Add new modules using the "Add Module" button
4. Edit existing modules by clicking "Edit"
5. Generate PDF report using "Export PDF" button
6. Logout when finished

Technical Notes:
---------------
- Uses SQLite database (db.sqlite3)
- ReportLab for PDF generation
- Bootstrap 5 for styling
- Django 5.0 with class-based views
- Secure user isolation (users can only access their own modules)
# N.S.O.G. Airsoft Club Platform

A professional Django web application for the N.S.O.G. (Danish Airsoft Club) management platform, featuring military-styled design, member authentication, rank hierarchy system, event management, and tactical operations coordination.

## Table of Contents

- [UX](#ux)
  - [Strategy](#strategy)
    - [Project Goal: Streamline Airsoft Club Operations](#project-goal-streamline-airsoft-club-operations)
    - [User Goals](#user-goals)
    - [User Values](#user-values)
    - [User Expectations](#user-expectations)
    - [User Stories](#user-stories)
    - [Strategy Table](#strategy-table)
    - [Trends of Modern Club Websites](#trends-of-modern-club-websites)
  - [Scope](#scope)
  - [Structure](#structure)
  - [Skeleton](#skeleton)
    - [Mobile Wireframe](#mobile-wireframe)
    - [Tablet Wireframe](#tablet-wireframe)
    - [Desktop Wireframe](#desktop-wireframe)
  - [Surface](#surface)
- [Features](#features)
  - [Existing Features](#existing-features)
    - [Military-Styled Landing Page](#military-styled-landing-page)
    - [Email-Based Authentication](#email-based-authentication)
    - [Custom User Management](#custom-user-management)
  - [Features Left to Implement](#features-left-to-implement)
- [Technologies Used](#technologies-used)
- [Testing](#testing)
- [Deployment](#deployment)
- [Credits](#credits)

## UX

### Strategy

#### Project Goal: Streamline Airsoft Club Operations

The primary goal of this project is to create a comprehensive web platform that streamlines all aspects of running a professional airsoft club in Denmark. The platform aims to provide both administrative efficiency and an engaging member experience while maintaining the tactical, military-inspired aesthetic that resonates with the airsoft community.

The platform aims to:

- **Professional Club Management**: Provide robust tools for administrators to manage members, events, and club operations efficiently
- **Member Engagement**: Create an immersive experience with military-styled design and interactive features that reflect the club's tactical identity
- **Rank Hierarchy System**: Implement a structured rank progression system that motivates members and recognizes their experience and commitment
- **Event Coordination**: Facilitate seamless planning, scheduling, and participation tracking for tactical operations and training sessions
- **Communication Hub**: Establish a centralized platform for club announcements, news, and member interaction
- **Privacy-First Approach**: Ensure members maintain control over their data with no public self-registration, emphasizing privacy and exclusivity

By combining tactical aesthetics with modern web technologies, the platform bridges the gap between traditional club management and the expectations of a digitally-native airsoft community, making operations more efficient while enhancing the overall member experience.

#### User Goals

**Visitor Goals:**

- Understand immediately that the site is about an airsoft/tactical club
- Read about the club's mission and values ("Crudeles in Proelio")
- View information about the club without requiring registration
- See visual evidence of club activities through imagery
- Find contact information to request membership
- Experience professional, military-themed design

**Member Goals:**

- Login securely using email and password
- Access personalized dashboard showing rank and profile
- View club news and upcoming events
- Update personal information and profile details
- Change password securely
- Track personal progression through rank system
- Communicate with other members
- Register for upcoming operations and events
- Access training schedules and resources

**Admin/Coach Goals:**

- Manage member accounts and approvals
- Assign and modify member ranks
- Create and manage events/operations
- Post club news and announcements
- Track member participation and activity
- Export member data for reporting
- Manage site content and pages
- Control privacy and access permissions
- View analytics on member engagement

#### User Values

- **Tactical Identity**: Military-themed design that resonates with airsoft culture and creates immersive experience
- **Privacy & Exclusivity**: Controlled membership with admin approval, no public registration
- **Security**: Email-based authentication with robust password management
- **Rank Recognition**: Clear hierarchy system that acknowledges experience and commitment
- **Community**: Centralized platform for communication and collaboration
- **Transparency**: Clear information about club operations, events, and activities
- **Mobile Accessibility**: Full functionality across all devices for on-the-go access
- **Danish Language**: Native language support for the primary user base

#### User Expectations

**Visitors expect:**

- Immediate understanding of the club's tactical nature through visual design
- Professional presentation with military-inspired aesthetics
- Clear information about club values and membership process
- Contact methods for membership inquiries
- Fast-loading pages with optimized images
- No forced registration to view basic club information

**Members expect:**

- Secure login with email and password
- Personalized dashboard showing rank and status
- Quick access to events and news
- Easy profile management
- Visual rank indicators and progression tracking
- Responsive design for mobile and tablet use
- Toast notifications with personality (Full Metal Jacket-style Danish messages)
- Reliable session management

**Admins expect:**

- Comprehensive member management dashboard
- Easy event creation and modification tools
- Bulk operations for member management
- Data export capabilities
- Content management for news and announcements
- Analytics on member activity
- Full control over rank assignments
- GDPR-compliant data handling

#### User Stories

**Visitor Stories**

Discover the club:

- As a visitor I want to immediately understand this is an airsoft club so that I know if it's relevant to me
- As a visitor I want to see the club's motto ("Crudeles in Proelio") so that I understand the club's identity
- As a visitor I want to view club information without logging in so that I can learn before committing
- As a visitor I want to see professional design that reflects military culture so that I feel aligned with the community
- As a visitor I want to find contact information so that I can request membership

**Member Stories**

Authentication:

- As a member I want to login with my email and password so that I can access the platform securely
- As a member I want to logout securely so that my session is properly terminated
- As a member I want to change my password so that I can maintain account security
- As a member I want to see my rank displayed in the navbar so that I feel recognized

Account Management:

- As a member I want to view my complete profile so that I can see my rank, nationality, and personal information
- As a member I want to update my personal details so that my profile stays current
- As a member I want to add optional information like nickname and residence so that I can personalize my profile
- As a member I want to see my join date so that I can track my membership tenure

Engagement:

- As a member I want to receive ironic Danish toast messages on login so that the experience feels personalized and fun
- As a member I want to view upcoming events so that I can plan my participation
- As a member I want to read club news so that I stay informed
- As a member I want to see other members' ranks so that I understand the hierarchy

**Admin Stories**

Member Management:

- As an admin I want to create member accounts manually so that I control who joins
- As an admin I want to assign ranks to members so that I can recognize experience
- As an admin I want to view all members in a list so that I can manage the club roster
- As an admin I want to filter members by rank so that I can organize operations
- As an admin I want to edit member information so that I can keep records accurate
- As an admin I want to deactivate members so that former members can't access the platform
- As an admin I want to add notes about members so that I can track important information

Content Management:

- As an admin I want to create news posts so that I can communicate with all members
- As an admin I want to schedule events so that members can register
- As an admin I want to manage event participation so that I can plan operations
- As an admin I want to upload images so that I can showcase club activities

Analytics:

- As an admin I want to see member statistics so that I can understand club growth
- As an admin I want to view event participation rates so that I can improve engagement
- As an admin I want to export member data so that I can create reports

#### Strategy Table

The strategy table illustrates the trade-off between importance and viability. As we move onto Scope soon, it is clear that this project requires different phases to implement the exhaustive list of features - it is an on-going process!

| Feature | Importance | Viability |
|---------|-----------|-----------|
| Email-based authentication system | 5 | 5 |
| Custom user model with rank system | 5 | 5 |
| Admin-only member creation | 5 | 5 |
| Military-styled responsive design | 5 | 4 |
| Member profile management | 5 | 5 |
| Password change functionality | 5 | 5 |
| Toast notifications with Danish messages | 4 | 5 |
| Landing page with club information | 5 | 5 |
| User navbar with dropdown menu | 5 | 5 |
| Admin panel integration | 5 | 5 |
| Rank display and hierarchy | 4 | 4 |
| Dark military color scheme | 4 | 5 |
| Parallax hero section | 3 | 4 |
| Event management system (comms) | 4 | 5 |
| News/blog functionality (comms) | 4 | 5 |
| Member directory with filters | 4 | 4 |
| Event registration system | 4 | 3 |
| Photo gallery | 3 | 4 |
| Training resources section | 3 | 3 |
| Email notifications | 3 | 3 |
| Member messaging system | 2 | 2 |
| Mobile native app | 2 | 1 |
| Export reports to PDF | 3 | 3 |
| Analytics dashboard | 3 | 3 |
| **Total** | **89** | **91** |

The table shows that while the project has high strategic value (importance = 89), most features are technically viable (viability = 91), though some advanced features like event management and messaging systems require more complex implementation and will be developed in later phases.

#### Trends of Modern Club Websites

Modern club and community websites are evolving to meet user expectations for engagement, mobile accessibility, and professional presentation. Key trends that influence this project include:

**Military/Tactical Aesthetics**

- Dark color schemes with military-inspired palettes
- Bold typography reminiscent of military communications
- Tactical iconography and visual elements
- Immersive hero sections with parallax effects
- Rough, authentic imagery over polished corporate photos

**Member-Centric Features**

- Personalized dashboards showing member status
- Rank and achievement display systems
- Profile customization options
- Member directories with filterable views
- Private member-only content areas

**Mobile-First Design**

- Responsive layouts that work seamlessly across all devices
- Touch-friendly navigation and interactions
- Fast loading times with optimized assets
- Progressive enhancement for advanced features
- Offline capabilities for essential features

**Privacy and Security**

- Email-based authentication without social login dependencies
- Manual member approval processes
- Role-based access control
- GDPR compliance with data management
- Secure session handling

**Event Management**

- Visual event calendars
- Easy registration and RSVP systems
- Participation tracking
- Event image galleries
- Post-event reporting

**Communication Features**

- Centralized news and announcements
- Email integration for notifications
- Comment systems on news posts
- Direct messaging between members
- Notification preferences

**Admin Efficiency**

- Comprehensive admin dashboards
- Bulk operations for member management
- Analytics and reporting tools
- Content management systems
- Data export capabilities

**User Experience**

- Toast notifications with personality
- Loading states and feedback
- Clear error messages
- Consistent navigation patterns
- Accessible design (WCAG compliance)

This project incorporates these trends by offering a military-themed immersive experience, secure email authentication, comprehensive member management, and robust tools for both members and administrators to facilitate a thriving airsoft community.

### Scope

Based on the strategy table analysis and the trade-off between importance and viability, the project will be developed in multiple phases. This phased approach ensures that we deliver a functional minimum viable product (MVP) quickly while maintaining the flexibility to expand features based on user feedback and technical feasibility.

The development is structured to prioritize high-importance, high-viability features first, establishing a solid foundation before adding more complex functionalities. Each phase builds upon the previous one, creating an iterative process that allows for continuous improvement and adaptation.

#### Phase 1: MVP - Core Platform (COMPLETED)

**Goal**: Launch a functional platform with authentication, user management, and military-styled design.

**Features:**

- Military-styled landing page with parallax hero section
- Email-based authentication system (login/logout)
- Custom User model with rank hierarchy system
- Admin-only member creation (no public signup)
- Password change functionality
- Member profile display with rank badges
- User navbar with dropdown menu
- Toast notifications with Full Metal Jacket-style Danish messages
- Responsive design (mobile, tablet, desktop)
- Admin panel integration
- Dark military color scheme

**Timeline**: 2-3 weeks

**Success Criteria**: Members can login, view their profile with rank, change password; admins can create and manage members; site displays professional military aesthetic.

#### Phase 2: Event Management & Content (COMPLETED)

**Goal**: Add event scheduling, news functionality, and member engagement features.

**Features delivered:**

- News post creation, editing, and deletion (staff only)
- Automatic news expiry after 4 months via management command
- Event creation and management with combined Post + Event form
- Member RSVP system (confirmed / standby / declined) via AJAX
- Admin attendees overview per event
- Image upload with automatic WebP compression and 5 MB size limit
- Full SEO meta tags + Open Graph for WhatsApp/Discord link previews
- Auto-generated slugs for clean URLs
- Public listing page at `/nyheder/` accessible to all visitors

**Remaining for this phase:**

- Comment system for news posts
- Member directory with rank filters
- Email notifications for new events
- Admin analytics dashboard

**Timeline**: 3-4 weeks

#### Phase 3: Enhanced Member Experience

**Goal**: Improve member engagement with advanced features and communication tools.

**Features:**

- Training resources library
- Photo gallery for operations
- Member achievement system
- Rank progression tracking
- Personal statistics dashboard
- Advanced profile customization
- Member-to-member messaging
- Notification preferences
- Export personal data (GDPR)
- Enhanced mobile experience

**Timeline**: 3-4 weeks

**Success Criteria**: Members have personalized experience with achievements, messaging, and comprehensive statistics; full GDPR compliance.

#### Phase 4: Advanced Features & Optimization

**Goal**: Implement advanced administrative tools and optimize performance.

**Features:**

- Advanced analytics and reporting
- PDF report generation
- Bulk member operations
- CSV data import/export
- Advanced search and filtering
- Performance optimizations
- Caching implementation
- SEO optimization
- Accessibility audit and improvements
- API for potential mobile app

**Timeline**: 4-5 weeks

**Success Criteria**: Platform offers complete club management ecosystem; excellent performance across all devices; high member satisfaction; ready for scaling.

#### Future Considerations

Beyond Phase 4, potential enhancements based on member feedback may include:

- Native mobile applications (iOS/Android)
- Integration with third-party booking systems
- Video library for training content
- Multi-language support (English, German)
- Public booking system for open events
- Merchandise shop integration
- Advanced tactical planning tools
- Geolocation features for event locations

This phased approach ensures that each development cycle delivers value while maintaining code quality, security, and user experience standards.

### Structure

The platform follows a hierarchical structure with clear parent-child relationships:

#### Information Architecture

```
Public Pages
├── Homepage (Landing)
│   ├── Hero Section (Parallax)
│   ├── About Club
│   ├── Mission Statement
│   └── Contact CTA
├── Login Page
└── Legal Pages
    ├── Privacy Policy
    ├── Terms of Service
    └── Cookie Policy

Member Dashboard (Authenticated)
├── Profile Overview
│   ├── Personal Information
│   ├── Rank Display
│   ├── Account Settings
│   └── Change Password
├── Events
│   ├── Upcoming Events
│   ├── Event Details
│   ├── Registration
│   └── My Events
├── News/Blog
│   ├── All Posts
│   ├── Post Details
│   └── Comments
├── Members Directory
│   ├── All Members
│   └── Filter by Rank
└── Logout

Admin Dashboard (Staff/Superuser)
├── Admin Panel
│   ├── User Management
│   │   ├── User List
│   │   ├── Add User
│   │   ├── Edit User
│   │   └── User Details
│   ├── Events Management
│   ├── News Management
│   └── Analytics
└── Site Settings
```

#### Navigation Patterns

**Top Navigation Bar:**

- Logo on the left (clickable home link)
- Main menu items in center (Events, News, Members for authenticated users)
- Login button or user dropdown on the right
- Hamburger menu on mobile devices
- Rank and name displayed for authenticated users

**User Dropdown Menu:**

- Profile link
- Change Password link
- Admin Panel link (staff only)
- Logout link with danger styling

**Footer:**

- Secondary navigation links
- Contact information
- Social media links (future)
- Legal links (Privacy, Terms)
- Copyright notice

#### Consistency Principles

- **Visual Consistency**: Military-themed design across all pages with consistent color palette
- **Component Consistency**: Reusable UI components (buttons, forms, cards) maintain same styling
- **Content Consistency**: Danish language throughout with English code/comments
- **Functional Consistency**: Similar actions work the same way across different sections

### Skeleton

Wireframes will be added in future iterations showing the layout across different device sizes.

#### Mobile Wireframe

To be implemented

#### Tablet Wireframe

To be implemented

#### Desktop Wireframe

To be implemented

### Surface

**Color Palette:**

The platform uses a military-inspired dark color scheme:

- **Primary Background**: `#1a1d17` - Deep forest green-black
- **Surface**: `#242820` - Dark military surface
- **Surface Soft**: `#2f3329` - Subtle elevated surface
- **Primary**: `#5a6b4e` - Military sage green
- **Primary Strong**: `#6d8159` - Brighter tactical green
- **Secondary**: `#d4c5a0` - Coyote tan (military beige)
- **Text**: `#f0ede5` - Off-white for readability
- **Muted**: `#b8b3a0` - Muted tan for secondary text
- **Border**: `rgba(212, 197, 160, 0.12)` - Subtle tan borders

**Typography:**

- **Headings**: "Barlow Semi Condensed" - Military-style condensed font
- **Body**: "Inter" - Clean, readable sans-serif
- **Eyebrow Badge**: Uppercase with letter-spacing for tactical feel

**Visual Elements:**

- Parallax hero section with background image overlay
- Dark overlay gradients for text readability
- Rounded corners with defined radius values
- Box shadows for depth and elevation
- Smooth transitions and hover effects
- Toast notifications with color-coded severity

**Design Principles:**

- Mobile-first responsive approach
- Accessibility considerations (contrast, focus states)
- Performance optimization (optimized images, minimal JS)
- Progressive enhancement
- Consistent spacing and rhythm

## Features

### Existing Features

#### Military-Styled Landing Page

The platform features a professional landing page designed with military aesthetics to immediately communicate the club's tactical identity.

**Key Features:**

- **Parallax Hero Section**: Full-viewport hero with fixed background and dark overlay for text readability
- **Responsive Design**: Seamless adaptation across mobile, tablet, and desktop devices
- **Eyebrow Badge**: Custom pill-shaped badge displaying "N.S.O.G. · Crudeles in Proelio"
- **Danish Content**: All user-facing text in Danish for the primary audience
- **Dark Military Theme**: Color palette inspired by tactical gear and military operations
- **Modern Typography**: Bold, condensed headers with clean body text
- **Smooth Scrolling**: Enhanced user experience with smooth scroll behavior
- **CTA Buttons**: Action buttons styled with military-inspired design

**Navigation:**

- Fixed navbar with glass morphism effect
- Responsive hamburger menu for mobile
- Dynamic authentication state (Login button vs User dropdown)
- Staff users see Admin panel link
- Logo prominently displayed in center
- Smooth transitions and hover effects

#### Email-Based Authentication

Secure email and password authentication system without dependency on social login providers.

**Login Features:**

- Email and password combination for authentication
- "Remember me" functionality for persistent sessions
- Clear error messaging with Full Metal Jacket-style Danish phrases
- Password field with secure input
- CSRF protection on all forms
- Redirect to dashboard after successful login
- Toast notifications with randomized ironic messages

**Logout Features:**

- Confirmation page before logout
- Secure session termination
- Toast notification on successful logout
- Option to cancel and return to dashboard

**Password Management:**

- Secure password change functionality
- Current password verification
- Password confirmation for new password
- Django's built-in password validators
- Strong password requirements
- Toast confirmation on successful change

**Security Features:**

- Session management with secure cookies (production)
- CSRF protection on all authentication forms
- Secure password storage using Django's PBKDF2 algorithm
- Custom User model with email as USERNAME_FIELD
- AllAuth integration for enhanced authentication
- Middleware protection for authentication state

#### Custom User Management

Comprehensive user model tailored specifically for airsoft club member management.

**User Model Attributes:**

- **Email** (Required): Primary authentication identifier, unique
- **First Name** (Nome - Required): Member's given name
- **Last Name** (Cognome - Required): Member's surname
- **Rank** (Default: PVT): Hierarchical position with 11 military ranks:
  - **Officers**: CPT (Captain), 1LT (First Lieutenant), 2LT (Second Lieutenant)
  - **NCOs**: SGT 1C (Sergeant First Class), SSGT (Staff Sergeant), SGT (Sergeant)
  - **Specialist**: CPL (Corporal)
  - **Enlisted**: SPC (Specialist), PVT 1, PVT 2, PVT (Private)
- **Nationality** (Optional): ISO country code (e.g., DNK, ITA)
- **Residence** (Optional): Current location
- **Nickname** (Optional): Callsign or preferred name
- **Info** (Optional): Additional member information

**Admin Features:**

- Custom admin interface with enhanced user management
- List view with email, name, rank, and status display
- Filterable by rank, nationality, and status
- Searchable by email, name, and nickname
- Fieldsets organized by category (Personal Info, Rank, Permissions, Dates)
- Read-only fields for join date and last login
- Inline password management
- Bulk actions for member management

**User Display:**

- Full name method combining first and last name
- Short name method returning first name only
- String representation showing rank and surname
- Rank display with proper capitalization

**Signals Integration:**

- Login success handler with randomized Danish welcome messages
- Login failure handler with randomized Danish error messages
- Messages formatted with user's rank and surname
- Full Metal Jacket-inspired ironic tone

**Access Control:**

- Staff status for admin panel access
- Superuser status for full permissions
- Active status for account enablement
- Groups and permissions support
- Role-based access ready for expansion

#### Enheden (Members-Only Command Structure)

A protected page accessible exclusively to authenticated members, displaying the unit's full command structure.

**Key Features:**

- Login-required access control — unauthenticated users are redirected to the login page
- Members grouped by rank according to the official hierarchy (CPT down to PVT)
- Colored rank pills for instant visual identification of rank category (Officers, NCOs, Specialist, Enlisted)
- Member details: full name, nationality badge, location, and rank displayed per row
- Accessible via "Enheden" link in the navbar (visible only to logged-in users)

#### Admin Kommandostruktur Panel

A staff-only admin page for managing the unit roster and assigning military ranks.

**Key Features:**

- Staff-only access enforced with `@staff_member_required`
- Full member table with sortable columns: Name, Nationality, Rank, Location
- Sortable in both ascending and descending order via clickable column headers
- Colored rank pills grouped by category: gold (Officers), red (NCOs), green (CPL), blue (Enlisted)
- Inline rank `<select>` dropdown per member row for quick rank changes
- Bootstrap confirmation modal before applying rank changes, with safe DOM construction (XSS-safe)
- AJAX rank update: no page reload, pill text updates instantly on success
- Server-side rank validation against a whitelist — invalid ranks rejected
- CSRF token injected via Django `{% csrf_token %}` hidden input (not cookie parsing)

#### Join Request Protection

Authenticated members are blocked from accessing the join request form (`/users/join/`) to prevent duplicate applications.

**Key Features:**

- Authenticated users attempting to visit `/users/join/` are immediately redirected to the homepage
- Full Metal Jacket-style Danish toast message informs the user they are already enlisted
- Unauthenticated visitors see the join form normally
- "Anmod om prøvekamp" link in the navbar is replaced by "Enheden" for logged-in users

#### Member Profile Card

Authenticated members can edit their personal profile card at `/users/profile/edit/`, accessible via the **Profil** link in the navbar dropdown (desktop) or the profile page (mobile).

**Editable Fields:**

- **Profile Image**: Upload JPG or WebP portrait photo. Constraints enforced server-side:
  - Max file size: 2 MB
  - Aspect ratio: approximately 600×840 px (portrait, ±15% tolerance)
  - Accepted formats: JPG, WebP (verified by Pillow, not just file extension)
  - Automatically converted and saved as WebP (quality 82, max 600×840 px) to reduce storage footprint
  - Only one image stored per user — the previous image is deleted from storage before saving the new one
- **Nationality**: Dropdown with full country list (ISO 3166-1 alpha-3), displaying flag emoji and ISO code
- **Bio**: Free-text field, max 500 characters, with live character counter

**Read-Only Fields (admin-controlled):**

- First name and last name
- Military rank (assigned by staff via Admin Kommandostruktur panel)

#### News & Events Management (comms app)

A dedicated `comms` Django app handles all club communication: news posts visible to everyone, and events that authenticated members can respond to.

**News (Nyheder):**

- Admin-only creation, editing, and deletion of news posts at `/nyheder/admin/news/`
- Accessible from the Admin Dashboard card
- Automatic slug generation from the post title using Django's `slugify`
- Optional SEO description field (max 160 characters) for Google search snippets
- Full Open Graph and Twitter Card meta tags (`og:title`, `og:description`, `og:image`) so links shared on WhatsApp and Discord show a rich preview
- **Automatic expiry**: news posts are deleted after 4 months via the management command `python manage.py delete_old_news` (supports `--dry-run`). Events are never affected. A persistent reminder banner is shown on the news admin page.

**Events:**

- Admin-only creation, editing, and deletion at `/nyheder/admin/events/`
- Each event is composed of a `Post` (title, content, image, SEO description) and an `Event` record (date/time, location, max participants)
- Admin can click any event to view the full **attendees list** split into three columns: Operativo / In Stand-by / Fuori Servizio
- Authenticated members can RSVP directly from the event detail page via three buttons; status updates instantly via a `fetch` (AJAX) call without a page reload
- Unauthenticated visitors can read event details but are prompted to log in to send an RSVP

**Image Handling:**

- Upload limit enforced at **5 MB** (validation error shown if exceeded)
- All uploaded images are automatically resized to a maximum of **1200 px** on the longest edge
- Converted and saved as **WebP** (quality 82) — typically 60–80 % smaller than the original JPEG
- In production, images are stored on the GCS media bucket

**Public listing page**: `/nyheder/` shows all posts (news and events) with pagination (12 per page), badge labels, and links to detail pages. Accessible to all visitors without login.

### Features Left to Implement

Future enhancements planned for the platform:

**Phase 2 - Remaining Content Features:**

- Comment system for news posts
- Member directory with filtering
- Email notification system for new events

**Phase 3 - Enhanced Member Experience:**

- Training resources library
- Photo gallery for operations
- Member achievement and badge system
- Personal statistics and progress tracking
- Member-to-member messaging
- Notification preferences
- GDPR data export functionality
- Advanced profile customization

**Phase 4 - Advanced Features:**

- Analytics and reporting dashboard
- PDF report generation
- Bulk member operations
- CSV import/export
- Advanced search functionality
- Performance optimization (caching, CDN)
- SEO optimization
- API development for mobile app

## Technologies Used

- **Pillow** - Python Imaging Library for server-side image processing, WebP conversion, and automatic resizing

### Backend Framework & Core

- **Python 3.11** - High-level programming language for backend development
- **Django 5.2.13** - Full-stack web framework providing ORM, admin interface, authentication, and security features
- **django-allauth 65.3.0** - Comprehensive authentication solution supporting email/password authentication
- **WSGI** - Web Server Gateway Interface for deploying Python web applications

### Database

- **SQLite** - Lightweight SQL database engine used for local development
- **PostgreSQL** - Advanced open-source relational database planned for production

### Frontend Technologies

- **HTML5** - Semantic markup for structuring content
- **CSS3** - Custom styling for military-themed design and responsive layouts
- **JavaScript (ES6+)** - Client-side interactivity and dynamic behavior
- **Bootstrap 5.3.0** - Responsive CSS framework for consistent UI components
  - Grid system for responsive layouts
  - Form components and validation
  - Navigation components
  - Dropdown menus
  - Utility classes
- **Font Awesome 6.4.0** - Icon library for UI elements
- **Google Fonts** - Custom typography (Barlow Semi Condensed, Inter)

### Authentication & Security

- **Django AllAuth** - Email-based authentication system
- **django.contrib.auth** - Django's built-in authentication framework
- **Custom User Model** - Email-based authentication instead of username
- **Session Management** - Secure session handling with cookie-based storage
- **CSRF Protection** - Cross-Site Request Forgery protection on all forms
- **Password Validators** - Strong password requirements

### Development Tools

- **pip** - Python package installer for dependency management
- **venv** - Python virtual environment for isolated development
- **Git** - Version control system for code management
- **VS Code** - Development environment with Python extensions

### Django Components

- **django.contrib.sites** - Multi-site support framework
- **django.contrib.staticfiles** - Static file management and serving
- **django.contrib.admin** - Built-in admin interface
- **asgiref 3.11.1** - ASGI (Asynchronous Server Gateway Interface) specification
- **sqlparse 0.5.5** - SQL statement parsing and formatting

### Package Management

All dependencies are tracked in `requirements.txt`:

```
asgiref==3.11.1
Django==5.2.13
sqlparse==0.5.5
django-allauth==65.3.0
```

## Testing

Testing documentation will be added in future iterations covering:

- Unit tests for models and views
- Integration tests for authentication flow
- Form validation testing
- Admin interface testing
- Responsive design testing
- Browser compatibility testing
- Accessibility testing (WCAG compliance)
- Security testing
- Performance testing

## Deployment

### Local Development Setup

1. Clone the repository:
```bash
git clone <repository-url>
cd teamhardball
```

2. Create and activate virtual environment:
```bash
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Run migrations:
```bash
python manage.py migrate
```

5. Create superuser (admin account):
```bash
python create_admin.py
# Or manually:
python manage.py createsuperuser
```

6. Run development server:
```bash
python manage.py runserver
```

7. Access the site at: `http://localhost:8000`

### Production Deployment

Production deployment instructions will be added covering:

- PostgreSQL database configuration
- Static file serving (WhiteNoise or CDN)
- Environment variables management
- HTTPS/SSL configuration
- Gunicorn or uWSGI setup
- Nginx reverse proxy configuration
- Security settings (DEBUG=False, ALLOWED_HOSTS, etc.)
- Regular backups
- Monitoring and logging

### Environment Variables

Key environment variables for production:

- `SECRET_KEY` - Django secret key
- `DEBUG` - Debug mode (False in production)
- `ALLOWED_HOSTS` - Permitted hosts
- `DATABASE_URL` - PostgreSQL connection string
- `EMAIL_BACKEND` - Email service configuration
- `STATIC_ROOT` - Static files directory
- `MEDIA_ROOT` - Media files directory

## Credits

### Development

- **Developer**: Andrea La Torre
- **Client**: N.S.O.G. Danish Airsoft Club
- **Framework**: Django Software Foundation
- **Design Inspiration**: Military tactical aesthetics and modern SaaS platforms

### Resources

- **Django Documentation**: https://docs.djangoproject.com/
- **Django AllAuth**: https://django-allauth.readthedocs.io/
- **Bootstrap 5**: https://getbootstrap.com/
- **Font Awesome**: https://fontawesome.com/
- **Google Fonts**: https://fonts.google.com/

### Acknowledgments

- Full Metal Jacket movie for toast message inspiration
- Airsoft community for feedback and requirements
- Open source community for tools and libraries

---

**N.S.O.G. - Crudeles in Proelio** 🎯

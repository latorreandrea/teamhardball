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
- **Real-Time Tactical Map**: Provide a shared real-time map for Milsim operations, enabling platoon coordination with GPS tracking, spotting, and marker placement

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
- **Participate in real-time tactical operations on the shared map**
- **Spot enemies and place tactical markers as a Team Leader**
- **Track platoon members' positions during Milsim events**

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
- **Create tactical game rooms with configurable spawn points and HQ locations**
- **Assign Team Leaders and organize platoons within each game**
- **Monitor live positions during operations**

#### User Values

- **Tactical Identity**: Military-themed design that resonates with airsoft culture and creates immersive experience
- **Privacy & Exclusivity**: Controlled membership with admin approval, no public registration
- **Security**: Email-based authentication with robust password management
- **Rank Recognition**: Clear hierarchy system that acknowledges experience and commitment
- **Community**: Centralized platform for communication and collaboration
- **Transparency**: Clear information about club operations, events, and activities
- **Mobile Accessibility**: Full functionality across all devices for on-the-go access
- **Danish Language**: Native language support for the primary user base
- **Real-Time Coordination**: Live tactical awareness during Milsim operations

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
- **Real-time visibility of all players on the tactical map during operations**
- **Clear visual distinction between own position, platoon members, and other squad members**
- **Automatic reconnection if the WebSocket drops during long Milsim sessions**

**Admins expect:**

- Comprehensive member management dashboard
- Easy event creation and modification tools
- Bulk operations for member management
- Data export capabilities
- Content management for news and announcements
- Analytics on member activity
- Full control over rank assignments
- GDPR-compliant data handling
- **Ability to create game rooms with pre-configured spawn points and HQ markers**
- **Ability to designate Team Leaders per platoon during game setup**
- **Live oversight of the tactical situation during operations**

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
- **As a member I want to see my own position (white marker) and my platoon members (green markers) on the tactical map so that I can coordinate with my unit**
- **As a member I want to see other squad members (blue markers) so that I maintain situational awareness across the operation**
- **As a Team Leader I want to spot enemies and place tactical markers so that my platoon has real-time intelligence**
- **As a member I want the map to survive 20-hour Milsim sessions with automatic WebSocket reconnection**

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
| Interactive org chart (hierarchy) | 4 | 5 |
| Event registration system | 4 | 3 |
| Photo gallery | 3 | 4 |
| Training resources section | 3 | 3 |
| Email notifications | 3 | 3 |
| Member messaging system | 2 | 2 |
| Mobile native app | 2 | 1 |
| Export reports to PDF | 3 | 3 |
| Analytics dashboard | 3 | 3 |
| **Real-time tactical map with GPS** | **5** | **4** |
| **Total** | **98** | **100** |

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

**Real-Time Operations**

- Live GPS tracking via WebSocket for tactical coordination
- In-memory state management via Redis (no database writes during gameplay)
- Shared map with real-time player positions and tactical markers
- Spotting system with configurable visibility duration
- Automatic reconnection for extended Milsim sessions

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
- Interactive org chart (`hierarchy` app) — see full description below

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

#### Phase 5: Real-Time Tactical Map — Milsim Operations (NEW)

**Goal**: Provide a shared real-time tactical map for Milsim operations, enabling platoon coordination via GPS tracking, enemy spotting, and tactical marker placement — all without touching the relational database during gameplay (pure Redis in-memory state).

**Features delivered in this phase:**

- **Django Channels + Redis Channel Layer**: WebSocket infrastructure for real-time bidirectional communication
- **Daphne ASGI Server**: replaces Gunicorn to handle WebSocket connections alongside HTTP
- **tactical Django app**: dedicated app for game rooms, player management, and map rendering
- **Game Room Model**: persistent Game and GamePlayer models (PostgreSQL), with Redis-only real-time state
- **Game Creation Interface**: admin creates game rooms with bounding box (area of play), spawn points, HQ locations, and pre-assigned Team Leaders per platoon
- **Leaflet.js Map**: full-screen interactive map with OpenStreetMap tiles, custom markers, and tactical overlays
- **GPS Throttling**: client-side GPS sent at most every 10 seconds or 5 metres, reducing bandwidth and CPU
- **Foreground Tracking Requirement**: reliable GPS updates require the map page to stay open and in the foreground; when the device is locked or the browser goes background, updates may pause on most mobile browsers
- **Keep-Awake Support**: where supported, the map can use the browser wake lock pattern to help keep the display active during an operation
- **Player Marker Colors**:
  - 🟢 **Green** — same platoon members
  - 🔵 **Blue** — same squad, different platoon
  - ⚪ **White** — own position
- **Directional Player Markers**: each player marker includes a heading vector (chevron/triangle) pointing in the direction of movement, calculated from GPS bearing between consecutive positions. The heading is sent alongside GPS coordinates as a `heading` field and rendered via rotated SVG on Leaflet — no extra dependencies required.
- **Spotting System**: All members can place "enemy spotted" markers (🔴, 10-second TTL via Redis)
- **Tactical Marker Types** (Team Leader only):
  - 🔴 **Spot** — enemy sighting (10s TTL)
  - 🎯 **Objective** — mission objective marker (300s TTL)
  - ➡️ **Move Order** — movement directive (60s TTL)
  - 📌 **Regroup** — rally point (120s TTL)
  - ⚠️ **Danger Zone** — hazardous area (120s TTL, available to all members)
- **Spawn & HQ Markers**: persistent fixed markers placed during game creation, visible to all players
- **Toast Notifications**: role-specific toasts on room join (e.g. "You are Team Leader of 1st Platoon" or "You are part of 1st Platoon — Alpha")
- **Automatic WebSocket Reconnection**: client automatically reconnects with exponential backoff (handles Cloud Run's 60-minute timeout)
- **Zero Database Writes During Gameplay**: all GPS positions, spots, and markers live in Redis with TTL-based auto-expiry
- **Cloud Run Optimized Configuration**: `--min-instances=1`, `--no-cpu-throttling`, `--session-affinity`, 60-minute timeout

**Software Architecture:**

```
┌─────────────────────────────────────────────────────────────┐
│                    Browser (Leaflet.js)                      │
│  • Geolocation API (throttled to 10s / 5m)                  │
│  • WebSocket client with auto-reconnect                     │
│  • Marker rendering with color-coded platoons               │
│  • Spot/marker placement UI (Team Leader only)              │
└─────────────────────┬───────────────────────────────────────┘
                      │ wss://host/ws/game/<id>/
                      ▼
┌─────────────────────────────────────────────────────────────┐
│                   Cloud Run Container                        │
│                                                             │
│  Daphne → Django Channels (AuthMiddlewareStack)             │
│         │                                                   │
│         ▼                                                   │
│  GameConsumer (AsyncWebsocketConsumer)                       │
│         │                                                   │
│         ├── group_send → all players in game_{id} group     │
│         └── Redis commands for state management             │
└─────────────────────┬───────────────────────────────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────────┐
│              Redis Cloud (Free Tier — 30 MB)                 │
│                                                             │
│  Keys (all auto-expire via TTL):                            │
│  • game:{id}:position:{user_id} → GPS (TTL 15s)            │
│  • game:{id}:marker:{type}:{uid} → Marker (TTL varies)      │
│  • game:{id}:players → Set of active user IDs               │
│                                                             │
│  Channels Layer (pub/sub):                                  │
│  • game_{id} → all messages broadcast to group              │
└─────────────────────────────────────────────────────────────┘
```

**Key Design Decisions:**

| Decision | Rationale |
|---|---|
| **Redis-only real-time state** | Zero load on PostgreSQL during gameplay; automatic cleanup via TTL |
| **GPS throttling (10s/5m)** | 90% reduction in messages vs. native Geolocation API rate |
| **All players visible to all** | Shared situational awareness for platoon coordination |
| **Spotting available to all members** | Shared enemy reporting for broader situational awareness |
| **Auto-reconnect on WebSocket drop** | Cloud Run hard 60-min timeout; required for 20-hour Milsim |
| **Daphne over Gunicorn** | Daphne handles both HTTP and WebSocket; Gunicorn is WSGI-only |
| **Redis Cloud Free Tier (30MB)** | Sufficient for 100 concurrent players; less than 200KB actual data |

**Target Game Size:** 3–20 players (scales to 100)

**Session Duration:** Up to 20 hours (Milsim)

**Cost Impact:** €0 (Cloud Run Free Tier + Redis Cloud Free Tier)

**Files Created (new `tactical` app):**

```
tactical/
├── __init__.py
├── admin.py
├── apps.py
├── consumers.py           # GameConsumer — WebSocket handler
├── models.py              # Game, GamePlayer
├── routing.py             # WebSocket URL patterns
├── urls.py                # HTTP views
├── views.py               # Game room views
├── migrations/
├── templates/tactical/
│   └── game_map.html      # Leaflet.js map page
├── static/tactical/
│   ├── js/map.js          # GPS + WebSocket client controller
│   └── css/map.css        # Map-specific styling
```

**Files Modified:**

| File | Change |
|---|---|
| `teamhardball/settings.py` | Add `channels`, `tactical` to INSTALLED_APPS; add `ASGI_APPLICATION`, `CHANNEL_LAYERS` with Redis URL |
| `teamhardball/asgi.py` | Rewrite with `ProtocolTypeRouter` for HTTP + WebSocket routing |
| `teamhardball/urls.py` | Add `path('tactical/', include('tactical.urls'))` |
| `entrypoint.sh` | Replace `gunicorn` with `daphne` server |
| `requirements.txt` | Add `channels`, `channels-redis`, `daphne`, `redis` |
| `templates/base.html` | Optional: add tactical map nav link for authenticated users |

**New Environment Variables:**

- `REDIS_URL` — Redis connection string (e.g. `redis://user:pass@host:6379/0`). Defaults to `redis://localhost:6379/0` for local development.

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
├── Hierarchy / Org Chart
│   └── Interactive D3.js org chart
├── Tactical Map [NEW]
│   ├── Active Games List
│   ├── Game Room (Full-Screen Map)
│   │   ├── Player Markers (White / Green / Blue)
│   │   ├── Spawn / HQ Markers (Fixed)
│   │   ├── Spot Markers (Team Leader — 10s TTL)
│   │   └── Tactical Markers (Team Leader — variable TTL)
│   └── Game Creation (Admin)
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
│   ├── Analytics
│   └── Tactical Games [NEW]
│       ├── Game List
│       ├── Create Game
│       │   ├── Area bounding box (lat/lng)
│       │   ├── Spawn points
│       │   ├── HQ locations
│       │   ├── Platoon assignments
│       │   └── Team Leader designations
│       └── Game Detail / Live View
└── Site Settings
```

#### Navigation Patterns

**Top Navigation Bar:**

- Logo on the left (clickable home link)
- Main menu items in center (Events, News, Members for authenticated users)
- Login button or user dropdown on the right
- Hamburger menu on mobile devices
- Rank and name displayed for authenticated users
- **Tactical Map link visible to authenticated members**

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
- **Leaflet.js map with OpenStreetMap tiles**
- **Custom SVG markers for player positions (white/green/blue)**
- **Pulsing red markers for enemy spots**
- **Military-style marker icons for tactical commands**

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

#### Interactive Org Chart — Hierarchy App *(Implemented: May 2026)*

A full-page, interactive organisational chart built with D3.js v7, showing the club's command structure as a zoomable, pannable SVG tree.

**Chart & Layout:**

- D3.js `d3.tree()` layout with `nodeSize` for fixed spacing
- Orthogonal (squared) link paths — classic org chart style with 90° corners
- Zoom and pan via `d3.zoom()` with scale limits `[0.2, 3]`
- Animated entry: chart eases in from a slightly zoomed-out starting position on load
- Node fade-in cascade: each card appears sequentially with a 40 ms delay between nodes
- **Reset button** (bottom-right): animated smooth zoom back to initial view
- **Locate-me button**: animates to the node where the current user is leader or member; hidden if user has no node
- Legend bar showing color coding for Kommando, Enhed, Patrulje

**Node Cards:**

- 270 × 248 px (staff) / 270 × 178 px (non-staff) SVG cards
- Color accent bar at top coded by node type
- Leader slot (44 × 44 px): shows photo, silhouette (if no photo), dashed `+` slot for staff (opens leader modal), or muted silhouette for non-staff — clicking a photo or silhouette navigates to the operator's profile
- Leader rank and name text fields
- Members section with circular avatar row (up to 9); clicking any avatar navigates to the operator's profile
- Staff `+/−` avatar button opens the member management modal
- Staff action bar (edit / delete buttons) visible only to staff
- Quick-add child button (below each node) and quick-add sibling button (right of non-root nodes)

**Staff Modals (AJAX, no page reload for data):**

- **Create node modal**: name, node type, parent, leader, order
- **Edit node modal**: pre-filled from clicked node data
- **Delete node modal**: confirmation with node name and cascade warning
- **Member management modal** (`nodeMembersModal`): full operator list with checkboxes, limit banner at 9, per-user "anden enhed" badge if already in another node, live counter in footer; saves via `fetch` POST then reloads
- **Leader assignment modal** (`nodeLeaderModal`): radio-button operator list, "anden enhed" badge if already leading another node, remove-leader button; saves via `fetch` POST then reloads

**Backend (`hierarchy` app):**

- `Node` model: `name`, `node_type` (command/unit/patrol), `parent` (FK self, SET_NULL), `leader` (FK User, nullable), `members` (M2M User), `order`
- `hierarchy_map` view: `@login_required`, serialises all nodes to JSON for client-side rendering
- `node_create`, `node_edit`, `node_delete`: `@staff_member_required`, use `get_object_or_404`; `node_edit` flashes a `messages.error` toast on invalid form
- `node_members`: `@staff_member_required`, GET returns paginated user list (cap 100, `?q=` search filter, `total` field in response); POST enforces `MEMBER_LIMIT = 9` server-side
- `node_leader`: `@staff_member_required`, GET returns users with `is_current`/`taken` flags; POST sets or clears the leader
- All mutating views log staff actions via Python `logging` (`logger.info` / `logger.warning`)
- All JSON endpoints return HTTP 400 with `{"error": "Invalid JSON"}` on malformed request bodies

**Security:**

- All write endpoints protected with `@staff_member_required`
- `get_object_or_404` on every pk lookup — no unhandled `DoesNotExist` 500 errors
- `json.JSONDecodeError` caught and returned as 400 JSON response
- `leader_id` validated against `is_active=True` users via `get_object_or_404`
- `member_ids` capped at `MEMBER_LIMIT` server-side regardless of client input

#### Achievement & Badge System *(Implemented: May 2026)*

A full achievement system that lets admins define badges and award them to operators, while members can browse the catalogue and track which badges they hold.

**Badge Catalogue (`/achievements/`):**

- Grid of achievement cards accessible to all authenticated members
- Each card shows the badge icon, title, and an owned indicator if the member already holds it
- Admin-only **"+ Nyt badge"** card (first in grid) opens a create modal in-page — no separate admin page required
- Create form validates title, slug, description, and icon; auto-reopens modal on validation errors

**Badge Detail Page (`/achievements/<id>/`):**

- Tilt card with GSAP parallax/shine effect displaying the badge icon
- Description, active status, and a list of up to 12 holders with their rank insignia icon and formatted name
- Holders list links to each operator's detail page

**Admin Controls (staff only):**

- **Edit modal**: pre-filled with current values and icon preview; saves changes in-page via POST
- **Delete modal**: shows cascade warning with total holder count before permanent deletion
- **Assignment modal** (`modal-lg`): full operator list with per-row visual state indicators:
  - **Tildelt** (green) — operator already holds the badge and checkbox is still checked
  - **Tilføjes** (tan) — operator will be added when saved
  - **Fjernes** (red) — operator will be removed when saved
  - Sort controls: by last name (Danish locale), by rank hierarchy, or by badge ownership
  - Live footer count updates on every checkbox change
  - Submits a diff to the server: only additions and removals are processed, existing unchanged rows are untouched

**Icon Handling:**

- Upload limit: **512 KB**
- Automatically converted to **WebP** via Pillow
- Resized to a maximum of **128 × 128 px**
- Accepted formats: PNG, JPG, WebP, GIF

**Models:**

- `AchievementDefinition`: slug, title, info, icon, is_active
- `UserAchievement`: FK to user (CASCADE), FK to definition (CASCADE), awarded_at, awarded_by (SET_NULL), reason; `UniqueConstraint(['user', 'achievement'])` prevents duplicates

### Features Left to Implement

Future enhancements planned for the platform:

**Phase 2 - Remaining Content Features:**

- Comment system for news posts
- Member directory with filtering
- Email notification system for new events

**Phase 3 - Enhanced Member Experience:**

- Training resources library
- Photo gallery for operations
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

**Phase 5 - Real-Time Tactical Map (PLANNED):**

- [ ] Create `tactical` Django app with Game and GamePlayer models
- [ ] Add Django Channels + Daphne ASGI server
- [ ] Configure Redis Channel Layer for real-time communication
- [ ] Implement GameConsumer with GPS, marker, and spotting handlers
- [ ] Build Leaflet.js map frontend with player markers (white/green/blue)
- [ ] Add GPS throttling (10s / 5m threshold)
- [ ] Implement spotting system (all members, 10s TTL via Redis)
- [ ] Add tactical marker types (Spot, Objective, Move, Regroup, Danger Zone)
- [ ] Build game creation interface with spawn/HQ points and platoon assignment
- [ ] Implement automatic WebSocket reconnection for 20-hour Milsim sessions
- [ ] Add toast notifications on room join (role/platoon assignment)
- [ ] Configure Cloud Run for WebSocket support (session affinity, no-cpu-throttling)
- [ ] Deploy with Redis Cloud Free Tier for zero-cost real-time state

## Technologies Used

- **Pillow** - Python Imaging Library for server-side image processing, WebP conversion, and automatic resizing

### Backend Framework & Core

- **Python 3.11** - High-level programming language for backend development
- **Django 5.2.13** - Full-stack web framework providing ORM, admin interface, authentication, and security features
- **django-allauth 65.3.0** - Comprehensive authentication solution supporting email/password authentication
- **Django Channels 4.2.0** - WebSocket/ASGI layer for Django, enabling real-time bidirectional communication
- **channels-redis 4.2.1** - Redis Channel Layer backend for Django Channels (pub/sub across containers)
- **Daphne 4.1.2** - ASGI HTTP/WebSocket server for Django (replaces Gunicorn for WebSocket support)
- **WSGI/ASGI** - Dual-protocol support for HTTP and WebSocket traffic

### Database

- **SQLite** - Lightweight SQL database engine used for local development
- **PostgreSQL** - Advanced open-source relational database planned for production
- **Redis 7.x** - In-memory data store for real-time game state (player positions, markers, spots) with automatic TTL expiry

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
- **D3.js v7** - Data-driven SVG visualisation library used for the interactive organisational chart (hierarchy app)
- **GSAP (GreenSock Animation Platform) 3** - JavaScript animation library used for tilt card effects, parallax shine, and entrance animations on operator and achievement detail pages
- **Leaflet.js 1.9** - Open-source interactive map library used for the real-time tactical map
- **OpenStreetMap Tiles** - Free map tile layer for the tactical map background

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
- **Docker** - Containerization for local Redis instance and production deployment

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
channels==4.2.0
channels-redis==4.2.1
daphne==4.1.2
redis==5.2.1
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
- **WebSocket consumer unit tests**
- **GPS throttling and reconnection edge cases**

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

6. Start local Redis instance (required for WebSocket/Channels):
```bash
docker run -d --name redis -p 6379:6379 redis:7-alpine
```

7. Run development server (Daphne for ASGI + WebSocket support):
```bash
daphne -b 0.0.0.0 -p 8000 teamhardball.asgi:application
```

8. Access the site at: `http://localhost:8000`

### Cloud Run Production Deployment

The project deploys via Google Cloud Build (see `cloudbuild.yaml`). For WebSocket support, ensure the following Cloud Run configuration:

```bash
gcloud run deploy nsog \
  --image=${_REGION}-docker.pkg.dev/${PROJECT_ID}/${_REPO}/nsog:$BUILD_ID \
  --region=europe-west1 \
  --platform=managed \
  --min-instances=1 \
  --max-instances=10 \
  --concurrency=80 \
  --timeout=3600 \
  --session-affinity \
  --no-cpu-throttling \
  --cpu=1 \
  --memory=512Mi \
  --set-env-vars="REDIS_URL=redis://<user>:<pass>@<host>:6379/0"
```

Required environment variables in production:

| Variable | Description |
|---|---|
| `REDIS_URL` | Redis connection string (e.g. Upstash, Redis Cloud, or Memorystore) |
| `SECRET_KEY` | Django secret key |
| `DATABASE_URL` | PostgreSQL connection string |
| `GS_BUCKET_NAME` | GCS bucket for static files |
| `GS_MEDIA_BUCKET_NAME` | GCS bucket for media files |

## Credits

- Club leadership and members of N.S.O.G. for their continued support and feedback
- OpenStreetMap contributors for free map tiles
- Leaflet.js community for the interactive mapping library
- Redis for the in-memory data store
- Django Channels team for WebSocket support
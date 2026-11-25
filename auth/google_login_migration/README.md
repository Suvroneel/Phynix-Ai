# Google Login Integration (Auth v2)

## Context
UnixOpens originally used Supabase email/password authentication.
This module adds Google OAuth login via Supabase Auth to reduce onboarding friction and improve user experience.

## Current State
- Email / Password auth: Stable
- Google OAuth: Functional, UX iteration in progress

Google login is enabled but remains in testing while UI polish and edge cases are being resolved.

## What Changed
- Added Google as an authentication provider in Supabase
- Unified session handling across email and OAuth users
- Updated auth flow to support multiple login methods

## Known Limitations
- OAuth UX still being refined
- Error feedback on OAuth failure is minimal
- Google OAuth is currently in testing mode

## Next Steps
- Finalize login screen UX
- Improve OAuth error handling
- Move Google login out of testing

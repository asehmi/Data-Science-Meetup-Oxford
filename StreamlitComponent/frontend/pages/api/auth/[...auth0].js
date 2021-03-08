// Using auto-configured SDK from nextjs-auth0 1.0.0.
// It provides ready-made routes for /api/auth/login, /api/auth/callback, /api/auth/logout and /api/auth/me
// Note: Adjust Auth0 service's connection settings to include these routes in callback and logout sections
import { handleAuth } from '@auth0/nextjs-auth0';

export default handleAuth();
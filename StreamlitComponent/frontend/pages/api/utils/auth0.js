import { initAuth0 } from '@auth0/nextjs-auth0';

export default initAuth0({
    domain: process.env.AUTH0_DOMAIN,
    clientId: process.env.AUTH0_CLIENT_ID,
    clientSecret: process.env.AUTH0_SECRET,
    audience: process.env.API_AUDIENCE,
    redirectUri: process.env.AUTH0_CALLBACK_URL,
    postLogoutRedirectUri: process.env.AUTH0_LOGOUT_URL,
    scope: 'openid profile email ClientId ContactId CompanyName name',
    session: {
        // The secret used to encrypt the cookie.
        cookieSecret: process.env.COOKIE_SECRET,
        // The cookie lifetime (expiration) in seconds. Set to 8 hours by default.
        cookieLifetime: 60 * 60 * 8,
        // (Optional) The cookie domain this should run on. Leave it blank to restrict it to your domain.
        // cookieDomain: process.env.COOKIE_DOMAIN,
        // (Optional) SameSite configuration for the session cookie. Defaults to 'lax', but can be changed to 'strict' or 'none'. Set it to false if you want to disable the SameSite setting.
        // cookieSameSite: 'lax',
        // (Optional) DOESN'T SEEM TO WORK WHEN TRUE!! Store the id_token in the session. Defaults to false.
        storeIdToken: false,
        // (Optional) Store the access_token in the session. Defaults to false.
        storeAccessToken: true,
        // (Optional) Store the refresh_token in the session. Defaults to false.
        storeRefreshToken: true,
    },
    oidcClient: {
        // (Optional) Configure the timeout in milliseconds for HTTP requests to Auth0.
        httpTimeout: 5000,
        // (Optional) Configure the clock tolerance in milliseconds, if the time on your server is running behind.
        clockTolerance: 60000
    }
});

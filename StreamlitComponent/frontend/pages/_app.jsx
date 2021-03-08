import React from 'react';
import { UserProvider } from '@auth0/nextjs-auth0';

import '../styles/globals.css';
import '../styles/index.css';
import 'tailwindcss/tailwind.css';

function App({ Component, pageProps }) {
  // You can optionally pass the `user` prop from pages that require server-side
  // rendering to prepopulate the `useUser` hook.
  const { user } = pageProps;

  return (
    <UserProvider user={user}>
        <Component {...pageProps} />
    </UserProvider>
  );
}

export default App;

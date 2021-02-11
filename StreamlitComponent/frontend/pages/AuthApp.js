import { useEffect, useState } from 'react'
import Head from 'next/head';

export default function AuthApp({ session }) {

    console.log('======== AuthApp ========')

    const SHOW_UI = false
    
    const user = session?.user
    const accessToken = session?.accessToken
    const accessTokenExpiresAt = session?.accessTokenExpiresAt

    console.log(user ? user : 'Null user')
    console.log(accessToken ? accessToken : 'Null token')
    console.log(accessTokenExpiresAt ? accessTokenExpiresAt : 'Null token expiry')

    useEffect(() => {
        if (accessToken && accessTokenExpiresAt) {
            window.localStorage.setItem('token', accessToken)
            window.localStorage.setItem('tokenExpiry', accessTokenExpiresAt)
            console.log('Stored token: ' + accessToken)
            console.log('Stored token expiry: ' + accessTokenExpiresAt)
        } else {
            window.localStorage.removeItem('token')
            window.localStorage.removeItem('tokenExpiry')
        }
    })

    return (
        <div className="container max-w-xl">
            <Head>
                <title>Authentication</title>
            </Head>
            <main>
                <div className="container my-0 max-w-xl">
                    {SHOW_UI && !user && (
                        <div className="text-xl my-2">Click to sign into the application...</div>
                    )}
                    {SHOW_UI && !user && (
                        <a  href="/api/login"
                            className="inline-flex px-4 py-1 border border-transparent
                            rounded-md shadow-sm text-md font-small text-white bg-indigo-600 hover:bg-pink-600
                            focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                            Login
                        </a>
                    )}
                    {SHOW_UI && user && (
                        <div className="text-xl my-2">Click to sign out of the application...</div>
                    )}
                    {SHOW_UI && user && (
                        <a  href="/api/logout"
                            className="inline-flex px-4 py-1 border border-transparent
                            rounded-md shadow-sm text-md font-small text-white bg-indigo-600 hover:bg-pink-600
                            focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                            Logout
                        </a>
                    )}
                </div>
            </main>
        </div>
    );
}

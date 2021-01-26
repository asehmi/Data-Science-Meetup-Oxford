import { useEffect } from 'react'
import Head from 'next/head';

export default function AuthApp({ session }) {

    console.log('======== AuthApp ========')

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
        <div className="container mx-auto my-10 max-w-xl p-2">
            <Head>
                <title>Authentication</title>
            </Head>
            <main>
                <div className="flex items-center justify-center py-4">
                    {user && (
                        <a  href="/api/logout"
                            className="rounded bg-blue-500 hover:bg-blue-600 text-white py-2 px-4">
                            Logout
                        </a>
                    )}
                    {!user && (
                        <a  href="/api/login"
                            className="rounded bg-blue-500 hover:bg-blue-600 text-white py-2 px-4">
                            Login
                        </a>
                    )}
                </div>
            </main>
        </div>
    );
}

import { useEffect, useState } from 'react'
import Head from 'next/head';

import STORAGE from '../utils/storage'

export default function AuthApp({ session }) {

    console.log('======== AuthApp ========')

    // Initialy there will be no session, then the post-login callback will pass in the session object
    const [user, setUser] = useState(session?.user)
    const [accessToken, setAccessToken] = useState(session?.accessToken)
    const [accessTokenExpiresAt, setAccessTokenExpiresAt] = useState(session?.accessTokenExpiresAt)

    console.log('AuthApp:')
    console.log(user ? user : 'Null user')
    console.log(accessToken ? accessToken : 'Null token')
    console.log(accessTokenExpiresAt ? accessTokenExpiresAt : 'Null token expiry')

    useEffect(() => {
        const setItems = async () => {
            console.log('AuthApp (set user, token, expiry)')
            await STORAGE.setItem('user', JSON.stringify(user))
            await STORAGE.setItem('token', accessToken)
            await STORAGE.setItem('tokenExpiry', accessTokenExpiresAt)
        }
        const removeItems = async () => {
            console.log('AuthApp (remove user, token, expiry)')
            await STORAGE.removeItem('user')
            await STORAGE.removeItem('token')
            await STORAGE.removeItem('tokenExpiry')
        }

        if (user && accessToken && accessTokenExpiresAt) {
            setItems()
        }
        if (!user || !accessToken || !accessTokenExpiresAt) {
            removeItems()
        }

    }, [user, accessToken, accessTokenExpiresAt])

    return (
        <div>
            <Head>
                <title>Authentication</title>
            </Head>
            <main>
                <div>
                    <div className="flex flex-col mx-20 my-10">
                        <img src='/logo.jpg'/>
                    </div>
                    {!user?.email && (
                        <div className="flex flex-col mx-20 gap-3">
                            <p className="text-xl">Sign into the application...</p>
                            <div>
                                <a  href="/api/login"
                                    className="inline-flex px-4 py-1 border border-transparent
                                    rounded-md shadow-sm text-md font-small text-white bg-indigo-600 hover:bg-pink-600
                                    focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                                    Login
                                </a>
                            </div>
                        </div>
                    )}
                    {user?.email && (
                        <div className="flex flex-col mx-20 gap-3">
                            <div className="text-xl">Signed in.</div>
                            <div className="text-xl">Return to the application, or sign out...</div>
                            <div>
                                <a  href="/api/logout"
                                    className="inline-flex px-4 py-1 border border-transparent
                                    rounded-md shadow-sm text-md font-small text-white bg-indigo-600 hover:bg-pink-600
                                    focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                                    Logout
                                </a>
                            </div>
                        </div>
                    )}
                </div>
            </main>
        </div>
    );
}

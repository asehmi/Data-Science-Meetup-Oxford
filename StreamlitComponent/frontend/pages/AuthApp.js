import { useEffect, useState } from 'react'
import Head from 'next/head';

import STORAGE from '../utils/storage'

export default function AuthApp({ session }) {

    console.log('======== AuthApp ========')

    // Initialy there will be no session, then the post-login callback will pass in the session object
    const [sessionInfo, setSessionInfo] = useState({user: session?.user, token: {value: session?.accessToken, value_id_token: session?.idToken, expiry: session?.accessTokenExpiresAt}})

    console.log(session ? session.user : 'Null user')
    console.log(session ? session.idToken : 'Null id token')
    console.log(session ? session.accessToken : 'Null access token')
    console.log(session ? session.accessTokenExpiresAt : 'Null token expiry')

    useEffect(() => {
        setSessionInfo({
            user: session?.user,
            token: {
                value: session?.accessToken,
                value_id_token: session?.idToken,
                expiry: session?.accessTokenExpiresAt
            }
        })
    }, [])

    useEffect(async () => {
        if (sessionInfo) {
            console.log('AuthApp (set session info: user, token, expiry)')
            await STORAGE.setItem('sessionInfo', JSON.stringify(sessionInfo))
        } else {
            console.log('AuthApp (remove session info: user, token, expiry)')
            await STORAGE.removeItem('sessionInfo')
        }
    }, [sessionInfo])

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
                    {!sessionInfo.user?.email && (
                        <div className="flex flex-col mx-20 gap-3">
                            <p className="text-xl">Sign into the application...</p>
                            <div>
                                <a  href="/api/auth/login"
                                    className="inline-flex px-4 py-1 border border-transparent
                                    rounded-md shadow-sm text-md font-small text-white bg-indigo-600 hover:bg-pink-600
                                    focus:outline-none focus:ring-2 focus:ring-offset-2 focus:ring-indigo-500">
                                    Login
                                </a>
                            </div>
                        </div>
                    )}
                    {sessionInfo.user?.email && (
                        <div className="flex flex-col mx-20 gap-3">
                            <div className="text-xl">Signed in.</div>
                            <div className="text-xl">Return to the application, or sign out...</div>
                            <div>
                                <a  href="/api/auth/logout"
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

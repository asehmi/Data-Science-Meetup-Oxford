import Head from 'next/head';
import AuthApp from './AuthApp'
import auth0 from './api/utils/auth0';

export default function Home({ session }) {

    console.log('======== Home ========')

    const SHOW_UI = true

    const user = session?.user
    const accessToken = session?.accessToken
    const accessTokenExpiresAt = session?.accessTokenExpiresAt

    console.log(user ? user : 'Null user')
    console.log(accessToken ? accessToken : 'Null token')
    console.log(accessTokenExpiresAt ? accessTokenExpiresAt : 'Null token expiry')

    return (
        <div className="container my-3 max-w-xl p-2">
            <Head>
                <title>Home - App Launcher</title>
            </Head>
            <main>
                <div className="flex flex-row gap-4">
                    <div>
                        <AuthApp session={session}/>
                    </div>
                </div>
                {/* {SHOW_UI && session?.accessToken && (
                    <div>
                        accessToken: <p className="text-gray-400 truncate ...">{session.accessToken}</p>
                    </div>
                )}
                {SHOW_UI && session?.accessTokenExpiresAt && (
                    <div>
                        tokenExpiry: <p className="text-gray-400 truncate ...">{session.accessTokenExpiresAt}</p>
                    </div>
                )} */}
            </main>
        </div>
    );
}

export async function getServerSideProps(context) {
    try {
    
        // EXPLORING: NOT REQUIRED
        // try {
        //     const tokenCache = auth0.tokenCache(context.req, context.res);
        //     const { accessToken } = await tokenCache.getAccessToken();
        
        //     console.log('Home AccessToken cache hit...')
        //     console.log(accessToken)
        
        // } catch (AccessTokenError) {
        //     console.log('Home AccessToken cache miss!')
        // }
    
        const session = await auth0.getSession(context.req);

        console.log('======== Home getServerSideProps ========')
        console.log(session ? session : 'Null session')

        return {
            props: {
                session: session,
            },
        };
    
    } catch (error) {
        console.error(error);
        return {
            props: { message: error.message }
        };
    }
}


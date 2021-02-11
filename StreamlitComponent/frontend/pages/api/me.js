import auth0 from './utils/auth0';

export default auth0.requireAuthentication(async (req, res) => {
    try {
        await auth0.handleProfile(req, res, { refetch: true });
        res.statusCode = 200;
    } catch (error) {
        console.error(error);
        res.statusCode = 500;
        res.json({ message: error.message });
    }
});

// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
// https://github.com/vercel/next.js/blob/canary/examples/api-routes-cors
import Cors from 'cors'
import initMiddleware from '../middleware/InitMiddleware'

// Initialize the cors middleware
const cors = initMiddleware(
  // You can read more about the available options here: https://github.com/expressjs/cors#configuration-options
  Cors({
    // Only allow requests with GET, POST and OPTIONS
    methods: ['GET', 'POST', 'OPTIONS'],
  })
)

const Pong = async (req, res) => {
 try {
    // Run cors
    await cors(req, res)

    console.log('======== Pong ========')

    const url = `${process.env.NEXT_PUBLIC_REMOTE_API_BASE_URL}/api/pong`;
    console.log('Pong url: ' + url)

    var accessToken = req.headers.accesstoken
    //console.log('Pong cookie: ' + req.headers.cookie)
    console.log('Pong access token: ' + accessToken)

    // BEARER AUTH WILL ONLY WORK FOR REMOTE API CALL
    const headers = {
      "Accept": "application/json",
      "Content-Type": "application/json",
      "Authorization": `Bearer ${accessToken}`}
    console.log('Headers: ' + JSON.stringify(headers))

    const response = await fetch(url, {
      method: 'get',
      headers: headers
    });

    const pong = await response.json();
    res.status(200).json(pong);
  } catch (error) {
    console.error(error);
    res.status(error.status || 500).json({
      code: error.code,
      error: error.message
    });
  }
}

export default Pong
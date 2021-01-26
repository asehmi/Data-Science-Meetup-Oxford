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

const Ping = async (req, res) => {
    // Run cors
    await cors(req, res)

    res.statusCode = 200;
    const data = res.json({ ping: new Date().toString() });

    return data
};

export default Ping
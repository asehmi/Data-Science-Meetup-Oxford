// Next.js API route support: https://nextjs.org/docs/api-routes/introduction
import { NextApiRequest, NextApiResponse } from 'next'

const handler = (_req: NextApiRequest, res: NextApiResponse) => {
  res.statusCode = 200
  res.setHeader("Access-Control-Allow-Origin", "null")
  res.setHeader("Access-Control-Allow-Headers", "Origin, X-Requested-With, Content-Type, Accept, Authorization")
  res.json({ "name": 'Arvindra Sehmi, https://www.linkedin.com/in/asehmi/' })
}

export default handler

import { NextApiResponse } from 'next';

export default async function handler(req, res) {
  console.log(req.body);
  await new Promise((resolve) => setTimeout(resolve, 1000));
  res.status(200).json({ text: 'Hello' });
}
